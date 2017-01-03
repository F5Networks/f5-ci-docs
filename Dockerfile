FROM ubuntu:latest

MAINTAINER Jodie Putrino <j.putrino@f5.com>
## Adapted from https://github.com/rtfd/readthedocs-docker-images/blob/master/14.04/Dockerfile

ENV DEBIAN_FRONTEND noninteractive
ENV APPDIR /app
ENV LANG C.UTF-8

RUN apt-get update \
    && apt-get -y install \
        ack-grep \
        build-essential \
        bzr \
        curl \
        doxygen \
        emacs \
        g++ \
        git-core \
        graphviz \
        graphviz-dev \
        latex-cjk-chinese-arphic-bkai00mp \
        latex-cjk-chinese-arphic-bsmi00lp \
        latex-cjk-chinese-arphic-gbsn00lp \
        latex-cjk-chinese-arphic-gkai00mp \
        libcairo2-dev \
        libenchant1c2a \
        libevent-dev \
        libffi-dev \
        libfreetype6 \
        libfreetype6-dev \
        libgraphviz-dev \
        libjpeg-dev \
        libjpeg8-dev \
        liblcms2-dev \
        libmysqlclient-dev \
        libpq-dev \
        libtiff5-dev \
        libwebp-dev \
        libxml2-dev \
        libxslt-dev \
        libxslt1-dev \
        mercurial \
        nodejs-legacy \
        npm \
        pandoc \
        pkg-config \
        postgresql-client \
        python-dev \
        python-m2crypto \
        python-matplotlib \
        python-numpy \
        python-pandas \
        python-scipy \
        python3 \
        python3-dev \
        python3-matplotlib \
        python3-numpy \
        python3-pandas \
        python3-pip \
        python3-scipy \
        software-properties-common \
        sqlite \
        subversion \
        texlive-fonts-recommended \
        texlive-full \
        texlive-latex-extra \
        vim \
        wget \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN easy_install3 pip

COPY ./requirements.docs.txt /
COPY ./entrypoint.sh /entrypoint.sh

RUN pip install -r requirements.docs.txt
RUN npm install -g write-good

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/bin/bash"]

