import azure.functions as func
import datetime
import logging
import os
import requests
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

# Environment variables
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME", "weather-logs")
CITY_NAME = os.getenv("CITY_NAME", "Lagos")
TIMER_SCHEDULE = os.getenv("TIMER_SCHEDULE", "0 */3 * * *")  # Default: every 3 hours

@app.timer_trigger(schedule=TIMER_SCHEDULE, arg_name="wedaTimer", run_on_startup=False, use_monitor=True)
def wedattfunc(wedaTimer: func.TimerRequest) -> None:
    if wedaTimer.past_due:
        logging.warning("The timer is past due.")

    logging.info("Starting weather logging function...")

    log_filename = "weather.log"
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y\t%b\t%d\t%H:%M:%S')

    try:
        # Fetch weather data
        url = f"http://wttr.in/{CITY_NAME}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current_temp = data["current_condition"][0]["temp_C"]
        tomorrow_temp = data["weather"][1]["hourly"][4]["tempC"]

        # Format log line
        log_line = f"{timestamp}\t{current_temp}°C\t{tomorrow_temp}°C\n"

        # Connect to Azure Blob Storage
        blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service.get_container_client(CONTAINER_NAME)

        if not container_client.exists():
            container_client.create_container()
            logging.info(f"Created container: {CONTAINER_NAME}")

        blob_client = container_client.get_blob_client(log_filename)

        try:
            # Try to read existing log
            existing_log = blob_client.download_blob().readall().decode("utf-8")
            updated_log = existing_log + log_line
        except Exception:
            # If log doesn’t exist, create with header
            header = "year\tmonth\tday\thour\tcurrent_temp\ttomorrow_temp\n"
            updated_log = header + log_line
            logging.info("Created new log file with header.")

        # Upload updated log
        blob_client.upload_blob(updated_log, overwrite=True)
        logging.info("Weather data appended successfully.")

    except Exception as e:
        logging.error(f"Error during weather logging: {e}")
