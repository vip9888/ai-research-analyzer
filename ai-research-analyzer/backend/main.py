from fastapi import FastAPI
from backend.api.routes import upload
from api.routes import analyze

app = FastAPI()

# Register API routes
app.include_router(upload.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")