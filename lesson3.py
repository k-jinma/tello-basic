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
tello.takeoff() # 離陸
time.sleep(2) # 少し待つ

tello.move_forward(WIDTH) # 前進
time.sleep(0.5) # 少し待つ
tello.rotate_clockwise(TURN_ANGLE) # 右回転
time.sleep(0.5) # 少し待つ


# プログラムを完成させよう




tello.land() # 着陸

tello.end() # 接続終了
print("終了しました")
