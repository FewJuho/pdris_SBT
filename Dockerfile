FROM alpine:3.11

RUN apk add --no-cache \
    openssh-client \
    ansible \
    git \
    sshpass \
    python3 \
    py3-pip \
    docker-cli \
    docker-py

COPY ./ansible /ansible
WORKDIR /ansible
