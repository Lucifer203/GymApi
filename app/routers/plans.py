from fastapi import FastAPI,Depends,Response,status,HTTPException,APIRouter
from typing import List
from .. import schemas,database,models
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/plans",response_model=List[schemas.PlanBase])
def get_gym_plans(db: Session = Depends(database.get_db)):

    results = db.query(models.GymPlans).all()
    # response = [
    #     {"Plans": plans} for plans in results
    # ]
    # return response
    return results

