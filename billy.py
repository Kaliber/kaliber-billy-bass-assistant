"""
Billy Bass stuff
"""

import time
import random
import threading
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

from adafruit_motorkit import MotorKit

class Billy:

    def __init__(self):
        self.motor = MotorKit()
        self.next = threading.Event()
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def wakeup(self):
        def f():
            self._wakeup()

        self.next.set()
        self.queue.put(f)

    def speak(self):
        self.next.set()
        self.queue.put(self._speak)

    def off(self):
        self.next.set()
        self.queue.put(self._off)

    def _run(self):
        while True:
            func = self.queue.get()
            func()

    def _wakeup(self):
        self.motor.motor2.throttle = 1.0

    def _speak(self):
        self._wakeup()
        self.next.clear()
        while not self.next.is_set():
            self.motor.motor1.throttle = 1
            time.sleep(random.uniform(0.05, 0.15))
            self.motor.motor1.throttle = -1
            time.sleep(random.uniform(0.05, 0.15))
            self.motor.motor1.throttle = 0
            time.sleep(random.uniform(0.05, 0.25))
        # self._off()

    def _off(self):
        self.motor.motor1.throttle = 0
        self.motor.motor2.throttle = -0.2
        time.sleep(0.2)
        self.motor.motor2.throttle = 0

billy = Billy()

