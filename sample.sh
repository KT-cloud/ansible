echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


sample="$phoronix benchmark sample-program"

sam=`$sample << EOF
n
EOF`
echo "$sam" > '/root/sample-program.txt'

echo "Finished phoronix-test-suite."
