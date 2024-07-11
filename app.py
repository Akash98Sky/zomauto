import logging
from typing import Any
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from zomato.logger import setLogLevel, setWebDriverLogLevel
from backend import browser, routes

# set logging level of zomato module only
setLogLevel(logging.DEBUG)
setWebDriverLogLevel(logging.WARNING)


app = FastAPI()

# config browser
browser.config(headless=True)
app.add_event_handler("startup", browser.startup)
app.add_event_handler("shutdown", browser.shutdown)

# config CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.mount("/api", routes.api_routes)

# Serve the React app
app.mount("/", StaticFiles(directory="frontend/build", html=True))
