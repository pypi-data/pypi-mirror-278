FROM python:3.10.11-alpine
COPY --from=caddy:2.4.6 /usr/bin/caddy /usr/local/bin/caddy

RUN apk add --no-cache bash docker-cli inotify-tools jq curl

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install pip==22.2.2

WORKDIR /opt/project
COPY requirements.txt ./
RUN pip install --no-cache -r requirements.txt

COPY setup.* test* README.md ./
COPY ingress/ ./ingress/
RUN pip install --no-cache -e .

CMD ["ingress", "control-loop"]
