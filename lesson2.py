"""
Telloで角度を入力して角度分回転後、30cm前進するプログラム
（move_forward + rotate_clockwise版）
"""

from djitellopy import Tello
import time

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
angle = int(float(input("角度を入力 (0-360): ")))

print(f"\n角度: {angle}°")
print("ドローンが回転して前進します")

# 飛行
tello.takeoff()
time.sleep(2)

# 入力角度分だけ回転
tello.rotate_clockwise(angle)
time.sleep(0.5)

# 前進
tello.move_forward(30)
time.sleep(1)

tello.land()

tello.end()
print("終了しました")
