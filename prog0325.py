
from djitellopy import Tello
import time

tello = Tello()

try:

    tello.connect(wait_for_state=False)

    time.sleep(1)

    tello.takeoff()

    time.sleep(1)

    tello.move_forward(30)

    time.sleep(1)

    tello.land()

except Exception:
    print("エラーが発生しました")
    tello.land()

