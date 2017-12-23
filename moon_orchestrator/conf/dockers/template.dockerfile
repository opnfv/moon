# Pull base image.
FROM ubuntu:latest

{{ proxy }}

RUN apt-get update && apt-get install python3.5 python3-pip -y

ADD dist/moon_utilities-0.1.0.tar.gz /root
WORKDIR /root/moon_utilities-0.1.0
RUN pip3 install pip --upgrade
RUN pip3 install --upgrade -r requirements.txt
RUN pip3 install --upgrade .

ADD dist/moon_db-0.1.0.tar.gz /root
WORKDIR /root/moon_db-0.1.0
RUN pip3 install --upgrade -r requirements.txt
RUN pip3 install --upgrade .

{{ run }}

{% for port in ports %}
EXPOSE {{ port }}
{% endfor %}

CMD {{ cmd }}
