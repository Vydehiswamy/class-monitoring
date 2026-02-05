import cv2

def open_camera(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError("Camera not accessible")
    return cap

def close_camera(cap):
    cap.release()
    cv2.destroyAllWindows()
