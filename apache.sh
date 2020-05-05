echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


apache="$phoronix benchmark apache"

apa=`$apache << EOF
n
EOF`
echo "$apa" > '/root/apache.txt'

echo "Finished phoronix-test-suite."
