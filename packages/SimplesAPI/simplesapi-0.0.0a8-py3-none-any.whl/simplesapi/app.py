
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

from simplesapi import lifespan, settings
from simplesapi.auto_routing import register_routes

class SimplesConfig(BaseModel):
    verbose: Optional[bool] = Field(default=False)
    base_path: Optional[str] = Field(default="/")
    routes_path: Optional[str] = Field(default="routes")
    redis_url: Optional[str] = Field(default=settings.SIMPLESAPI_REDIS_URL)
    redis_ssl: Optional[bool] = Field(default=settings.SIMPLESAPI_REDIS_SSL)
    database_connection_string: Optional[str] = Field(default=settings.SIMPLESAPI_DB_CONN)

class SimplesAPI(FastAPI):
    def __init__(self, routes_path=None, *args, **kwargs):
        self.simples = SimplesConfig(routes_path=routes_path,**kwargs)
        super().__init__(lifespan=lifespan.lifespan, *args, **kwargs)
        if self.simples.routes_path:
            register_routes(self,self.simples.routes_path)

