from fastapi import FastAPI
from backend.api.routes import upload
from backend.api.routes import analyze
from backend.api.routes import recommend

app = FastAPI()

# Register API routes
app.include_router(upload.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(recommend.router, prefix="/api")
