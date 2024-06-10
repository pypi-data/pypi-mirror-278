from contextlib import asynccontextmanager

database = None

@asynccontextmanager
async def lifespan(app):
    database = {}
    yield
