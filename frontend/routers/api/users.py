from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Security
from pydantic import BaseModel
from sqlalchemy.orm import Session

from utils.dependency import get_db
import utils.default_schemas
import utils.models

router = APIRouter(
    prefix="/api/user",
    tags=["Application User"],
)


# region schemas
class FullApplicationUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str


class OptionalFullApplicationUserRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]


# endregion schemas


# region crud


async def get_member_from_db(db: Session, user_id: int):
    return (
        db.query(utils.models.ApplicationUser)
        .filter(utils.models.ApplicationUser.id == user_id)
        .first()
    )


async def delete_db_user(db: Session, user_id: int):
    member = await get_member_from_db(db, user_id=user_id)
    name = f"{member.first_name} {member.last_name}"
    db.delete(member)
    db.commit()
    return f"User: {name} Deleted."


async def create_db_user(
    db: Session, first_name: str, last_name: str, email: str, phone_number: str
):
    db_user = utils.models.ApplicationUser()
    db_user.first_name = first_name
    db_user.last_name = last_name
    db_user.email = email
    db_user.phone_number = phone_number
    db.add(db_user)
    db.commit()
    return db_user


# endregion crud

# region endpoints

# region endpoints.get


@router.get("/{user_id}", response_model=utils.default_schemas.ApplicationUser)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get User By ID
    """
    db_user = await get_member_from_db(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return db_user


# endregion endpoints.get


# region endpoints.put


@router.put(
    "/{user_id}",
    response_model=utils.default_schemas.ApplicationUser,
)
async def update_user_by_id(
    user_id: int,
    userData: OptionalFullApplicationUserRequest,
    db: Session = Depends(get_db),
):
    db_user = await get_member_from_db(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    db_user.email = userData.email
    db_user.phone_number = userData.phone_number
    db.add(db_user)
    db.commit()
    return db_user


# endregion endpoints.put


# region endpoints.post


@router.post(
    "/create",
    response_model=utils.default_schemas.ApplicationUser,
)
async def create_user(
    userData: FullApplicationUserRequest, db: Session = Depends(get_db)
):
    db_user = await create_db_user(
        db,
        userData.first_name,
        userData.last_name,
        userData.email,
        userData.phone_number,
    )
    return db_user


# endregion endpoints.post

# region endpoint.delete


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    await delete_db_user(db, user_id=user_id)
    return delete_db_user


# endregion endpoint.delete

# endregion endpoints
