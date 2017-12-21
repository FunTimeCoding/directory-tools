# DirectoryTools

## Setup

This section explains how to install and uninstall the project.

Install pip package from GitHub.

```sh
pip3 install git+https://git@github.com/FunTimeCoding/directory-tools.git#egg=directory-tools
```

Install pip package from DevPi.

```sh
pip3 install -i https://testpypi.python.org/pypi directory-tools
```

Uninstall package.

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

This section explains how to use the project.

Run program.

```sh
dt
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

This section explains how to improve the project.

Configure Git on Windows before cloning. This avoids problems with Vagrant and VirtualBox.

```sh
git config --global core.autocrlf input
```

Build project. This installs dependencies.

```sh
script/build.sh
```

Run tests, check style and measure metrics.

```sh
script/test.sh
script/check.sh
script/measure.sh
```

Build package.

```sh
script/package.sh
```

Install Debian package.

```sh
sudo dpkg --install build/python3-directory-tools_0.1.0-1_all.deb
```

Show files the package installed.

```sh
dpkg-query --listfiles python3-directory-tools
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
