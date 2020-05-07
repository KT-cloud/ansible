echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


gnupg="$phoronix benchmark gnupg"

gnu=`$gnupg << EOF
n
EOF`
echo "$gnu" > '/root/gnupg.txt'

echo "Finished phoronix-test-suite."
