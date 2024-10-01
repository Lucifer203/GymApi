from sqlalchemy import Integer,Column,String,Boolean,ForeignKey,DOUBLE_PRECISION
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base

class GymPlans(Base):
    __tablename__ = "Plans"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    monthly_price = Column(Integer,nullable=False)
    quarterly_price = Column(Integer,nullable=False)
    yearly_price = Column(Integer,nullable=False)
    discount_available = Column(Boolean,nullable=False,server_default=text('FALSE'))

    users = relationship("User",back_populates="plan")



class User(Base):
    __tablename__ = "Users"

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    name = Column(String,nullable=False)
    age = Column(Integer,nullable=False)
    height = Column(DOUBLE_PRECISION,nullable=False)
    weight = Column(DOUBLE_PRECISION,nullable=False)
    # plan_title = Column(String,nullable=False)
    enrolled_plan_id = Column(Integer,ForeignKey("Plans.id"),nullable=False)
    remaining_days = Column(Integer,nullable=False,server_default=text('0'))
    joined_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


    plan = relationship("GymPlans",back_populates="users")
    plan_type = Column(String,nullable=False)


