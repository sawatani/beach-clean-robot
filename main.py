import time
from RPi import GPIO

channel = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

p = GPIO.PWM(channel, 50)

try:
    p.start(0.0)
    while True:
        print("input Duty Cyle (2.5 - 12)")
        try:
            dc = float(input())
        except ValueError:
            dc = 2.5

        #DutyCycle dc%
        p.ChangeDutyCycle(dc)

        #最大180°回転を想定し、0.3sec以上待つ
        time.sleep(0.4)

        #回転終了したら一旦DutyCycle0%にする
        p.ChangeDutyCycle(0.0)
finally:
    print('Cleaning up GPIO channels')
    GPIO.cleanup()

