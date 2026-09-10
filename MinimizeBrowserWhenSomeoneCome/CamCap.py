import cv2
import time
import ctypes
import psutil

# 精准最小化 Chrome 浏览器（不影响其他窗口）
def minimize_chrome():
    try:
        # 遍历所有进程找到Chrome窗口
        for proc in psutil.process_iter(['name', 'pid']):
            if 'chrome' in proc.info['name'].lower():
                # 调用Windows API最小化Chrome
                user32 = ctypes.WinDLL('user32', use_last_error=True)
                hwnd = user32.GetForegroundWindow()
                user32.ShowWindow(hwnd, 6)  # 6 = 最小化
                print("Chrome minimized!")
                return
    except Exception as e:
        print("minimize Chrome failed!")

# ================== 运动检测 + 冷却设置 ==================
bg = cv2.createBackgroundSubtractorMOG2(history=200, detectShadows=False)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 冷却时间设置（单位：秒）
COOLDOWN_TIME = 10  
last_triggered_time = 0  # 记录上一次触发时间

trigger_count = 0
TRIGGER_LIMIT = 10  # 连续3帧检测到才触发，防误触

while True:
    ret, frame = cap.read()
    if not ret:
        break

    mask = bg.apply(frame)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    motion_detected = False
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # 物体大小阈值，越大越不容易误触
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            motion_detected = True

    # 核心逻辑：检测到运动 + 不在冷却期 → 执行最小化
    current_time = time.time()
    if motion_detected:
        trigger_count += 1
        # 连续3帧确认移动
        if trigger_count >= TRIGGER_LIMIT:
            # 判断是否在冷却时间内
            if current_time - last_triggered_time > COOLDOWN_TIME:
                minimize_chrome()
                last_triggered_time = current_time  # 更新触发时间
            else:
                # 冷却中，不执行
                remaining = int(COOLDOWN_TIME - (current_time - last_triggered_time))
            trigger_count = 0
    else:
        trigger_count = 0

    # 显示画面
    cv2.imshow("CamCap", frame)

    # ESC 退出
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
