from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from datetime import datetime,date
from typing import List


class PlanBase(BaseModel):
    title: str
    monthly_price: int
    quarterly_price: int
    yearly_price: int
    discount_available: bool = False

    class Config:
        orm_mode = True

class User(BaseModel):
    email: EmailStr
    name: str
    age: int
    height: float
    weight: float
    remaining_days: int = 0

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    age: int
    height: float  # Use float instead of double_precision
    weight: float  # Use float instead of double_precision
    remaining_days: Optional[int] = 0
    plan_title: str  # Plan title provided by the user
    plan_type: str


class UserOut(BaseModel):
    name: str
    email: EmailStr
    enrolled_plan_id: int
    joined_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None 


## workout tracker schemas ###

class WorkoutSetBase(BaseModel):
    set_number: int
    reps: int
    weight: float

class WorkoutSetCreate(WorkoutSetBase):
    pass

class WorkoutSet(WorkoutSetBase):
    id: int

    class Config:
        orm_mode = True

class WorkoutBase(BaseModel):
    exercise_name: str
    workout_date: date = date.today()

class WorkoutCreate(WorkoutBase):
    sets: List[WorkoutSetCreate]

class Workout(WorkoutBase):
    id: int
    sets: List[WorkoutSet]

    class Config:
        orm_mode = True
