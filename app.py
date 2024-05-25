from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

light_level = 0
temp = 0
humidity = 0
to_display = ""

# Configuration
app = FastAPI()
# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/light_level", response_class=JSONResponse)
def load_menu() -> JSONResponse:
  response = {}
  response["light_level"] = light_level
  return JSONResponse(response)

@app.get("/temp", response_class=JSONResponse)
def load_menu() -> JSONResponse:
  response = {}
  response["temp"] = temp
  return JSONResponse(response)

@app.get("/humidity", response_class=JSONResponse)
def load_menu() -> JSONResponse:
  response = {}
  response["humidity"] = humidity
  return JSONResponse(response)

@app.post("/set_display")
def add_item(display_data: dict):
  global to_display
  to_display = display_data["to_display"]

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
  with open("index.html") as html:
    return HTMLResponse(content=html.read())

if __name__ == "__main__":
  uvicorn.run("app:app", host="0.0.0.0", port=1234, reload=True)