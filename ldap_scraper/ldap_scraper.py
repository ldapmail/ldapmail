import os
import shutil
from flask import Flask, Response, request
import subprocess
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
from ldap3 import Server, Connection, ALL, SUBTREE

load_dotenv()

DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
LOG_INTERVAL_MIN = int(os.getenv('LOG_INTERVAL_MIN', 1))

LDAP_SERVER = os.getenv('LDAP_SERVER', 'ldap://ldap:1389')  # Replace with your LDAP server
BASE_DN = os.getenv('BASE_DN', 'dc=mail,dc=com')  # Replace with your base DN
BIND_DN = os.getenv('BIND_DN', 'cn=admin,dc=mail,dc=com')  # Replace with your bind DN
PASSWORD = os.getenv('PASSWORD', 'admin$')  # Replace with your password

MAIL_PATH = '/var/mail/vol_1'

app = Flask(__name__)

def count_created_accounts(minutes):
    """Count the number of email accounts created."""
    count = 0
    now = datetime.now()
    time_ago = now - timedelta(minutes=minutes)

    timestamp = time_ago.strftime('%Y%m%d%H%M%SZ')

    try:
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(server, user=BIND_DN, password=PASSWORD, auto_bind=True)
        search_filter = f'(&(createTimestamp>={timestamp})(objectClass=PostfixBookMailAccount))'
        conn.search(BASE_DN, search_filter, SUBTREE, attributes=['mail'])
        count = len(conn.entries)
        conn.unbind()

    except Exception as e:
        print(f"Error querying LDAP: {e}")
        return 0

    return count

def get_disk_usage(path):
    """Get disk usage statistics for the given path."""
    try:
        total, used, free = shutil.disk_usage(path)
        # Convert bytes to gigabytes for easier understanding
        total_gb = total // (2**30)
        used_gb = used // (2**30)
        free_gb = free // (2**30)
        return total_gb, used_gb, free_gb
    except Exception as e:
        print(f"Error getting disk usage for {path}: {e}")
        return 0, 0, 0

@app.route("/metrics")
def metrics():

    """Expose Prometheus metrics."""

    # Get the number of email accounts created in the last 1 minute
    created_accounts_count = count_created_accounts(LOG_INTERVAL_MIN)

    # Get disk usage for the /var/mail/vol_1 path
    total_gb, used_gb, free_gb = get_disk_usage(MAIL_PATH)

    response = f"""
# HELP ldap_email_accounts_created Total number of email accounts created.
# TYPE ldap_email_accounts_created counter
ldap_email_accounts_created {created_accounts_count}

# HELP mail_storage_total_gb Total storage in GB for /var/mail/vol_1.
# TYPE mail_storage_total_gb gauge
mail_storage_total_gb {total_gb}

# HELP mail_storage_used_gb Used storage in GB for /var/mail/vol_1.
# TYPE mail_storage_used_gb gauge
mail_storage_used_gb {used_gb}

# HELP mail_storage_free_gb Free storage in GB for /var/mail/vol_1.
# TYPE mail_storage_free_gb gauge
mail_storage_free_gb {free_gb}
"""
    return Response(response, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9777, debug=DEBUG)
