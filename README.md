[![Software License](https://img.shields.io/badge/license-BSD--3-brightgreen.svg?style=flat-square)](https://github.com/jorge-matricali/dora/blob/master/LICENSE.txt)

# Dora, the explorer
Dora is a network host discovery daemon. Built in _Python_ and _JavaScript_

## Requeriments
* Python 2.7
* ElasticSearch ~5.4.x
* AngularJS
* Bootstrap
* Nodejs
* npm
* bower

## Installation
It can be easily installed using _Docker_ and _docker-compose_

```bash
git clone --depth=1 https://github.com/jorge-matricali/dora.git

docker-compose up -d

cd dora/frontend
bower install
```
Then go to http://localhost:420/

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
