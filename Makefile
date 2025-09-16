# Makefile for movie-server

.PHONY: build install clean run

default: build

generate:
	echo "package main" > version.go
	echo "" >> version.go
	echo "const version = \"$$(git describe --tags --always --long --dirty)\"" >> version.go

build: generate
	go mod tidy
	go build -o movie-server

install: generate
	go mod tidy
	go install

run: build
	./movie-server

clean:
	rm -f movie-server version.go