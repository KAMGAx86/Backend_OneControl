from fastapi import FastAPI
from endpoints import data_endpoint,auth_endpoint
from database import engine
import models

app = FastAPI()

# connexion au model si il n'exites pas on les creer(les table)
models.Base.metadata.create_all(bind=engine)

#inclure un router
app.include_router(data_endpoint.router)
app.include_router(auth_endpoint.router)