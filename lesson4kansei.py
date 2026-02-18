"""
Telloで正三角形を描くプログラム
（sin/cosで移動方向を計算、向きは変えない）
"""

from djitellopy import Tello
import time
import math

MOVE_DISTANCE = 30  # 1辺の長さ (cm)
FLIGHT_SPEED = 20   # 飛行速度 (cm/s)

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

print("正三角形を描きます")

# 飛行
tello.takeoff()
time.sleep(2)


rad = math.radians(0)
x = int(MOVE_DISTANCE * math.cos(rad))  # 左右方向
y = int(MOVE_DISTANCE * math.sin(rad))  # 前後方向
tello.go_xyz_speed(y, x, 0, FLIGHT_SPEED)
time.sleep(1)

rad = math.radians(120)
x = int(MOVE_DISTANCE * math.cos(rad))  # 左右方向
y = int(MOVE_DISTANCE * math.sin(rad))  # 前後方向
tello.go_xyz_speed(y, x, 0, FLIGHT_SPEED)
time.sleep(1)

rad = math.radians(240)
x = int(MOVE_DISTANCE * math.cos(rad))  # 左右方向
y = int(MOVE_DISTANCE * math.sin(rad))  # 前後方向
tello.go_xyz_speed(y, x, 0, FLIGHT_SPEED)
time.sleep(1)

tello.land()

tello.end()
print("終了しました")
