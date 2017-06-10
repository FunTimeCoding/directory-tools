#!/bin/sh -e

~/Code/Personal/jenkins-tools/bin/delete-job.sh directory-tools || true
~/Code/Personal/jenkins-tools/bin/put-job.sh directory-tools job.xml
