"""
Lesson 6: Telloで円に近い軌道を描くプログラム

`curve_xyz_speed`を2回使って、
1) 半円
2) もう半円
を飛行し、開始位置付近に戻ります。
"""

from djitellopy import Tello
import time


def main():
    print("Telloに接続中...")
    tello = Tello()
    tello.connect(wait_for_state=False)
    time.sleep(1)

    try:
        battery = tello.send_read_command("battery?")
        print(f"接続成功。バッテリー: {battery}%")
    except Exception:
        print("バッテリー確認に失敗しました。")

    print("Lesson 6開始: カーブコマンドで円飛行を行います。")

    took_off = False
    try:
        tello.takeoff()
        took_off = True
        time.sleep(2)

        # curve_xyz_speed(x1, y1, z1, x2, y2, z2, speed)
        # x1,y1,z1: 途中で通る点（今の位置からの距離 cm）
        # x2,y2,z2: 最後に着く点（今の位置からの距離 cm）
        # zは高さ（+で上、-で下、0で高さを変えない）
        # このプログラムは z1=0, z2=0 なので、上下せず水平に飛びます。
        # 1回目は円の上半分を飛びます。
        tello.curve_xyz_speed(
            60, 60, 0,   # x1, y1, z1（途中点）
            0, 2 * 60, 0,       # x2, y2, z2（終点）
            20                 # speed（速さ）
        )
        time.sleep(1)

        # 2回目は反対側の半円を飛んで、開始位置付近に戻ります。
        # ここも z1=0, z2=0 なので、高さは変わりません。
        # tello.curve_xyz_speed(
        #     -60, -60, 0,  # x1, y1, z1（途中点）
        #     0, -2 * 60, 0,       # x2, y2, z2（終点）
        #     20                  # speed（速さ）
        # )
        # time.sleep(1)

    except Exception as exc:
        print(f"飛行中にエラーが発生しました: {exc}")
    finally:
        if took_off:
            try:
                tello.land()
            except Exception:
                pass
        tello.end()
        print("処理を終了しました。")


if __name__ == "__main__":
    main()
