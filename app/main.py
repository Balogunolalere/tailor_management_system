from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.api import auth, users, measurements, contacts, families
from app.database import engine, Base
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Authentication"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["Users"])
app.include_router(measurements.router, prefix=settings.API_V1_STR, tags=["Measurements"])
app.include_router(contacts.router, prefix=settings.API_V1_STR, tags=["Contacts"])
app.include_router(families.router, prefix=settings.API_V1_STR, tags=["Families"])

@app.get("/")
async def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."},
    )