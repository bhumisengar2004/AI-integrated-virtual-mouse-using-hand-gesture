# AI-Integrated Virtual Mouse Using Hand Gestures

Control your computer mouse with hand gestures using a webcam, OpenCV, MediaPipe, and PyAutoGUI.

## Features

- Move the cursor with your index finger.
- Left-click by bringing your index and middle fingertips together.
- Right-click by bringing your index and ring fingertips together while the relevant fingers are raised.
- Scroll by raising your index and middle fingers and moving them vertically apart.
- Display hand landmarks and the active control area in a live camera window.

## Requirements

- Python 3.8 or later
- A working webcam
- Windows, macOS, or Linux
- Permission for Python to access the webcam and control the mouse

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bhumisengar2004/AI-integrated-virtual-mouse-using-hand-gesture.git
   cd AI-integrated-virtual-mouse-using-hand-gesture
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage

Start the application with:

```bash
python main.py
```

A window named **AI Virtual Mouse** will open and show the webcam feed. Place your hand inside the highlighted rectangle and use the gestures below.

| Gesture | Action |
| --- | --- |
| Index finger raised | Move the cursor |
| Index and middle fingers raised, fingertips close | Left-click |
| Index, middle, and ring fingers raised, index and ring fingertips close | Right-click |
| Index and middle fingers raised and apart | Scroll vertically |
| Press `Esc` in the camera window | Exit the application |

## Live Browser Demo

A browser version is included in [`web-demo/`](./web-demo/). It uses the webcam through the browser and displays a virtual cursor and gesture feedback on the page. It does not control the computer's real mouse, because browsers cannot safely generate OS-level mouse input.

To run it locally, serve the repository over HTTP (camera access is blocked from most local `file://` pages):

```bash
python -m http.server 8000
```

Then open [http://localhost:8000/web-demo/](http://localhost:8000/web-demo/) and select **Start camera**. The `web-demo` folder can be deployed directly to Vercel as a static site with no build command.

## Project Structure

```text
.
├── hand_tracking.py   # Hand landmark detection and gesture helpers
├── main.py            # Main virtual mouse application
├── utils.py           # Distance and cursor-smoothing utilities
├── virtual_mouse.py   # Alternative standalone implementation
├── web-demo/           # Static browser demo for Vercel
├── requirements.txt    # Python dependencies
└── README.md
```

## Troubleshooting

### Webcam is not detected

- Make sure the webcam is connected and not being used by another application.
- Check that Python has permission to access the camera.
- If you have multiple cameras, update the camera index in `main.py`:

  ```python
  cap = cv2.VideoCapture(0)
  ```

  Try `1` or another available index instead of `0`.

### Mouse control does not work

- Make sure the application has accessibility or input-control permission where required by your operating system.
- Keep your hand well lit and fully visible to the camera.
- Move your hand inside the highlighted control rectangle.

### Gestures trigger repeatedly

The application includes a short delay after clicking to reduce accidental repeated clicks. Keep your fingertips apart when you are not trying to click.

## Safety

This application can move the cursor and generate mouse clicks. Close the camera window with `Esc` if the mouse behaves unexpectedly, and only run it when you are ready for gesture-based input.

## License

No license has been specified for this project yet.
