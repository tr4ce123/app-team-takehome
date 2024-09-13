from fastapi import APIRouter, Depends
from sqlalchemy import JSON

from ..services.weather import WeatherService
from ..models.weather import Weather

api = APIRouter(prefix="/weather", tags=["Weather"])
openapi_tags = {
    "name": "Weather",
    "description": "Create, update, delete, and retrieve Weather Data from a third-party API.",
}

@api.get("/forecast/{city}", response_model=list[Weather], tags=["Weather"])
def get_five_day_forecast_by_city(city: str, weather_service: WeatherService = Depends(WeatherService)) -> list[Weather]:
    """
    Gets the forecast from OpenWeather's forecast API endpoint for every three hours of the current day, and the next five days.

    Params:
        weather_service: Service for interacting with weather data
        city: The location to get the forecast for in the form of a string

    Returns:
        Weather: All Weather data in the Weather database table
    """
        
    return weather_service.get_five_day_forecast(city)


@api.get("/current/{city}/", response_model=Weather, tags=["Weather"])
def get_current_weather_by_location(city: str, weather_service: WeatherService = Depends(WeatherService)) -> Weather:
    """
    Gets the current weather for a given location.

    Params:
        weather_service: Service for interacting with weather data
        date: The date to get the forecast for in the form of a string
        city: The location to get the forecast for in the form of a string

    Returns:
        Weather: The weather forecast for the given date and location
    """

    return weather_service.get_current_weather_by_location(city)


@api.post("/forecast/{city}", response_model=list[Weather], tags=["Weather"])
def create_five_day_forecast_by_city(city: str, weather_service: WeatherService = Depends(WeatherService)) -> list[Weather]:
    """
    Creates a new weather forecast for the current day, and the next five days for a given location.

    Params:
        weather_service: Service for interacting with weather data
        city: The location to get the forecast for in the form of a string

    Returns:
        list[Weather]: The newly created weather forecasts
    """

    return weather_service.store_five_day_weather_forecast(city)