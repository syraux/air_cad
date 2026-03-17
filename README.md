# ✋ Air-CAD

**A hand-gesture-driven 3D CAD prototyping tool that runs in your webcam feed.**

Air-CAD lets you select, move, and manipulate 3D wireframe objects in real time using just your hands — no mouse, no touchscreen, no controller. Powered by MediaPipe hand tracking and OpenCV rendering.

---

## Demo

| Gesture | Action |
|---|---|
| ✌️ Pinch (thumb + index close together) | Select & drag objects |
| ✋ Open palm | Release / idle |
| `c` key | Spawn a new cube |
| `s` key | Export scene to `.obj` file |
| `x` key | Clear the scene |
| `q` key | Quit |

---

## How It Works

The pipeline has five main stages:

```
Webcam → Perception → Gesture Engine → Intent Manager → Visualizer
                                                      ↓
                                               Scene Graph (3D Objects)
```

1. **Perception** (`perception.py`) — Captures each frame and runs MediaPipe's `HandLandmarker` to extract 21 3D hand landmarks per frame.
2. **Gesture Engine** (`gestures.py`) — Analyses landmark positions to classify the current gesture (`PINCH`, `OPEN`, or `NONE`) using Euclidean distance between thumb tip and index tip.
3. **Intent Manager** (`intent.py`) — A state machine (`IDLE → SELECTING → DRAGGING`) that maps gestures + hand position to meaningful actions like selecting or dragging an object.
4. **Geometry** (`geometry.py`) — Defines `Primitive` base class, `Cube` and `Cylinder` subclasses, and a `SceneGraph` that holds all objects. Each object stores position, rotation, and scale, and can produce its own model matrix.
5. **Visualizer** (`visualization.py`) — Projects 3D wireframes onto the 2D camera frame using a perspective projection matrix. Renders object edges, selection highlights, and a status HUD.

Export (`export.py`) can dump the entire scene to a `.obj` file using line primitives.

---

## Project Structure

```
air-cad/
├── main.py              # Entry point — main loop
├── perception.py        # MediaPipe hand tracking
├── gestures.py          # Gesture classification
├── intent.py            # State machine & object interaction
├── geometry.py          # 3D primitives & scene graph
├── visualization.py     # 3D→2D projection & OpenCV rendering
├── export.py            # OBJ file exporter
├── utils.py             # Math helpers (projection matrix, distance)
├── hand_landmarker.task # MediaPipe model file (required)
└── requirements.txt     # Python dependencies
```

---

## Installation

### Prerequisites

- Python 3.9+
- A webcam

### Setup

```bash
# 1. Clone / download the project
git clone <your-repo-url>
cd air-cad

# 2. Install dependencies
pip install -r requirements.txt

# 3. Make sure hand_landmarker.task is in the project root
#    Download from: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker

# 4. Run
python main.py
```

### Dependencies

```
opencv-python
mediapipe
numpy
```

---

## Usage

Once running, a window opens showing your webcam feed with a wireframe cube rendered in the scene.

- **Pinch** your thumb and index finger together near an object to grab it
- **Move your hand** while pinching to drag it around
- **Open your hand** to release
- Press **`c`** to spawn additional cubes at random positions
- Press **`s`** to save the current scene as `air_cad_output.obj`
- Press **`x`** to wipe the scene
- Press **`q`** to quit

The HUD in the top bar shows live FPS, detected gesture, and current interaction state.

---

## Architecture Notes

### Coordinate System

Objects live in a right-handed 3D world space. The camera is placed at `z = -5` looking toward the origin. Screen drag deltas are mapped to world-space movement with a `0.01` scale factor (Y-axis is flipped to match screen conventions).

### Hit Testing

Object selection uses a simple screen-space proximity check — the pinch center is compared against the projected 2D position of each object's origin. Closest object within 50px wins. This is a heuristic; true raycasting would unproject the screen point.

### Rotation / Scale

The `Primitive` base class supports full TRS transforms (Translation × Rotation × Scale). Rotation and non-uniform scaling are not yet exposed via gestures in this prototype — they're ready to be wired up.

---

## Extending the Project

| Feature | Where to add it |
|---|---|
| New gesture (e.g. two-finger rotate) | `gestures.py` → `detect_gesture()` |
| New primitive (e.g. sphere) | `geometry.py` → subclass `Primitive` |
| Rotate / scale via gesture | `intent.py` → new states + `geometry.py` transforms |
| Better hit testing | `intent.py` → `_raycast()` |
| Draw hand skeleton overlay | `perception.py` → `draw_landmarks()` |
| Export to other formats (STL, glTF) | `export.py` |

---

## Known Limitations

- Single hand only (`num_hands=1`)
- Translation only — no gesture-driven rotation or scale yet
- Screen-to-world mapping is a linear approximation (no true unprojection)
- OBJ export uses line primitives (`l`), not face-based meshes
- No undo / redo

---

## License

MIT — do whatever you want with it.
