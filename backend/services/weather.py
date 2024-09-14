from datetime import datetime, timedelta
from pytz import timezone

from dotenv import load_dotenv

from sqlalchemy import JSON, select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from backend.entities.weather import WeatherEntity
from backend.models.weather import Weather
from ..database import db_session

import requests, os
# Geolocator to get the latitude and longitude of a city
from geopy.geocoders import Nominatim
from geopy.adapters import RequestsAdapter
geolocator = Nominatim(user_agent="app-team-takehome", adapter_factory=RequestsAdapter, ssl_context=None)

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast?"
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather?"

tz = timezone("EST")


class WeatherService:
    """
    Stores the business logic for interacting with weather data and the Open Weather API.
    """

    def __init__(self, session: Session = Depends(db_session)) -> dict:
        self._session = session


    def fetch_five_day_forecast_from_api(self, city: str):
        """
        Uses geolocator to get the latitude and longitude of a city 
        and uses the OpenWeather API to get the weather forecast for every three hours of the next five days.
        
        Params:
            city: The city to get the weather data for
            
        Returns:
            dict: Weather data for the given location
        """

        # Use geolocator to get longitude and latitude from the specified city
        location = geolocator.geocode(city)
        latitude, longitude = location.latitude, location.longitude


        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": api_key,
            "units": "imperial"
        }

        # Make a request to the OpenWeather API and store it
        response = requests.get(FORECAST_URL, params)

        # Simple check to see if the request was successful
        if response is None or response.status_code != 200:
            raise HTTPException(status_code=404, detail="Weather data not found")

        # Ensure the response a dictionary
        data = response.json()

        return data
    
    
    def fetch_current_weather_from_api(self, city: str) -> dict:
        """
        Uses geolocator to get the latitude and longitude of a city 
        and uses the OpenWeather API to get the current weather data.
        
        Params:
            city: The city to get the weather data for
            
        Returns:
            dict: Weather data for the given location
        """

        # Use geolocator to get longitude and latitude from the specified city
        location = geolocator.geocode(city)
        latitude, longitude = location.latitude, location.longitude

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": api_key,
            "units": "imperial"
        }

        # Make a request to the OpenWeather API and store it
        response = requests.get(CURRENT_URL, params)

        # Simple check to see if the request was successful
        if response is None or response.status_code != 200:
            return HTTPException(status_code=404, detail="Weather data not found")

        # Ensure the response a dictionary
        data = response.json()

        return data
    
    
    def store_five_day_weather_forecast(self, city: str) -> list[Weather]:
        """
        Retrieves the weather forecast for the next seven days for a given location and stores it in the database.
        
        Params:
            city: The location to get the forecast for
            
        Returns:
            list[Weather]: List of weather forecasts for the next seven days
        """

        data = self.fetch_five_day_forecast_from_api(city)
        daily_data = {}

        # Iterate through the dict and aggregate the data from every three hours of a given day
        for entry in data['list']:
            # Split the string such that we only get the date 'YYYY-MM-DD'
            date_str = entry['dt_txt'].split(" ")[0]

            # If the date is not in the dictionary, add it with empty lists for each data point
            if date_str not in daily_data:
                daily_data[date_str] = {
                    "feels_like": [],
                    "humidity": [],
                    "temp_min": [],
                    "temp_max": [],
                    "temp_avg": [],
                    "wind_speed": [],
                    "weather_main": [],
                    "weather_description": []
                }

            # Append the data to the respective lists
            daily_data[date_str]['feels_like'].append(entry['main']['feels_like'])
            daily_data[date_str]['humidity'].append(entry['main']['humidity'])
            daily_data[date_str]['temp_min'].append(entry['main']['temp_min'])
            daily_data[date_str]['temp_max'].append(entry['main']['temp_max'])
            daily_data[date_str]['temp_avg'].append(entry['main']['temp'])
            daily_data[date_str]['wind_speed'].append(entry['wind']['speed'])
            daily_data[date_str]['weather_main'].append(entry['weather'][0]['main'])
            daily_data[date_str]['weather_description'].append(entry['weather'][0]['description'])

        new_entities = []

        # Iterate through the dictionary and store the data in the database
        for date_str, values in daily_data.items():
            entity = WeatherEntity(
                city=city.lower(),
                date=date_str,
                feels_like=round(sum(values['feels_like']) / len(values['feels_like']), 0),
                humidity=round(sum(values['humidity']) / len(values['humidity']), 0),
                temp_min=round(sum(values['temp_min']) / len(values['temp_min']), 0),
                temp_max=round(sum(values['temp_max']) / len(values['temp_max']), 0),
                temp_avg=round(sum(values['temp_avg']) / len(values['temp_avg']), 0),
                wind_speed=round(sum(values['wind_speed']) / len(values['wind_speed']), 0),
                weather_main=max(set(values['weather_main']), key=values['weather_main'].count),
                weather_description=max(set(values['weather_description']), key=values['weather_description'].count),
                is_current=False
            )

            self._session.add(entity)
            self._session.commit()

            new_entities.append(entity)
        

        return new_entities    
    
    
    def store_current_weather(self, city: str) -> Weather:
        """
        Retrieves the current weather data for a given location and stores it in the database.
        
        Params:
            city: The location to get the forecast for
            
        Returns:
            Weather: The current weather data for the given location
        """

        data = self.fetch_current_weather_from_api(city)

        if data is None:
            return HTTPException(status_code=404, detail="Weather data not found")

        entity = WeatherEntity(
            city=city.lower(),
            date=datetime.now(tz).date().strftime('%Y-%m-%d') + " " + datetime.now(tz).strftime('%I:%M %p'),
            feels_like=round(data['main']['feels_like'], 0),
            humidity=round(data['main']['humidity'], 0),
            temp_min=round(data['main']['temp_min'], 0),
            temp_max=round(data['main']['temp_max'], 0),
            temp_avg=round(data['main']['temp'], 0),
            wind_speed=round(data['wind']['speed'], 0),
            weather_main=data['weather'][0]['main'],
            weather_description=data['weather'][0]['description'],
            is_current=True
        )

        self._session.add(entity)
        self._session.commit()

        return entity.to_model()
    

    def get_weather_by_id(self, weather_id: int) -> Weather:
        """
        Retrieves a weather entity by its ID.
        Raises an error if no weather with the given ID is found.
        
        Params:
            weather_id: The ID of the weather entity to retrieve
            
        Returns:
            Weather: The weather entity with the specified ID
        """

        entity = self._session.query(WeatherEntity).filter(WeatherEntity.id == weather_id).one_or_none()

        if entity is None:
            raise HTTPException(status_code=404, detail=f"Weather with ID: { weather_id } does not exist")
        
        return entity.to_model()
    

    def get_five_day_forecast(self, city: str) -> list[Weather]:
        """
        Retrieves the weather forecast for the current day and next five days for a given location.
        
        Params:
            city: The location to get the forecast for
            
        Returns:
            dict: Weather data for the given location
        """

        start_date = datetime.now(tz).date()
        end_date = start_date + timedelta(days=5)

        # Search for existing data in the database by city, date, and is_current
        query = select(WeatherEntity).filter(WeatherEntity.city == city.lower(), WeatherEntity.date >= start_date, WeatherEntity.date <= end_date, WeatherEntity.is_current == False)

        # To prevent duplicates, return the existing data if it exists
        existing_entities = self._session.scalars(query).all()
        if existing_entities:
            return [entity.to_model() for entity in existing_entities]
        
        # If the data does not exist in the database, fetch it from the API
        self.store_five_day_weather_forecast(city)

        # Grab the newly stored data from the database and return it
        stored_entities = self._session.scalars(query).all()
        return [entity.to_model() for entity in stored_entities]
    

    def get_weather_by_date_and_location(self, city: str, date: str) -> Weather:
        """
        Retrieves the weather forecast for a given date. Raises an error if no weather data for the given date is found.
        
        Params:
            date: The date to get the forecast for
            
        Returns:
            Weather: The weather forecast for the given date
        """

        query = select(WeatherEntity).filter(WeatherEntity.date == date, WeatherEntity.city == city.lower(), WeatherEntity.is_current == False)

        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            return self.store_weather_by_date(city, date)

        return entity.to_model()
    
    
    def get_current_weather_by_location(self, city: str) -> Weather:
        """
        Retrieves the weather forecast for a given date. Raises an error if no weather data for the given date is found.
        
        Params:
            date: The date to get the forecast for
            
        Returns:
            Weather: The weather forecast for the given date
        """

        query = select(WeatherEntity).filter(WeatherEntity.date == datetime.now(tz), WeatherEntity.city == city.lower(), WeatherEntity.is_current == True)

        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            return self.store_current_weather(city)

        return entity.to_model()


    def delete_weather(self, weather_id) -> None:
        """
        Deletes the weather entity by its ID
        
        Params:
            weather_id: The ID of the weather entity to delete
        """

        query = select(WeatherEntity).filter(WeatherEntity.id == weather_id)
        entity = self._session.scalars(query).one_or_none()

        if entity:
            self._session.delete(entity)
            self._session.commit()