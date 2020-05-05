echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


comgzip="$phoronix benchmark compress-gzip"

gzip=`$comgzip << EOF
n
EOF`
echo "$gzip" > '/root/compress-gzip.txt'

echo "Finished phoronix-test-suite."
