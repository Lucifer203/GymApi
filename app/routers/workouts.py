from fastapi import FastAPI,Depends,Response,status,HTTPException,APIRouter
from .. import models,schemas,utils,oauth2
from ..database import engine,get_db,SessionLocal
from typing import List,Optional
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from datetime import date


router  = APIRouter(prefix="/workouts",tags=["Workouts"])

@router.post("/create",response_model=schemas.Workout)
def create_workout(
    workout: schemas.WorkoutCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # create new workout
    new_workout = models.Workout(
        exercise_name=workout.exercise_name,
        date=workout.workout_date or date.today(),
        user_id = current_user.id
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    print(f"Created workout Id: {new_workout.id}")

    ## create workoutSets
    workout_sets = []
    for set_data in workout.sets:
        new_set = models.WorkoutSet(
            workout_id= new_workout.id,
            set_number=set_data.set_number,
            reps = set_data.reps,
            weight=set_data.weight
        )
        workout_sets.append(new_set)

    db.add_all(workout_sets)
    db.commit()

    return new_workout


## getting the users workout

@router.get("/",response_model=List[schemas.Workout])
def get_workouts(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    workouts = db.query(models.Workout).filter(models.Workout.user_id == current_user.id).all()
    return workouts
