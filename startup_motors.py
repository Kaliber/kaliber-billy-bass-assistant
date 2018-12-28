"""Simple test for using adafruit_motorkit with a DC motor"""
import time
from adafruit_motorkit import MotorKit

kit = MotorKit()
COUNT = 10
CURRENT_COUNT = 0

while CURRENT_COUNT < COUNT:
  kit.motor2.throttle = 1
  time.sleep(0.1)
  kit.motor2.throttle = 0
  time.sleep(0.1)
  kit.motor2.throttle = -1
  time.sleep(0.1)
  kit.motor2.throttle = 0
  time.sleep(0.1)

  kit.motor1.throttle = -1
  time.sleep(0.1)
  kit.motor1.throttle = 0
  time.sleep(0.1)
  kit.motor1.throttle = 1
  time.sleep(0.1)
  kit.motor1.throttle = 0
  time.sleep(0.1)
  CURRENT_COUNT += 1

kit.motor2.throttle = 0
kit.motor1.throttle = -1
