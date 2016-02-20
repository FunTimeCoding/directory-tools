# DirectoryTools

## Usage

This section explains how to use this project.

Run the main entry point program.

```sh
PYTHONPATH=. bin/dt
```

Configure `~/.directory-tools.yml`.

```yml
domain: example
top_level: org
password: example
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

Create an organizational unit for POSIX accounts and add an account.

```sh
unit.sh add users
user.sh add "Alexander Reitzel"
```

Show the whole suffix.

```sh
suffix.sh
```

Show debug information.

```sh
status.sh
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


## Setup

This section explains how to install this project and how to include it in another.

Install the project from a local clone.

```sh
pip3 install --user --editable .
```

Install the project from GitHub.

```sh
pip3 install git+ssh://git@github.com/FunTimeCoding/directory-tools.git#egg=directory-tools
```

Uninstall the project.

```sh
pip3 uninstall directory-tools
```

Require this repository in another projects `requirements.txt`.

```
git+ssh://git@github.com/FunTimeCoding/directory-tools.git#egg=directory-tools
```


## Development

This section explains how to use scripts that are intended to ease the development of this project.

Install tools on Debian Jessie.

```sh
apt-get install shellcheck
```

Install tools on OS X.

```sh
brew install shellcheck
```

Install pip requirements.

```sh
pip3 install --upgrade --user --requirement requirements.txt
```

Run code style check, metrics and tests.

```sh
./run-style-check.sh
./run-metrics.sh
./run-tests.sh
```

Build the project like Jenkins.

```sh
./build.sh
```


## Skeleton details

* The `tests` directory is not called `test` because that package already exists.
* Dashes in the project name become underscores in Python.
