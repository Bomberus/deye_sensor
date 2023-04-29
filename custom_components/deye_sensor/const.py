"""Constants for deye_sensor."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Deye Sensor"
DOMAIN = "deye_sensor"
VERSION = "0.0.0"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

CURRENT_POWER = "webdata_now_p"
GENERATED_TODAY = "webdata_today_e"
GENERATED_TOTAL = "webdata_total_e"
ALARMS = "webdata_alarm"
POWERED_ON = "powered_on"

PATH = "/status.html"
