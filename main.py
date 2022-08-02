import secure
import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI, APIRouter
from fastapi.templating import Jinja2Templates
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
from starlette.responses import JSONResponse, RedirectResponse, HTMLResponse

import utils
from utils.path import get_segment
from frontend.routers.api import projects
from utils.dependency import get_db


app = FastAPI()

router = APIRouter(tags=["frontend"], include_in_schema=False)

templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def redirect_to_login():
    return RedirectResponse("/home")


# region crud


async def get_project_from_db_by_id(db: Session, project_id: int):
    db_project = (
        db.query(utils.models.Projects)
        .filter(utils.models.Projects.id == project_id)
        .first()
    )
    if not db_project:
        raise HTTPException(status_code=404, detail="Project Not Found")
    return db_project


async def get_all_projects_from_db(db: Session):
    db_project = db.query(utils.models.Projects).all()
    return db_project


# endregion crud


@app.get(
    "/project/{project_id}",
    response_class=HTMLResponse,
)
async def home_page(project_id: int, request: Request, db: Session = Depends(get_db)):
    db_project = await get_project_from_db_by_id(db, project_id=project_id)

    return templates.TemplateResponse(
        "project.html",
        context={"request": request, "project": db_project},
    )


@app.get(
    "/home",
    response_class=HTMLResponse,
)
async def home_page(request: Request, db: Session = Depends(get_db)):
    db_project = await get_all_projects_from_db(db)

    return templates.TemplateResponse(
        "projects.html",
        context={"request": request, "projects": db_project},
    )


app.include_router(projects.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
