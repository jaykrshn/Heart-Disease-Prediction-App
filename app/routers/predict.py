from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from starlette import status
from ..models import Predict
from ..data_base import SessionLocal
from .auth import get_current_user
import numpy as np
import pickle
import os

router = APIRouter(
    prefix='/prediction',
    tags=['prediction'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Get the absolute path to the trained model file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINED_MODEL_PATH = os.path.join(BASE_DIR, "trained_model", "reg_model.pkl")
SCALLING_MODEL_PATH = os.path.join(BASE_DIR, "trained_model", "scaling.pkl")

# Load the model and scaler
regmodel = pickle.load(open(TRAINED_MODEL_PATH, 'rb'))
scalar = pickle.load(open(SCALLING_MODEL_PATH, 'rb'))



# class PredictRequest(BaseModel):
#     age: float
#     cigsPerDay: float
#     prevalentStroke: float
#     sysBP: float
#     diaBP: float
#     heartRate: float
#     glucose: float


class PredictRequest(BaseModel):
    age: int = Field(..., gt=0, description="Age must be greater than 0")
    cigsPerDay: int = Field(..., ge=0, description="Cigarettes per day must be 0 or greater")
    prevalentStroke: int = Field(..., ge=0, le=1, description="Prevalent stroke must be 0 or 1")
    sysBP: float = Field(..., gt=0, description="Systolic BP must be greater than 0")
    diaBP: float = Field(..., gt=0, description="Diastolic BP must be greater than 0")
    heartRate: float = Field(..., gt=0, description="Heart rate must be greater than 0")
    glucose: float = Field(..., gt=0, description="Glucose level must be greater than 0")

    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "cigsPerDay": 10,
                "prevalentStroke": 0,
                "sysBP": 120.5,
                "diaBP": 80.2,
                "heartRate": 72.5,
                "glucose": 95.3,
            }
        }


@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Predict).filter(Predict.owner_id == user.get('id')).all()

@router.get("/{prediction_id}", status_code=status.HTTP_200_OK)
async def read_prediction(user: user_dependency, db: db_dependency, prediction_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    prediction_model = db.query(Predict).filter(Predict.id == prediction_id).filter(Predict.owner_id == user.get('id')).first()
    if prediction_model is not None:
        return prediction_model
    raise HTTPException(status_code=404, detail='Prediction not found')



@router.post("/", status_code=status.HTTP_201_CREATED)
async def make_prediction(user: user_dependency, db: db_dependency, 
                          predict_request: PredictRequest = Body(
                            ..., 
                            example={
                                "age": 45,
                                "cigsPerDay": 10,
                                "prevalentStroke": 0,
                                "sysBP": 120.5,
                                "diaBP": 80.2,
                                "heartRate": 72.5,
                                "glucose": 95.3,
                            })):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    # Process the input data (scaling and prediction)
    data = predict_request.model_dump()  # Convert Pydantic model to dictionary
    scaled_data = scalar.transform(np.array(list(data.values())).reshape(1, -1))
    output = regmodel.predict(scaled_data)[0]
    
    prediction_model = Predict(
        age=predict_request.age,
        cigsPerDay=predict_request.cigsPerDay,
        prevalentStroke=predict_request.prevalentStroke,
        sysBP=predict_request.sysBP,
        diaBP=predict_request.diaBP,
        heartRate=predict_request.heartRate,
        glucose=predict_request.glucose,
        result=str(output),
        owner_id=user.get('id')
    )
    db.add(prediction_model)
    db.commit()
    return prediction_model

@router.delete("/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prediction(user: user_dependency, db: db_dependency, prediction_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    prediction_model = db.query(Predict).filter(Predict.id == prediction_id).filter(Predict.owner_id == user.get('id')).first()
    if prediction_model is None:
        raise HTTPException(status_code=404, detail='Prediction not found')
    db.query(Predict).filter(Predict.id == prediction_id).filter(Predict.owner_id == user.get('id')).delete()
    db.commit()
