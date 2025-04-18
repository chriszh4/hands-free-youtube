import cv2
import mediapipe as mp
import time
import pyautogui

from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizer
from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizerOptions
from mediapipe.tasks.python.vision import RunningMode

from gestures import GestureStates

gesture_states = GestureStates()

print("Loading gesture recognizer...")
# Load the recognizer model
options = GestureRecognizerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=RunningMode.VIDEO
)

recognizer = GestureRecognizer.create_from_options(options)
recognizer_cw = GestureRecognizer.create_from_options(options)

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # First check for faces
    gesture_states.detect_faces(frame)

    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Rotate image 90 degrees to the right
    img_rgb_rotate_cw = cv2.rotate(img_rgb, cv2.ROTATE_90_CLOCKWISE)

    # Send the frame into the recognizer
    timestamp = int(time.time() * 1000)
    result = recognizer.recognize_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb), timestamp)
    
    if result.gestures:
        # Assume one gesture for now
        gesture_name = result.gestures[0][0].category_name.lower()
        gesture_states.update_gesture(gesture_name, True)

    result_cw = recognizer_cw.recognize_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb_rotate_cw), timestamp)
    
    if result_cw.gestures:
        # Assume one gesture for now
        gesture_name = result_cw.gestures[0][0].category_name.lower()
        if gesture_name == "thumb_up":
            gesture_name = "thumb_right"
        elif gesture_name == "thumb_down":
            gesture_name = "thumb_left"
        gesture_states.update_gesture(gesture_name, True)

    # Show the video feed (for debugging)
    cv2.imshow('Hands Free Youtube Stream', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()