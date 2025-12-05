from fastapi import FastAPI
from endpoints import data_endpoint


app = FastAPI()


#inclure un router
app.include_router(data_endpoint.router)