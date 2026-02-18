"""
Telloで角度を入力して任意方向に移動するシンプルプログラム
"""

from djitellopy import Tello
import time
import math

MOVE_DISTANCE = 30

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

# 角度を入力
angle = float(input("角度を入力 (0-360): "))

# 角度からx, y成分を計算
rad = math.radians(angle)
x = int(MOVE_DISTANCE * math.cos(rad))  # 横はどれくらい移動するか
y = int(MOVE_DISTANCE * math.sin(rad))  # 縦はどれくらい移動するか

print(f"\n角度: {angle}°")
print(f"移動: x={x}cm, y={y}cm")

# 飛行
tello.takeoff()
time.sleep(2)
tello.go_xyz_speed(y, x, 0, 20)
time.sleep(1)
tello.land()

tello.end()
print("終了しました")
