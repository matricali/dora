from flask import Flask
import nmap

dora = Flask(__name__)


@dora.route('/api/scan/<target>')
def perform_scan(target):
    nm = nmap.PortScanner()
    nm.scan(target)
    # return 'El target a escanear es %s' % target
    return nm.all_hosts()


if __name__ == '__main__':
    dora.run(host='0.0.0.0', port=80, debug=True)
