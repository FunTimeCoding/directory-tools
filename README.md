# DirectoryTools

## Setup

This section explains how to install and uninstall this project.

Install the project.

```sh
pip3 install git+https://git@github.com/FunTimeCoding/directory-tools.git#egg=directory-tools
```

Uninstall the project.

```sh
pip3 uninstall directory-tools
```

Configuration file location: `~/.directory-tools.yml`.

Configure the project.

```yml
host: ldap
domain: example
top_level: org
manager-name: example
manager-password: example
```


## Usage

This section explains how to use this project.

Run the main program.

```sh
bin/dt
```

Install OpenLDAP on Debian.

```sh
install.sh
enable-security.sh
```

Change the manager password.

```sh
set-manager-password.sh admin
```

Create an organizational unit for people and add a person.

```sh
unit.sh add people
person.sh add "Alexander Reitzel"
```

Create a group for a POSIX account.

```sh
unit.sh add groups
group.sh add areitzel
```

Create an organizational unit for POSIX accounts and add an account.

```sh
unit.sh add users
user.sh add "Alexander Reitzel"
group.sh add_user areitzel
```

Show the whole suffix.

```sh
suffix.sh
```

Show status information.

```sh
status.sh
```


## Development

This section explains commands to help the development of this project.

Install the project from a clone.

```sh
./setup.sh
```

Run tests, style check and metrics.

```sh
./run-tests.sh
./run-style-check.sh
./run-metrics.sh
```

Build the project.

```sh
./build.sh
```


## Abbreviations

* O - Organization
* CN - Common Name
* OU - Organizational Unit
* DC - Domain Component
* LDIF LDAP Data Interchange Format
* DN - Distinguished Name
* SN - Surname
* BaseDN - Tree branch to work from.
 * Alias: suffix
 * Example: 'dc=example,dc=org'
* BindDN - User who connects to the server.
 * Example: 'cn=admin,dc=example,dc=org'
* DSE - DSA Specific Entry.
 * Alias: RootDSE
* DSA - Directory System Agent
* OLC - On-Line Configuration.
 * Aliases: cn=config, slapd.d
* DIT - Directory Information Tree. Sum of entries in the database.
