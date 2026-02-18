"""
Telloで長方形を描くプログラム
（sin/cosで移動方向を計算、向きは変えない）
"""

from djitellopy import Tello
import time
import math

WIDTH = 40   # 横の長さ (cm)
HEIGHT = 20  # 縦の長さ (cm)
FLIGHT_SPEED = 20  # 飛行速度 (cm/s)

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

print("長方形を描きます")

# 飛行
tello.takeoff()
time.sleep(2)

# 角度と距離を個別に指定して長方形を描く
rad = math.radians(0)
x = int(WIDTH * math.cos(rad))  # 左右方向 cos(0) = 1 右に移動
y = int(WIDTH * math.sin(rad))  # 前後方向 sin(0) = 0 前後には移動しない
tello.go_xyz_speed(y, x, 0, FLIGHT_SPEED)
time.sleep(1)

rad = math.radians(90)
x = int(HEIGHT * math.cos(rad))  # 左右方向 cos(90) = 0 左右には移動しない
y = int(HEIGHT * math.sin(rad))  # 前後方向 sin(90) = 1 前に移動
tello.go_xyz_speed(y, x, 0, FLIGHT_SPEED)
time.sleep(1)

rad = math.radians(180)
x = int(WIDTH * math.cos(rad))  # 左右方向 cos(180) = -1 左に移動
y = int(WIDTH * math.sin(rad))  # 前後方向 sin(180) = 0 前後には移動しない
tello.go_xyz_speed(y, x, 0, FLIGHT_SPEED)
time.sleep(1)

rad = math.radians(270)
x = int(HEIGHT * math.cos(rad))  # 左右方向 cos(270) = 0 左右には移動しない
y = int(HEIGHT * math.sin(rad))  # 前後方向 sin(270) = -1 後ろに移動
tello.go_xyz_speed(y, x, 0, FLIGHT_SPEED)
time.sleep(1)

tello.land()

tello.end()
print("終了しました")
