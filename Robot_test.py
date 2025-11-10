import time
from xarm.wrapper import XArmAPI

################初期設定################

arm = XArmAPI("192.168.1.199")
arm.motion_enable(enable=True)   # モーション有効化
arm.set_mode(0)                  # ポジションモード
arm.set_state(0)                 # 状態を「動作準備OK」に

speed = 100

#######################################

def CheckIfNewPositionInWorkspace(x, y, z):
    if x > 680 or x < 300:
        return False
    if y < -330 or y > 420:
        return False
    if z < 94 or z > 550:
        return False
    return True


def MoveTo(x, y, z):
    if CheckIfNewPositionInWorkspace(x, y, z):
        print(f"➡ Moving to ({x}, {y}, {z})")
        arm.set_position(x, y, z, speed=speed, wait=True)
    else:
        print("⚠️ Position is out of workspace")


def main():
    # 初期位置
    x, y, z = 500, -100, 200

    # 1. 初期位置へ
    MoveTo(x, y, z)
    time.sleep(1)

    # 2. Z軸を上へ
    z += 100
    MoveTo(x, y, z)
    time.sleep(1)

    # 3. Y軸を右へ
    y += 100
    MoveTo(x, y, z)
    time.sleep(1)

    # 4. Z軸を下へ
    z -= 100
    MoveTo(x, y, z)
    time.sleep(1)

    # 5. X軸を奥へ
    x -= 100
    MoveTo(x, y, z)
    time.sleep(1)

    print("✅ Sequence completed.")


if __name__ == "__main__":
    try:
        main()
    finally:
        arm.disconnect()
        print("🔌 Disconnected from xArm")
