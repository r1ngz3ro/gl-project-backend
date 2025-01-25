# this commit contians the files as they will be uploaded on the server
# frontend
   - put your frontend here so that nginx and docker can find it
# Nginx Configuration with Enhanced Features

## Overview
This Nginx configuration enhances security, performance, and reliability while serving a frontend and backend application.

## Features

### 1. **Security Headers**
- **X-Frame-Options DENY**: Prevents clickjacking attacks by disallowing the page to be embedded in an iframe.
- **X-XSS-Protection**: Enables cross-site scripting (XSS) protection in browsers.
- **X-Content-Type-Options**: Prevents MIME-type sniffing to mitigate certain attacks.
- **Referrer-Policy**: Controls when the referrer information is sent.
- **Content-Security-Policy**: Restricts resource loading to the same origin, reducing risks of cross-site scripting attacks.

### 2. **Rate Limiting**
- Limits API requests to 10 per second per IP to prevent abuse.
- Burst limit of 20 requests, allowing short spikes without overwhelming the server.
- routes request to 6666 for backend and 80 for frontend

### 3. **Gzip Compression**
- Reduces response sizes for various content types, improving load times and reducing bandwidth usage.

### 4. **Access Restrictions**
- Denies access to hidden files (e.g., `.git`, `.env`) to prevent unauthorized exposure of sensitive data.

## Summary
This configuration optimizes performance, enhances security, and ensures proper handling of WebSocket connections. It also includes rate limiting and gzip compression to improve efficiency.

# Docker Compose Commands

This document provides an explanation of various Docker Compose commands commonly used for managing services in a multi-container application.

---

## `docker-compose up -d`
- **Description**: Starts up the services defined in your `docker-compose.yml` file in detached mode (in the background).
- **Usage**: This will create and start the containers as specified in the configuration file without attaching to their output.

---

## `docker-compose run --rm backend alembic upgrade head`
- **Description**: Runs a one-off command in a new container based on the `backend` service. The `--rm` flag ensures the container is removed after the command finishes.
- **Command**: Executes Alembic migrations (database schema upgrades) by running the `alembic upgrade head` command inside the `backend` container.
  
---

## `docker-compose build`
- **Description**: Builds or rebuilds services defined in your `docker-compose.yml` file.
- **Usage**: It is useful when you modify the Dockerfile or the images for the services and need to rebuild them.

---

## `docker-compose restart`
- **Description**: Restarts all services defined in the `docker-compose.yml` file.
- **Usage**: This is useful when you need to refresh your services without fully stopping and recreating them.

---

## `docker-compose down`
- **Description**: Stops and removes all containers, networks, and volumes associated with the services defined in your `docker-compose.yml` file.
- **Usage**: This command is useful when you want to completely shut down and clean up your environment.

---

## `docker-compose run --rm backend alembic upgrade head`
- **Description**: (Repeat of Command #2)
  - Runs Alembic database migrations inside a one-off container for the `backend` service.
  - Removes the container after the command finishes.

---

## `docker-compose run backend pytest`
- **Description**: Runs `pytest` tests in the `backend` service container.
- **Usage**: This allows you to run unit tests or other types of tests in the `backend` container, useful for test-driven development (TDD).

---

## `docker-compose run frontend test`
- **Description**: Runs tests inside the `frontend` container.
- **Usage**: This is typically used for running frontend unit or integration tests in a containerized environment.

---

## `docker-compose logs`
- **Description**: Displays logs for all running services.
- **Usage**: This helps you monitor the output from all 


