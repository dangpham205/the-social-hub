ARG ELK_VERSION
FROM elasticsearch:${ELK_VERSION}

ARG ELASTICSEARCH_PORT
ENV ELASTICSEARCH_PORT ${ELASTICSEARCH_PORT}
EXPOSE ${ELASTICSEARCH_PORT}
RUN cd /usr/share/elasticsearch && \
  bin/elasticsearch-plugin install analysis-icu
