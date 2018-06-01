####################
#
# Run:
#     docker run -it --rm -p 8008:8008 -p 8009:8009 -p 1900:1900/udp -p 5353:5353/udp  --name flask local/flask bash
#     docker run -it --rm --privileged --net="host" --name tvcast local/tvcast
#     docker run -d --privileged --net="host" --name tvcast local/tvcast
# Build:
#     docker build -t local/flask .
# Gunicorn HTTP Server
#     gunicorn --workers 3 --bind 0.0.0.0:8000 handler
# Refer:
# Command:
#
####################

FROM python:3.7-rc-stretch

ENV TERM=xterm
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_ALL=C.UTF-8 

# Add Files
#ADD container-files/mitmf /usr/bin/mitmf
ADD app /app

#RUN apt-get update \
#    && apt-get install -y \
#            python-pip \
#            vim 

RUN pip install flask gunicorn pychromecast lxml pdbpp --no-cache-dir

WORKDIR /app

# pychromecast
#RUN cd /app \
#    && git clone https://github.com/balloob/pychromecast.git \
#    && pip install -r pychromecast/requirements.txt

# custom plugins
# SSlstrip2 - https://github.com/singe/sslstrip2/tree/892b014bd1b62e01f5ea0924839d08a931a6a2b1
# Dns2Proxy - https://github.com/singe/dns2proxy/tree/38428f60770fd8639e61a6bc91d6d7318086755f
#RUN cd /tmp/plugins/sslstrip2 && python setup.py install



EXPOSE 5000
#CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "handler"]
