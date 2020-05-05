echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


compbzip2="$phoronix benchmark compress-pbzip2"

pbzip2=`$compbzip2 << EOF
n
EOF`
echo "$pbzip2" > '/root/compress-pbzip2.txt'

echo "Finished phoronix-test-suite."
