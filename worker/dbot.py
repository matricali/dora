#!/usr/bin/env python
"""
# Python-DoraBot
"""
from __future__ import print_function
import sys
import nmap
import time
from elasticsearch import Elasticsearch
from geoip import geolite2
from faker import Faker
import threading

es = Elasticsearch()
nma = nmap.PortScannerAsync()
faker = Faker()

class scanThread (threading.Thread):
    def __init__(self, threadID, name, **kwargs):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        if 'target' in kwargs:
            self.target = kwargs['target']
        else:
            self.target = faker.ipv4()
    def run(self):
        self.log('Starting thread...')
        nma = nmap.PortScannerAsync()
        while True:
            try:
                target = faker.ipv4()
                self.log('Performing scan on', target)
                nma.scan(target, '7,9,13,21,22,23,25,26,37,53,79,80,81,82,83,84,85,106,110,111,113,119,135,139,143,144,179,389,427,443,444,445,465,990,993,995,1025,1027,1433,2049,2121,3128,3306,3389,5009,5432,5631,5666,5800,5900,8000,8008,8009,8080,8081,8443,9100,9200,5672,27017,27015,25565', arguments='-A', callback=self.procesar_resultado)
                while nma.still_scanning():
                    nma.wait(2)
            except KeyboardInterrupt:
                self.log('Exiting thread...')
    def procesar_resultado(self, host, scan_result):
        if scan_result['nmap']['scanstats']['uphosts'] == '1':
            self.log(host, 'UP', scan_result['scan'][host]['hostnames'][0]['name'])
            data = scan_result['scan'][host]
            data['last_scan'] = time.time()
            ntcp = []
            geoinfo = geolite2.lookup(data['addresses']['ipv4'])
            if geoinfo is not None:
                data['geo'] = geoinfo.get_info_dict()
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
            res = es.index(index='dora', doc_type='host', id=host, body=data)
        else:
            self.log(host, 'DOWN')
    def log(self, *args):
        print(time.ctime(time.time()), self.name, *args)

# def infiniteRandom():
#     while True:
#         try:
#             target = faker.ipv4()
#             print 'Performing scan on', target
#             nma.scan(target, '7,9,13,21,22,23,25,26,37,53,79,80,81,82,83,84,85,106,110,111,113,119,135,139,143,144,179,389,427,443,444,445,465,990,993,995,1025,1027,1433,2049,2121,3128,3306,3389,5009,5432,5631,5666,5800,5900,8000,8008,8009,8080,8081,8443,9100,9200,5672,27017,27015,25565', arguments='-A', callback=procesar_resultado)
#             while nma.still_scanning():
#                 nma.wait(2)
#         except KeyboardInterrupt:
#             print 'Exiting...'
#             sys.exit()

# try:
#     target = sys.argv[1]
# except IndexError:
#     target = faker.ipv4()
#     infiniteRandom()
#     sys.exit()

# nma.scan(target, '7,9,13,21,22,23,25,26,37,53,79,80,81,82,83,84,85,106,110,111,113,119,135,139,143,144,179,389,427,443,444,445,465,990,993,995,1025,1027,1433,2049,2121,3128,3306,3389,5009,5432,5631,5666,5800,5900,8000,8008,8009,8080,8081,8443,9100,9200,5672,27017,27015,25565', arguments='-A', callback=procesar_resultado)
# while nma.still_scanning():
#     print("Aguantiiando >>>")
#     nma.wait(2)

if __name__ == '__main__':
    thread1 = scanThread(1, 'Thread-1')
    thread2 = scanThread(2, 'Thread-2')
    thread3 = scanThread(3, 'Thread-3')
    thread4 = scanThread(4, 'Thread-4')
    thread5 = scanThread(5, 'Thread-5')
    thread6 = scanThread(6, 'Thread-6')
    thread7 = scanThread(7, 'Thread-7')
    thread8 = scanThread(8, 'Thread-8')

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            print('Killing program...')
            for t in threading.enumerate():
                try:
                    t.stop()
                except:
                    pass

    print('Exiting Main Thread')
