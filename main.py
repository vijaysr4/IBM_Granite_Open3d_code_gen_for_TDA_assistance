import subprocess

def main():
    # Hard-coded image path
    img_input = "images/Tesseract_torus.png"

    # Run clip.py with the image path as an argument
    print("Running clip.py to generate image description...")
    subprocess.run(["python", "clip.py", img_input], check=True)

    # Run granite_code.py to generate Open3D code based on the description
    print("Running granite_code.py to generate Open3D code...")
    subprocess.run(["python", "granite_code.py"], check=True)

    # Visualization Example output
    # mesh_file_path = r"output/torus_point_cloud.ply"
    # print("Visualizing the generated mesh...")
    # plot_mesh(mesh_file_path)

if __name__ == "__main__":
    main()
