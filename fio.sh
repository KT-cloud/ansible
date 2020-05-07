apt-get install fio << EOF
Y
EOF

fio --directory=/root/fio --name fio_test_file --direct=1 --rw=randread --bs=4K --size=1G --numjobs=5 --time_based --runtime=180 --group_reporting --norandommap > '/root/fio.txt'

