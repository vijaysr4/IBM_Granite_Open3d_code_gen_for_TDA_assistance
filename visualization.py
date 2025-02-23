import pyvista as pv

def plot_mesh(file_path):
    """
    Reads a mesh from the provided file_path and plots it.
    """
    mesh = pv.read(file_path)
    mesh.plot()

if __name__ == "__main__":
    # Example usage: change the path as needed
    default_path = r"/output"
    plot_mesh(default_path)
