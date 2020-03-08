import uvicorn
from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import users, projects

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router,
                   prefix='/users',
                   tags=['users'])
app.include_router(projects.router,
                   prefix='/projects',
                   tags=['projects'],
                   responses={404: {'description': 'Not found'}})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
