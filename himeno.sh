echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


himeno="$phoronix benchmark himeno"

him=`$himeno << EOF
n
EOF`
echo "$him" > '/root/himeno.txt'

echo "Finished phoronix-test-suite."
