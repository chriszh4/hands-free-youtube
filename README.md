# Hands-Free YouTube

We introduce Hands-Free Youtube, a project that enables intuitive, hands-free interaction with YouTube using computer vision (gesture recognition), speech commands, and presence detection via webcam. It combines MediaPipe for gesture recognition, speech recognition for audio commands, and keyboard simulated outputs.

---

## Project Structure

| File                      | Description                                                                                                                                        |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app.py`                  | Main application script that ties together video feed, gesture recognition, face detection, and voice commands. Run this file to start the system. |
| `gestures.py`             | Contains the `GestureStates` class which manages gesture tracking, video playback control, and face detection logic.                               |
| `requirements.txt`        | List of required Python packages to run the application. Install this before launching the code.                                                   |
| `gesture_recognizer.task` | Pre-trained MediaPipe gesture recognition model file. This must be placed in the same directory as `app.py`.                                       |

---

## Setup Instructions

### Requirements

- **OS**: macOS, Windows, or Linux with access to a webcam and microphone.
- **Python**: 3.11.11  
  _(Project is tested with this version — other versions may work but are not guaranteed)_
- **Hardware**: Webcam and microphone.
- **Permissions**: Allow access to camera and microphone. Allow laptop keyboard access from VSCode or other IDE.

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/handsfree-youtube.git
   cd handsfree-youtube
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the gesture recognition model**:

   Download the model file manually and place it in the same directory as `app.py`:

   [Download gesture_recognizer.task](https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/latest/gesture_recognizer.task)

   Or run:

   ```bash
   wget https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/latest/gesture_recognizer.task
   ```

---

5. **Install Youtube Like/Dislike Keyboard Shortcut**:

   Install the following [extension](https://chromewebstore.google.com/detail/youtube-like-dislike-shor/fdkpkpelkkdkjhpacficichkfifijipc?pli=1) for keyboard compatability with liking/disliking Youtube videos.

---

## Supported Gestures and Voice Commands

### Gesture Controls

| Gesture           | Action          |
| ----------------- | --------------- |
| Thumb Up          | Like video      |
| Thumb Down        | Dislike video   |
| Thumb Left        | Rewind 5s       |
| Thumb Right       | Skip forward 5s |
| Face Leaves Frame | Pause video     |
| Face Returns      | Play video      |

> Note: Holding a gesture for a very short period (5 frames by default) is required to trigger the action.

### Voice Commands

| Command Example          | Effect                    |
| ------------------------ | ------------------------- |
| "Pause the video"        | Pauses playback           |
| "Play the video"         | Resumes playback          |
| "Like the video"         | Likes Youtube Video       |
| "Dislike the video"      | Dislikes Youtube Video    |
| "Go forward 10 seconds"  | Skips forward 10 seconds  |
| "Go backward 30 seconds" | Rewinds 30 seconds        |
| "Go forward 2 minutes"   | Skips forward 120 seconds |
| "Go back 1 minute"       | Rewinds 60 seconds        |

> User may say any combinations of Go [forward/backward] [quantity] [seconds/minutes]

---

## Running the Application

Once everything is installed, launch the system:

```bash
python app.py
```
