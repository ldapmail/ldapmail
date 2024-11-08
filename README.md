# ldapmail

This repository provides a Dockerized solution combining docker-mailserver for hosting a secure and
customizable mail server with OpenLDAP for centralized user authentication and management. It allows
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

To start the services, ensure your `.env` files and `docker-compose.yml` are configured, then run:

```bash
$ docker-compose up -d
```

in order to stop the services:

```bash
$ docker-compose down
```