# Running Workout Tracker REST API

## Instructions / Usage
### Environment setup
1) Clone the repository into your favorite IDE.
2) Creating a python virtual environment is recommended to prevent conflicts with you global environment's interpreter. You can do this by running `python3 -m venv <yourenvname>` in your root directory or preferably, use VSCode and follow these steps: https://code.visualstudio.com/docs/python/environments.
3) If in the root directory of the repo, run `python3 -m pip install -r backend/requirements.txt` in your terminal to install the required packages.
4) SQLite is also required and can be installed on MacOS via homebrew `brew install sqlite`. Installing via brew is recommended because of ease and homebrew is very easy to install itself.
5) To start the backend server, run `uvicorn backend.main:app --reload` in the root directory and navigate to http://127.0.0.1:8000/docs to interact with the API in a browser. I have set up the FastAPI docs in an organized and intuitive way so feel free to use this link rather than running Postman or something equivalent. Postman does work if that is your preference and you can use the same URL to serve it: http://127.0.0.1:8000 or just localhost port 8000. Parameters can be passed through the URL through Postman and the FastAPI docs will have a form that act as the URL params.
7) Once the server is up, a file called `sql_app.db` will be created and you can simply delete the file if you want to restart the database. A new one will be created when the server is started up.
8) Now you can play around with the API to test out its functionality. I'll have documentation below that gives explanations for the api endpoints and their services as well as a high level explanation.
