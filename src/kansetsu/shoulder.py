"""
肩関節の制御
"""

from lib.servo.sg90 import SG90by180


class ShoulderJoint:
    """
    肩関節
    """

    def __init__(
        self,
        servoX: SG90by180,
        servoY: SG90by180,
        start_x: float = 90,
        start_y: float = 90,
    ):
        self.servo_x = servoX
        self.servo_y = servoY
        self.current_angle_x = start_x
        self.current_angle_y = start_y

    def __move_to(self):
        self.servo_x.set_angle(self.current_angle_x)
        self.servo_y.set_angle(self.current_angle_y)

    def set_angle(self, degree_x: float, degree_y: float):
        """
        それぞれのサーボモーターの角度を指定する。
        """
        self.current_angle_x = degree_x
        self.current_angle_y = degree_y
        self.__move_to()

    def move(self, degree_x: float, degree_y: float):
        """
        現在の相対角度で指定する。
        """
        self.current_angle_x += degree_x
        self.current_angle_y += degree_y
        self.__move_to()


# サンプルコード
if __name__ == "__main__":
    from lib.i2c.pca9685 import PWM, run_with

    def _proc(pca_pwm: PWM):
        sg90_x = SG90by180(pca_pwm, 0)
        sg90_y = SG90by180(pca_pwm, 1)
        shoulder = ShoulderJoint(sg90_x, sg90_y)
        shoulder.move(0, 0)

        while True:
            try:
                print("x: ", end="")
                degree_x = float(input())
                print("y: ", end="")
                degree_y = float(input())

                shoulder.move(degree_x, degree_y)
            except ValueError:
                print("Invalid input.")

    run_with(_proc)
