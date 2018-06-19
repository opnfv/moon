FROM python:3.5

LABEL Name=Dashboard
LABEL Description="User interface for the Moon platform"
LABEL Maintainer="Thomas Duval"
LABEL Url="https://wiki.opnfv.org/display/moon/Moon+Project+Proposal"

ENV MANAGER_HOST="127.0.0.1"
ENV MANAGER_PORT=30001
ENV KEYSTONE_HOST="127.0.0.1"
ENV KEYSTONE_PORT=30005
ENV OPENSTACK_HOST="127.0.0.1"
ENV OPENSTACK_KEYSTONE_URL="http://${KEYSTONE_HOST}:${KEYSTONE_PORT}/v2.0"

USER root

WORKDIR /root/
ADD . /root

RUN git clone https://git.openstack.org/openstack/horizon

WORKDIR /root/horizon

RUN pip install --no-cache-dir -c http://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt .

RUN cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py
RUN pip install --no-cache-dir tox

WORKDIR /root/

RUN cp -v moon/enabled/_32000_moon.py horizon/openstack_dashboard/local/enabled/_32000_moon.py
RUN cp -rv moon/ horizon/openstack_dashboard/dashboards/

CMD ["/bin/sh", "/root/run.sh"]