from fastapi import FastAPI,Depends,Response,status,HTTPException
from . import models,schemas
from .database import engine,get_db,SessionLocal
from typing import List,Optional
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager


models.Base.metadata.create_all(bind=engine)



# function to reduce remaining days
def reduce_remaining_days(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    for user in users:
        if user.remaining_days > 0:
            user.remaining_days -= 1
    db.commit()

# ## background job to run daily
# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(func=reduce_remaining_days,trigger="interval",days=1)
#     scheduler.start()

## wrapper task to get the db session for the reduce_remaining_days function
def reduce_remaining_days_task(db: Session = Depends(get_db)):
    # db = SessionLocal()
    try:
        reduce_remaining_days(db=db)
    except Exception as e:
        print(f"Error reducing remaining days: {e}")
        

# # start the scheduler when the application starts
# @app.on_event("startup")
# async def on_startup():
#     start_scheduler()

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

@app.get("/")
def read_root():
    return {"message":"Welcome to our Gym Api."}



@app.get("/plans",response_model=List[schemas.PlanBase])
def get_gym_plans(db: Session = Depends(get_db)):

    results = db.query(models.GymPlans).all()
    # response = [
    #     {"Plans": plans} for plans in results
    # ]
    # return response
    return results

@app.post('/register',response_model=schemas.UserOut)
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
    

    new_user = models.User(
        email=user.email,
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


@app.get('/users/{id}',response_model= schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    
    return user




