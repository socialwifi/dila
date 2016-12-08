FROM python:3.6
COPY dila /package/dila
COPY setup.py /package/
COPY base_requirements.txt /package/
RUN pip install -r /package/base_requirements.txt
RUN pip install -e /package
COPY test_config.py /package
WORKDIR /package
ENV DILA_CONFIG_MODULE=test_config
CMD dila run_dev_server
