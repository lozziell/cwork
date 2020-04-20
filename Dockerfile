FROM ubuntu:18.04
WORKDIR /mysymp
COPY . /mysymp
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && pip3 install flask \
  && pip3 install requests \
  && pip3 install cassandra-driver \
  && pip3 install flask-bcrypt
EXPOSE 80
CMD ["python", "symp.py"]

