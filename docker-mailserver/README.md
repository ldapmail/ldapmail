# Customized docker-mailserver to work with OpenLDAP

Set environment variables

```bash
$ cp .env.dist .env
```

Variables which needs to be set:

```env
LDAP_SERVER_HOST=ldap://ldap:1389
LDAP_SEARCH_BASE=ou=users,dc=%d,dc=mail,dc=com
LDAP_BIND_DN=cn=admin,dc=mail,dc=com
LDAP_BIND_PW=admin$

# Optional for SSL
SSL_TYPE=letsencrypt
```

Setup volume directories

```bash
$ sudo mkdir -p /mnt/volume_nyc1_01/openldap \
&& sudo mkdir -p /mnt/volume_nyc1_01/mail_logs \
&& sudo mkdir -p /mnt/volume_nyc1_01/mail_state \
&& sudo mkdir -p /mnt/volume_nyc1_01/mail_data \
&& sudo mkdir -p /mnt/volume_nyc1_01/mail_config
```

Copy configs for the Docker mail server to use.

```bash
$ cp config/* /mnt/volume_nyc1_01/mail_config/
```

For other configurations check docker-mailserver:
https://github.com/docker-mailserver/docker-mailserver