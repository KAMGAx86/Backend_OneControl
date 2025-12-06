from fastapi import FastAPI
from endpoints import data_endpoint
from database import engine
import models

app = FastAPI()


#inclure un router
app.include_router(data_endpoint.router)