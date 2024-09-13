# Running Workout Tracker REST API
This is a RESTful API designed to track running workouts. The API allows users to record, update, and retrieve workout data, including various filters for aggregating and analyzing workouts. It also integrates third-party weather data and the OpenAI API to enhance the workout experience with additional insights like outfit suggestions based on weather conditions.


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

## Features

### Core Features

- **Create Workout**: Add new workout records with details like name, location, distance, duration, and date.
- **Retrieve Workouts**: Fetch individual or multiple workouts, with filtering options for retrieving recent workouts, such as weekly data.
- **Update Workout**: Modify existing workout records.
- **Delete Workout**: Remove workouts by their ID.
- **Aggregate Data**: Retrieve total and average workout data points such as distance and duration for the past week.
- **Personal Bests**: Track personal bests for distance and duration per mile.
- **Weather Integration**: Fetch and store current and five-day weather forecasts for workout locations.
- **Outfit Suggestions**: Get outfit recommendations for workouts based on weather conditions using the OpenAI API.
- **Improvement Advice**: Receive advice on improving workout performance based on weekly averages.

### Bonus Features

- **Image Handling**: Potential to include image uploads (e.g., route snapshots or post-run selfies).
- **Simple Web Frontend**: Future enhancements may include a web interface to interact with the API.

## Technologies Used

- **FastAPI**: Framework for building the RESTful API.
- **SQLAlchemy**: ORM for interacting with a SQLite database.
- **SQLite**: Database for storing workouts and weather data.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **OpenWeather API**: For fetching weather data related to workouts.
- **OpenAI API**: To provide personalized workout advice and outfit suggestions based on weather conditions.

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

- `GET /workouts/`: Retrieve all workouts.
- `GET /workouts/{workout_id}`: Retrieve a workout by its ID.
- `GET /workouts/weekly/workouts`: Retrieve workouts from the last 7 days.
- `GET /workouts/weekly/{data_point}/sum`: Get the sum of a specified data point (distance or duration) from the last 7 days.
- `GET /workouts/weekly/{data_point}/average`: Get the average of a specified data point (distance or duration) from the last 7 days.
- `GET /workouts/personal-bests/distance`: Get the personal best distance.
- `GET /workouts/personal-bests/duration`: Get the personal best duration per mile.
- `GET /workouts/advice/weather/outfit/{city}`: Get outfit suggestions based on the weather in the specified city.
- `GET /workouts/advice/improvement/`: Get advice on how to improve workouts based on weekly averages.
- `POST /workouts/`: Create a new workout record.
- `PUT /workouts/{workout_id}`: Update an existing workout.
- `DELETE /workouts/{workout_id}`: Delete a workout by its ID.

### Weather Endpoints

- `GET /weather/{city}/forecast`: Retrieve a five-day weather forecast for a specified city.
- `GET /weather/{city}/current`: Retrieve the current weather for a specified city.
- `POST /weather/{city}/forecast`: Create a new five-day weather forecast for a specified city.

## Project Design and Considerations

- **API Design**: Emphasized clarity and consistency in endpoint naming and data handling. Each endpoint is intuitively structured to make API calls straightforward and predictable.
- **Data Validation**: Used Pydantic models to ensure data integrity and validation, reducing the chance of invalid data entries.
- **Error Handling**: Implemented robust error handling to provide meaningful feedback for failed operations, like invalid data points or missing records.
- **Performance**: Optimized database queries and utilized relationships in SQLAlchemy to efficiently handle data retrieval.
- **Extensibility**: The architecture allows for easy addition of new features, such as more aggregated data points or further integration with third-party APIs.

## Presentation

- A brief presentation and a demo video demonstrating the API endpoints and their usage have been created. This covers the API design choices, challenges faced, and the overall thought process in developing the application.
