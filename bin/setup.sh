#!/bin/sh -e

create-tree.sh
create-root-suffix.sh
set-index.sh
add-access-control-settings.sh
add-unit.sh People
add-unit.sh users
add-unit.sh groups
add-person.sh "Alexander Reitzel"
add-account.sh "Alexander Reitzel"
