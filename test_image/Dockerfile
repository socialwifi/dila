FROM python:3.6
RUN apt-get update && apt-get install -y libldap2-dev libsasl2-dev && rm -rf /var/lib/apt/lists/*
COPY base_requirements.txt /package/
RUN pip install -r /package/base_requirements.txt
COPY dila /package/dila
COPY setup.py /package/
RUN pip install -e /package
WORKDIR /package
RUN bash -c 'mv *.egg-info $(python -c "import site; print(site.getsitepackages()[0])")'
COPY test_config.py /package
ENV DILA_CONFIG_MODULE=test_config
CMD dila run_dev_server
