FROM golang:1.24-alpine AS builder

WORKDIR /app

# Copy go.mod and go.sum files
COPY whatsservice/go.mod whatsservice/go.sum ./
RUN go mod download

# Copy the source code
COPY whatsservice/ .

# Build the application
RUN CGO_ENABLED=0 go build -o whatsservice .

# Final stage
FROM alpine:latest

RUN apk add --no-cache ca-certificates

WORKDIR /app

# Copy the binary from the builder stage
COPY --from=builder /app/whatsservice .

# Expose the port
EXPOSE 3000

# Command to run
CMD ["./whatsservice"]
