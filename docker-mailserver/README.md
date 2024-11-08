# Customized docker-mailserver to work with OpenLDAP

Set environment variables
```bash
$ cp .env.dist .env
```

Variables which needs to be set correctly in order to work with OpenLDAP are:
```env
LDAP_SERVER_HOST=
LDAP_SEARCH_BASE=
LDAP_BIND_DN=
LDAP_BIND_PW=
```

For other configurations check docker-mailserver:
https://github.com/docker-mailserver/docker-mailserver