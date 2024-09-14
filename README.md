# Running Workout Tracker REST API
This is a RESTful API designed to track running workouts. The API allows users to record, update, and retrieve workout data, including various filters for aggregating and analyzing workouts. It also integrates third-party weather data and the OpenAI API to enhance the workout experience with additional insights like outfit suggestions based on weather conditions.

# Table of Contents

- [Running Workout Tracker REST API](#running-workout-tracker-rest-api)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Design and Considerations](#project-design-and-considerations)
- [Presentation](#presentation)
- [Instructions / Usage](#instructions--usage)
  - [Environment Setup Mac](#environment-setup-mac)
  - [Environment Setup Windows](#environment-setup-windows)
- [Data Model](#data-model)
  - [Workout Model](#workout-model)
  - [Weather Model](#weather-model)
- [API Endpoints](#api-endpoints)
  - [Workouts Endpoints](#workouts-endpoints)
  - [Weather Endpoints](#weather-endpoints)
- [Service Methods](#service-methods)
  - [WeatherService Methods](#weatherservice-methods)
  - [WorkoutService Methods](#workoutservice-methods)
  - [OpenAIService Methods](#openaiservice-methods)

# Big Picture

## Features

- **Create Workout**: Add new workout records with details like name, location, distance, duration, and date.
- **Retrieve Workouts**: Fetch individual or multiple workouts, with filtering options for retrieving recent workouts, such as weekly data.
- **Update Workout**: Modify existing workout records.
- **Delete Workout**: Remove workouts by their ID.
- **Aggregate Data**: Retrieve total and average workout data points such as distance and duration for the past week.
- **Personal Bests**: Track personal bests for distance and duration per mile.
- **Weather Integration**: Fetch and store current and five-day weather forecasts for workout locations.
- **Outfit Suggestions**: Get outfit recommendations for workouts based on weather conditions using the OpenAI API.
- **Improvement Advice**: Receive advice on improving workout performance based on weekly averages.

## Technologies Used

- **FastAPI**: Framework for building the RESTful API.
- **SQLAlchemy**: ORM for interacting with a SQLite database.
- **SQLite**: Database for storing workouts and weather data.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **OpenWeather API**: For fetching weather data related to workouts.
- **OpenAI API**: To provide personalized workout advice and outfit suggestions based on weather conditions.

### Why use this stack?

#### FastAPI
- Familiar with Python and wanted a Python-based backend.
- Popularity and automatic API documentation with interactive `/docs` page.
- Great for new developers to explore and test endpoints easily.
- Strong validation, typing, and good performance, all contained within Python.

#### SQLite, SQLAlchemy, Pydantic
- **SQLite:**
  - Chose it for its relational database structure—easy to create relationships, like one-to-many between Weather and Workout entities.
  - Perfect for quick, small-scale projects; easy local development and testing.
  - Would consider PostgreSQL for larger scale, but SQLite fits this project well.
- **SQLAlchemy:**
  - Allows interaction with Python objects instead of raw SQL—better readability and fewer errors.
  - Integrates smoothly with Pydantic models for cleaner API responses.
  - Adds an extra layer of protection with safer queries compared to raw SQL.
- **Pydantic:**
  - Ensures data validation and integrity with Python type annotations.
  - Seamlessly integrates with FastAPI to validate incoming data and define response models.

#### OpenWeather API
- Wanted a weather API for relevant data to enhance user experience.
- Easy-to-use, well-documented endpoints; straightforward JSON data over SDK.
- Focused on fields relevant to the frontend: max/min/average temps, conditions, etc.
- Adds value by providing more context than just workout tracking; useful and informative data for the user.

#### OpenAI API
- Familiar with the OpenAI Python SDK; integrates a powerful, widely-used API.
- The GPT-4o model makes generating tailored user recommendations easy.
- Wanted flexible, accurate suggestions for workouts and outfits based on weather without hardcoding responses.
- Enhances user experience with personalized, context-aware feedback using simple prompts.

## Project Design and Considerations
Throughout my API endpoints, routes, and service methods, I try to be as verbose as possible in as few words as possible. Throughout my code you'll see some decently long method names and api routes which is done intentionally because readability is so important. The way I try to program, ESPECIALLY while on a team, is to leave the person reading the code as minimally confused as possible. Readable code makes everyone's lives easier and all it takes it a few extra words and a docstring.

### API Endpoint Structure
`/workouts/{workout_id}`
`/workouts/weekly/{data_point}/sum`
`/workouts/advice/improvement/{workout_id}`
`/workouts/personal-bests/distance`

When I was naming the url routes to my endpoints, I organized them by functionality and meaning. If you want weekly data, add `/weekly`, if you want advice add `/advice`, etc. When an endpoint is related to a data model, I prepend it with the name of the model i.e. `/workouts`. This way it is painfully obvious what the endpoint is referencing along with the several categorizations of functionality you can see above and below in my routes. 

## Presentation

- A brief presentation and a demo video demonstrating the API endpoints and their usage have been created. This covers the API design choices, challenges faced, and the overall thought process in developing the application.

## Instructions / Usage
### Environment setup Mac
1) Clone the repository into your favorite IDE.
2) Creating a python virtual environment is recommended to prevent conflicts with you global environment's interpreter. You can do this by running `python3 -m venv <yourenvname>` in your root directory or preferably, use VSCode and follow these steps: https://code.visualstudio.com/docs/python/environments. Make sure you activate the venv by running `source venv/bin/activate`.
3) If in the root directory of the repo, run `python3 -m pip install -r backend/requirements.txt` in your terminal to install the required packages.
4) To start the backend server, run `uvicorn backend.main:app --reload` in the root directory and navigate to http://127.0.0.1:8000/docs to interact with the API in a browser (note: I ran into issues on my windows desktop using 127.0.0.1:8000 and instead you should just use localhost:8000 if you run into CORS issues). I have set up the FastAPI docs in an organized and intuitive way so feel free to use this link rather than running Postman or something equivalent. Postman does work if that is your preference and you can use the same URL to serve it: http://127.0.0.1:8000 or just localhost port 8000. Parameters can be passed through the URL through Postman and the FastAPI docs will have a form that act as the URL params.
5) Once the server is up, a file called `sql_app.db` will be created and you can simply delete the file if you want to restart the database. A new one will be created when the server is started up.
6) Now you can play around with the API to test out its functionality. I'll have documentation below that gives explanations for the api endpoints and their services as well as a high level explanation.

### Environment setup Windows
1) Clone the repository into your favorite IDE.
2) Creating a python virtual environment is recommended to prevent conflicts with you global environment's interpreter. You can do this by running `py -m venv <yourenvname>` in your root directory or preferably, use VSCode and follow these steps: https://code.visualstudio.com/docs/python/environments. Make sure you activate the venv by cding into your venv file `cd <yourenvname>` and then run `.\Scripts\activate`. If you're running into trouble and you get an error saying you can't run scripts because they're disabled use this and make sure to run PowerShell as administrator: https://stackoverflow.com/questions/4037939/powershell-says-execution-of-scripts-is-disabled-on-this-system.
3) Before running the install for requirements, remove uvloop from the requirements.txt file because Windows does not support it and it will still work without it. If in the root directory of the repo, run `py -m pip install -r backend/requirements.txt` in your terminal to install the required packages.
4) To start the backend server, run `uvicorn backend.main:app --reload` in the root directory and navigate to http://127.0.0.1:8000/docs to interact with the API in a browser (note: I ran into issues on my windows desktop using 127.0.0.1:8000 and instead you should just use localhost:8000 if you run into CORS issues). I have set up the FastAPI docs in an organized and intuitive way so feel free to use this link rather than running Postman or something equivalent. Postman does work if that is your preference and you can use the same URL to serve it: http://127.0.0.1:8000 or just localhost port 8000. Parameters can be passed through the URL through Postman and the FastAPI docs will have a form that act as the URL params.
5) Once the server is up, a file called `sql_app.db` will be created and you can simply delete the file if you want to restart the database. A new one will be created when the server is started up. Installation of SQLite is not required.
6) Now you can play around with the API to test out its functionality. I'll have documentation below that gives explanations for the api endpoints and their services as well as a high level explanation.


## Data Model

### Workout Model

- **ID**: Unique identifier for each workout.
- **Name**: Name or description of the workout.
- **City**: Location where the workout took place.
- **Distance**: Distance covered during the workout (miles).
- **Duration**: Duration of the workout (minutes).
- **Date**: Date and time of the workout.
- **Weather ID**: Optional foreign key linking to the related weather data.

### Weather Model

- **ID**: Unique identifier for each weather record.
- **City**: City associated with the weather data.
- **Date**: Date and time of the weather data.
- **Feels Like**: Average "feels like" temperature for the day.
- **Humidity**: Average humidity percentage for the day.
- **Temperature Min/Max/Avg**: Minimum, maximum, and average temperatures for the day.
- **Wind Speed**: Average wind speed.
- **Weather Main**: Main weather condition (e.g., Clear, Rain).
- **Weather Description**: Detailed weather description (e.g., light rain).
- **Is Current**: Boolean indicating if the weather data is the current weather or a forecast.

## API Endpoints

### Workouts Endpoints
| Method | Endpoint                                  | Description                                                                                 | Required Parameters                     | Expected Response                   |
|--------|-------------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------|-------------------------------------|
| GET    | `/workouts/`                              | Retrieves all workouts.                                                                     | None                                    | `list[Workout]`                     |
| GET    | `/workouts/{workout_id}`                  | Retrieves a specific workout by its ID.                                                     | `workout_id: int`                       | `Workout`                           |
| GET    | `/workouts/weekly/workouts`               | Retrieves all workouts logged in the last 7 days.                                           | None                                    | `list[Workout]`                     |
| GET    | `/workouts/weekly/{data_point}/sum`       | Retrieves the sum of a specific workout data point from the last 7 days.                    | `data_point: str`                       | `float`                             |
| GET    | `/workouts/weekly/{data_point}/average`   | Retrieves the average of a specific workout data point from the last 7 days.                | `data_point: str`                       | `float`                             |
| GET    | `/workouts/personal-bests/distance`       | Retrieves the personal best distance.                                                       | None                                    | `str`                               |
| GET    | `/workouts/personal-bests/duration`       | Retrieves the personal best duration.                                                       | None                                    | `str`                               |
| GET    | `/workouts/advice/weather/outfit/{city}`  | Provides workout outfit advice based on the current weather in a specified city.            | `city: str`                             | `str`                               |
| GET    | `/workouts/advice/improvement/`           | Provides general advice on improving workouts based on weekly averages.                     | None                                    | `str`                               |
| GET    | `/workouts/advice/improvement/{workout_id}` | Provides advice on improving a specific workout based on its data.                         | `workout_id: int`                       | `str`                               |
| POST   | `/workouts/`                              | Creates a new workout entry, optionally with weather data for the workout date.             | `workout: Workout`                      | `Workout`                           |
| PUT    | `/workouts/{workout_id}`                  | Updates an existing workout.                                                               | `workout_id: int`, `workout: Workout`   | `Workout`                           |
| DELETE | `/workouts/{workout_id}`                  | Deletes a specific workout by its ID.                                                      | `workout_id: int`                       | None                                |



### Weather Endpoints

| Method | Endpoint                    | Description                                                                                           | Required Parameters  | Expected Response                |
|--------|-----------------------------|-------------------------------------------------------------------------------------------------------|----------------------|-----------------------------------|
| GET    | `/weather/{city}/forecast`  | Gets the 5-day weather forecast for a specified city. Each day includes data for every three hours.   | `city: str`          | `list[Weather]`                  |
| GET    | `/weather/{city}/current`   | Gets the current weather for a specified city.                                                        | `city: str`          | `Weather`                        |
| GET    | `/weather/{weather_id}/`    | Gets weather data by its ID from the database.                                                        | `weather_id: int`    | `Weather`                        |
| POST   | `/weather/{city}/forecast`  | Creates and stores a new 5-day weather forecast for a specified city.                                 | `city: str`          | `list[Weather]`                  |
| POST   | `/weather/{city}/current`   | Creates and stores the current weather for a specified city.                                          | `city: str`          | `Weather`                        |
| DELETE | `/weather/{weather_id}/`    | Deletes the weather data by its ID from the database.                                                 | `weather_id: int`    | `None`                           |


## Service Methods
### WeatherService Methods
| Method                                | Description                                                                                          | Required Parameters                  | Expected Response             |
|---------------------------------------|------------------------------------------------------------------------------------------------------|--------------------------------------|-------------------------------|
| `fetch_five_day_forecast_from_api`    | Retrieves the 5-day weather forecast for a city using OpenWeather API.                               | `city: str`                          | `dict`                        |
| `fetch_current_weather_from_api`      | Retrieves the current weather data for a city using OpenWeather API.                                 | `city: str`                          | `dict`                        |
| `store_five_day_weather_forecast`     | Stores the 5-day weather forecast for a city in the database.                                        | `city: str`                          | `list[Weather]`               |
| `store_current_weather`               | Stores the current weather data for a city in the database.                                          | `city: str`                          | `Weather`                     |
| `get_weather_by_id`                   | Retrieves weather data by its ID from the database.                                                  | `weather_id: int`                    | `Weather`                     |
| `get_five_day_forecast`               | Retrieves the 5-day weather forecast for a city from the database, fetching from API if not present. | `city: str`                          | `list[Weather]`               |
| `get_weather_by_date_and_location`    | Retrieves weather data for a specific date and city.                                                 | `city: str`, `date: str`             | `Weather`                     |
| `get_current_weather_by_location`     | Retrieves the current weather data for a city, fetching from API if not present.                     | `city: str`                          | `Weather`                     |
| `delete_weather`                      | Deletes weather data by its ID from the database.                                                    | `weather_id: int`                    | `None`                        |

### WorkoutService Methods
| Method                                | Description                                                                                          | Required Parameters                   | Expected Response             |
|---------------------------------------|------------------------------------------------------------------------------------------------------|---------------------------------------|-------------------------------|
| `all`                                 | Retrieves all workouts from the database.                                                            | None                                  | `list[Workout]`               |
| `get_workout_by_id`                   | Retrieves a workout by its ID.                                                                       | `workout_id: int`                     | `Workout`                     |
| `get_weekly_workouts`                 | Retrieves all workouts from the past 7 days.                                                         | None                                  | `list[Workout]`               |
| `get_total_weekly_aggreate_workout_data` | Retrieves the sum of a specified workout data point from the last 7 days.                         | `data_point: str`                     | `float`                       |
| `get_average_weekly_aggreate_workout_data` | Retrieves the average of a specified workout data point from the last 7 days.                    | `data_point: str`                     | `float`                       |
| `get_personal_best_distance`          | Retrieves the personal best distance.                                                                | None                                  | `str`                         |
| `get_personal_best_duration_per_mile` | Retrieves the personal best duration per mile.                                                       | None                                  | `str`                         |
| `create_workout`                      | Creates a new workout and optionally links it with weather data.                                     | `workout: Workout`, `weather: Weather` | `Workout`                     |
| `update_workout`                      | Updates an existing workout.                                                                         | `workout: Workout`                    | `Workout`                     |
| `delete_workout`                      | Deletes a workout by its ID.                                                                         | `workout_id: int`                     | `None`                        |

### OpenAIService Methods
| Method                                | Description                                                                                          | Required Parameters                   | Expected Response             |
|---------------------------------------|------------------------------------------------------------------------------------------------------|---------------------------------------|-------------------------------|
| `generate_workout_outfit`             | Generates a workout outfit suggestion based on the weather using the OpenAI API.                     | `weather: Weather`                    | `str`                         |
| `generate_all_workout_improvement_advice` | Generates advice for improving workout performance based on average distance and duration.         | `avg_distance: float`, `avg_duration: float` | `str`                     |
| `generate_workout_improvement_advice` | Generates advice for improving a specific workout based on its distance and duration.                | `workout: Workout`                    | `str`                         |


