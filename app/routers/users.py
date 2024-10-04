from fastapi import FastAPI,Depends,Response,status,HTTPException,APIRouter
from .. import models,schemas,utils
from ..database import engine,get_db,SessionLocal
from typing import List,Optional
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager


router = APIRouter()

@router.post('/users/register',response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    plan = db.query(models.GymPlans).filter(models.GymPlans.title == user.plan_title).first()

    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Gym plan not found")
    
    if user.plan_type == "monthly":
        remaining_days = 30
    elif user.plan_type == "quarterly":
        remaining_days = 90
    elif user.plan_type == "yearly":
        remaining_days = 365
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Plan Type")
    
    hashed_password = utils.hash(user.password)

    new_user = models.User(
        email=user.email,
        password = hashed_password,
        name=user.name,
        age=user.age,
        height=user.height,
        weight=user.weight,
        enrolled_plan_id=plan.id,  # Use the plan's ID
        remaining_days=remaining_days,
        plan_type = user.plan_type
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/users/{id}',response_model= schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    
    return user