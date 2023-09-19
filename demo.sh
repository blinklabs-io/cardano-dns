#!/usr/bin/env bash

echo Starting cdnsd root server
docker run -d \
	--name cdnsd-container \
	-e DNS_LISTEN_PORT=53 \
	-e STATE_DIR=/tmp/.state \
	-p 20053:53 \
        --ip 69.69.42.42 \
	-v $(pwd -P)/.state:/tmp/.state \
	-u root \
	ghcr.io/blinklabs-io/cdnsd:main

sleep 10
__root=$(docker inspect cdnsd-container | jq -r .[].NetworkSettings.IPAddress)

echo Starting BIND server container
docker run -d \
	--name bind9-container \
	-e TZ=UTC \
	-p 30053:53 \
	--ip 42.42.31.31 \
	-v $(pwd -P)/bind/named.conf.options:/etc/bind/named.conf.options \
	-v $(pwd -P)/bind/named.conf.default-zones:/etc/bind/named.conf.default-zones \
	-v $(pwd -P)/bind/named.conf.local:/etc/bind/named.conf.local \
	-v $(pwd -P)/bind/root.hints:/usr/share/dns/root.hints \
	-v $(pwd -P)/bind/dolphin.zone:/var/lib/bind/dolphin.zone \
	-v $(pwd -P)/bind/snorkel.zone:/var/lib/bind/snorkel.zone \
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

echo Looking up ns1.dolphin.cardano A records
dig @${__dns} ns1.dolphin.cardano A
sleep 1

echo
echo

echo Looking up www.dolphin.cardano CNAME record
dig @${__dns} www.dolphin.cardano CNAME
sleep 1

echo
echo

echo Looking up www.google.com A record
dig @${__dns} www.google.com A
dig @103.196.38.39 +short www.google.com A
sleep 1

echo
echo

echo Looking up namebase A record
dig @${__dns} namebase A
dig @103.196.38.39 +short namebase A
sleep 1


echo
echo

echo cdnsd logs
docker logs cdnsd-container

echo
echo

echo bind9 logs
docker logs bind9-container

docker rm -f bind9-container 2>&1 >/dev/null
docker rm -f cdnsd-container 2>&1 >/dev/null
