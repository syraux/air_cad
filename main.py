import cv2
import time
import numpy as np
import os

from perception import HandTracker
from gestures import GestureEngine
from intent import IntentManager
from geometry import SceneGraph, Cube, Cylinder
from visualization import Visualizer
from export import export_to_obj


def main():
    # 1. Initialization
    print("Initializing Air-CAD Systems...")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not found.")
        return

    # Set resolution (optional, helps performance)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    tracker = HandTracker(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    gesture_engine = GestureEngine(pinch_threshold=40)
    intent_manager = IntentManager()
    scene = SceneGraph()

    # 2. Setup Scene
    # Add a default cube
    cube1 = Cube("Cube1", position=(0, 0, 0), size=1.0)
    scene.add(cube1)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    visualizer = Visualizer(w, h)

    prev_time = 0
    print("System Ready. 'q' to quit, 's' to save .obj, 'c' to spawn cube.")

    # 3. Main Loop
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Flip frame horizontally for mirror effect (intuitive for UX)
        frame = cv2.flip(frame, 1)

        # --- PERCEPTION ---
        results, landmarks_data = tracker.process_frame(frame)

        # --- GESTURE & INPUT ---
        primary_hand = landmarks_data[0] if landmarks_data else None
        current_gesture = "NONE"
        pinch_pos = None

        if primary_hand:
            current_gesture = gesture_engine.detect_gesture(primary_hand)
            # Calculate pinch center for interaction
            tx, ty = primary_hand[4]['x'], primary_hand[4]['y']
            ix, iy = primary_hand[8]['x'], primary_hand[8]['y']
            pinch_pos = ((tx + ix) / 2, (ty + iy) / 2)

            # Debug Draw Hand
            tracker.draw_landmarks(frame, results)

            # Visual feedback on pinch
            if current_gesture == "PINCH":
                cv2.circle(frame, (int(pinch_pos[0]), int(pinch_pos[1])), 10, (0, 255, 0), 2)

        # --- INTENT & LOGIC ---
        state = intent_manager.update_intent(current_gesture, pinch_pos, scene, visualizer)

        # Keyboard Input (Fallback)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            export_to_obj(scene, "air_cad_output.obj")
        elif key == ord('c'):
            # Spawn random cube
            import random
            offset = [random.uniform(-1, 1) for _ in range(3)]
            new_cube = Cube(f"Cube_{len(scene.objects)}", position=offset)
            new_cube.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            scene.add(new_cube)
        elif key == ord('x'):
            # Clear scene
            scene.objects = []

        # --- VISUALIZATION ---
        visualizer.render_scene(frame, scene)

        # FPS Calculation
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time

        visualizer.draw_ui(frame, current_gesture, state, fps)

        cv2.imshow('Air-CAD Prototype', frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
