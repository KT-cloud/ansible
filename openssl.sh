echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


openssl="$phoronix benchmark openssl"

ssl=`$openssl << EOF
n
EOF`
echo "$ssl" > '/root/openssl.txt'

echo "Finished phoronix-test-suite."
