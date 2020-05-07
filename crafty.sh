dpkg --configure -a

apt-get update

apt-get install php-cli php-xml << EOF
y
EOF

apt-get install -y php5-cli php5-json php5-gd
apt-get install -y xdg-utils
wget -O phoronix.tar.gz https://phoronix-test-suite.com/releases/phoronix-test-suite-9.6.0.tar.gz
tar xvf phoronix.tar.gz


cd phoronix-test-suite/
./install-sh


echo "Starting Phoronix-test-suite...."


phoronix=/root/phoronix-test-suite/phoronix-test-suite
list-tests=/root/phoronix-test-suite/phoronix-test-suite list-tests

list=`$phoronix list-tests << EOF
y
y
y
EOF`


crafty="$phoronix benchmark crafty"

cra=`$crafty << EOF
n
EOF`
echo "$cra" > '/root/crafty.txt'

echo "Finished phoronix-test-suite."

