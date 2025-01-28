FROM ubuntu:22.04

ENV USER=asphyxia

USER root
RUN apt update && apt install -y socat python3
RUN adduser $USER

USER $USER
WORKDIR /app
COPY ./checker.py /app/checker.py
COPY ./flag.txt /app/flag.txt
COPY ./asphyxia /app/asphyxia

EXPOSE 1337
CMD ["socat", "-T60", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 checker.py,nofork,stderr"]