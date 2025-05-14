#!/bin/sh

echo "==== Raspberry software updater ===="

cd ..

dt=$(date '+%d-%m-%Y_%H:%M:%S')

cp ./src/msg_parser.log ~/Logs/log-$dt.log 2>/dev/null || :
echo "Your previous log saved at ~/Logs/log-$dt.log"

if [ $# -eq 0 ] ; then
    branch=master
    echo "No arguments supplied. Using branch master."
else
    branch=$1
    echo "Using branch $branch"
fi

git reset --hard
git clean -fxd

git fetch origin
git checkout origin/$branch

chmod +x src/*.py

echo "==== Everything is ready ===="