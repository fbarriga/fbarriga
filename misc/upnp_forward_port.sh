#!/bin/bash

NETWORK_IFACE=eth0
DHT_PORT=6881                                                                                   
TORRENT_PORT=9876                                                                               

###########################################################
ip=$(ip -f inet -o addr show $NETWORK_IFACE | cut -d' ' -f 7 | cut -d'/' -f 1)                                 

upnpc -a $ip $TORRENT_PORT $TORRENT_PORT UDP                                                    
upnpc -a $ip $TORRENT_PORT $TORRENT_PORT TCP                                                    

upnpc -a $ip $DHT_PORT $DHT_PORT UDP 

