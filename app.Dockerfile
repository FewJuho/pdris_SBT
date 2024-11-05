FROM alpine:3.11

RUN apk add --no-cache \
    python3 \
    sudo \
    bash \
    && ln -sf python3 /usr/bin/python

RUN adduser -D ansible && \
    echo "ansible ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ansible

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
