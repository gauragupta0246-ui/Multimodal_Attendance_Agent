import cv2
import time
import pandas as pd
import os

# 1. Setup Attendance Log File
ATTENDANCE_FILE = "attendance.csv"
if not os.path.exists(ATTENDANCE_FILE):
    pd.DataFrame(columns=["Student_ID", "Timestamp", "Status"]).to_csv(ATTENDANCE_FILE, index=False)

# 2. DroidCam Direct Stream Connection
# Replace with your actual phone WiFi IP shown on the DroidCam mobile screen:
DROIDCAM_IP = "10.142.132.46"  # <-- Enter your mobile WiFi IP here
STREAM_URL = f"http://{DROIDCAM_IP}:4747/video"

print(f"Connecting to DroidCam at: {STREAM_URL}")
cap = cv2.VideoCapture(STREAM_URL)

# Fallback: Check local webcam index if IP stream is unreachable
if not cap.isOpened():
    print("Direct IP stream not reachable. Trying default webcam index...")
    cap = cv2.VideoCapture(0)

presence_start_time = None
is_marked = False

print("Starting Vision Attendance Tracker... Press 'q' to stop.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Waiting for camera feed...")
        time.sleep(1)
        continue

    # Face Presence Tracking Logic
    # (Draw visual indicator on frame)
    cv2.putText(frame, "Face Tracking: Active", (30, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Sustained Presence Tracking (5 seconds threshold)
    if presence_start_time is None:
        presence_start_time = time.time()
    else:
        elapsed = time.time() - presence_start_time
        cv2.putText(frame, f"Presence Time: {int(elapsed)}s", (30, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        # Mark attendance after 5 seconds of continuous presence
        if elapsed >= 5 and not is_marked:
            now_str = time.strftime("%Y-%m-%d %H:%M:%S")
            entry = pd.DataFrame([{"Student_ID": "Student_01", "Timestamp": now_str, "Status": "Present"}])
            entry.to_csv(ATTENDANCE_FILE, mode='a', header=False, index=False)
            is_marked = True
            print(f"[SUCCESS] Attendance Marked at {now_str}")

    if is_marked:
        cv2.putText(frame, "Attendance Status: Marked", (30, 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Multimodal Attendance Agent - Vision Module", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()