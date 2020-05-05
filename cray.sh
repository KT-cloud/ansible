echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


cray="$phoronix benchmark c-ray"

ray=`$cray << EOF
n
EOF`
echo "$ray" > '/root/c-ray.txt'

echo "Finished phoronix-test-suite."

