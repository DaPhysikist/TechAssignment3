from multiprocessing import Process
import os
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import requests
import json
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
    light_url = "http://raspberrypi.local:1234/light_level"
    temp_url = "http://raspberrypi.local:1234/temperature"
    humidity_url = "http://raspberrypi.local:1234/humidity"
    while True:
        try:
            light_data = requests.get(light_url).json()
            light_value = light_data.get("light_level")
            temp_data = requests.get(temp_url).json()
            temp = temp_data.get("temperature")
            humidity_data = requests.get(humidity_url).json()
            humidity = humidity_data.get("humidity")
            print("Light Level:", light_value)
            print("Temperature:", temp)
            print("Humidity:", humidity)
            db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
        except requests.RequestException as e:
            print("Request Error:", e)
        except ValueError as e:
            print("JSON Decode Error:", e)
        except Exception as e:
            print("Unexpected Error:", e)
        finally:
            # Adjust sleep time as needed
            time.sleep(5)

# Configuration
app = FastAPI()
# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/light_level", response_class=JSONResponse)
def get_light_level() -> JSONResponse:
  response = {}
  
  return JSONResponse(response)

@app.get("/temperature", response_class=JSONResponse)
def get_temperature() -> JSONResponse:
  response = {}
  
  return JSONResponse(response)

@app.get("/humidity", response_class=JSONResponse)
def get_humidity() -> JSONResponse:
  response = {}
  
  return JSONResponse(response)

if __name__ == "__main__":
    try:
        p = Process(target=collect_data)
        p.start()
        uvicorn.run("app:app", host="0.0.0.0", port=4321, reload=True)
    finally:
        p.terminate()
        p.join()