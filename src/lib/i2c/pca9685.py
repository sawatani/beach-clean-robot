"""
Handle GPIO via PCA9685
"""

import sys
import time
import traceback

import pigpio


class PWM:

    """
    This class provides an interface to the I2C PCA9685 PWM chip.

    The chip provides 16 PWM channels.

    All channels use the same frequency which may be set in the
    range 24 to 1526 Hz.

    If used to drive servos the frequency should normally be set
    in the range 50 to 60 Hz.

    The duty cycle for each channel may be independently set
    between 0 and 100%.

    It is also possible to specify the desired pulse width in
    microseconds rather than the duty cycle.  This may be more
    convenient when the chip is used to drive servos.

    The chip has 12 bit resolution, i.e. there are 4096 steps
    between off and full on.
    """

    _MODE1 = 0x00
    _MODE2 = 0x01
    _SUBADR1 = 0x02
    _SUBADR2 = 0x03
    _SUBADR3 = 0x04
    _PRESCALE = 0xFE
    _LED0_ON_L = 0x06
    _LED0_ON_H = 0x07
    _LED0_OFF_L = 0x08
    _LED0_OFF_H = 0x09
    _ALL_LED_ON_L = 0xFA
    _ALL_LED_ON_H = 0xFB
    _ALL_LED_OFF_L = 0xFC
    _ALL_LED_OFF_H = 0xFD

    _RESTART = 1 << 7
    _AI = 1 << 5
    _SLEEP = 1 << 4
    _ALLCALL = 1 << 0

    _OCH = 1 << 3
    _OUTDRV = 1 << 2

    def __init__(self, gpio: pigpio.pi, bus: int = 1, address: int = 0x40):

        self.gpio = gpio
        self.bus = bus
        self.address = address

        self.handle = gpio.i2c_open(bus, address)

        self._write_reg(self._MODE1, self._AI | self._ALLCALL)
        self._write_reg(self._MODE2, self._OCH | self._OUTDRV)

        time.sleep(0.0005)

        mode = self._read_reg(self._MODE1)
        self._write_reg(self._MODE1, mode & ~self._SLEEP)

        time.sleep(0.0005)

        self.set_duty_cycle(-1, 0)
        self.set_frequency(200)

    def get_frequency(self):

        "Returns the PWM frequency."

        return self._frequency

    def set_frequency(self, frequency):

        "Sets the PWM frequency."

        prescale = int(round(25000000.0 / (4096.0 * frequency)) - 1)

        if prescale < 3:
            prescale = 3
        elif prescale > 255:
            prescale = 255

        mode = self._read_reg(self._MODE1)
        self._write_reg(self._MODE1, (mode & ~self._SLEEP) | self._SLEEP)
        self._write_reg(self._PRESCALE, prescale)
        self._write_reg(self._MODE1, mode)

        time.sleep(0.0005)

        self._write_reg(self._MODE1, mode | self._RESTART)

        self._frequency = (25000000.0 / 4096.0) / (prescale + 1)
        self._pulse_width = 1000000.0 / self._frequency

    def set_duty_cycle(self, channel, percent):

        "Sets the duty cycle for a channel.  Use -1 for all channels."

        steps = int(round(percent * (4096.0 / 100.0)))

        if steps < 0:
            level_high = 0
            level_low = 4096
        elif steps > 4095:
            level_high = 4096
            level_low = 0
        else:
            level_high = 0
            level_low = steps

        if 0 <= channel <= 15:
            self.gpio.i2c_write_i2c_block_data(
                self.handle,
                self._LED0_ON_L + 4 * channel,
                [level_high & 0xFF, level_high >> 8, level_low & 0xFF, level_low >> 8],
            )

        else:
            self.gpio.i2c_write_i2c_block_data(
                self.handle,
                self._ALL_LED_ON_L,
                [level_high & 0xFF, level_high >> 8, level_low & 0xFF, level_low >> 8],
            )

    def set_pulse_width(self, channel, width):

        "Sets the pulse width for a channel.  Use -1 for all channels."

        print(f"Calculating {width}/{self._pulse_width}")
        self.set_duty_cycle(channel, (float(width) / self._pulse_width) * 100.0)

    def cancel(self):

        "Switches all PWM channels off and releases resources."

        self.set_duty_cycle(-1, 0)
        self.gpio.i2c_close(self.handle)

    def _write_reg(self, reg, byte):
        self.gpio.i2c_write_byte_data(self.handle, reg, byte)

    def _read_reg(self, reg):
        return self.gpio.i2c_read_byte_data(self.handle, reg)


def run_with(func, bus: int = 1, address: int = 0x40):
    """
    GPIO の接続確認から片付けまでをしてくれる。
    """
    gpio_pi = pigpio.pi()
    if not gpio_pi.connected:
        print("GPIO could not start")
        sys.exit(1)

    pca9685_pwm = None
    try:
        pca9685_pwm = PWM(gpio_pi, bus, address)
        func(pca9685_pwm)
    finally:
        traceback.print_exc()
        print("Tidy up...")
        if pca9685_pwm:
            pca9685_pwm.cancel()
        gpio_pi.stop()
