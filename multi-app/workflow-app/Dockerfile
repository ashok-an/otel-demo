FROM golang:1.18-alpine

WORKDIR /go/app

COPY app.go .

RUN go build -o main app.go

EXPOSE 8080
ENV BUILD_URL=build-app:5001
ENV TEST_URL=build-app:3001

CMD ["./main"]