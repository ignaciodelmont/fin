import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import middleware


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
print("DIR PATH", DIR_PATH)


app = FastAPI()

app.middleware("http")(middleware.log_time)
app.middleware("http")(middleware.load_user)
app.middleware("http")(middleware.log_headers)


app.mount("/static", StaticFiles(directory=f"{DIR_PATH}/static"), name="static")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(f"{DIR_PATH}/static/images/favicon.ico")


templates = Jinja2Templates(directory=f"{DIR_PATH}/templates")
