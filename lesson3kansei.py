"""
Telloで長方形を描くシンプルプログラム
（前進 + 回転の繰り返し）
"""

from djitellopy import Tello
import time

WIDTH = 40   # 横の長さ (cm)
HEIGHT = 20  # 縦の長さ (cm)
TURN_ANGLE = 90  # 右回転角度 (deg)

# Telloに接続
print("Telloに接続中...")
tello = Tello()
tello.connect(wait_for_state=False)
time.sleep(1)

try:
    battery = tello.send_read_command("battery?")
    print(f"接続成功！バッテリー: {battery}%")
except:
    print("接続成功！")

print("正方形を描きます")

# 飛行
tello.takeoff()
time.sleep(2)

tello.move_forward(WIDTH)
time.sleep(0.5)
tello.rotate_clockwise(TURN_ANGLE)
time.sleep(0.5)

tello.move_forward(HEIGHT)
time.sleep(0.5)
tello.rotate_clockwise(TURN_ANGLE)
time.sleep(0.5)

tello.move_forward(WIDTH)
time.sleep(0.5)
tello.rotate_clockwise(TURN_ANGLE)
time.sleep(0.5)

tello.move_forward(HEIGHT)
time.sleep(0.5)
tello.rotate_clockwise(TURN_ANGLE)
time.sleep(0.5)

tello.land()

tello.end()
print("終了しました")
