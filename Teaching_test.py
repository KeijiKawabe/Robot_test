from xarm.wrapper import XArmAPI
import keyboard
import time
import matplotlib.pyplot as plt

arm = XArmAPI('192.168.1.199')
arm.connect()

# --- Teachモード ---
arm.motion_enable(True)
arm.set_mode(2)     # Teach Mode
arm.set_state(0)

print("=== Teachモード開始 ===")
print("手でアームを動かしてください。")
print("Enterキー：現在位置を記録 / Escキー：終了")

positions = []  # 座標リスト
while True:
    if keyboard.is_pressed('enter'):
        pos = arm.get_position(is_radian=False)  # [x, y, z, roll, pitch, yaw]
        positions.append(pos)
        print(f"記録 {len(positions)}: x={pos[0]:.1f}, y={pos[1]:.1f}, z={pos[2]:.1f}")
        arm.save_record_point()
        time.sleep(0.5)
    elif keyboard.is_pressed('esc'):
        print("記録終了。")
        break

# --- 保存 ---
filename = 'feeding_motion.traj'
arm.save_record_trajectory(filename)
print(f"合計 {len(positions)} ポイントを保存しました：{filename}")

# --- 軌跡の可視化 ---
if positions:
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    zs = [p[2] for p in positions]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(xs, ys, zs, marker='o')

    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('xArm Teaching Trajectory')

    plt.show()

# --- PlayBack ---
print("=== PlayBackモードで再生 ===")
arm.set_mode(4)
arm.set_state(0)
arm.playback_trajectory(filename=filename, wait=True)

arm.disconnect()
print("完了。")
