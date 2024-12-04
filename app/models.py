from .data_base import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)      
    email = Column(String, unique=True)                     
    username = Column(String, unique=True)                
    first_name = Column(String)                    
    last_name = Column(String)                   
    hashed_password = Column(String)
    is_active = Column(Boolean)
    role = Column(String)
    phone_number = Column(String)


class Predict(Base):
    __tablename__ = 'predict'

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    cigsPerDay = Column(Integer)
    prevalentStroke = Column(Integer)
    sysBP = Column(Float)
    diaBP = Column(Float)
    heartRate = Column(Float)
    glucose = Column(Float)
    result = Column(Integer)
    owner_id = Column(Float, ForeignKey('users.id'))
