"""
肩関節の制御
"""

from lib.servo import sg90


class ShoulderJoint:
    """
    肩関節
    """

    def __init__(self, servoX: sg90.SG90by180, servoY: sg90.SG90by180):
        self.servo_x = servoX
        self.servo_y = servoY
        self.current_angle_x = 0.0
        self.current_angle_y = 0.0

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
    import lib.i2c.pca9685

    def _proc(pca_pwm: lib.i2c.pca9685.PWM):
        sg90_x = sg90.SG90by180(pca_pwm, 0)
        sg90_y = sg90.SG90by180(pca_pwm, 1)
        shoulder = ShoulderJoint(sg90_x, sg90_y)
        shoulder.set_angle(90, 90)

        while True:
            try:
                print("x: ", end="")
                degree_x = float(input())
                print("y: ", end="")
                degree_y = float(input())

                shoulder.move(degree_x, degree_y)
            except ValueError:
                print("Invalid input.")

    lib.i2c.pca9685.run_with(_proc)
