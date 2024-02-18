from fastapi import Request
from fin.db import dynamodb
import logging

logger = logging.getLogger("middlware")

client = dynamodb.DDBFinClient()


async def log_time(request: Request, call_next):
    import time

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Processed request: {request.url.path} in {process_time} seconds")
    return response


async def load_user(request: Request, call_next):
    x_user = request.headers.get("x-user")
    logger.info(f"User: {x_user}")
    user = client.users.get_user(x_user) if x_user else None
    request.state.user = user
    request.state.db = client
    response = await call_next(request)
    return response
