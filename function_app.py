import azure.functions as func
import datetime
import json
import logging
import requests
import os

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */2 * * * *", arg_name="wedaTimer", run_on_startup=False, use_monitor=True) 
def wedattfunc(wedaTimer: func.TimerRequest) -> None:
    
    if wedaTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    # Define the city and date format
    city = "Casablanca"
    today = datetime.datetime.now().strftime("%Y%m%d")
    weather_report = f"raw_data_{today}"

    # Download the weather report
    response = requests.get(f"http://wttr.in/{city}?format=%t")
    with open(weather_report, 'w') as file:
        file.write(response.text)

    # Extract temperatures
    with open(weather_report, 'r') as file:
        lines = file.readlines()
    
    logging.info(f"Lines content: {lines}")
    logging.info(f"Number of lines: {len(lines)}")

    obs_tmp = lines[0].strip() if len(lines) > 0 else "N/A"

    # Extract tomorrow's temperature forecast for noon
    fc_tmp = lines[2].strip() if len(lines) >= 3 else "N/A"

    # Get the current date and time
    now = datetime.datetime.now()
    year = now.year
    month = now.strftime("%b")
    day = now.day
    hour = now.strftime("%H:%M:%S")

    # Create the header if the log file doesn't exist
    log_file = "rx_poc.log"
    if not os.path.exists(log_file):
        with open(log_file, 'w') as file:
            file.write("year\tmonth\tday\thour\tobs_tmp\tfc_tmp\n")

    # Append the current weather data to the log file
    with open(log_file, 'a') as file:
        file.write(f"{year}\t{month}\t{day}\t{hour}\t{obs_tmp}\t{fc_tmp}\n")

    logging.info('Weather data logged successfully.')