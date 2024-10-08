from fastapi import FastAPI
from .database import engine, Base
from .api import workout, weather

app = FastAPI(
    title="Running Workouts API: App Team Takehome",
    description="API for Running Workouts",
    version="0.1",
    openapi_tags=[
        workout.openapi_tags,
        weather.openapi_tags
    ]
)

Base.metadata.create_all(bind=engine)

app.include_router(workout.api)
app.include_router(weather.api)