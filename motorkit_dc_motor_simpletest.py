"""Simple test for using adafruit_motorkit with a DC motor"""
import time
from adafruit_motorkit import MotorKit

kit = MotorKit()

#while True:
kit.motor1.throttle = -1.0
time.sleep(0.2)
kit.motor1.throttle = 1.0
time.sleep(0.2)