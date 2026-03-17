import numpy as np
import math


class Primitive:
    def __init__(self, name, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), color=(0, 255, 0)):
        self.name = name
        self.position = list(position)
        self.rotation = list(rotation)  # Euler angles in degrees
        self.scale = list(scale)
        self.color = color
        self.selected = False

    def get_vertices(self):
        raise NotImplementedError("Subclasses must implement get_vertices")

    def get_edges(self):
        raise NotImplementedError("Subclasses must implement get_edges")

    def get_model_matrix(self):
        # Simplistic transformation matrix construction (Translation * Rotation * Scale)
        # Note: Proper matrix multiplication order matters. T * R * S

        # Translation
        T = np.identity(4)
        T[0, 3] = self.position[0]
        T[1, 3] = self.position[1]
        T[2, 3] = self.position[2]

        # Scale
        S = np.identity(4)
        S[0, 0] = self.scale[0]
        S[1, 1] = self.scale[1]
        S[2, 2] = self.scale[2]

        # Rotation (Z * Y * X)
        rad_x = math.radians(self.rotation[0])
        rad_y = math.radians(self.rotation[1])
        rad_z = math.radians(self.rotation[2])

        Rx = np.array([
            [1, 0, 0, 0],
            [0, math.cos(rad_x), -math.sin(rad_x), 0],
            [0, math.sin(rad_x), math.cos(rad_x), 0],
            [0, 0, 0, 1]
        ])

        Ry = np.array([
            [math.cos(rad_y), 0, math.sin(rad_y), 0],
            [0, 1, 0, 0],
            [-math.sin(rad_y), 0, math.cos(rad_y), 0],
            [0, 0, 0, 1]
        ])

        Rz = np.array([
            [math.cos(rad_z), -math.sin(rad_z), 0, 0],
            [math.sin(rad_z), math.cos(rad_z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        R = np.dot(Rz, np.dot(Ry, Rx))

        return np.dot(T, np.dot(R, S))


class Cube(Primitive):
    def __init__(self, name, size=1.0, **kwargs):
        super().__init__(name, **kwargs)
        self.size = size
        # Base vertices for a unit cube centered at origin
        self.base_vertices = np.array([
            [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],  # Front
            [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]  # Back
        ]) * size

        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
            (0, 4), (1, 5), (2, 6), (3, 7)  # Connecting edges
        ]

    def get_vertices(self):
        return self.base_vertices

    def get_edges(self):
        return self.edges


class Cylinder(Primitive):
    def __init__(self, name, radius=0.5, height=1.0, segments=12, **kwargs):
        super().__init__(name, **kwargs)
        self.radius = radius
        self.height = height
        self.segments = segments

        verts = []
        # Top circle
        for i in range(segments):
            theta = 2.0 * math.pi * i / segments
            x = radius * math.cos(theta)
            z = radius * math.sin(theta)
            verts.append([x, height / 2, z])

        # Bottom circle
        for i in range(segments):
            theta = 2.0 * math.pi * i / segments
            x = radius * math.cos(theta)
            z = radius * math.sin(theta)
            verts.append([x, -height / 2, z])

        self.base_vertices = np.array(verts)

        edges = []
        # Top circle
        for i in range(segments):
            edges.append((i, (i + 1) % segments))

        # Bottom circle
        for i in range(segments):
            base_idx = i + segments
            next_idx = (i + 1) % segments + segments
            edges.append((base_idx, next_idx))

        # Connecting lines
        for i in range(segments):
            edges.append((i, i + segments))

        self.edges = edges

    def get_vertices(self):
        return self.base_vertices

    def get_edges(self):
        return self.edges


class SceneGraph:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def get_objects(self):
        return self.objects
