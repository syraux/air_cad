import numpy as np
def export_to_obj(scene_graph, filename="scene_export.obj"):
    """
    Exports the current scene to an OBJ file.
    Note: Simply concatenates all primitives.
    """
    with open(filename, 'w') as f:
        f.write(f"# Air-CAD Export\n")

        vertex_offset = 1

        for idx, obj in enumerate(scene_graph.get_objects()):
            f.write(f"o {obj.name}_{idx}\n")

            model_matrix = obj.get_model_matrix()
            verts = obj.get_vertices()

            # Write Vertices
            for v in verts:
                # Transform to world space
                vh = np.array([v[0], v[1], v[2], 1.0])
                vw = np.dot(model_matrix, vh)
                f.write(f"v {vw[0]:.4f} {vw[1]:.4f} {vw[2]:.4f}\n")

            # Write Faces (Edges are simpler for wireframes, but OBJ uses faces)
            # We will approximate faces for the cube/cylinder or just export lines if we want wireframe
            # For this prototype, let's export LINES 'l' to keep it robust and consistent with the wireframe view

            lines = obj.get_edges()
            for l in lines:
                # OBJ indices are 1-based
                f.write(f"l {l[0] + vertex_offset} {l[1] + vertex_offset}\n")

            vertex_offset += len(verts)

    print(f"Scene exported to {filename}")

