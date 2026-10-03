from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router
from utils.config import get_settings
settings=get_settings()
app=FastAPI(title=settings.app_name,version="1.0.0",description="AI-assisted legal document drafting API.")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,allow_credentials=True,allow_methods=["GET","POST"],allow_headers=["*"])
app.include_router(router)
@app.get("/")
def root(): return {"service":settings.app_name,"status":"running","environment":settings.app_env,"docs":"/docs"}
@app.get("/health")
def health(): return {"status":"ok"}
