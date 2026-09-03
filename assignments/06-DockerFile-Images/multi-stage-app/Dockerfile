# Stage 1: Build the static binary
FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY main.go ./

# Compile statically linked binary (no CGO dependencies)
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o hello-multistage main.go

# Stage 2: Production minimal runtime
FROM alpine:latest

WORKDIR /app

# Copy only the compiled executable from the builder stage
COPY --from=builder /app/hello-multistage ./

EXPOSE 8080

CMD ["./hello-multistage"]
