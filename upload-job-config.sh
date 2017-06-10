#!/bin/sh -e

~/src/jenkins-tools/bin/delete-job.sh directory-tools || true
~/src/jenkins-tools/bin/put-job.sh directory-tools job.xml
