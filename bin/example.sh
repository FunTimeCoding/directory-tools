#!/bin/sh -e

install.sh
enable-security.sh

# Change the manager password
set-manager-password.sh admin

# Create a second database.
#create-tree.sh
#create-root-suffix.sh
# Set index on uid
#set-index.sh
# Allow posixAccount to log in.
#add-access-control-settings.sh

# Not sure if this OU is really necessary.
#unit.sh add people
#people.sh add "Alexander Reitzel"

# Not fully worked out yet.
unit.sh add groups

# Create an OU for users and add a user to it.
unit.sh add users
user.sh add "Alexander Reitzel"

# Show the created suffix.
show-suffix.sh

# Show a lot of debug information.
#show-status.sh
