import secure
import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse


from frontend.routers.api import projects


app = FastAPI()


@app.get("/home")
async def root():
    return {"message": "Hello World"}


app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def redirect_to_login():
    return RedirectResponse("/home")


app.include_router(projects.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
