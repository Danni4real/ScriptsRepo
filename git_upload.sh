#!/bin/bash

git pull
git add -u
git commit -m "$@"
git push origin HEAD:refs/for/23MM

