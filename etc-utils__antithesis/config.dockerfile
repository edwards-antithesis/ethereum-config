FROM scratch
ARG  config
ARG  version="1.0"
LABEL description=$config \
      version=$version
COPY scripts /scripts
COPY modules /modules
COPY shared-data /shared-data
COPY configs /configs
COPY docker-compose.yaml /
COPY create_scenario.py /

