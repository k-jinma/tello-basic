"""
Telloドローン基本動作テストプログラム
djitellopyライブラリを使用してTelloドローンの基本的な操作をテストします。

【室内飛行用】移動距離・速度を最小限に設定しています。
"""

from djitellopy import Tello
import time

# === 室内飛行用の安全設定 ===
MOVE_DISTANCE = 20      # 移動距離 (cm) - 最小値: 20cm
ROTATE_ANGLE = 45       # 回転角度 (度)
RC_POWER = 20           # RCコントロールのパワー (%) - 低速で安全
FLIGHT_SPEED = 10       # 飛行速度 (cm/s) - 最小値: 10cm/s


def connect_tello():
    """Telloドローンに接続する"""
    print("\nTelloに接続中...")
    print("※ TelloのWi-Fi（TELLO-XXXXXX）に接続していることを確認してください\n")
    
    try:
        tello = Tello()
        
        # 状態パケットを待たずに接続を試みる
        tello.RETRY_COUNT = 3
        tello.connect(wait_for_state=False)
        
        time.sleep(1)  # 接続安定のため少し待つ
        
        # バッテリー確認でコマンドが通るかテスト
        try:
            battery = tello.get_battery()
            print(f"接続成功！バッテリー残量: {battery}%")
        except:
            print("接続成功！（バッテリー情報は取得できませんでした）")
        
        # 室内用に低速設定
        try:
            tello.set_speed(FLIGHT_SPEED)
            print(f"飛行速度を{FLIGHT_SPEED}cm/sに設定しました（室内モード）")
        except:
            print("速度設定をスキップしました")
        
        return tello
    
    except Exception as e:
        print("\n" + "=" * 50)
        print("❌ 接続エラー: Telloに接続できませんでした")
        print("=" * 50)
        print("\n【トラブルシューティング】")
        print("1. Telloの電源が入っているか確認")
        print("   → LEDが点滅していればOK")
        print("")
        print("2. PCがTelloのWi-Fiに接続しているか確認")
        print("   → ネットワーク名: TELLO-XXXXXX")
        print("   → 通常のWi-Fiやイーサネットではなく、")
        print("     TelloのWi-Fiに接続する必要があります")
        print("")
        print("3. ファイアウォールがUDP通信をブロックしていないか確認")
        print("   → ポート 8889, 8890, 11111 を許可")
        print("")
        print("4. Telloを再起動してみる")
        print("   → 電源を切って5秒待ち、再度電源を入れる")
        print("")
        print("5. 他のTello制御アプリが起動していないか確認")
        print("   → Telloアプリなどを終了する")
        print("=" * 50)
        raise


def get_status(tello):
    """ドローンの状態を取得する（コマンドベース）"""
    print("=== ドローン状態 ===")
    
    # send_commandを使用して直接クエリ（状態パケットに依存しない）
    queries = [
        ("battery?", "バッテリー残量", "%"),
        ("temp?", "温度", ""),
        ("height?", "高度", "cm"),
        ("baro?", "気圧", "cm"),
        ("time?", "飛行時間", "s"),
    ]
    
    for cmd, label, unit in queries:
        try:
            response = tello.send_read_command(cmd)
            print(f"{label}: {response}{unit}")
        except Exception as e:
            print(f"{label}: 取得失敗 ({e})")
    
    # 速度は状態パケットからのみ取得可能なので、エラーを許容
    try:
        print(f"速度 (x, y, z): ({tello.get_speed_x()}, {tello.get_speed_y()}, {tello.get_speed_z()}) cm/s")
    except:
        print("速度: 取得失敗（状態パケット未受信）")


def basic_flight_test(tello):
    """基本的な飛行テスト（離陸→ホバリング→着陸）"""
    print("\n=== 基本飛行テスト開始 ===")
    
    # 離陸
    print("離陸します...")
    tello.takeoff()
    time.sleep(3)
    
    # ホバリング中の状態確認
    get_status(tello)
    
    # 着陸
    print("着陸します...")
    tello.land()
    print("基本飛行テスト完了")


def movement_test(tello):
    """移動テスト（前後左右・上下）- 室内用に小さな動作"""
    print("\n=== 移動テスト開始（室内モード） ===")
    print(f"移動距離: {MOVE_DISTANCE}cm")
    
    # 離陸
    tello.takeoff()
    time.sleep(2)
    
    # 上昇
    print(f"上昇 ({MOVE_DISTANCE}cm)...")
    tello.move_up(MOVE_DISTANCE)
    time.sleep(1)
    
    # 前進
    print(f"前進 ({MOVE_DISTANCE}cm)...")
    tello.move_forward(MOVE_DISTANCE)
    time.sleep(1)
    
    # 後退
    print(f"後退 ({MOVE_DISTANCE}cm)...")
    tello.move_back(MOVE_DISTANCE)
    time.sleep(1)
    
    # 右移動
    print(f"右移動 ({MOVE_DISTANCE}cm)...")
    tello.move_right(MOVE_DISTANCE)
    time.sleep(1)
    
    # 左移動
    print(f"左移動 ({MOVE_DISTANCE}cm)...")
    tello.move_left(MOVE_DISTANCE)
    time.sleep(1)
    
    # 下降
    print(f"下降 ({MOVE_DISTANCE}cm)...")
    tello.move_down(MOVE_DISTANCE)
    time.sleep(1)
    
    # 着陸
    tello.land()
    print("移動テスト完了")


