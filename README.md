# Movie-test-submission
This repository contains my submission for the Sysadmin & Software Developer Test exercise. The task involved fixing a broken build for a simple REST server, developing a command-line client to query movie counts by year, and containerizing both components using Docker. I completed all three parts, overcoming several challenges along the way. The language used for the client is Python, chosen for its simplicity and ease of use. The final container includes the fixed server and the client, allowing them to run together efficiently.
The exercise was a valuable learning experience, highlighting the importance of troubleshooting setup issues, adapting to tool limitations, and ensuring compatibility across environments. Below, I describe each part, the hurdles I faced, and how I resolved them, followed by instructions for building and running the components.

# Part 1: Fixing the Server
The repository provided a Makefile that did not build the server correctly due to issues with the go generate directive, which relied on shell commands incompatible with my Windows environment.

Hurdles Faced
Initial setup: Cloned the repository using GitHub Desktop.
Command not found errors: The go command was not recognized in Git Bash, requiring repairs to the Go installation and manual PATH additions.
Make command missing: I installed make using Chocolatey, but encountered an existing installation that needed backup and removal.
Makefile syntax issues: Errors like "missing separator" due to spaces instead of tabs, and shell command failures on Windows.
Go version mismatches: The go.mod required a higher Go version, leading to build failures.

 # How I Fixed It
Used Git Bash for Unix-like compatibility.
Modified the Makefile to manually generate version.go using bash-friendly commands, added go mod tidy, and changed the output to "movie-server" for Linux compatibility in the container.
Verified the build locally and tested the server with curl for authentication and movie queries.

Highlights
The server now compiles and runs without altering the source code, using basic authentication (username: "username", password: "password").
This part taught me the importance of cross-platform build processes.

# Part 2: Writing the Client
I developed a command-line Python application that connects to the server, accepts one or more years as input, and prints the number of films for each year. The code prioritizes clarity with separate functions for authentication and counting, and is organized for potential extensions (e.g., adding more endpoints).

Hurdles Faced
Initial Go attempt: Dependency and version issues led me to switch to Python for simplicity.
Syntax errors: F-strings and non-ASCII characters caused problems in Python 2; I rewrote using concatenation.
Module imports: "requests" was not installed, leading to errors; switched to built-in urllib2 to avoid installations.
Token expiration: The server's token lasts only 10 seconds, causing 401 errors during paging; added automatic refresh logic.
Connection errors: [Errno 10061] when the server was not running.

# How I Fixed It
Used built-in modules (urllib2, json) for HTTP requests and JSON parsing.
Implemented a loop to fetch all pages for a year, counting movies until less than 10 or 404.
Added token refresh on 401 errors to handle expiration during long queries.
Tested with the local server, ensuring it handles multiple years.

Highlights
The client is robust, with error handling and refresh logic, making it maintainable.
Output example: For years 2000 and 2010, it counted 4619 and 11591 movies, respectively, refreshing tokens as needed.

# Part 3: Containerize
I packaged the server and the client in a Docker container, fixing the server build inside, running the server, and making the client executable.

Hurdles Faced
Docker setup: App wouldn't open; resolved by reinstalling and enabling WSL.
Dockerfile errors: Go version mismatch (1.22 vs 1.24.6 required); Python install failed ( 'python' not available, used 'python3').
Executable name: "movie-server.exe" not found in Linux container; removed .exe in Makefile.
Build arguments: Missing "." in command; file naming issues (e.g., "Dockerfile.dockerfile").
Run errors: Port conflicts and "no such file" for executable.

How I Fixed It
Used golang:1.25.1-bookworm base for compatibility.
Updated Makefile to output "movie-server" (no .exe).
Installed python3 in Dockerfile.
Rebuilt and tested multiple times, adjusting for Linux environment.

Highlights
The container is efficient, containing only necessary files, and supports automated builds.
It demonstrates good practices like multi-stage builds (though simplified here for the test).

# How to Build, Test, and Run
# Prerequisites
Git, Go, Python 2/3, Docker Desktop installed.
Clone this repository: git clone [your-repo-url].

# Building and Running Locally (Without Container)
Server: In movie-server folder, make build, then make run (runs on :8080).
Client: python movie_client.py 2000 2010 (with server running).

# Building and Running the Container
Build: docker build -t movie-box . (takes ~5-10 minutes).
Run server: docker run -p 8080:8080 movie-box (starts server).
Test client outside: python movie_client.py 2000 2010.
Run client inside: docker run -it movie-box python3 /app/movie_client.py 2000 2010.
For quality checks: The project can be tested manually; future additions could include automated tests with pytest for the client.
