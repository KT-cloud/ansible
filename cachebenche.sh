echo "Starting Phoronix-test-suite...."

phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`

cachebench="$phoronix benchmark cachebench"

cache=`$cachebench << EOF
4
n
EOF`
echo "$cache" > '/root/cachebench.txt'


echo "Finished phoronix-test-suite."
