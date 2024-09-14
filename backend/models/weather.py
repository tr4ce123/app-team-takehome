
from pydantic import BaseModel

class Weather(BaseModel):
    """
    Pydantic model to represent one weather object.

    This model is based on the WeatherEntity model, which defines the shape of the 
    'Weather' database table in the SQLite database.

    All units are Imperial.
    """

    id: int | None = None
    city: str
    date: str
    feels_like: float
    humidity: float
    temp_min: float
    temp_max: float
    temp_avg: float
    wind_speed: float
    weather_main: str
    weather_description: str
    is_current: bool
