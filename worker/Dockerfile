FROM alpine

MAINTAINER Jorge Matricali <jorgematricali@gmail.com>

COPY requirements.txt /requirements.txt
COPY dbot.py /dbot.py
COPY entrypoint.sh /entrypoint.sh

RUN apk add --no-cache bash git
RUN apk add --no-cache nmap nmap-scripts
RUN apk add --no-cache py2-pip \
	&& pip2 install --upgrade pip \
	&& pip2 install -r /requirements.txt

# exectute start up script
ENTRYPOINT ["/entrypoint.sh"]
