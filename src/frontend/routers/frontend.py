from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.dependency import get_db
from sqlalchemy.orm import Session


from main import app
from utils.path import get_segment


router = APIRouter(tags=["frontend"], include_in_schema=False)

templates = Jinja2Templates(directory="src/templates")


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


# endregion crud


@router.get(
    "/project/{project_id}",
    response_class=HTMLResponse,
)
async def home_page(project_id: int, request: Request, db: Session = Depends(get_db)):
    db_project = get_project_from_db_by_id(db, project_id=project_id)
    segment = get_segment(request)
    return templates.TemplateResponse(
        "portfolio/project.html",
        context={"request": request, "segment": segment, "project": db_project},
    )
