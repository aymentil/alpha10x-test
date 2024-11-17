from fastapi import FastAPI
from src.api.routes.organizations import router as organizations_router

app = FastAPI()


app.include_router(organizations_router, prefix="/api/v1", tags=["organizations"])