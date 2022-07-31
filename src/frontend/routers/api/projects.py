from datetime import datetime
from typing import Optional


from fastapi import APIRouter, Depends, HTTPException, Security
from pydantic import BaseModel
from sqlalchemy.orm import Session


import utils.default_schemas
import utils.models
from utils.dependency import get_db


router = APIRouter(
    prefix="/api/project",
    tags=["Projects"]
)


class ProjectRequest(BaseModel):
    title: str
    link: str
    first_name: str
    last_name: str


async def create_db_project(
    db: Session,
    title: str,
    link: str,
    first_name: str,
    last_name: str,
):
    db_project = src.utils.models.Projects()
    db_project.title = title
    db_project.link = link
    db_project.first_name = first_name
    db_project.last_name = last_name
    db.add(db_project)
    db.commit()
    return db_project




@router.post(
    "/",
    response_model=utils.default_schemas.Projects,
)
async def create_project(
    release_request: ProjectRequest, db: Session = Depends(get_db)
):
    project = create_db_project(
        db, 
        release_request.title, 
        release_request.link, 
        release_request.first_name, 
        release_request.last_name
    )
    return project