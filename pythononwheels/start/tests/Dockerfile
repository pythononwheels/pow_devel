FROM ubuntu:20.04

EXPOSE 8080

RUN apt-get -y update
ARG DEBIAN_FRONTEND="noninteractive"
# see: https://github.com/phusion/baseimage-docker/issues/319
RUN apt-get -y install apt-utils

RUN apt-get -y install software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y update

RUN apt-get -y install python3.6
RUN apt-get -y install python3.7
# python 3.8 is laready the default python3 in focal (20.04)
RUN mkdir /devel
WORKDIR /devel

CMD ["/bin/bash"]