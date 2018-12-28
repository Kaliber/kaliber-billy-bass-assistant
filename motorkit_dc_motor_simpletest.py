"""Simple test for using adafruit_motorkit with a DC motor"""
import time
from adafruit_motorkit import MotorKit

kit = MotorKit()
COUNT = 5
CURRENT_COUNT = 0

while CURRENT_COUNT < 10:
  kit.motor1.throttle = -1
  time.sleep(0.2)
  kit.motor1.throttle = 0
  time.sleep(0.2)
  kit.motor1.throttle = 1
  time.sleep(0.2)
  kit.motor1.throttle = 0
  time.sleep(0.2)
  CURRENT_COUNT += 1

kit.motor1.throttle = -1
