#!/usr/bin/env python
"""
# Python-DBot
"""
import sys
import nmap
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

#
# nm = nmap.PortScanner()
# nm.scan('204.12.243.0/24', '21,22,80,443,25565')
#
# for host in nm.all_hosts():
#     print('----------------------------------------------------')
#     print('Host : %s (%s)' % (host, nm[host].hostname()))
#     print('State : %s' % nm[host].state())
#     for proto in nm[host].all_protocols():
#         print('----------')
#         print('Protocol : %s' % proto)
#
#         lport = nm[host][proto].keys()
#         lport.sort()
#         for port in lport:
#             print ('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))


nma = nmap.PortScannerAsync()

def procesar_resultado(host, scan_result):
    if scan_result['nmap']['scanstats']['uphosts'] == '1':
        print host, 'UP', scan_result['scan'][host]['hostnames'][0]['name']
        data = scan_result['scan'][host]
        ntcp = []
        if 'tcp' in data:
            for port in data['tcp']:
                value = data['tcp'][port]
                value['proto'] = 'tcp'
                value['port'] = int(port)
                ntcp.append(value)
            del data['tcp']
        if 'udp' in data:
            for port in data['udp']:
                value = data['udp'][port]
                value['proto'] = 'udp'
                value['port'] = int(port)
                ntcp.append(value)
            del data['udp']
        data['services'] = ntcp


        res = es.index(index='dbot', doc_type='host', id=host, body=data)
    else:
        print host, 'DOWN'

nma.scan(sys.argv[1], '7,9,13,21,22,23,25,26,37,53,79,80,81,82,83,84,85,106,110,111,113,119,135,139,143,144,179,389,427,443,444,445,465,990,993,995,1025,1027,1433,2049,2121,3128,3306,3389,5009,5432,5631,5666,5800,5900,8000,8008,8009,8080,8081,8443,9100,9200,5672,27017,27015,25565', arguments='-A', callback=procesar_resultado)
while nma.still_scanning():
    print("Aguantiiando >>>")
    nma.wait(2)
