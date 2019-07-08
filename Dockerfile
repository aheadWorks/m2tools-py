FROM python:3.6

ARG SOURCES_SIGNATURE
ARG COMPOSER_SUPPORT_DOCS
ARG COMPOSER_SUPPORT_EMAIL
ARG LICENSE_URL

ENV SOURCES_SIGNATURE=${SOURCES_SIGNATURE}
ENV COMPOSER_SUPPORT_DOCS=${COMPOSER_SUPPORT_DOCS}
ENV COMPOSER_SUPPORT_EMAIL=$COMPOSER_SUPPORT_EMAIL
ENV LICENSE_URL=${LICENSE_URL}

COPY m2tools /package/m2tools
COPY tests /package/tests
COPY setup.py /package/setup.py

COPY entrypoint.sh /entrypoint.sh
COPY ext.py /ext.py

WORKDIR /package
RUN pip install pytest click
RUN pip install -e .
RUN find . -name "*.pyc" -exec rm -f {} \;

ENTRYPOINT ["python", "/ext.py"]