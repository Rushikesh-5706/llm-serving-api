FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install --no-cache-dir fastapi uvicorn transformers torch python-dotenv

FROM python:3.10-slim
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY app ./app
COPY run.sh .
EXPOSE 8000
CMD ["./run.sh"]
