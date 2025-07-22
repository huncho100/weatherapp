import azure.functions as func
import datetime
import logging
import os
import requests
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

# Read connection info from environment
CONNECTION_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
CONTAINER_NAME = "weather-logs"

@app.timer_trigger(schedule=os.environ["TIMER_SCHEDULE"], arg_name="wedaTimer", run_on_startup=False, use_monitor=True) 
def wedattfunc(wedaTimer: func.TimerRequest) -> None:

    if wedaTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Starting weather logging function...')

    city = os.getenv("CITY_NAME", "Lagos")
    today = datetime.datetime.now().strftime("%Y%m%d")
    log_filename = "rx_poc.log"

    try:
        # Fetch JSON weather data
        response = requests.get(f"http://wttr.in/{city}?format=j1")
        response.raise_for_status()
        data = response.json()

        # Extract current temperature (°C)
        obs_tmp = data["current_condition"][0]["temp_C"]

        # Extract tomorrow's temperature at around 12:00 (index 4 = ~noon)
        fc_tmp = data["weather"][1]["hourly"][4]["tempC"]

        # Timestamp
        now = datetime.datetime.now()
        log_line = f"{now.year}\t{now.strftime('%b')}\t{now.day}\t{now.strftime('%H:%M:%S')}\t{obs_tmp}°C\t{fc_tmp}°C\n"

        # Connect to Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)

        if not container_client.exists():
            container_client.create_container()

        # Upload or update log file
        blob_client_log = container_client.get_blob_client(log_filename)
        try:
            existing_log = blob_client_log.download_blob().readall().decode('utf-8')
        except Exception:
            existing_log = "year\tmonth\tday\thour\tobs_tmp\tfc_tmp\n"

        updated_log = existing_log + log_line
        blob_client_log.upload_blob(updated_log, overwrite=True)

        logging.info("Weather data logged successfully.")

    except Exception as e:
        logging.error("Unhandled error during execution")