def rotation_test(tello):
    """回転テスト - 室内用に小さな角度"""
    print("\n=== 回転テスト開始（室内モード） ===")
    print(f"回転角度: {ROTATE_ANGLE}度")
    
    tello.takeoff()
    time.sleep(2)
    
    # 時計回りに回転
    print(f"時計回りに{ROTATE_ANGLE}度回転...")
    tello.rotate_clockwise(ROTATE_ANGLE)
    time.sleep(1)
    
    # 反時計回りに回転
    print(f"反時計回りに{ROTATE_ANGLE}度回転...")
    tello.rotate_counter_clockwise(ROTATE_ANGLE)
    time.sleep(1)
    
    # 着陸
    tello.land()
    print("回転テスト完了")


def flip_test(tello):
    """フリップ（宙返り）テスト"""
    print("\n=== フリップテスト ===")
    print("⚠️  警告: フリップは室内では危険です！")
    print("⚠️  天井までの高さが2m以上必要です")
    print("※バッテリー残量が50%以上必要です")
    
    confirm = input("本当に実行しますか？ (y/N): ").strip().lower()
    if confirm != 'y':
        print("フリップテストをキャンセルしました")
        return
    
    battery = tello.get_battery()
    if battery < 50:
        print(f"バッテリー残量不足: {battery}%")
        return
    
    tello.takeoff()
    time.sleep(2)
    
    # 前方フリップ
    print("前方フリップ...")
    tello.flip_forward()
    time.sleep(2)
    
    # 着陸
    tello.land()
    print("フリップテスト完了")


def rc_control_test(tello):
    """RCコントロールテスト（ゲームパッド風の操作）- 室内用低速"""
    print("\n=== RCコントロールテスト開始（室内モード） ===")
    print(f"パワー: {RC_POWER}%（低速）")
    
    tello.takeoff()
    time.sleep(2)
    
    # send_rc_control(left_right, forward_backward, up_down, yaw)
    # 値は -100 から 100 の範囲
    
    print(f"前進（{RC_POWER}%パワー）で1秒間...")
    tello.send_rc_control(0, RC_POWER, 0, 0)
    time.sleep(1)
    
    print("停止...")
    tello.send_rc_control(0, 0, 0, 0)
    time.sleep(1)
    
    print(f"後退（{RC_POWER}%パワー）で1秒間...")
    tello.send_rc_control(0, -RC_POWER, 0, 0)
    time.sleep(1)
    
    print("停止...")
    tello.send_rc_control(0, 0, 0, 0)
    time.sleep(1)
    
    # 着陸
    tello.land()
    print("RCコントロールテスト完了")


def video_stream_test(tello):
    """ビデオストリームテスト（OpenCV使用）"""
    print("\n=== ビデオストリームテスト開始 ===")
    
    try:
        import cv2
    except ImportError:
        print("OpenCV (cv2) がインストールされていません")
        print("pip install opencv-python でインストールしてください")
        return
    
    # ストリーム開始
    tello.streamon()
    
    print("カメラ映像を表示中... 'q'キーで終了")
    
    frame_count = 0
    max_frames = 300  # 約10秒間（30fps想定）
    
    while frame_count < max_frames:
        frame = tello.get_frame_read().frame
        
        if frame is not None:
            cv2.imshow("Tello Camera", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    # ストリーム停止
    tello.streamoff()
    cv2.destroyAllWindows()
    print("ビデオストリームテスト完了")


def emergency_stop(tello):
    """緊急停止（モーター即時停止）"""
    print("緊急停止！")
    tello.emergency()


def main():
    """メイン関数"""
    print("=" * 50)
    print("Tello ドローン基本動作テスト【室内モード】")
    print("=" * 50)
    print(f"安全設定: 移動距離={MOVE_DISTANCE}cm, 速度={FLIGHT_SPEED}cm/s")
    print("⚠️  狭い場所での飛行用に動作を制限しています")
    print("=" * 50)
    
    # Telloに接続
    tello = connect_tello()
    
    try:
        # テストメニュー
        while True:
            print("\n=== テストメニュー ===")
            print("1: 状態確認")
            print("2: 基本飛行テスト（離陸→ホバリング→着陸）")
            print("3: 移動テスト（前後左右・上下）")
            print("4: 回転テスト")
            print("5: フリップテスト")
            print("6: RCコントロールテスト")
            print("7: ビデオストリームテスト")
            print("0: 終了")
            print("e: 緊急停止")
            
            choice = input("選択してください: ").strip()
            
            if choice == "1":
                get_status(tello)
            elif choice == "2":
                basic_flight_test(tello)
            elif choice == "3":
                movement_test(tello)
            elif choice == "4":
                rotation_test(tello)
            elif choice == "5":
                flip_test(tello)
            elif choice == "6":
                rc_control_test(tello)
            elif choice == "7":
                video_stream_test(tello)
            elif choice == "0":
                print("プログラムを終了します")
                break
            elif choice.lower() == "e":
                emergency_stop(tello)
                break
            else:
                print("無効な選択です")
    
    except KeyboardInterrupt:
        print("\nプログラムが中断されました")
        try:
            tello.land()
        except:
            pass  # 飛行中でなければエラーになるが無視
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # 飛行中かもしれないので着陸を試みる（エラーは無視）
        try:
            tello.land()
        except:
            pass
    
    finally:
        try:
            tello.end()
        except:
            pass
        print("接続を終了しました")


if __name__ == "__main__":
    main()
