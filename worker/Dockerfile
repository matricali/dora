FROM alpine

MAINTAINER Jorge Matricali <jorgematricali@gmail.com>

COPY requeriments.txt /requeriments.txt
COPY dbot.py /dbot.py
COPY entrypoint.sh /entrypoint.sh

RUN apk add --no-cache bash git py2-pip nmap \
	&& pip2 install --upgrade pip \
	&& pip2 install -r /requeriments.txt

# exectute start up script
ENTRYPOINT ["/entrypoint.sh"]
