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
#unit.sh add People
#person.sh add "Alexander Reitzel"

# Not fully worked out yet.
unit.sh add groups

# Create an OU for users and add a user to it.
unit.sh add users
account.sh add "Alexander Reitzel"

# Show the created suffix.
show-suffix.sh

# Show a lot of debug information.
#show-status.sh
