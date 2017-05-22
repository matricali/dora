FROM alpine

MAINTAINER Jorge Matricali <jorgematricali@gmail.com>

RUN apk add --no-cache bash git
RUN apk add --no-cache nginx uwsgi uwsgi-python
RUN apk add --no-cache nmap nmap-scripts
RUN apk add --no-cache py2-pip \
	&& pip2 install --upgrade pip

RUN pip2 install flask

ENV APP_DIR /dora

# app dir
RUN mkdir ${APP_DIR} \
	&& chown -R nginx:nginx ${APP_DIR} \
	&& chmod 777 /run/ -R \
	&& chmod 777 /root/ -R
VOLUME [${APP_DIR}]
WORKDIR ${APP_DIR}

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 80

# copy config files into filesystem
COPY nginx.conf /etc/nginx/nginx.conf
COPY frontend.ini /frontend.ini
COPY entrypoint.sh /entrypoint.sh


# exectute start up script
ENTRYPOINT ["/entrypoint.sh"]
