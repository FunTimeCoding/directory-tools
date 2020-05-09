#!/bin/sh -e

#multitail -e slapd /var/log/syslog
journalctl --unit slapd --follow
