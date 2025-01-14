# ldapmail

Dockerized solution combining docker-mailserver with OpenLDAP for centralized user authentication
and management. It allows
you to quickly set up a self-hosted email system with LDAP integration, offering an easy-to-deploy
and scalable solution for both email and user management.

## Docker Mailserver

Customized docker-mailserver to work with OpenLDAP.

[Docs for setting up Docker Mailserver](docker-mailserver/README.md)

## OpenLDAP

OpenLDAP with custom schema for mail accounts and phpldapadmin.

[Docs for setting up OpenLDAP](openldap/README.md)

## TypeScript utility library

A TypeScript utility library for managing LDAP authentication and IMAP email operations with
docker-mailserver. This package simplifies the integration process, providing easy-to-use functions
for secure user authentication via LDAP and efficient email management through IMAP.

https://github.com/ldapmail/ldapmail-ts-utils

## Setup

The Docker Compose configuration currently sets up *Docker Mailserver* and *OpenLDAP* to work
together seamlessly. However, they can easily be decoupled and deployed independently on separate
servers for enhanced scalability.

Steps to set up the system:

1. Install Docker
2. Clone ldapmail from https://github.com/ldapmail/ldapmail.git into `/opt/ldapmail`
3. Setup environments

    - [docker-mailserver/README.md](docker-mailserver/README.md)

    - [openldap/README.md](openldap/README.md)

5. Setup Let's Encrypt

    ```bash
    $ docker run --rm -v "/etc/letsencrypt:/etc/letsencrypt" -v "/opt/ldapmail/webroot:/var/www/certbot" -p 80:80 certbot/certbot certonly --standalone --non-interactive --agree-tos --email office@xxx.xxx -d mail.xxx.xxx
    ```

    ```bash
    # Set in crontab to renew certificates
    0 0,12 * * * docker run -it --rm --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /opt/ldapmail/webroot:/var/www/certbot certbot/certbot renew
    ```

6. Set DKIM, DMARC, SPF
   https://docker-mailserver.github.io/docker-mailserver/latest/config/best-practices/dkim_dmarc_spf/#dns-zone-file

7. Test mail server

   https://www.mail-tester.com

   https://mxtoolbox.com/deliverability

To start the services, ensure your `.env` files and `docker-compose.yml` are configured, then run:

```bash
$ docker-compose up --build -d
```

in order to stop the services:

```bash
$ docker-compose down
```

## Contributors
- https://github.com/Codenetz