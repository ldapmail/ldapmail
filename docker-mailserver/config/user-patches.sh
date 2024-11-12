#!/bin/bash

LDAP_RECEIVE_CONF_FILE="/etc/postfix/ldap-receiveonly.cf"
cat <<EOF > $LDAP_RECEIVE_CONF_FILE
server_host = ${LDAP_SERVER_HOST}
search_base = ${LDAP_SEARCH_BASE}
bind = yes
bind_dn = ${LDAP_BIND_DN}
bind_pw = ${LDAP_BIND_PW}
query_filter = ${LDAP_QUERY_FILTER_USER}
result_attribute = mailSendAllowed
version = 3
EOF

LDAP_ALIASES_CONF_FILE="/etc/postfix/ldap-aliases.cf"
cat <<EOF > $LDAP_ALIASES_CONF_FILE
server_host = ${LDAP_SERVER_HOST}
search_base = ${LDAP_SEARCH_BASE}
bind = yes
bind_dn = ${LDAP_BIND_DN}
bind_pw = ${LDAP_BIND_PW}
query_filter = ${LDAP_QUERY_FILTER_ALIAS}
result_attribute = mail
version = 3
EOF

LDAP_FORWARDING_CONF_FILE="/etc/postfix/ldap-forwarding.cf"
cat <<EOF > $LDAP_FORWARDING_CONF_FILE
server_host = ${LDAP_SERVER_HOST}
search_base = ${LDAP_SEARCH_BASE}
bind = yes
bind_dn = ${LDAP_BIND_DN}
bind_pw = ${LDAP_BIND_PW}
query_filter = ${LDAP_QUERY_FILTER_FORWARDING}
result_attribute = mailForwardingAddress
version = 3
EOF

DMS_SMTPD_SENDER_RESTRICTIONS="dms_smtpd_sender_restrictions = permit_mynetworks, check_sender_access ldap:/etc/postfix/ldap-receiveonly.cf, reject_unauth_destination, reject_unknown_sender_domain, permit_sasl_authenticated"
VIRTUAL_ALIAS_MAPS="virtual_alias_maps = ldap:/etc/postfix/ldap-aliases.cf, ldap:/etc/postfix/ldap-groups.cf, ldap:/etc/postfix/ldap-forwarding.cf"

sed -i "s|^dms_smtpd_sender_restrictions.*|$DMS_SMTPD_SENDER_RESTRICTIONS|" /etc/postfix/main.cf
sed -i "s|^virtual_alias_maps.*|$VIRTUAL_ALIAS_MAPS|" /etc/postfix/main.cf

# Enable quota
if [[ -f /etc/dovecot/conf.d/90-quota.conf.disab ]]
then
  mv /etc/dovecot/conf.d/90-quota.conf.disab /etc/dovecot/conf.d/90-quota.conf
  sedfile -i \
	"s|mail_plugins = \$mail_plugins|mail_plugins = \$mail_plugins quota|g" \
	/etc/dovecot/conf.d/10-mail.conf
  sedfile -i \
	"s|mail_plugins = \$mail_plugins|mail_plugins = \$mail_plugins imap_quota|g" \
	/etc/dovecot/conf.d/20-imap.conf
fi

MESSAGE_SIZE_LIMIT_MB=$((POSTFIX_MESSAGE_SIZE_LIMIT / 1000000))
MAILBOX_LIMIT_MB=$((POSTFIX_MAILBOX_SIZE_LIMIT / 1000000))

sedfile -i \
"s|quota_max_mail_size =.*|quota_max_mail_size = ${MESSAGE_SIZE_LIMIT_MB}$([[ ${MESSAGE_SIZE_LIMIT_MB} -eq 0 ]] && echo "" || echo "M")|g" \
/etc/dovecot/conf.d/90-quota.conf

sedfile -i \
"s|quota_rule = \*:storage=.*|quota_rule = *:storage=${MAILBOX_LIMIT_MB}$([[ ${MAILBOX_LIMIT_MB} -eq 0 ]] && echo "" || echo "M")|g" \
/etc/dovecot/conf.d/90-quota.conf

# enable quota policy check in postfix
sedfile -i -E \
"s|(reject_unknown_recipient_domain)|\1, check_policy_service inet:localhost:65265|g" \
/etc/postfix/main.cf
