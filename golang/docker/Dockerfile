FROM golang:1.14-buster

WORKDIR /app

COPY src/ .

RUN go install && go build

EXPOSE 8001

CMD "./app"

