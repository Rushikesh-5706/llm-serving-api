import os

MODEL_NAME = os.getenv("MODEL_NAME", "distilgpt2")
API_KEY = os.getenv("API_KEY", "changeme")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
