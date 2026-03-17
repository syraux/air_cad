import cv2
import numpy as np
from utils import Utils


class Visualizer:
    def __init__(self, width, height, fov=60):
        self.width = width
        self.height = height
        self.view_matrix = np.identity(4)
        # Position camera slightly back
        self.view_matrix[2, 3] = -5.0
        self.proj_matrix = Utils.create_perspective_projection_matrix(fov, width / height, 0.1, 100.0)

    def project_point(self, point_3d):
        return Utils.world_to_screen(point_3d, self.view_matrix, self.proj_matrix, self.width, self.height)

    def render_scene(self, frame, scene_graph):
        """
        Draws wireframe objects onto the frame.
        """
        for obj in scene_graph.get_objects():
            model_matrix = obj.get_model_matrix()
            verts = obj.get_vertices()

            # Transform vertices to World Space
            transformed_verts = []
            for v in verts:
                # Homogeneous coord
                vh = np.array([v[0], v[1], v[2], 1.0])
                vw = np.dot(model_matrix, vh)
                transformed_verts.append(vw[:3])

            # Project to Screen
            screen_points = []
            for v in transformed_verts:
                sp = self.project_point(v)
                screen_points.append(sp)

            # Draw Edges
            color = (0, 0, 255) if obj.selected else obj.color

            for edge in obj.get_edges():
                p1 = screen_points[edge[0]]
                p2 = screen_points[edge[1]]

                if p1 and p2:
                    cv2.line(frame, p1, p2, color, 2)

            # Draw Center reference
            center = self.project_point(obj.position)
            if center:
                cv2.circle(frame, center, 3, (0, 255, 255), -1)

    def draw_ui(self, frame, gesture, intent_state, fps):
        h, w, _ = frame.shape

        # Toolbar / Status Bar
        cv2.rectangle(frame, (0, 0), (w, 60), (50, 50, 50), -1)

        # Text Info
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 20), font, 0.5, (200, 200, 200), 1)
        cv2.putText(frame, f"Gesture: {gesture}", (10, 45), font, 0.5,
                    (0, 255, 0) if gesture != "NONE" else (100, 100, 100), 1)
        cv2.putText(frame, f"Mode: {intent_state}", (200, 45), font, 0.6, (0, 200, 255), 2)

        # Instructions
        cv2.putText(frame, "Pinch to Select/Drag", (w - 200, 20), font, 0.4, (200, 200, 200), 1)
        cv2.putText(frame, "'c'-Spawn Cube, 'x'-Clear", (w - 200, 40), font, 0.4, (200, 200, 200), 1)
