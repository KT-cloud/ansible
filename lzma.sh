echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


comlzma="$phoronix benchmark compress-lzma"

lzma=`$comlzma << EOF
n
EOF`
echo "$lzma" > '/root/compress-lzma.txt'

echo "Finished phoronix-test-suite."
