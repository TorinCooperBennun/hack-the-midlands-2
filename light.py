"""
Controls our horrific ratchet emergency exit light.

RUN setup() FIRST
"""

# This should be GPIO21, right on the end of the pinout.
OUTPUT_PIN = 40

setup_done = False


def setup():
    """
    RUN THIS FIRST
    """
    try:
        import RPi.GPIO as gpio
    except:
        print("Unable to import RPi.GPIO (please run as superuser)")
        exit()

    gpio.setmode(gpio.BOARD)
    gpio.setup(OUTPUT_PIN, gpio.OUT)

    setup_done = True


def activate(light_on=True):
    """
    activate(True) to turn the thing on
    activate(False) to turn it off
    lmao
    """
    if not setup_done:
        raise RuntimeError("setup() was never called!")

    gpio.output(OUTPUT_PIN, gpio.HIGH if light_on else GPIO.LOW)