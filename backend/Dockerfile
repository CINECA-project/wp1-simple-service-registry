FROM python:3
LABEL Maintainer "CanDIG Project"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt && \
    python setup.py install

EXPOSE 3000

# Run the service registry server
# provide some explicit defaults if no arugments are given
ENTRYPOINT [ "service_registry", "--port", "3000"]
CMD [ "--logfile", "/data/service_registry.log",\
      "--database", "/data/services.sqlite" ]
