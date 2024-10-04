from fastapi import FastAPI,Depends,Response,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import models,schemas
from .database import engine,get_db,SessionLocal
from typing import List,Optional
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from .routers import users,auth,workouts,plans

models.Base.metadata.create_all(bind=engine)



# function to reduce remaining days
def reduce_remaining_days(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    for user in users:
        if user.remaining_days > 0:
            user.remaining_days -= 1
    db.commit()



## wrapper task to get the db session for the reduce_remaining_days function
def reduce_remaining_days_task(db: Session = Depends(get_db)):
    # db = SessionLocal()
    try:
        reduce_remaining_days(db=db)
    except Exception as e:
        print(f"Error reducing remaining days: {e}")
        


@asynccontextmanager
async def lifespan(app:FastAPI):
    scheduler = BackgroundScheduler()

    scheduler.start()
    print("Scheduler Started")

    @scheduler.scheduled_job(trigger="interval",days = 1)

    def scheduled_job():
        db = SessionLocal()
        try:
            reduce_remaining_days_task(db)
        finally:
            db.close()
    yield

    scheduler.shutdown()
    print("Scheduler shut down.")



app = FastAPI(lifespan=lifespan)

app.include_router(plans.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(workouts.router)

@app.get("/")
def read_root():
    return {"message":"Welcome to our Gym Api."}








