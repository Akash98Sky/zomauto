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
@app.on_event("startup")
async def startup():
    await browser.startup()
@app.on_event("shutdown")
async def shutdown():
    await browser.shutdown()

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
