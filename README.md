# Telloドローン基本動作ガイド

## 概要

このドキュメントでは、PythonでTelloドローンを操作するための基本的な関数と使い方を説明します。

## セットアップ

### 1. 仮想環境の作成（推奨）

プロジェクト専用の仮想環境を作成することで、依存関係を分離できます。

#### Windows (コマンドプロンプト)

```bash
# プロジェクトディレクトリに移動
cd d:\tello-basic

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
venv\Scripts\activate
```

#### Windows (PowerShell)

```powershell
# プロジェクトディレクトリに移動
cd d:\tello-basic

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
# プロジェクトディレクトリに移動
cd /path/to/tello-basic

# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate
```

### 2. 必要なライブラリのインストール

仮想環境を有効化した状態で、以下のコマンドを実行します。

```bash
# requirements.txtからインストール（推奨）
pip install -r requirements.txt
```

または個別にインストール：

```bash
pip install djitellopy
pip install opencv-python  # カメラ機能を使用する場合
```

### 3. 仮想環境の終了

作業が終わったら、以下のコマンドで仮想環境を終了できます。

```bash
deactivate
```

### 4. Telloとの接続

1. Telloの電源を入れる
2. PCのWi-FiでTelloのネットワーク（TELLO-XXXXXX）に接続する
3. Pythonプログラムを実行する

---

## 基本関数リファレンス

### 接続・切断

| 関数 | 説明 | 使用例 |
|------|------|--------|
| `Tello()` | Telloオブジェクトを作成 | `tello = Tello()` |
| `connect()` | Telloに接続 | `tello.connect()` |
| `end()` | 接続を終了 | `tello.end()` |

```python
from djitellopy import Tello

tello = Tello()
tello.connect()
print(f"バッテリー: {tello.get_battery()}%")
tello.end()
```

---

### 離陸・着陸

| 関数 | 説明 | 使用例 |
|------|------|--------|
| `takeoff()` | 離陸（約80cm上昇） | `tello.takeoff()` |
| `land()` | 着陸 | `tello.land()` |
| `emergency()` | 緊急停止（モーター即時停止） | `tello.emergency()` |

```python
tello.takeoff()
time.sleep(3)
tello.land()
```

---

### 移動

#### 基本移動（距離指定）

| 関数 | 説明 | 引数 |
|------|------|------|
| `move_forward(x)` | 前進 | x: 距離（20-500cm） |
| `move_back(x)` | 後退 | x: 距離（20-500cm） |
| `move_left(x)` | 左移動 | x: 距離（20-500cm） |
| `move_right(x)` | 右移動 | x: 距離（20-500cm） |
| `move_up(x)` | 上昇 | x: 距離（20-500cm） |
| `move_down(x)` | 下降 | x: 距離（20-500cm） |

```python
tello.takeoff()
tello.move_forward(50)   # 50cm前進
tello.move_up(30)        # 30cm上昇
tello.move_left(40)      # 40cm左移動
tello.land()
```

#### 座標指定移動

| 関数 | 説明 | 引数 |
|------|------|------|
| `go_xyz_speed(x, y, z, speed)` | 指定座標へ移動 | x, y, z: 距離（-500~500cm）, speed: 速度（10-100cm/s） |

```python
# 前方50cm、右30cm、上20cmの位置へ速度50cm/sで移動
tello.go_xyz_speed(50, 30, 20, 50)
```

---

### 回転

| 関数 | 説明 | 引数 |
|------|------|------|
| `rotate_clockwise(x)` | 時計回りに回転 | x: 角度（1-360度） |
| `rotate_counter_clockwise(x)` | 反時計回りに回転 | x: 角度（1-360度） |

```python
tello.takeoff()
tello.rotate_clockwise(90)           # 右に90度回転
tello.rotate_counter_clockwise(180)  # 左に180度回転
tello.land()
```

---

### フリップ（宙返り）

**注意**: バッテリー残量50%以上必要

| 関数 | 説明 |
|------|------|
| `flip_forward()` | 前方フリップ |
| `flip_back()` | 後方フリップ |
| `flip_left()` | 左フリップ |
| `flip_right()` | 右フリップ |

```python
if tello.get_battery() >= 50:
    tello.takeoff()
    tello.flip_forward()
    tello.land()
```

---

### RCコントロール（連続制御）

リアルタイムでの連続制御に使用します。

| 関数 | 説明 |
|------|------|
| `send_rc_control(left_right, forward_backward, up_down, yaw)` | RC制御コマンド送信 |

**引数の範囲**: -100 ～ 100

