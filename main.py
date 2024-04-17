from fastapi import FastAPI
from routes import *
from database.connection import Base, engine

app = FastAPI()
app.include_router(root_router)


# @app.on_event("startup")
# def startup():
#     with engine.begin() as conn:
#         conn.run(Base.metadata.create_all)
