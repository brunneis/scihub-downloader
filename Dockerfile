# Sci-Hub PDF downloader through Tor Network
# Copyright (C) 2016 Rodrigo Martínez <dev@brunneis.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

FROM centos:7.2.1511
MAINTAINER "Rodrigo Martínez" <dev@brunneis.com>

################################################
# SCI-HUB DOWNLOADER
################################################

ENV EPEL_RPM epel-release-latest-7.noarch.rpm
ENV EPEL_URL https://download-ib01.fedoraproject.org/pub/epel/$EPEL_RPM

# UTF-8 locale
RUN localedef -c -f UTF-8 -i en_US en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

RUN \
	yum -y update \
	&& yum -y install \
		wget \
		git \
		httpd \
	&& yum clean all \
	&& wget $EPEL_URL \
	&& rpm -i $EPEL_RPM \
	&& rm -f $EPEL_RPM \
	&& yum -y install \
		tor \
		privoxy \
		python-devel \
		python-pip \
	&& git clone https://github.com/aaronsw/pytorctl.git \
	&& git clone https://github.com/ahupp/python-magic.git \
	&& pip install \
		pytorctl/ \
		python-magic/ \
		beautifulsoup4 \
		requests \
		libmagic \
	&& echo "forward-socks5 / localhost:9050 ." >> /etc/privoxy/config \
	&& rm -f /etc/httpd/conf.d/welcome.conf \
	&& rm -rf /var/www/html \
	&& ln -s /data /var/www/html

# Data volume
VOLUME ["/data"]

# Scripts
COPY init.sh /
COPY download.py /
RUN chmod +x /init.sh /download.py

# The container launches Privoxy, Httpd and Tor
CMD /init.sh
