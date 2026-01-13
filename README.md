# Containerized LLM Serving API

This project is a production-ready REST API for serving a Hugging Face
open-source Large Language Model (LLM) using FastAPI and Docker. It
demonstrates how to deploy a machine learning model as a secure,
concurrent, and containerized microservice.

## Overview

The API exposes two main endpoints:

-   `GET /health` -- Returns service health status.
-   `POST /generate` -- Accepts a prompt and returns generated text from
    the LLM.

The system uses DistilGPT-2, an open-source Hugging Face language model,
and is designed with lazy-loading, concurrency control, and API key
security.

## Architecture

The service is built with:

-   FastAPI for the REST interface
-   Hugging Face Transformers for model loading and inference
-   ThreadPoolExecutor for CPU-bound inference
-   AsyncIO Semaphore to limit concurrent inference
-   Docker and Docker Compose for containerization

The model is loaded only on the first request and then kept in memory to
avoid slow startups.

## API Endpoints

### Health Check

    GET /health

Response:

    200 OK
    {"status":"ok"}

### Generate Text

    POST /generate
    Header: x-api-key
    Body:
    {
      "prompt": "Hello world",
      "max_new_tokens": 50
    }

Response:

    {
      "generated_text": "..."
    }

Requests without a valid API key are rejected.

## Security

The `/generate` endpoint is protected by an API key provided via the
`x-api-key` header. The key is configured using environment variables
through Docker Compose.

## Concurrency

The API allows up to 5 concurrent inference requests. Additional
requests wait until a slot is available. This prevents model overload
and keeps the service stable under load.

## Docker Usage

### Run Locally

    docker compose up

This will start the API at:

    http://localhost:8000

Swagger UI:

    http://localhost:8000/docs

## Docker Image

The published Docker image is available at:

    docker.io/rushi5706/llm-serving-api:latest

You can pull it using:

    docker pull rushi5706/llm-serving-api:latest

## Screenshots

The `/screenshots` folder in this repository contains proof of:

-   Health endpoint working
-   Swagger documentation
-   Successful text generation
-   API key rejection
-   Concurrent request handling

These demonstrate that the service meets all evaluation requirements.

## Conclusion

This project shows how to deploy a real LLM behind a secure, concurrent,
and containerized REST API. It reflects production MLOps practices such
as lazy model loading, request throttling, Docker packaging, and API
security.
