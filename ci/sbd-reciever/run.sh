#!/bin/sh
#
# Based on https://github.com/gadomski/sbd-rs
#
cargo install sbd
sbd serve 0.0.0.0:10800 /var/iridium