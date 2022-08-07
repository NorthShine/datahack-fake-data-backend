FROM python:3.8

WORKDIR /fake_data_generator

COPY . .

RUN apt-get update -y && apt-get upgrade -y && apt install -y default-jdk
RUN python -m pip install -r requirements.txt
RUN chmod a+rwx docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]