import vestaboard
from vestaboard.formatter import Formatter
import requests
from datetime import datetime, timedelta, timezone
import calendar
import os

clear = [
    67,
    67,
    67,
    64,
    64,
    64,
    65,
    65,
    65,
    65,
    65,
    65,
    65,
    65,
    65,
    65,
    64,
    64,
    64,
    67,
    67,
    67,
]
partial = [
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    65,
    65,
    65,
    65,
    65,
    65,
    65,
    65,
    64,
    64,
    67,
]
scattered_clouds = [
    69,
    69,
    69,
    69,
    69,
    69,
    67,
    67,
    67,
    69,
    69,
    69,
    69,
    69,
    69,
    67,
    67,
    67,
    69,
    69,
    69,
    69,
]
broken_clouds = [
    67,
    67,
    67,
    69,
    69,
    69,
    67,
    67,
    67,
    69,
    69,
    69,
    67,
    67,
    67,
    69,
    69,
    69,
    67,
    67,
    67,
    69,
]
shower_rain = [
    67,
    69,
    59,
    67,
    69,
    59,
    67,
    69,
    59,
    67,
    69,
    59,
    67,
    69,
    59,
    67,
    69,
    59,
    67,
    69,
    59,
    67,
]
rain = [
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
]
snow = [
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
    67,
    59,
]
mist = [
    67,
    69,
    67,
    69,
    67,
    69,
    67,
    69,
    67,
    69,
    67,
    69,
    67,
    69,
    67,
    69,
    67,
    69,
    67,
    69,
    67,
    69,
]
unknown_conditions = [
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
    69,
]


def get_pattern(icon_info):
    match icon_info:
        case 1:
            return clear
        case 2:
            return partial
        case 3:
            return scattered_clouds
        case 4:
            return broken_clouds
        case 9:
            return shower_rain
        case 10:
            return rain
        case 11:
            return rain
        case 13:
            return snow
        case 50:
            return mist
        case _:
            return unknown_conditions


def lambda_handler(event, context):
    # Instantiate VB
    installable = vestaboard.Installable(
        os.environ["VB"],
        os.environ["VB_KEY"],
        saveCredentials=False,
    )

    vboard = vestaboard.Board(installable)

    # Open Weather API call
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q=Seattle,us&units=imperial&APPID="
        + os.environ["WEATHER_KEY"]
    )
    weath_data = response.json()
    # Place values
    current_temp = round(weath_data["main"]["temp"])
    high = round(weath_data["main"]["temp_max"])
    low = round(weath_data["main"]["temp_min"])
    condition = weath_data["weather"][0]["main"]
    condition_info = int(weath_data["weather"][0]["icon"][0:2])
    repeat_pattern = get_pattern(condition_info)

    # Output formatting
    weather = f"{current_temp}° {condition}"
    h_outlook = f"High: {high}°"
    l_outlook = f"Low: {low}°"

    # Date
    today = datetime.now(timezone(timedelta(hours=-8)))
    # Date formatting
    day = f"{calendar.day_name[today.weekday()]}, {calendar.month_name[today.month][0:3]} {today.day}"

    characters = [
        Formatter().convertLine(day),
        repeat_pattern,
        Formatter().convertLine(weather),
        Formatter().convertLine(h_outlook),
        Formatter().convertLine(l_outlook),
        repeat_pattern,
    ]

    vboard.raw(characters)

    return "Updated!"
