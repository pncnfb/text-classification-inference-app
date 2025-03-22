FROM python:3.11.2-slim-bullseye as builder

RUN apt-get -y upgrade


FROM builder as production

WORKDIR /inference_application
COPY . /inference_application

RUN pip install .
RUN chmod 0700 entry_point.sh

ENTRYPOINT [ "./entry_point.sh" ]
