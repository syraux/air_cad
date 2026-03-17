import numpy as np
import math


class Utils:
    @staticmethod
    def get_distance(p1, p2):
        """Euclidean distance between two 3D points."""
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

    @staticmethod
    def create_perspective_projection_matrix(fov_degrees, aspect_ratio, near, far):
        """Creates a projection matrix for rendering 3D points to 2D."""
        f = 1.0 / math.tan(math.radians(fov_degrees) / 2)
        proj = np.zeros((4, 4))
        proj[0, 0] = f / aspect_ratio
        proj[1, 1] = f
        proj[2, 2] = (far + near) / (near - far)
        proj[2, 3] = (2 * far * near) / (near - far)
        proj[3, 2] = -1.0
        return proj

    @staticmethod
    def world_to_screen(point_3d, view_matrix, proj_matrix, screen_width, screen_height):
        """Projects a 3D world point to 2D screen coordinates."""
        # Convert to homogeneous coordinates
        p = np.array([point_3d[0], point_3d[1], point_3d[2], 1.0])

        # Apply view and projection
        p_view = np.dot(view_matrix, p)
        p_clip = np.dot(proj_matrix, p_view)

        # Perspective divide
        if p_clip[3] == 0:
            return None

        ndc = p_clip[:3] / p_clip[3]

        # Map to screen coordinates
        x = int((ndc[0] + 1) * 0.5 * screen_width)
        y = int((1 - ndc[1]) * 0.5 * screen_height)

        return (x, y)
