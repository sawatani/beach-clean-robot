import time

import pigpio
from lib.i2c import PCA9685


class SG90:
    def __init__(
        self,
        pwm: PCA9685.PWM,
        channel: int,
        pulse_min: float = 0.5,
        pulse_max: float = 2.4,
    ):
        """
        ARGS:
          pwm: instance of PCA9685.PWM
          channel: id on PCA9685
          pulse_min: min value of pulse width
          pulse_max: max value of pulse width
        """
        self.pwm = pwm
        self.channel = channel
        self.pulse_min = pulse_min
        self.pulse_max = pulse_max

        pwm.set_frequency(50)

    def set_pulse_rate(self, rate: float):
        """
        ARGS:
          rate: float 0.0 - 1.0
        """
        pw = self.pulse_min + (self.pulse_max - self.pulse_min) * rate
        self.pwm.set_pulse_width(self.channel, pw)


class SG90_180:
    def __init__(
        self,
        pwm: PCA9685.PWM,
        channel: int,
        pulse_min: float = 0.5,
        pulse_max: float = 2.4,
    ):
        super().__init__(self, pwm, pulse_min, pulse_max)

    def set_angle(self, degree: float):
        """
        Move motor to specified degree

        ARGS:
          degree: float 0.0 - 180.0
        """
        self.set_pulse_rate(degree / 180)


class SG90_360(SG90):
    def __init__(
        self,
        pwm: PCA9685.PWM,
        channel: int,
        pulse_min: float = 0.5,
        pulse_max: float = 2.4,
    ):
        super().__init__(self, pwm, pulse_min, pulse_max)

    def move_angle(self, degree: float):
        """
        Move motor to specified degree

        ARGS:
          degree: float -180.0 - 180.0
        """
        self.set_pulse_rate(degree / 360)


# サンプルコード
if __name__ == "main":
    pi = pigpio.pi()
    if not pi.connected:
        print("GPIO could not start")
        exit(1)

    try:
        pwm = PCA9685.PWM(pi)
        sg90 = SG90_180(pwm, 0)

        for d in range(0, 180, step=10):
            sg90.set_angle(d)
            time.sleep(0.5)

        pwm.cancel()
    finally:
        pi.stop()
