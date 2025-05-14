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

sed -i '/scipy.*/d' ./requirements.txt

sudo apt update
sudo apt install -y python3-scipy

pip install -r ./requirements.txt

sed -i -e 's/ttyUSB0/ttyAMA0/g' configs/config.yaml

chmod +x src/*.py

# Disable bluetooth stuff
sudo systemctl disable hciuart.service
sudo systemctl disable bluealsa.service
sudo systemctl disable bluetooth.service
sudo echo "dtoverlay=disable-bt" >> /boot/config.txt
sudo echo "dtoverlay=pi3-disable-bt" >> /boot/config.txt

echo "===== Everything is ready ====="
echo "###############################"
echo "##########           ##########"
echo "######     Rebooting     ######"
echo "##########           ##########"
echo "###############################"
