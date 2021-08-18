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
