#!/usr/bin/env python
"""
Copyright 2017 Jorge Matricali

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function
import sys
import nmap
import time
import threading
import argparse
import signal
from elasticsearch import Elasticsearch
from geoip import geolite2
from faker import Faker

exit_flag = False
threads = []
es = Elasticsearch(['elasticsearch'])
nma = nmap.PortScannerAsync()
faker = Faker()
PORT_LIST = """7,9,13,21,22,23,25,26,37,53,79,80,81,82,83,84,85,106,110,111,113,
119,135,139,143,144,179,389,427,443,444,445,465,990,993,995,1025,1027,1433,2049,
2121,3128,3306,3389,5009,5432,5631,5666,5800,5900,8000,8008,8009,8080,8081,8443,
9100,9200,5672,27017,27015,25565"""


def teardown(signal=0):
    print('Stopping threads...')
    exit_flag = True
    try:
        for t in threads:
            try:
                t.stop()
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    sys.exit(signal)


def signal_handler(signal, frame):
    teardown(0)


class scanThread (threading.Thread):
    def __init__(self, threadID, name, **kwargs):
        super(scanThread, self).__init__()
        self._threadID = threadID
        self._name = name
        self._running = True

    def run(self):
        self.log('Starting thread...')
        self._nma = nmap.PortScannerAsync()
        while self._running:
            try:
                target = faker.ipv4()
                self.log('Performing scan on', target)
                self._nma.scan(
                    target, PORT_LIST, arguments='-A',
                    callback=self.procesar_resultado)
                while self._nma.still_scanning():
                    self._nma.wait(2)
            except Exception:
                self.log('Exiting thread...')
                self.stop()

    def stop(self):
        self.log('Stopping...')
        self._running = False

    def procesar_resultado(self, host, scan_result):
        if scan_result['nmap']['scanstats']['uphosts'] == '1':
            self.log(
                host, 'UP', scan_result['scan'][host]['hostnames'][0]['name'])
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
        print(time.ctime(time.time()), self._name, *args)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser(description='Dora Scanner Worker')

    parser.add_argument('-t', '--threads',
                        dest='numThreads', action='store', type=int,
                        default=1, help='Total number of threads to use')

    args = parser.parse_args()

    try:
        numThreads = int(args.numThreads)
    except NameError:
        numThreads = 1

    print('Starting %d threads...' % numThreads)

    threads = [None]*numThreads
    for nt in range(numThreads):
        threads[nt] = scanThread(nt+1, 'Thread-%d' % (nt+1))
        threads[nt].daemon = True
        threads[nt].start()

    while not exit_flag:
        pass

    print('Exiting Main Thread')
