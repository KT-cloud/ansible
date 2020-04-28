apt-get update

apt-get install php-cli php-xml << EOF
y
EOF

apt-get install -y php5-cli php5-json php5-gd
apt-get install -y xdg-utils
wget -O phoronix.tar.gz https://phoronix-test-suite.com/releases/phoronix-test-suite-9.6.0.tar.gz
tar xvf phoronix.tar.gz

sleep 4

cd phoronix-test-suite/
./install-sh


echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

$phoronix list-tests << EOF
y
y
y
EOF

sleep 4

crafty="$phoronix benchmark crafty"

$crafty << EOF
n
EOF
sleep 4

'''
cachebench="$phoronix benchmark cachebench"

$cachebench << EOF
4
n
EOF
sleep 4

for benchmark in compress-7zip compress-gzip compress-lzma compress-pbzip2 c-ray openssl gnupg himeno sample-program apache; do
        $phoronix-test-suite benchmark $benchmark << EOF
        n
EOF
        sleep 2
        done

'''
echo "Finished phoronix-test-suite."

Uptime