| 引数 | 正の値 | 負の値 |
|------|--------|--------|
| left_right | 右移動 | 左移動 |
| forward_backward | 前進 | 後退 |
| up_down | 上昇 | 下降 |
| yaw | 時計回り回転 | 反時計回り回転 |

```python
tello.takeoff()

# 前進（50%パワー）で2秒間
tello.send_rc_control(0, 50, 0, 0)
time.sleep(2)

# 停止
tello.send_rc_control(0, 0, 0, 0)

# 右回転しながら上昇
tello.send_rc_control(0, 0, 30, 50)
time.sleep(2)

tello.send_rc_control(0, 0, 0, 0)
tello.land()
```

---

### 状態取得

| 関数 | 説明 | 戻り値 |
|------|------|--------|
| `get_battery()` | バッテリー残量 | 0-100 (%) |
| `get_temperature()` | 温度 | 温度 (°C) |
| `get_height()` | 高度 | 高さ (cm) |
| `get_barometer()` | 気圧高度 | 高さ (cm) |
| `get_flight_time()` | 飛行時間 | 時間 (秒) |
| `get_speed_x()` | X軸速度 | 速度 (cm/s) |
| `get_speed_y()` | Y軸速度 | 速度 (cm/s) |
| `get_speed_z()` | Z軸速度 | 速度 (cm/s) |
| `get_acceleration_x()` | X軸加速度 | 加速度 (cm/s²) |
| `get_acceleration_y()` | Y軸加速度 | 加速度 (cm/s²) |
| `get_acceleration_z()` | Z軸加速度 | 加速度 (cm/s²) |
| `get_pitch()` | ピッチ角 | 角度 (度) |
| `get_roll()` | ロール角 | 角度 (度) |
| `get_yaw()` | ヨー角 | 角度 (度) |

```python
print(f"バッテリー: {tello.get_battery()}%")
print(f"高度: {tello.get_height()}cm")
print(f"温度: {tello.get_temperature()}°C")
```

---

### カメラ・ビデオ

| 関数 | 説明 |
|------|------|
| `streamon()` | ビデオストリーム開始 |
| `streamoff()` | ビデオストリーム停止 |
| `get_frame_read()` | フレームリーダーを取得 |

```python
import cv2

tello.streamon()

while True:
    frame = tello.get_frame_read().frame
    cv2.imshow("Tello Camera", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.streamoff()
cv2.destroyAllWindows()
```

---

### 速度設定

| 関数 | 説明 | 引数 |
|------|------|------|
| `set_speed(x)` | 移動速度を設定 | x: 速度（10-100 cm/s） |

```python
tello.set_speed(50)  # 50cm/sに設定
```

---

## カーブ飛行

| 関数 | 説明 |
|------|------|
| `curve_xyz_speed(x1, y1, z1, x2, y2, z2, speed)` | カーブを描いて飛行 |

```python
# 曲線を描いて飛行
# (x1, y1, z1): 中間点, (x2, y2, z2): 終点
tello.curve_xyz_speed(50, 50, 0, 100, 0, 0, 30)
```

---

## 安全に関する注意事項

1. **飛行前の確認**
   - バッテリー残量を確認（20%以下は飛行を避ける）
   - 周囲に障害物がないか確認
   - 十分な広さのある場所で飛行

2. **緊急時の対応**
   - `emergency()` で即時モーター停止
   - `land()` で安全に着陸

3. **プログラムの構造**
   ```python
   try:
       tello.takeoff()
       # 飛行処理
   except Exception as e:
       print(f"エラー: {e}")
       tello.land()
   finally:
       tello.end()
   ```

---

## サンプルコード：四角形飛行

```python
from djitellopy import Tello
import time

tello = Tello()
tello.connect()

try:
    tello.takeoff()
    time.sleep(2)
    
    # 四角形を描く
    for _ in range(4):
        tello.move_forward(50)
        time.sleep(1)
        tello.rotate_clockwise(90)
        time.sleep(1)
    
    tello.land()

except Exception as e:
    print(f"エラー: {e}")
    tello.land()

finally:
    tello.end()
```

---

## トラブルシューティング

| 問題 | 解決方法 |
|------|----------|
| 接続できない | TelloのWi-Fiに接続しているか確認 |
| 動作が遅い | バッテリー残量を確認、充電する |
| コマンドが無視される | 最小移動距離（20cm）以上を指定する |
| フリップできない | バッテリー残量50%以上必要 |
| ビデオが表示されない | OpenCVがインストールされているか確認 |

---

## 参考リンク

- [djitellopy GitHub](https://github.com/damiafuentes/DJITelloPy)
- [Tello SDK Documentation](https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf)
