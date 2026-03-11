from djitellopy import Tello
import time

t = Tello()
time.sleep(1)
t.connect()
print(t.get_battery())
t.end()