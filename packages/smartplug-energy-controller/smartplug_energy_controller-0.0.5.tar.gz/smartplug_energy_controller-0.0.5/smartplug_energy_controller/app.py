import logging
import uvicorn
import os

from dotenv import load_dotenv
from pathlib import Path
root_path = str( Path(__file__).parent.absolute() )

from fastapi import FastAPI, Request
from typing import Union
from pydantic_settings import BaseSettings

from smartplug_energy_controller.plug_controller import TapoPlugController

class Settings(BaseSettings):
    tapo_control_user: str
    tapo_control_passwd: str
    tapo_plug_ip: str
    # Time in minutes for which the energy consumption should be evaluated
    eval_time_in_min: int = 10 
    # Expected consumption value in Watt of consumer(s) being plugged into the Tapo Plug
    expected_consumption: float = 200 
    # Efficiency of the consumer(s) being plugged into the Tapo Plug (0 < x < 1)
    # 0 means that the plug should be turned on only when no energy has to be obtained from the provider. 
    # 1 means that the plug should be turned on when the the obtained energy from the provider is equal to the expected consumption.
    consumer_efficiency: float = 0.5 
    # Write logging to this file instead of to stdout
    log_file: Union[str, None] = None 
    log_level: int = logging.INFO

def create_logger(file : Union[str, None]) -> logging.Logger:
    logger = logging.getLogger('smartplug-energy-controller')
    log_handler : Union[logging.FileHandler, logging.StreamHandler] = logging.FileHandler(file) if file else logging.StreamHandler() 
    formatter = logging.Formatter("%(levelname)s: %(asctime)s: %(message)s")
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    return logger

if os.path.exists(f"{root_path}/.env"):
    load_dotenv(f"{root_path}/.env")

try:
    import importlib.metadata
    __version__ = importlib.metadata.version('smartplug_energy_controller')
except:
    __version__ = 'development'

settings = Settings()
logger=create_logger(settings.log_file)
logger.setLevel(logging.INFO)
logger.info(f"Starting smartplug-energy-controller version {__version__}")
logger.setLevel(settings.log_level)
controller=TapoPlugController(logger, settings.eval_time_in_min, settings.expected_consumption, settings.consumer_efficiency,
                              settings.tapo_control_user, settings.tapo_control_passwd, settings.tapo_plug_ip)
app = FastAPI()

@app.get("/")
async def root(request: Request):
    return {"message": "Hallo from Tapo Plug Controller"}

@app.post("/add_obtained_watt_from_provider")
async def add_obtained_watt_from_provider(request: Request):
    value = float(await request.body())
    await controller.add_obtained_watt_from_provider(value)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)