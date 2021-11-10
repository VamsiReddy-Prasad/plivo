#!/usr/bin/bash

invite200ok=$(grep -a -B 3 -e '200 OK' $4$1 | awk '/[0-9]*:[0-9]*:[0-9]*/{print $2,$3}' | head -1)
bye=$(grep -a -B 3 -e 'BYE sip:' $4$1 | awk '/[0-9]*:[0-9]*:[0-9]*/{print $2,$3}' | head -1)
invite=$(grep -a -B 3 -e 'INVITE sip:' $4$2 | awk '/[0-9]*:[0-9]*:[0-9]*/{print $2,$3}' | head -1)
callduration=$(awk '/Call Length.*[0-9]/{print $6}' $4$3)
echo "caller received answer at $invite200ok"
echo "caller received bye at $bye"
echo "callee recived INVITE at $invite"
echo "Total call duration  is $callduration"
