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

def collect_data():
    """
    Every several seconds, make requests to the Raspberry Pi API to collect sensor data and store it in the SQL database, then make a request to Raspberry Pi API to display the most recent weather data on the LCD.
    """
    global light_value, temp, humidity
    light_url = "http://raspberrypi.local:1234/light_level"
    temp_and_humid_url = "http://raspberrypi.local:1234/temperature_and_humidity"
    display_url = "http://raspberrypi.local:1234/set_display"
    while True:
        try:
            light_data = requests.get(light_url).json()
            light_level = light_data.get("light_level")
            temp_and_humid_data = requests.get(temp_and_humid_url).json()
            temp = temp_and_humid_data.get("temperature")
            humidity = temp_and_humid_data.get("humidity")
            data = {"temperature":temp, "humidity": humidity, "light_level":light_level}
            x = requests.post(display_url, json = data)
            print("Light Level:", light_level)
            print("Temperature:", temp)
            print("Humidity:", humidity)
            print(x)
            db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
            cursor = db.cursor()
            query = "insert into sensordata(temperature, humidity, light_level) values (%s, %s, %s)"
            value = (temp, humidity, light_level)
            cursor.execute(query, value)
            db.commit()
            db.close()
        except requests.RequestException as e:
            print("Request Error:", e)
        except ValueError as e:
            print("JSON Decode Error:", e)
        except Exception as e:
            print("Unexpected Error:", e)
        except RuntimeError as err:
            print("runtime error: {0}".format(err))
        finally:
            # Adjust sleep time as needed
            time.sleep(5)

# Configuration
app = FastAPI()
# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)       
def get_index() -> HTMLResponse:
  with open('index.html') as html:          
    return HTMLResponse(content=html.read())

@app.get("/sensor_data", response_class=JSONResponse)
async def get_sensor_data() -> JSONResponse:
    response = {}
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("select temperature, humidity, light_level, created_at from sensordata order by created_at desc limit 10")
    records = cursor.fetchall()
    db.close()
    for index, row in enumerate(records):    #iterates through the database data to construct the dict
        response[index] = {"temperature": float(row[0]),"humidity": int(row[1]),"light_level": float(row[2]),"timestamp": row[3].strftime("%Y-%m-%d %H:%M:%S")
     }
    return JSONResponse(response)

if __name__ == "__main__":
    try:
        p = Process(target=collect_data)
        p.start()
        uvicorn.run("app:app", host="0.0.0.0", port=4321)
    finally:
        p.terminate()
        p.join()