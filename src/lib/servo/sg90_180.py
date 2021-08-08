import time

import pigpio
from lib.i2c import PCA9685


class SG90_180:
    def __init__(
        self,
        pwm: PCA9685.PWM,
        channel: int,
        pulse_min: float = 0.5,
        pulse_max: float = 2.4,
    ):
        self.pwm = pwm
        self.channel = channel

        pwm.set_frequency(50)  # suitable for servos

    def set_angle(self, degree: float):
        """
        Move motor to specified degree

        ARGS:
          degree: float 0.0 - 180.0
        """
        pw = self.pulse_min + degree * (self.pulse_max - self.pulse_min) / 180
        self.pwm.set_pulse_width(self.channel, pw)


# サンプルコード
if __name__ == "main":
    pi = pigpio.pi()
    if not pi.connected:
        print("GPIO could not start")
        exit(1)

    try:
        sg90 = SG90_180(PCA9685.PWM(pi), 0)

        for d in range(0, 180, step=10):
            sg90.set_angle(d)
            time.sleep(0.5)

        pwm.cancel()
    finally:
        pi.stop()
