#!/bin/bash

sudo openvpn "./vpn/"$1".ovpn" > /dev/null 2> /dev/null &

how=`route -n | wc -l`

while [ ${how} != 6 ]
do
	how=`route -n | wc -l`
done

temp=`route -n | tail -2 | head -1 | grep -o '^\S*'`

sudo ip route add $2 via ${temp}
ping -c 2 $2 > $3
sudo ip route delete $2 via ${temp}
sudo killall openvpn > /dev/null 2> /dev/null
exit 0