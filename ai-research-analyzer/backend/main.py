from fastapi import FastAPI
from api.routes import upload

app = FastAPI()

# Register API routes
app.include_router(upload.router, prefix="/api")