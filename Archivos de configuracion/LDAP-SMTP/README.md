# LDAP
## Instalación de LDAP
`apt -y install slapd ldap-utils"`

## Archivos de configuración
- base.ldif
- ldapbeto.ldif

Donde los archivos _ldapNombre.ldif_ corresponden a los archivos de cada usuario.

# SMTP
## Hostname: _ldap-smtp.cert.unam.mx_

## Instalación de herramientas:
### Postfix
`apt-get install curl net-tools bash-completion wget lsof`

### Mailutils
`apt-get install mailutils`

### Dovecot IMAP
`apt install dovecot-core dovecot-imapd`

### Rainloop Webmail
`curl -sL https://repository.rainloop.net/installer.php | php`

## Archivos de configuración
- main.cf
- dovecot.conf
- 10-auth.conf
- 10-mail.conf
- 10-master.conf

# Máquina
- Archivo de configuración de apache: _security.conf_
- iptables: _iptables.rules_
