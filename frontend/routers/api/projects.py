from datetime import datetime
from typing import Optional


from fastapi import APIRouter, Depends, HTTPException, Security
from pydantic import BaseModel
from sqlalchemy.orm import Session


import utils.default_schemas
import utils.models
from utils.dependency import get_db


router = APIRouter(prefix="/api/project", tags=["Projects"])

# region schemas
class ProjectRequest(BaseModel):
    title: str
    link: str
    picture: str
    user_id: int


class OptionalProjectRequest(BaseModel):
    title: Optional[str]
    link: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    picture: Optional[str]
    user_id: Optional[int]


# endregion schemas


# region crud
async def get_member_from_db(db: Session, user_id: int):
    return (
        db.query(utils.models.ApplicationUser)
        .filter(utils.models.ApplicationUser.id == user_id)
        .first()
    )


async def create_db_project(
    db: Session, title: str, link: str, picture: str, user_id: int
):
    db_project = utils.models.Projects()
    db_project.title = title
    db_project.link = link
    db_project.picture = picture
    db_project.user_id = user_id
    db_user = await get_member_from_db(db, user_id=user_id)
    db_project.first_name = db_user.first_name
    db_project.last_name = db_user.last_name
    db.add(db_project)
    db.commit()
    return db_project


async def get_project_from_db_by_id(db: Session, project_id: int):
    db_project = (
        db.query(utils.models.Projects)
        .filter(utils.models.Projects.id == project_id)
        .first()
    )
    if not db_project:
        raise HTTPException(status_code=404, detail="Project Not Found")
    return db_project


async def get_project_from_db_by_title(db: Session, title: str):
    db_project = (
        db.query(utils.models.Projects)
        .filter(utils.models.Projects.title == title)
        .first()
    )
    if not db_project:
        raise HTTPException(status_code=404, detail="Project Not Found")
    return db_project


async def delete_db_project(db: Session, project_id: int):
    db_project = await get_project_from_db_by_id(db, project_id=project_id)
    project_title = db_project.title
    db.delete(db_project)
    db.commit()
    return f"Project {project_title} Deleted"


# endregion crud

# region endpoints

# region endpoints.get


@router.get("/{project_id}", response_model=utils.default_schemas.Projects)
async def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    """
    Get Project by ID
    """
    db_project = await get_project_from_db_by_id(db, project_id=project_id)
    return db_project


@router.get("/title/{title}", response_model=utils.default_schemas.Projects)
async def get_project_by_title(title: str, db: Session = Depends(get_db)):
    """
    Get Project by Title
    """
    db_project = await get_project_from_db_by_title(db, title=title)
    return db_project


# endregion endponts.get

# region endpoints.post


@router.post(
    "",
    response_model=utils.default_schemas.Projects,
)
async def create_project(
    project_request: ProjectRequest, db: Session = Depends(get_db)
):
    project = await create_db_project(
        db,
        project_request.title,
        project_request.link,
        project_request.picture,
        project_request.user_id,
    )
    return project


# region endpoints.put


@router.put(
    "/update/{project_id}",
    response_model=utils.default_schemas.Projects,
)
async def update_full_project(
    project_id: int,
    project_request: OptionalProjectRequest,
    db: Session = Depends(get_db),
):

    db_project = await get_project_from_db_by_id(db, project_id=project_id)

    db_project.title = project_request.title
    db_project.link = project_request.link
    db_project.first_name = project_request.first_name
    db_project.last_name = project_request.last_name
    db_project.picture = project_request.picture
    db_project.user_id = project_request.user_id
    db.add(db_project)
    db.commit()
    return db_project


# endregion endponts.put

# region endpoints.delete


@router.delete("/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = await delete_db_project(db, project_id=project_id)
    return db_project


# endregion endpoints.delete

# endregion endpoints
