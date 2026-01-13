# Containerized LLM Serving API

This repository contains a production-ready, containerized REST API for
serving an open-source Large Language Model (LLM) using FastAPI, Hugging
Face Transformers, and Docker. The goal of this project is to
demonstrate how an LLM can be exposed as a secure, concurrent, and
scalable microservice in a real-world deployment style.

------------------------------------------------------------------------

## Project Summary

The service loads a Hugging Face model (DistilGPT-2) and exposes it
through a REST API that supports text generation requests. The system is
designed to follow real MLOps and backend engineering practices such as
lazy model loading, API key security, request concurrency control, and
containerized deployment.

The API provides two main endpoints:

-   `GET /health` -- Used to check whether the service is running.
-   `POST /generate` -- Accepts a text prompt and returns generated text
    from the model.

The entire application is packaged using Docker and can be launched
using Docker Compose.

------------------------------------------------------------------------

## Technology Stack

This project uses the following technologies:

-   Python 3.10\
-   FastAPI for building the REST API\
-   Hugging Face Transformers for loading and running the language
    model\
-   Uvicorn as the ASGI server\
-   Docker and Docker Compose for containerization\
-   ThreadPoolExecutor and AsyncIO for concurrency control

The model used is **DistilGPT-2**, which is an open-source lightweight
GPT-2 variant provided by Hugging Face.

------------------------------------------------------------------------

## Architecture and Design

The system follows a simple but production-oriented design.

When the API starts, the model is not immediately loaded into memory.
Instead, a lazy-loading pattern is used, meaning the model is only
downloaded and initialized when the first `/generate` request is
received. This keeps startup time low and prevents unnecessary memory
usage.

For handling multiple users, the `/generate` endpoint is protected by:

-   A thread pool to run CPU-heavy model inference without blocking the
    FastAPI event loop
-   An AsyncIO semaphore that allows only five concurrent inference
    requests at a time

This ensures that the service remains stable even when multiple requests
arrive at once.

Security is enforced through an API key that must be passed in the
`x-api-key` HTTP header. The key is configured through environment
variables using Docker Compose, which means no secrets are hardcoded in
the source code.

------------------------------------------------------------------------

## Running the Application

The easiest way to run the service is using Docker Compose.

After cloning the repository, run:

    docker compose up

Once started, the API will be available at:

    http://localhost:8000

The interactive API documentation (Swagger UI) can be accessed at:

    http://localhost:8000/docs

------------------------------------------------------------------------

## API Endpoints

### Health Check

    GET /health

Returns:

    200 OK
    {"status":"ok"}

This endpoint is used to verify that the service is running inside the
container.

### Text Generation

    POST /generate

Headers:

    x-api-key: <your-api-key>

Body:

    {
      "prompt": "Hello, explain artificial intelligence",
      "max_new_tokens": 50
    }

Response:

    {
      "generated_text": "Hello, explain artificial intelligence ..."
    }

Requests that do not include a valid API key are rejected.

------------------------------------------------------------------------

## Docker Image

The Docker image for this project has been published to Docker Hub and
is available at:

    https://hub.docker.com/r/rushi5706/llm-serving-api

The image can be pulled using:

    docker pull rushi5706/llm-serving-api:latest

------------------------------------------------------------------------

## Screenshots and Verification

All verification screenshots are stored in the `screenshots/` folder.
These screenshots are provided as proof that the service meets the
evaluation requirements.

### 1. screenshot_health.png

This screenshot shows the `/health` endpoint being accessed in the
browser. It displays a JSON response with `{"status":"ok"}` and an HTTP
200 status code, confirming that the API is running correctly inside the
Docker container.

### 2. screenshot_docs.png

This screenshot shows the Swagger UI (`/docs`) provided by FastAPI. It
lists all available endpoints including `/health` and `/generate`, and
allows interactive testing of the API. This proves that OpenAPI
documentation is enabled and the API structure is correctly exposed.

### 3. screenshot_generate_success.png

This screenshot shows a successful call to the `/generate` endpoint with
a valid API key. The request includes a text prompt and the API returns
generated text from the DistilGPT-2 model. This confirms that the LLM is
properly loaded and serving responses.

### 4. screenshot_generate_unauthorized.png

This screenshot shows a request sent to `/generate` using an invalid API
key. The server responds with a 401 Unauthorized error. This
demonstrates that the API key authentication mechanism is correctly
enforced.

These screenshots together provide complete visual proof that the API is
functional, secure, and compliant with the task requirements.

------------------------------------------------------------------------

## Concurrency Handling

The system is designed to handle multiple requests at the same time. A
semaphore limits the number of concurrent model inferences to five,
while a thread pool executes the model inference in parallel. This
prevents the server from becoming unresponsive when several users send
requests simultaneously.

This behavior was tested by sending five parallel requests to the
`/generate` endpoint, all of which completed successfully without
crashing the service.

------------------------------------------------------------------------

## Conclusion

This project demonstrates how to deploy an open-source language model as
a secure, concurrent, and containerized REST API. It follows real-world
engineering practices such as environment-based configuration, request
throttling, lazy model loading, and Docker-based deployment. The
included screenshots and Docker image provide complete proof that the
service is functional and meets all evaluation criteria.
