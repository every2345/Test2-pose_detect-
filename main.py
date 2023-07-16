import cv2
from cvzone.PoseModule import PoseDetector
import time

# Khởi tạo PoseDetector
detector = PoseDetector()

# Khởi tạo camera laptop
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Khởi tạo thời gian trước đó
previous_time = time.time()

# Khởi tạo biến cảnh báo và thời gian bắt đầu cảnh báo
alert = False
alert_start_time = 0

while True:
    success, img = cap.read()

    # Tìm và vẽ khung chữ nhật bao quanh cơ thể
    img = detector.findPose(img)
    lmlist, bboxInfo = detector.findPosition(img, bboxWithHands=True)

    # Hiển thị độ dài khung chữ nhật bao quanh cơ thể
    if bboxInfo:
        # Lấy thông tin về tọa độ của khung chữ nhật
        x, y, w, h = bboxInfo["bbox"]

        # Tính độ dài của cạnh bên ngang và hiển thị
        length_horizontal = w
        cv2.putText(img, f"Be Rong: {length_horizontal}px", (x, y - 30),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

        # Tính độ dài của cạnh bên dọc và hiển thị
        length_vertical = h
        cv2.putText(img, f"Chieu Cao: {length_vertical}px", (x, y - 10),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

        # Tính thời gian hiện tại
        current_time = time.time()

        # Tính thời gian thay đổi của giá trị horizon và vertical
        delta_time = current_time - previous_time

        # Hiển thị thời gian thay đổi
        cv2.putText(img, f"Delta Time: {delta_time:.2f}s", (10, 30),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        # Kiểm tra điều kiện phát hiện té ngã
        if delta_time > 0.065 and length_vertical < length_horizontal:
            if not alert:
                # Bắt đầu cảnh báo
                alert = True
                alert_start_time = current_time
            else:
                # Kiểm tra thời gian cảnh báo
                elapsed_time = current_time - alert_start_time
                if elapsed_time < 5:
                    # In cảnh báo "Phát hiện Té ngã"
                    cv2.putText(img, "Phát hiện Té ngã", (x, y - 50),
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                else:
                    # Kết thúc cảnh báo
                    alert = False

        # Cập nhật thời gian trước đó
        previous_time = current_time

    cv2.imshow("Result", img)
    if cv2.waitKey(1) == ord("q"):
        break

# Giải phóng bộ nhớ và tắt camera
cap.release()
cv2.destroyAllWindows()
