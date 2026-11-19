FROM alpine:3.21

# Актуальную версию смотреть: https://github.com/pocketbase/pocketbase/releases
ARG PB_VERSION=0.40.6

RUN apk add --no-cache unzip ca-certificates curl

ADD https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip /tmp/pb.zip
RUN unzip /tmp/pb.zip -d /pb && rm /tmp/pb.zip

EXPOSE 8090
VOLUME /pb/pb_data

CMD ["/pb/pocketbase", "serve", "--http=0.0.0.0:8090"]
