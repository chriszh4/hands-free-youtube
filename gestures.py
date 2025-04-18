import cv2
import time
import pyautogui
import threading

class Gesture:
    def __init__(self, key, callback):
        self.timestamp = None
        self.key = key
        self.callback = callback
        self.activation_counter = 0

class GestureStates:
    def __init__(self):
        self.activation_threshold = 5 # Number of positives in a row before activating
        self.cooldown = 2 #in seconds
        self.in_frame = False
        self.video_playing = False
        self.last_in_frame_update = None
        self.frame_confidence = 0
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
        self.lock = threading.Lock()
    
    def update_gesture(self, gesture_name, active):
        with self.lock:
            if gesture_name in self.gestures:
                gesture = self.gestures[gesture_name]
                # Check if enough time has passed since the last update
                if gesture.timestamp is None or (time.time() - gesture.timestamp) > self.cooldown:
                    gesture.activation_counter += 1 
                    # Clear all other counts
                    for g in self.gestures.values():
                        if g.key != gesture.key:
                            g.activation_counter = 0

                    # Check if the gesture has been activated
                    if gesture.activation_counter >= self.activation_threshold:
                        print(f"Gesture {gesture_name} {'activated' if active else 'deactivated'} at {gesture.timestamp}")
                        gesture.activation_counter = 0
                        gesture.timestamp = time.time()
                        gesture.callback()

    def detect_faces(self, vid):
        # TODO: add time period before toggling (for example gesture blocks face and toggles right now)
        # TODO: filter for sizes of faces
        # If updated recently, return early to prevent jitter
        with self.lock:
            if self.last_in_frame_update and (time.time() - self.last_in_frame_update) < self.cooldown:
                return
            gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
            faces = self.face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
            for (x, y, w, h) in faces:
                cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)

            if self.in_frame != (len(faces) > 0):
                # Kind of convoluted but positive values are confidence for in frame, negative for out of frame
                if len(faces)> 0:
                    self.frame_confidence = max(self.frame_confidence + 1, 1)
                else:
                    self.frame_confidence = min(self.frame_confidence - 1, -1)
                if abs(self.frame_confidence) >= self.activation_threshold:
                    self.in_frame = len(faces) > 0
                    self.last_in_frame_update = time.time()
                    if self.in_frame:
                        print("Face detected!")
                        if not self.video_playing:
                            self.video_playing = True
                            pyautogui.press("k")
                    else:
                        print("Face not detected!")
                        if self.video_playing:
                            self.video_playing = False
                            pyautogui.press("k")
        
    def play_video(self):
        with self.lock:
            if not self.video_playing:
                self.video_playing = True
                pyautogui.press("k")
    
    def pause_video(self):
        with self.lock:
            if self.video_playing:
                self.video_playing = False
                pyautogui.press("k")

    def like_video(self):
        with self.lock:
            pyautogui.hotkey('shift', '=')

    def dislike_video(self):
        with self.lock:
            pyautogui.hotkey('shift', '-')