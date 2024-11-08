# OpenLDAP with phpldapadmin

This project runs `bitnami/openldap` alongside `phpldapadmin` and is configured to work seamlessly
with
a customized `docker-mailserver`. It includes a custom LDIF schema and ACL setup.

## Setup Instructions

### 1. Configure Environment Variables

Copy the provided .env.dist file to .env to set up your environment variables:

```bash
$ cp .env.dist .env
```

### 2. ACL Configuration
The ACL configuration is available in the `acl-mail-config.ldif` file.

### 3. Access the UI
You can access the phpLDAPadmin UI at:

```bash
http://localhost:6443
```

### 4. Apply ACL Settings

Run the following command to apply the ACL settings to the LDAP server:

```bash
$ docker exec -it mail-server_ldap_1 bash /tmp/acl/apply-acl.sh
```