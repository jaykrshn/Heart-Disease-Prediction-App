from fastapi import FastAPI
from .models import Base
from .data_base import engine
from .routers import auth, predict, users, admin
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(admin.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)