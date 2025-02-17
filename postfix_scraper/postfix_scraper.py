import os
from flask import Flask, Response, request
import subprocess
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = "/var/log/mail.log"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
LOG_INTERVAL_MIN = int(os.getenv('LOG_INTERVAL_MIN', 1))
TAIL_LINES = int(os.getenv('TAIL_LINES', 10000))
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

app = Flask(__name__)

def parse_mail_log(minutes):
    """Parse the last N lines of mail.log and count email statuses from the given interval."""
    outgoing_sent_count = 0
    outgoing_rejected_count = 0
    outgoing_deferred_count = 0
    outgoing_bounced_count = 0
    outgoing_queued_count = 0
    outgoing_unknown_count = 0

    incoming_sent_count = 0
    incoming_rejected_count = 0
    incoming_deferred_count = 0
    incoming_bounced_count = 0
    incoming_queued_count = 0
    incoming_unknown_count = 0

    now = datetime.now().astimezone()
    time_ago = now - timedelta(minutes=minutes)

    try:
        output = subprocess.run(
            ["tail", "-n", str(TAIL_LINES), LOG_FILE], capture_output=True, text=True
        )
        lines = output.stdout.split("\n")
    except Exception as e:
        print(f"Error reading mail log: {e}")
        return  outgoing_sent_count, outgoing_rejected_count, outgoing_deferred_count, outgoing_bounced_count, outgoing_queued_count, outgoing_unknown_count, \
                incoming_sent_count, incoming_rejected_count, incoming_deferred_count, incoming_bounced_count, incoming_queued_count, incoming_unknown_count

    for line in lines:
        outgoing_pattern = r"(?P<date>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+[\+\-]\d{2}:\d{2}).*?postfix/smtp.*?status=(?P<status>\w+)"
        incoming_pattern = r"(?P<date>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+[\+\-]\d{2}:\d{2}).*?postfix/lmtp.*?status=(?P<status>\w+)"

        # Outgoing Match status log lines
        outgoing_status_match = re.search(outgoing_pattern, line)
        if outgoing_status_match:
            outgoing_log_time = outgoing_status_match.group("date")
            outgoing_log_status = outgoing_status_match.group("status")

            try:
                outgoing_log_datetime = datetime.strptime(outgoing_log_time, TIME_FORMAT).astimezone()
            except ValueError as e:
                print(f"Skipping invalid date: {outgoing_log_time} - Error: {e}")
                continue

            if outgoing_log_datetime >= time_ago:
                if outgoing_log_status == "sent":
                    outgoing_sent_count += 1
                elif outgoing_log_status == "rejected":
                    outgoing_rejected_count += 1
                elif outgoing_log_status == "deferred":
                    outgoing_deferred_count += 1
                elif outgoing_log_status == "bounced":
                    outgoing_bounced_count += 1
                elif outgoing_log_status == "queued":
                    outgoing_queued_count += 1
                else:
                    outgoing_unknown_count += 1

        # Incoming Match status log lines
        incoming_status_match = re.search(incoming_pattern, line)
        if incoming_status_match:
            incoming_log_time = incoming_status_match.group("date")
            incoming_log_status = incoming_status_match.group("status")

            try:
                incoming_log_datetime = datetime.strptime(incoming_log_time, TIME_FORMAT).astimezone()
            except ValueError as e:
                print(f"Skipping invalid date: {incoming_log_time} - Error: {e}")
                continue

            if incoming_log_datetime >= time_ago:
                if incoming_log_status == "sent":
                    incoming_sent_count += 1
                elif incoming_log_status == "rejected":
                    incoming_rejected_count += 1
                elif incoming_log_status == "deferred":
                    incoming_deferred_count += 1
                elif incoming_log_status == "bounced":
                    incoming_bounced_count += 1
                elif incoming_log_status == "queued":
                    incoming_queued_count += 1
                else:
                    incoming_unknown_count += 1

    return  outgoing_sent_count, outgoing_rejected_count, outgoing_deferred_count, outgoing_bounced_count, outgoing_queued_count, outgoing_unknown_count,  \
            incoming_sent_count, incoming_rejected_count, incoming_deferred_count, incoming_bounced_count, incoming_queued_count, incoming_unknown_count
@app.route("/metrics")
def metrics():

    # Unpack the counts returned from parse_mail_log
    outgoing_sent_count, outgoing_rejected_count, outgoing_deferred_count, outgoing_bounced_count, outgoing_queued_count, outgoing_unknown_count, \
    incoming_sent_count, incoming_rejected_count, incoming_deferred_count, incoming_bounced_count, incoming_queued_count, incoming_unknown_count = parse_mail_log(LOG_INTERVAL_MIN)

    # Create the response in Prometheus format using the unpacked counts
    response = f"""# HELP postfix_sent_emails Number of outgoing sent emails in the given interval
# TYPE postfix_sent_emails counter
postfix_outgoing_sent_emails {outgoing_sent_count}

# HELP postfix_rejected_emails Number of outgoing rejected emails in the given interval
# TYPE postfix_rejected_emails counter
postfix_outgoing_rejected_emails {outgoing_rejected_count}

# HELP postfix_deferred_emails Number of outgoing deferred emails in the given interval
# TYPE postfix_deferred_emails counter
postfix_outgoing_deferred_emails {outgoing_deferred_count}

# HELP postfix_bounced_emails Number of outgoing bounced emails in the given interval
# TYPE postfix_bounced_emails counter
postfix_outgoing_bounced_emails {outgoing_bounced_count}

# HELP postfix_queued_emails Number of outgoing queued emails in the given interval
# TYPE postfix_queued_emails counter
postfix_outgoing_queued_emails {outgoing_queued_count}

# HELP postfix_outgoing_unknown_count Number of outgoing unknown emails in the given interval
# TYPE postfix_outgoing_unknown_count counter
postfix_outgoing_unknown_count {outgoing_unknown_count}

# HELP postfix_incoming_sent_emails Number of incoming sent emails in the given interval
# TYPE postfix_incoming_sent_emails counter
postfix_incoming_sent_emails {incoming_sent_count}

# HELP postfix_incoming_rejected_emails Number of incoming rejected emails in the given interval
# TYPE postfix_incoming_rejected_emails counter
postfix_incoming_rejected_emails {incoming_rejected_count}

# HELP postfix_incoming_deferred_emails Number of incoming deferred emails in the given interval
# TYPE postfix_incoming_deferred_emails counter
postfix_incoming_deferred_emails {incoming_deferred_count}

# HELP postfix_incoming_bounced_emails Number of incoming bounced emails in the given interval
# TYPE postfix_incoming_bounced_emails counter
postfix_incoming_bounced_emails {incoming_bounced_count}

# HELP postfix_incoming_queued_emails Number of incoming queued emails in the given interval
# TYPE postfix_incoming_queued_emails counter
postfix_incoming_queued_emails {incoming_queued_count}

# HELP postfix_incoming_unknown_count Number of incoming unknown emails in the given interval
# TYPE postfix_incoming_unknown_count counter
postfix_incoming_unknown_count {incoming_unknown_count}
"""
    return Response(response, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9555, debug=DEBUG)
