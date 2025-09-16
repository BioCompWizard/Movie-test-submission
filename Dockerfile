# Start with a base with Go and Python.
FROM golang:1.25.1-bookworm

# Add Python.
RUN apt-get update && apt-get install -y python3

# Copy server and build.
COPY movie-server /app/movie-server
WORKDIR /app/movie-server
RUN make build

# Copy client.
COPY movie-client.py /app/movie-client.py

# Start server.
CMD ["./movie-server"]