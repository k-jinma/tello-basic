"""
Telloで学ぶ三角関数
ドローンの動きで sin, cos を体験的に理解する教育プログラム

対象: 中学生〜高校生
"""

from djitellopy import Tello
import time
import math

# === 安全設定 ===
MOVE_DISTANCE = 30      # 基本移動距離 (cm)
FLIGHT_SPEED = 20       # 飛行速度 (cm/s)
MIN_DISTANCE = 20       # Telloの最小移動距離


def connect_tello():
    """Telloに接続"""
    print("\nTelloに接続中...")
    tello = Tello()
    tello.connect(wait_for_state=False)
    time.sleep(1)
    
    try:
        battery = tello.send_read_command("battery?")
        print(f"接続成功！バッテリー: {battery}%")
    except:
        print("接続成功！")
    
    return tello


def lesson_1_angle_direction(tello):
    """
    レッスン1: 角度と方向
    入力した角度の方向にドローンが移動する
    """
    print("\n" + "=" * 50)
    print("【レッスン1】角度と方向")
    print("=" * 50)
    print("""
    角度の基準:
      0° = 右方向 (→)
     90° = 前方向 (↑)
    180° = 左方向 (←)
    270° = 後方向 (↓)
    
         90°(前)
           ↑
           │
    180° ←─┼─→ 0°
           │
           ↓
         270°(後)
    """)
    
    input("離陸します。Enterキーを押してください...")
    tello.takeoff()
    time.sleep(2)
    
    while True:
        try:
            angle_input = input("\n角度を入力 (0-360, qで終了): ").strip()
            if angle_input.lower() == 'q':
                break
            
            angle = float(angle_input)
            
            # 角度からx, y成分を計算
            rad = math.radians(angle)
            x = MOVE_DISTANCE * math.cos(rad)  # 左右方向
            y = MOVE_DISTANCE * math.sin(rad)  # 前後方向
            
            print(f"\n【計算結果】")
            print(f"  角度: {angle}°")
            print(f"  cos({angle}°) = {math.cos(rad):.3f}")
            print(f"  sin({angle}°) = {math.sin(rad):.3f}")
            print(f"  右方向(x): {MOVE_DISTANCE} × cos({angle}°) = {x:.1f} cm")
            print(f"  前方向(y): {MOVE_DISTANCE} × sin({angle}°) = {y:.1f} cm")
            
            # 移動（最小距離未満の成分は0にする）
            x_move = int(x) if abs(x) >= MIN_DISTANCE else 0
            y_move = int(y) if abs(y) >= MIN_DISTANCE else 0
            
            if x_move == 0 and y_move == 0:
                print("移動距離が小さすぎます（最小20cm）")
                continue
            
            print(f"\n  → ドローンが移動します...")
            tello.go_xyz_speed(y_move, x_move, 0, FLIGHT_SPEED)
            time.sleep(1)
            
            # 元の位置に戻る
            print("  → 元の位置に戻ります...")
            tello.go_xyz_speed(-y_move, -x_move, 0, FLIGHT_SPEED)
            time.sleep(1)
            
        except ValueError:
            print("数値を入力してください")
        except Exception as e:
            print(f"エラー: {e}")
    
    tello.land()
    print("\nレッスン1終了")


def lesson_2_triangle(tello):
    """
    レッスン2: 正三角形を描く
    内角60°、外角120°を使用
    """
    print("\n" + "=" * 50)
    print("【レッスン2】正三角形を描く")
    print("=" * 50)
    print("""
    正三角形の性質:
    - 内角: 60°
    - 外角: 120° (180° - 60°)
    
    ドローンの動き:
    1. 前進 → 2. 右に120°回転 → 3. 前進 → ...
    
        ╱╲
       ╱  ╲
      ╱ 60°╲
     ╱──────╲
    """)
    
    input("離陸して正三角形を描きます。Enterキーを押してください...")
    tello.takeoff()
    time.sleep(2)
    
    side_length = MOVE_DISTANCE
    turn_angle = 120  # 外角
    
    print(f"\n1辺の長さ: {side_length}cm")
    print(f"回転角度（外角）: {turn_angle}°")
    
    for i in range(3):
        print(f"\n辺 {i+1}/3: 前進 {side_length}cm")
        tello.move_forward(side_length)
        time.sleep(0.5)
        
        print(f"回転: 右に {turn_angle}°")
        tello.rotate_clockwise(turn_angle)
        time.sleep(0.5)
    
    print("\n正三角形完成！")
    tello.land()
    print("レッスン2終了")


def lesson_3_square(tello):
    """
    レッスン3: 正方形を描く
    内角90°を使用
    """
    print("\n" + "=" * 50)
    print("【レッスン3】正方形を描く")
    print("=" * 50)
    print("""
    正方形の性質:
    - 内角: 90°
    - 外角: 90° (180° - 90°)
    
    ドローンの動き:
    1. 前進 → 2. 右に90°回転 → 3. 前進 → ...
    
     ┌────┐
     │    │
     │ 90°│
     └────┘
    """)
    
    input("離陸して正方形を描きます。Enterキーを押してください...")
    tello.takeoff()
    time.sleep(2)
    
    side_length = MOVE_DISTANCE
    turn_angle = 90
    
    print(f"\n1辺の長さ: {side_length}cm")
    print(f"回転角度: {turn_angle}°")
    
    for i in range(4):
        print(f"\n辺 {i+1}/4: 前進 {side_length}cm")
        tello.move_forward(side_length)
        time.sleep(0.5)
        
        print(f"回転: 右に {turn_angle}°")
        tello.rotate_clockwise(turn_angle)
        time.sleep(0.5)
    
    print("\n正方形完成！")
    tello.land()
    print("レッスン3終了")


def main():
    print("=" * 50)
    print("🎓 Telloで学ぶ三角関数")
    print("=" * 50)
    print("ドローンの動きで sin, cos を体験しよう！")
    
    tello = connect_tello()
    
    try:
        while True:
            print("\n" + "=" * 50)
            print("【レッスン選択】")
            print("=" * 50)
            print("1: 角度と方向 (sin/cosの基本)")
            print("2: 正三角形を描く (外角120°)")
            print("3: 正方形を描く (外角90°)")
            print("0: 終了")
            
            choice = input("\n選択: ").strip()
            
            if choice == "1":
                lesson_1_angle_direction(tello)
            elif choice == "2":
                lesson_2_triangle(tello)
            elif choice == "3":
                lesson_3_square(tello)
            elif choice == "0":
                print("プログラムを終了します")
                break
            else:
                print("1-3 または 0 を入力してください")
    
    except KeyboardInterrupt:
        print("\n中断されました")
        try:
            tello.land()
        except:
            pass
    
    except Exception as e:
        print(f"エラー: {e}")
        try:
            tello.land()
        except:
            pass
    
    finally:
        try:
            tello.end()
        except:
            pass
        print("終了しました")


if __name__ == "__main__":
    main()
