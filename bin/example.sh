#!/bin/sh -e

install.sh
set-manager-password.sh admin
enable-security.sh

# Create a second database.
#create-tree.sh
#create-root-suffix.sh
# Set index on uid
#set-index.sh
# Allow posixAccount to log in.
#add-access-control-settings.sh

# Not sure if this OU is really necessary.
#add-unit.sh People
#add-person.sh "Alexander Reitzel"

# Not fully worked out yet.
add-unit.sh groups

# Create an OU for users and add a user to it.
add-unit.sh users
add-account.sh "Alexander Reitzel"

show-status.sh
