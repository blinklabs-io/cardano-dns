#!/usr/bin/env bash

echo Starting BIND server container
docker run -d \
	--name bind9-container \
	-e TZ=UTC \
	-p 30053:53 \
	-v $(pwd -P)/bind/named.conf.options:/etc/bind/named.conf.options \
	-v $(pwd -P)/bind/named.conf.default-zones:/etc/bind/named.conf.default-zones \
	-v $(pwd -P)/bind/named.conf.local:/etc/bind/named.conf.local \
	-v $(pwd -P)/bind/root.hints:/usr/share/dns/root.hints \
	-v $(pwd -P)/bind/root.zone:/var/lib/bind/root.zone \
	-v $(pwd -P)/cardano.zone:/var/lib/bind/cardano.zone \
	-v $(pwd -P)/bind/treehouse.zone:/var/lib/bind/treehouse.zone \
	ubuntu/bind9:9.18-22.04_beta

sleep 1
__dns=$(docker exec -ti bind9-container ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1)

echo Looking up . NS records
dig @${__dns} . NS
sleep 1

echo
echo

echo Looking up . A records
dig @${__dns} . A
sleep 1

echo
echo

echo Looking up ns1.cardano A records
dig @${__dns} ns1.cardano A
sleep 1

echo
echo

echo Looking up ns1.treehouse.cardano A records
dig @${__dns} ns1.treehouse.cardano A
sleep 1

echo
echo

echo Looking up www.treehouse.cardano CNAME record
dig @${__dns} www.treehouse.cardano CNAME
sleep 1

docker rm -f bind9-container 2>&1 >/dev/null
