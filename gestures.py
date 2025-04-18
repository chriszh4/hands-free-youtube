import cv2
import mediapipe as mp
import time
import pyautogui

from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizer
from mediapipe.tasks.python.vision.gesture_recognizer import GestureRecognizerOptions
from mediapipe.tasks.python.vision import RunningMode

class Gesture:
    def __init__(self, key, callback):
        self.timestamp = None
        self.key = key
        self.callback = callback

class GestureStates:
    def __init__(self):
        self.cooldown = 3 #in seconds
        self.in_frame = False
        self.last_in_frame_update = None
        self.gestures = {
            'thumb_up': Gesture('thumbs_up', lambda: pyautogui.hotkey('shift', '=')),
            'thumb_down': Gesture('thumbs_down', lambda: pyautogui.hotkey('shift', '-')),
            'thumb_left': Gesture('thumbs_left', lambda: pyautogui.press('left')),
            'thumb_right': Gesture('thumbs_right', lambda: pyautogui.press('right')),
        }
        print("Loading face cascade classifier...")
        self.face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
    
    def update_gesture(self, gesture_name, active):
        # TODO: implement some confidence before activating gesture
        if gesture_name in self.gestures:
            gesture = self.gestures[gesture_name]
            # Check if enough time has passed since the last update
            if gesture.timestamp is None or (time.time() - gesture.timestamp) > self.cooldown:
                gesture.timestamp = time.time()
                print(f"Gesture {gesture_name} {'activated' if active else 'deactivated'} at {gesture.timestamp}")
                gesture.callback()

    def detect_faces(self, vid):
        # TODO: add time period before toggling (for example gesture blocks face and toggles right now)
        # TODO: filter for sizes of faces
        # If updated recently, return early to prevent jitter
        if self.last_in_frame_update and (time.time() - self.last_in_frame_update) < self.cooldown:
            return
        gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
        for (x, y, w, h) in faces:
            cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)

        if self.in_frame != (len(faces) > 0):
            self.in_frame = len(faces) > 0
            self.last_in_frame_update = time.time()
            if self.in_frame:
                print("Face detected!")
            else:
                print("Face not detected!")
            pyautogui.press("k")