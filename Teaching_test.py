from xarm.wrapper import XArmAPI
import keyboard, time, csv, matplotlib.pyplot as plt

arm = XArmAPI('192.168.1.199')
arm.connect()

# --- 安全初期化 ---
arm.clean_error()
arm.clean_warn()
time.sleep(0.3)

# Teachモードで動かすためにサーボを無効化
arm.motion_enable(False)
time.sleep(0.3)

arm.motion_enable(True)
arm.set_mode(2)
arm.set_state(0)


print("=== Teachモード開始 ===")
print("手でアームを動かしてください。")
print("Enterキー：現在位置を記録 / Escキー：終了")

positions = []
while True:
    if keyboard.is_pressed('enter'):
        ret = arm.get_position(is_radian=False)
        if isinstance(ret, tuple):
            code, pos = ret
        else:
            pos = ret
        positions.append(pos)
        print(f"記録 {len(positions)}: x={pos[0]:.1f}, y={pos[1]:.1f}, z={pos[2]:.1f}")
        time.sleep(0.5)
    elif keyboard.is_pressed('esc'):
        print("記録終了。")
        break

filename = 'feeding_motion.csv'
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(positions)
print(f"合計 {len(positions)} ポイントを保存しました：{filename}")

# --- 可視化 ---
if positions:
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    zs = [p[2] for p in positions]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(xs, ys, zs, marker='o')
    plt.show()

# --- 再生 ---
print("=== PlayBackモードで再生 ===")
arm.motion_enable(True)
arm.clean_error()
arm.clean_warn()
arm.set_mode(0)
arm.set_state(0)
for pos in positions:
    x, y, z, roll, pitch, yaw = pos
    arm.set_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw, speed=50, wait=True)

arm.disconnect()
print("完了。")
