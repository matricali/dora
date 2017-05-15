FROM busybox

MAINTAINER Jorge Matricali <jorgematricali@gmail.com>

ADD python2.7-static /bin/python
RUN chmod a+x /bin/python

WORKDIR /var/www/
EXPOSE 8080

CMD [ "python", "-m", "SimpleHTTPServer", "8080" ]
