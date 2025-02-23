import open3d as o3d
import os

def export_mesh(geometry, output_folder, file_name, file_format="ply"):
    """
    Exports an Open3D geometry (TriangleMesh or PointCloud) to the specified output folder and file name.

    For TriangleMesh:
      Supported formats: ply, obj, stl
    For PointCloud:
      Supported formats: ply, pcd
    """
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, file_name)

    if isinstance(geometry, o3d.geometry.TriangleMesh):
        if file_format.lower() in ["ply", "obj", "stl"]:
            o3d.io.write_triangle_mesh(output_path, geometry)
        else:
            raise ValueError("Unsupported file format for TriangleMesh. Supported formats: ply, obj, stl")
    elif isinstance(geometry, o3d.geometry.PointCloud):
        if file_format.lower() in ["ply", "pcd"]:
            o3d.io.write_point_cloud(output_path, geometry)
        else:
            raise ValueError("Unsupported file format for PointCloud. Supported formats: ply, pcd")
    else:
        raise ValueError("Unsupported geometry type. Supported types: TriangleMesh, PointCloud")

    print(f"Geometry saved to: {output_path}")
