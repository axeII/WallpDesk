"""Horizon

Horizon module for checking local sunset and sunrise hours
"""
__author__ = "ales lerch"

import datetime
from astral import Astral
from subprocess import PIPE, Popen
from dateutil.parser import parse


def get_horizon_time(db_city=""):
    astr = Astral()
    astr.solar_depression = "civil"

    if not db_city:
        cmd = b"""do shell script ("/usr/sbin/systemsetup -gettimezone ") with administrator privileges """
        proc = Popen(["osascript", "-"], stdin=PIPE, stdout=PIPE)
        city, _ = proc.communicate(cmd)
        try:
            city = astr[city.decode("utf-8").split("/")[-1].strip()]
        except:
            """ Neutral city london for settings in case of error"""
            city = astr["London"]
    else:
        try:
            city = astr[db_city]
        except:
            return {}

    today = datetime.date.today()
    time = datetime.datetime.today()
    sun = city.sun(date=datetime.date(today.year, today.month, today.day), local=True)
    sunset = parse(str(sun["sunset"]))
    sunrise = parse(str(sun["sunrise"]))

    return {
        "sunset": (sunset.hour, sunset.minute, sunset.second),
        "sunrise": (sunrise.hour, sunrise.minute, sunrise.second),
        "today_time": (time.hour, time.minute, time.second),
        "timezone": city.name,
    }
