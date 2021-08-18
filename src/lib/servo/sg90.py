"""
Handle servo motor SG90
"""

import sys

import pigpio

from lib.i2c import pca9685


class SG90:
    """
    Abstract class of SG90
    """

    def __init__(
        self,
        pwm: pca9685.PWM,
        channel: int,
        pulse_min: float = 0.5,
        pulse_max: float = 2.4,
    ):
        """
        ARGS:
          pwm: instance of pca9685.PWM
          channel: id on PCA9685
          pulse_min: min value of pulse width
          pulse_max: max value of pulse width
        """
        self.pwm = pwm
        self.channel = channel
        self.pulse_min = pulse_min
        self.pulse_max = pulse_max

        pwm.set_frequency(50)

    def calc_pulse_width(self, rate: float):
        """
        Calculate pulse width by rate

        ARGS:
          rate: 0.0 - 1.0
        """
        return self.pulse_min + (self.pulse_max - self.pulse_min) * rate

    def set_pulse_rate(self, rate: float):
        """
        Set pulse width by rate

        ARGS:
          rate: float 0.0 - 1.0
        """
        pulse_width = self.calc_pulse_width(rate)
        print(f"Setting pulse width {pulse_width}")
        self.pwm.set_pulse_width(self.channel, pulse_width * 1000)


class SG90by180(SG90):
    """
    SG90 with 180 degrees
    """

    def __init__(
        self,
        pwm: pca9685.PWM,
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


class SG90by360(SG90):
    """
    SG90 with 360 degrees
    """

    def __init__(
        self,
        pwm: pca9685.PWM,
        channel: int,
        pulse_min: float = 0.5,
        pulse_max: float = 2.4,
    ):
        super().__init__(self, pwm, pulse_min, pulse_max)

    def move_angle(self, direction: float):
        """
        Move motor to specified degree

        ARGS:
          direction: float -100.0 - 100.0
        """
        self.set_pulse_rate((direction + 100) / 200)


# サンプルコード
if __name__ == "__main__":
    pi = pigpio.pi()
    if not pi.connected:
        print("GPIO could not start")
        sys.exit(1)

    PCA9685_PWM = None
    try:
        PCA9685_PWM = pca9685.PWM(pi)
        sg90s = list(map(lambda i: SG90(PCA9685_PWM, i), range(16)))

        while True:
            try:
                print("channel(0-15): ", end="")
                ch = int(input())
                print("rate(0-100): ", end="")
                rt = float(input()) / 100

                sg90s[ch].set_pulse_rate(rt)
            except ValueError:
                print("Invalid input.")
    finally:
        import traceback

        traceback.print_exc()
        print("Tidy up...")
        if PCA9685_PWM:
            PCA9685_PWM.cancel()
        pi.stop()
