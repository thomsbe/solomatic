import nxppy
import time
from RPi import GPIO

GREEN = 47
RED = 35
PIEP = 26
ON = GPIO.HIGH
OFF = GPIO.LOW


def init_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GREEN, GPIO.OUT)
    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(PIEP, GPIO.OUT)
    GPIO.output(RED, OFF)
    GPIO.output(GREEN, OFF)
    GPIO.output(PIEP, OFF)


def blinkled(led, duration, piep):
    GPIO.output(led, ON)
    if piep:
        GPIO.output(PIEP, ON)
    time.sleep(duration)
    GPIO.output(led, OFF)
    if piep:
        GPIO.output(PIEP, OFF)

def init_mifare():
    mifare = nxppy.Mifare()
    return mifare


def get_uid(mifare, color, time, logger):
    blinkled(color, time, False)
    try:
        uid = mifare.select()
        return uid
    except nxppy.SelectError:
        return None
    except Exception:
        import traceback

        logger.error('generic exception: ' + traceback.format_exc())
        return None


def piep(duration):
    GPIO.output(PIEP, ON)
    time.sleep(duration)
    GPIO.output(PIEP, OFF)
