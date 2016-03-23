#! /bin/bash

# This will be launched by /etc/init.d/unicorn

echo "Launching rainbow!"

echo $pwd

sudo python _main.py

exit 0
