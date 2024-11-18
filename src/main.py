from fastapi import FastAPI
from src.api.routes.organizations import router as organizations_router
from src.api.routes.transformed_organizations import router as transformed_organizations_router

app = FastAPI()


app.include_router(organizations_router, prefix="/api/v1", tags=["organizations"])
app.include_router(transformed_organizations_router, prefix="/api/v1", tags=["transformed_organizations"])