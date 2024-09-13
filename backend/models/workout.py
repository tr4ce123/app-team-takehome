import datetime
from pydantic import BaseModel
from pytz import timezone
tz = timezone("EST")

class Workout(BaseModel):
    """
    Pydantic model to represent one workout.

    This model is based on the WorkoutEntity model, which defines the shape of the 
    'Workout' database table in the PostgreSQL database.
    """

    id: int | None = None
    name: str
    distance: float
    duration: int
    date: str | None = datetime.datetime.now(tz).strftime("%Y-%m-%d")
    