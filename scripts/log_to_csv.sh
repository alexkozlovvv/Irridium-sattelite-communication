#!/bin/sh

sed '/Final response from modem got.*SBDI/!d' test.log > tmp1.log

grep --only-matching ' \[.*\].*SBDI:..' tmp1.log > tmp2.log

sed 's/  Final.*SBDI: /;/' tmp2.log > sends.log

rm tmp1.log tmp2.log
