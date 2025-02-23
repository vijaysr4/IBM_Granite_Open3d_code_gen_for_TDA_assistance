import open3d as o3d
import numpy as np
from export_mesh import export_mesh  # Ensure export_mesh.py is in the same directory

# Torus parameters
R = 2.0   # Major radius: distance from the center of the tube to the center of the torus
r = 0.5   # Minor radius: radius of the tube
num_points = 5000  # Number of points to sample

# Generate parameters uniformly
u = np.random.uniform(0, 2 * np.pi, num_points)
v = np.random.uniform(0, 2 * np.pi, num_points)

# Parametric equations for a torus
x = (R + r * np.cos(v)) * np.cos(u)
y = (R + r * np.cos(v)) * np.sin(u)
z = r * np.sin(v)

# Stack into a (N,3) array
points = np.vstack((x, y, z)).T

# Create the Open3D PointCloud and assign points
torus_pcd = o3d.geometry.PointCloud()
torus_pcd.points = o3d.utility.Vector3dVector(points)

# Optionally, paint the point cloud (e.g., green)
torus_pcd.paint_uniform_color([0.0, 1.0, 0.0])

# Define output folder and file name
output_folder = "./output"
file_name = "torus_point_cloud.ply"

# Export the point cloud using the dedicated function
export_mesh(torus_pcd, output_folder, file_name)
