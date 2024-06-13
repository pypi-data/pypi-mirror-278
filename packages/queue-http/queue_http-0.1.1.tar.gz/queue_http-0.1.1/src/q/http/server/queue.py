from typing import TypeVar
from q.api import Queue
from fastapi import FastAPI
from .read import read_api
from .write import write_api

T = TypeVar('T')
U = TypeVar('U')

def api(queue: Queue[T], *, timeout: int = 15) -> FastAPI:

  app = FastAPI(generate_unique_id_function=lambda route: route.name)
  app.mount('/read', read_api(queue, timeout=timeout))
  app.mount('/write', write_api(queue))

  return app