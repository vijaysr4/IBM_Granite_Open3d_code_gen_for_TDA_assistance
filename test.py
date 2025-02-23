import open3d as o3d
import numpy as np

def create_colored_cubelet(center, size, face_colors):
    """
    Create a cubelet as a TriangleMesh with each face colored individually.
    """
    vertices = []
    triangles = []
    colors = []
    half = size / 2.0

    # Each face is defined with its own set of vertices.
    faces = [
        # Right face (constant x = +half)
        ("R", [
            [ half, -half, -half],
            [ half, -half,  half],
            [ half,  half,  half],
            [ half,  half, -half]
        ]),
        # Left face (constant x = -half)
        ("L", [
            [-half, -half,  half],
            [-half, -half, -half],
            [-half,  half, -half],
            [-half,  half,  half]
        ]),
        # Top face (constant y = +half)
        ("U", [
            [-half,  half, -half],
            [ half,  half, -half],
            [ half,  half,  half],
            [-half,  half,  half]
        ]),
        # Bottom face (constant y = -half)
        ("D", [
            [-half, -half,  half],
            [ half, -half,  half],
            [ half, -half, -half],
            [-half, -half, -half]
        ]),
        # Front face (constant z = +half)
        ("F", [
            [ half, -half,  half],
            [-half, -half,  half],
            [-half,  half,  half],
            [ half,  half,  half]
        ]),
        # Back face (constant z = -half)
        ("B", [
            [-half, -half, -half],
            [ half, -half, -half],
            [ half,  half, -half],
            [-half,  half, -half]
        ]),
    ]

    for face_name, face_verts in faces:
        start_index = len(vertices)
        for v in face_verts:
            vertices.append(np.array(v) + np.array(center))
        # Each face is made of two triangles.
        triangles.append([start_index, start_index+1, start_index+2])
        triangles.append([start_index, start_index+2, start_index+3])
        # Use the provided color (or a default dark gray if not provided).
        color = face_colors.get(face_name, [0.1, 0.1, 0.1])
        colors.extend([color, color, color, color])

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(np.array(vertices))
    mesh.triangles = o3d.utility.Vector3iVector(np.array(triangles))
    mesh.vertex_colors = o3d.utility.Vector3dVector(np.array(colors))
    mesh.compute_vertex_normals()
    return mesh

# Parameters for cubelets
cubelet_size = 0.9  # slightly less than 1 to allow a gap
gap = 0.1
step = cubelet_size + gap

# Rubik's Cube standard colors (RGB values between 0 and 1)
COLORS = {
    "R": [1, 0, 0],    # Right: Red
    "L": [1, 0.5, 0],  # Left: Orange
    "U": [1, 1, 1],    # Up: White
    "D": [1, 1, 0],    # Down: Yellow
    "F": [0, 1, 0],    # Front: Green
    "B": [0, 0, 1]     # Back: Blue
}
default_color = [0.1, 0.1, 0.1]  # for inner faces

# Create the full Rubik's Cube mesh by combining cubelets.
rubiks_cube = o3d.geometry.TriangleMesh()
for i in range(3):
    for j in range(3):
        for k in range(3):
            x = (i - 1) * step
            y = (j - 1) * step
            z = (k - 1) * step
            center = (x, y, z)
            face_colors = {
                "R": COLORS["R"] if i == 2 else default_color,
                "L": COLORS["L"] if i == 0 else default_color,
                "U": COLORS["U"] if j == 2 else default_color,
                "D": COLORS["D"] if j == 0 else default_color,
                "F": COLORS["F"] if k == 2 else default_color,
                "B": COLORS["B"] if k == 0 else default_color,
            }
            cubelet = create_colored_cubelet(center, cubelet_size, face_colors)
            rubiks_cube += cubelet

rubiks_cube.compute_vertex_normals()

# --- WEB VISUALIZER SETUP ---
# Enable the WebRTC server backend
o3d.visualization.webrtc_server.enable_webrtc()

# Launch the web visualizer.
# The default port is 8888. Open your browser and navigate to http://localhost:8888
o3d.visualization.draw([rubiks_cube])
