import asyncio

request_semaphore = asyncio.Semaphore(5)
