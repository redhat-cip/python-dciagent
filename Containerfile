FROM registry.access.redhat.com/ubi8/ubi-minimal

COPY . /usr/src/python-dciagent

RUN microdnf update && \
    microdnf install python39 procps-ng && \
    microdnf clean all
RUN pip-3.9 --no-cache-dir install 'ansible<2.10' && \
    pip-3.9 --no-cache-dir install /usr/src/python-dciagent

ENTRYPOINT ["/usr/local/bin/dci-agent-ctl"]
