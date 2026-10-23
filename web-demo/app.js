const video = document.querySelector("#video");
const overlay = document.querySelector("#overlay");
const overlayContext = overlay.getContext("2d");
const startButton = document.querySelector("#start-button");
const status = document.querySelector("#status");
const gestureLabel = document.querySelector("#gesture");
const cameraMessage = document.querySelector("#camera-message");
const virtualScreen = document.querySelector("#virtual-screen");
const cursor = document.querySelector("#cursor");
const clickIndicator = document.querySelector("#click-indicator");

let camera;
let lastGesture = "";
let clickTimer;

function distance(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

function setGesture(label) {
  if (label === lastGesture) return;
  lastGesture = label;
  gestureLabel.textContent = label;
}

function showClick() {
  clickIndicator.style.display = "block";
  clearTimeout(clickTimer);
  clickTimer = setTimeout(() => { clickIndicator.style.display = "none"; }, 350);
}

function onResults(results) {
  overlay.width = video.videoWidth;
  overlay.height = video.videoHeight;
  overlayContext.save();
  overlayContext.clearRect(0, 0, overlay.width, overlay.height);

  if (!results.multiHandLandmarks?.length) {
    setGesture("Show your hand");
    cameraMessage.textContent = "Show your hand";
    cameraMessage.hidden = false;
    overlayContext.restore();
    return;
  }

  cameraMessage.hidden = true;
  const landmarks = results.multiHandLandmarks[0];
  drawConnectors(overlayContext, landmarks, HAND_CONNECTIONS, { color: "#9bb0ff", lineWidth: 3 });
  drawLandmarks(overlayContext, landmarks, { color: "#ffffff", lineWidth: 1, radius: 3 });

  const index = landmarks[8];
  const middle = landmarks[12];
  const ring = landmarks[16];
  const indexUp = index.y < landmarks[6].y;
  const middleUp = middle.y < landmarks[10].y;
  const ringUp = ring.y < landmarks[14].y;
  const fingertipsClose = distance(index, middle) < 0.07;
  const ringClose = distance(index, ring) < 0.07;
  const screenBounds = virtualScreen.getBoundingClientRect();
  const x = Math.max(8, Math.min(screenBounds.width - 26, (1 - index.x) * screenBounds.width - 10));
  const y = Math.max(8, Math.min(screenBounds.height - 30, index.y * screenBounds.height - 10));
  cursor.style.left = `${x}px`;
  cursor.style.top = `${y}px`;
  clickIndicator.style.left = `${x}px`;
  clickIndicator.style.top = `${y}px`;

  if (indexUp && middleUp && ringUp && ringClose) {
    setGesture("Right-click");
    showClick();
  } else if (indexUp && middleUp && fingertipsClose) {
    setGesture("Left-click");
    showClick();
  } else if (indexUp && middleUp) {
    setGesture("Scroll");
  } else if (indexUp) {
    setGesture("Move");
  } else {
    setGesture("Ready");
  }

  overlayContext.restore();
}

async function startCamera() {
  startButton.disabled = true;
  status.textContent = "Requesting camera access...";
  try {
    const hands = new Hands({ locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}` });
    hands.setOptions({ maxNumHands: 1, modelComplexity: 1, minDetectionConfidence: 0.7, minTrackingConfidence: 0.7 });
    hands.onResults(onResults);
    camera = new Camera(video, {
      onFrame: async () => { await hands.send({ image: video }); },
      width: 640,
      height: 480
    });
    await camera.start();
    status.textContent = "Camera active";
    startButton.textContent = "Camera running";
  } catch (error) {
    status.textContent = "Camera could not start. Check browser permissions.";
    startButton.disabled = false;
    console.error(error);
  }
}

startButton.addEventListener("click", startCamera);
