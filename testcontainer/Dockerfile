FROM ubuntu:20.04

EXPOSE 8888

RUN apt-get clean
RUN apt-get -y update
ARG DEBIAN_FRONTEND="noninteractive"
# see: https://github.com/phusion/baseimage-docker/issues/319
RUN apt-get -y install apt-utils

RUN apt-get -y install software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y update

RUN apt-get -y install python3.6
RUN apt-get -y install python3.7
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-venv
RUN apt-get -y install python3.6-venv
RUN apt-get -y install python3.7-venv
# python 3.8 is laready the default python3 in focal (20.04)
RUN mkdir /devel
RUN mkdir /results
WORKDIR /devel
# define the arg handed over by --build-args in invoke task
ARG POW_WHEEL
#RUN echo ${POW_WHEEL} > ./args.txt
# copy the latest build wheel
COPY ./${POW_WHEEL} .
# install the wheel
RUN pip3 install ${POW_WHEEL}

ENV PYTHONPATH=/devel

#
# python 3.6
# 
RUN generate_app -n testapp36 -p .
RUN cd /devel/testapp36
WORKDIR /devel/testapp36
RUN python3.6 -m venv .venv
RUN /bin/bash -c "source /devel/testapp36/.venv/bin/activate"
RUN /devel/testapp36/.venv/bin/pip install --upgrade pip
RUN /devel/testapp36/.venv/bin/pip install -r requirements.txt
RUN cd /devel/testapp36/tests
WORKDIR /devel/testapp36/tests
RUN /devel/testapp36/.venv/bin/python3.6 runtests.py
RUN cp /devel/testapp36/views/testreport.html /results/testresults36.html
#RUN cp /devel/testapp36/views/testreport.xml /results/testresults36.xml

#
# python 3.7
# 
RUN cd /devel
WORKDIR /devel
RUN generate_app -n testapp37 -p .
RUN cd /devel/testapp37
WORKDIR /devel/testapp37
RUN python3.7 -m venv .venv
RUN /bin/bash -c "source /devel/testapp37/.venv/bin/activate"
RUN /devel/testapp37/.venv/bin/pip install --upgrade pip
RUN /devel/testapp37/.venv/bin/pip install -r requirements.txt
RUN cd /devel/testapp37/tests
WORKDIR /devel/testapp37/tests
RUN /devel/testapp37/.venv/bin/python3.7 runtests.py
RUN cp /devel/testapp37/views/testreport.html /results/testresults37.html
#RUN cp /devel/testapp37/views/testreport.xml /results/testresults37.xml

#
# python 3.8
# 
RUN cd /devel
WORKDIR /devel
RUN generate_app -n testapp38 -p .
RUN cd /devel/testapp38
WORKDIR /devel/testapp38
RUN python3.8 -m venv .venv
RUN /bin/bash -c "source /devel/testapp38/.venv/bin/activate"
RUN /devel/testapp38/.venv/bin/pip install --upgrade pip
RUN /devel/testapp38/.venv/bin/pip install -r requirements.txt
RUN cd /devel/testapp38/tests
WORKDIR /devel/testapp38/tests
RUN /devel/testapp38/.venv/bin/python3.8 runtests.py
RUN cp /devel/testapp38/views/testreport.html /results/testresults38.html
#RUN cp /devel/testapp38/views/testreport.xml /results/testresults38.xml

# serve the results
RUN cd /devel/testapp38
WORKDIR /devel/testapp38
RUN cp /results/* /devel/testapp38/static
CMD ["/bin/bash", "-c", "/devel/testapp38/.venv/bin/python3.8 /devel/testapp38/server.py"]

#CMD ["/bin/bash"]