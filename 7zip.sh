echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


com7zip="$phoronix benchmark compress-7zip"

zip7=`$com7zip << EOF
n
EOF`
echo "$zip7" > '/root/compress-7zip.txt'

echo "Finished phoronix-test-suite."
