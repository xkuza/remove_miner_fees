
# based on:
# Demonlj comment
# https://stackoverflow.com/questions/27293924/change-tcp-payload-with-nfqueue-scapy?rq=1
# https://github.com/DanMcInerney/cookiejack/blob/master/cookiejack.py

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import nfqueue
from scapy.all import *
import os
import re
from os import path
from datetime import datetime, timedelta
import json
from collections import OrderedDict

# https://forum.z.cash/t/about-dev-fees-and-how-to-remove-them/9600/36
#os.system('iptables -A OUTPUT -p tcp --dport 8008 -j NFQUEUE --queue-num 0')  # for dwarfpool
os.system('iptables -A OUTPUT -p tcp --dport 9999 -d eth-eur.nanopool.org -j NFQUEUE --queue-num 0')
#os.system('iptables -A OUTPUT -p tcp --dport 5000 -j NFQUEUE --queue-num 0')
#os.system('iptables -A INPUT -p tcp --dport 5000 -j NFQUEUE --queue-num 0')
# miner fees iptables rule for mitm  
#os.system('iptables -A FORWARD -o ens33 -p tcp --dport 4444 -d us1.ethermine.org -j NFQUEUE --queue-num 0')


my_eth_address = '0xf5ec8c6afc3dd2712b43b95128813bd09787a782'

def callback(arg1, payload):
  data = payload.get_data()
  pkt = IP(data)

  payload_before = len(pkt[TCP].payload)

  payload_text = str(pkt[TCP].payload)
  # jason
  print("%s:%s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), payload_text))
  if ('submitLogin' in payload_text) or ('eth_login' in payload_text):
    json_data=json.loads(payload_text, object_pairs_hook=OrderedDict)
    if json_data['params']:
      if my_eth_address not in json_data['params'][0]:
        print('[*] DevFee Detected - Replacing Address - %s\n' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('[*] REPLACED FROM %s TO %s\n' % (json_data['params'][0], my_eth_address))
        json_data['params'][0] = my_eth_address
        print("[*] BEFORE: %s\n" % payload_text)
        print("[*] AFTER: %s\n" % json.dumps(json_data))
        payload_text=json.dumps(json_data) + '\n'
  pkt[TCP].payload = payload_text

  payload_after = len(payload_text)

  payload_dif = payload_after - payload_before

  pkt[IP].len = pkt[IP].len + payload_dif

  pkt[IP].ttl = 40

  del pkt[IP].chksum
  del pkt[TCP].chksum
  payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(pkt), len(pkt))

def main():
  q = nfqueue.queue()
  q.open()
  q.bind(socket.AF_INET)
  q.set_callback(callback)
  q.create_queue(0)
  try:
    q.try_run() # Main loop
  except KeyboardInterrupt:
    q.unbind(socket.AF_INET)
    q.close()
    if path.exists('./restart_iptables'):
      os.system('./restart_iptables')
      
#ith regards to the restart_iptables script that's missing from the repo feel free to add this to satisfy the missing script. Perhaps a small contribution could be beneficial here

#!/bin/bash
#echo "Stopping firewall and allowing everyone..."
#ipt="/sbin/iptables"
#[ ! -x "$ipt" ] && { echo "$0: \"${ipt}\" command not found."; exit 1; }
#$ipt -P INPUT ACCEPT
#$ipt -P FORWARD ACCEPT
#$ipt -P OUTPUT ACCEPT
#$ipt -F
#$ipt -X
#$ipt -t nat -F
#$ipt -t nat -X
#$ipt -t mangle -F
#$ipt -t mangle -X
#$ipt -t raw -F
#$ipt -t raw -X

main()
