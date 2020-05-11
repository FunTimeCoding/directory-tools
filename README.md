# DirectoryTools

## Setup

Install project dependencies:

```sh
script/setup.sh
```

Install pip package from GitHub:

```sh
pip3 install git+https://git@github.com/FunTimeCoding/directory-tools.git#egg=directory-tools
```

Install pip package from DevPi:

```sh
pip3 install -i https://testpypi.python.org/pypi directory-tools
```

Uninstall package:

```sh
pip3 uninstall directory-tools
```

Configuration file location: `~/.directory-tools.yml`

Configure the project:

```yml
host: ldap
domain: example
top_level: org
manager-name: example
manager-password: example
```


## Usage

Run the main program:

```sh
bin/dt
```

Run the main program inside the container:

```sh
docker run -it --rm funtimecoding/directory-tools
```

Create an organizational unit for people and add a person:

```sh
bin/unit.sh add people
bin/person.sh add "Alexander Reitzel"
```

Create a group for a POSIX account:

```sh
bin/unit.sh add groups
bin/group.sh add areitzel
```

Create an organizational unit for POSIX accounts and add an account:

```sh
bin/unit.sh add users
bin/user.sh add "Alexander Reitzel"
bin/group.sh add_user areitzel
```

Show the whole suffix:

```sh
bin/suffix.sh
```

Show status information:

```sh
bin/status.sh
```


## Development

Configure Git on Windows before cloning:

```sh
git config --global core.autocrlf input
```

Install NFS plug-in for Vagrant on Windows:

```bat
vagrant plugin install vagrant-winnfsd
```

Create the development virtual machine on Linux and Darwin:

```sh
script/vagrant/create.sh
```

Create the development virtual machine on Windows:

```bat
script\vagrant\create.bat
```

Run tests, style check and metrics:

```sh
script/test.sh [--help]
script/check.sh [--help]
script/measure.sh [--help]
```

Build project:

```sh
script/build.sh
```

Install Debian package:

```sh
sudo dpkg --install build/python3-directory-tools_0.1.0-1_all.deb
```

Show files the package installed:

```sh
dpkg-query --listfiles python3-directory-tools
```


## Abbreviations

- O - Organization
- CN - Common Name
- OU - Organizational Unit
- DC - Domain Component
- LDIF LDAP Data Interchange Format
- DN - Distinguished Name
- SN - Surname
- BaseDN - Tree branch to work from.
  - Alias: suffix
  - Example: 'dc=example,dc=org'
- BindDN - User who connects to the server.
  - Example: 'cn=admin,dc=example,dc=org'
- DSE - DSA Specific Entry.
  - Alias: RootDSE
- DSA - Directory System Agent
- OLC - On-Line Configuration.
  - Aliases: cn=config, slapd.d
- DIT - Directory Information Tree. Sum of entries in the database.
