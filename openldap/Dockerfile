FROM bitnami/openldap:latest

# Schema
COPY ldif/schema/postfix-book.ldif /opt/bitnami/openldap/etc/schema/postfix-book.ldif

# ACL
COPY apply-acl.sh /tmp/acl/apply-acl.sh
COPY ldif/acl/acl-mail-config.ldif /tmp/acl/acl-mail-config.ldif