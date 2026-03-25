
from djitellopy import Tello
import time

tello = Tello()

try:

    tello.connect(wait_for_state=False)

    time.sleep(1)

    tello.takeoff()

    time.sleep(1)

    for i in range(4):
        tello.move_forward(30)
        if i < 3:
            tello.rotate_clockwise(90)
    

    tello.land()

except Exception:
    print("エラーが発生しました")
    tello.land()

