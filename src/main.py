import sys
import time
import traceback

import pigpio

from lib.i2c.pca9685 import PWM
from lib.servo.sg90 import SG90

pi = pigpio.pi()
if not pi.connected:
    print("GPIO could not start")
    sys.exit(1)

pwm = None
try:
    pwm = PWM(pi)
    sg90s = list(map(lambda i: SG90(pwm, i), range(16)))

    while True:
        try:
            print("channel(0-15): ", end="")
            channel = int(input())
            print("rate(0-100): ", end="")
            rate = float(input()) / 100

            sg90s[channel].set_pulse_rate(rate)
        except ValueError:
            print("Invalid input.")
except:
    traceback.print_exc()
    print("Tidy up...")
    if pwm:
        pwm.cancel()
    pi.stop()
