"""Definition of a SQLAlchemy table-backed object mapping entity for workouts."""

import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean

from backend.models.weather import Weather

from ..database import Base

from sqlalchemy.orm import  Mapped, mapped_column

class WeatherEntity(Base):
    """SQLAlchemy entity representing the weather. This entity represents the aggregate data of weather for one day for a given city. All units are Imperial."""

    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Just city for ease, but could be changed to a specific location
    city: Mapped[str] = mapped_column(String, nullable=False)

    date: Mapped[str] = mapped_column(String, nullable=False)

    # Average feels like temp for the day
    feels_like: Mapped[float] = mapped_column(Float, nullable=False)

    # Average humidity for the day
    humidity: Mapped[float] = mapped_column(Float, nullable=False)

    # Minimum temperature for the day
    temp_min: Mapped[float] = mapped_column(Float, nullable=False)

    # Maximum temperature for the day
    temp_max: Mapped[float] = mapped_column(Float, nullable=False)

    # Average temperature for the day
    temp_avg: Mapped[float] = mapped_column(Float, nullable=False)

    # Average wind speed for the day
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)

    # Most common weather condition for the day
    weather_main: Mapped[str] = mapped_column(String, nullable=False)

    # Most common weather description for the day
    weather_description: Mapped[str] = mapped_column(String, nullable=False)

    # Boolean to determine if the weather is the current weather or a forecast
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def to_model(self) -> Weather:
        """
        Converts a Weather Entity object into a Weather Pydantic Model object

        Returns:
            Weather: A Weather Pydantic Model object
        """

        return Weather(
            id=self.id,
            city=self.city,
            date=self.date,
            feels_like=self.feels_like,
            humidity=self.humidity,
            temp_min=self.temp_min,
            temp_max=self.temp_max,
            temp_avg=self.temp_avg,
            wind_speed=self.wind_speed,
            weather_main=self.weather_main,
            weather_description=self.weather_description,
            is_current=self.is_current
        )
    
    @classmethod
    def from_model(cls, weather: Weather) -> "WeatherEntity":
        """
        Class method that converts a Weather Pydantic Model object into a Weather Entity object

        Params:
            weather: A Weather Pydantic Model object

        Returns:
            WeatherEntity: Entity created from model
        """

        return cls(
            id=weather.id,
            city=weather.city,
            date=weather.date,
            feels_like=weather.feels_like,
            humidity=weather.humidity,
            temp_min=weather.temp_min,
            temp_max=weather.temp_max,
            temp_avg=weather.temp_avg,
            wind_speed=weather.wind_speed,
            weather_main=weather.weather_main,
            weather_description=weather.weather_description,
            is_current=weather.is_current
        )