from datetime import datetime, timedelta
from pytz import timezone

from dotenv import load_dotenv

from sqlalchemy import JSON, select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from backend.entities.weather import WeatherEntity
from backend.models.weather import Weather
from backend.models.workout import Workout
from backend.entities.workout import WorkoutEntity
from ..database import db_session

import requests, os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

tz = timezone("EST")

class OpenAIService:
    """
    Stores the business logic for interacting with the OpenAI API.
    """

    def __init__(self, session: Session = Depends(db_session)) -> dict:
        self._session = session

    
    def generate_workout_outfit(self, weather: Weather) -> str:
        """
        Uses the OpenAI API to generate an outfit suggestion based on the weather

        Params:
            weather: The weather data for the location
        
        Returns:
            str: The outfit suggestion
        """

        
        prompt = f"""
            Generate an outfit suggestion for a workout in {weather.city} 
            with this weather data measured in imperial units: max-temp: {weather.temp_max}, min-temp: {weather.temp_min}, avg-temp: {weather.temp_avg}, weather description: {weather.weather_description}, humidity (percentage): {weather.humidity}, feels-like {weather.feels_like}.
            List out each stat I gave at the end.
            """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages= [
            {
                "role": "system",
                "content": "You are a fitness bot."
            },
            {
                "role": "user",
                "content": prompt
            }
            ],
        )

        generated_text = response.choices[0].message.content
        
        return generated_text
    
    
    def generate_all_workout_improvement_advice(self, avg_distance: float, avg_duration: float) -> str:
        """
        Uses the OpenAI API to generate a recommendation for improving a workout based on the average distance and duration across all workouts.

        Params:
            workout: The workout data
        
        Returns:
            str: The workout advice
        """

        
        prompt = f"Generate advice for how to improve the distance and time of a runner with {avg_distance} miles and {avg_duration} minutes over the course of their workouts for the last 7 days. Include things like speed, endurance, form, and how often they should be running."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages= [
            {
                "role": "system",
                "content": "You are a fitness bot that is giving advice to a user for a running workout application."
            },
            {
                "role": "user",
                "content": prompt
            }
            ],
        )

        generated_text = response.choices[0].message.content
        
        return generated_text
    

    def generate_workout_improvement_advice(self, workout: Workout) -> str:
        """
        Uses the OpenAI API to generate a recommendation for improving a single workout based on the distance and duration.

        Params:
            workout: The workout data
        
        Returns:
            str: The workout advice
        """

        
        prompt = f"Generate advice for how to improve the distance and time of a runner with {workout.distance} miles and {workout.duration} minutes. Include things like speed, endurance, form, and how often they should be running."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages= [
            {
                "role": "system",
                "content": "You are a fitness bot that is giving advice to a user for a running workout application."
            },
            {
                "role": "user",
                "content": prompt
            }
            ],
        )

        generated_text = response.choices[0].message.content
        
        return generated_text