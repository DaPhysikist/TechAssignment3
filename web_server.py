from multiprocessing import Process
import os
import time
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import requests
import mysql.connector as mysql
from dotenv import load_dotenv

load_dotenv()

# Read Database connection variables
db_host = "localhost"
db_user = "root"
db_pass = os.environ['MYSQL_ROOT_PASSWORD']
db_name = "TechAssignment3"

light_value = 0
temp = 0
humidity = 0

def collect_data():
  """
  Every several seconds, make requests to the Raspberry Pi API to collect sensor data and store it in the SQL database, then make a request to Raspberry Pi API to display the most recent weather data on the LCD.
  """
  global light_value, temp, humidity
  light_url = "raspberrypi.local:1234/light_level"
  temp_url = "raspberrypi.local:1234/temp"
  humidity_url = "raspberrypi.local:1234/humidity"
  while True:
    light_data = requests.get(light_url).json()
    light_value = light_data["light_value"]
    temp_data = requests.get(temp_url).json()
    temp = temp_data["temp"]
    humidity_data = requests.get(humidity_url).json()
    humidity = humidity_data["humidity"]

# Configuration
app = FastAPI()
# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")




if __name__ == "__main__":
  p = Process(target=collect_data)
  p.start()
  uvicorn.run("app:app", host="0.0.0.0", port=4321, reload=True)

