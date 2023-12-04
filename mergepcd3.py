import os
import sys
import open3d as o3d
import numpy as np

def merge_pcd_in_directory(input_directory, output_pcd, output_format="pcd"):
    # Get a list of all PCD files in the specified directory
    pcd_files = [f for f in os.listdir(input_directory) if f.endswith(".pcd")]

    if not pcd_files:
        print(f"No PCD files found in the directory: {input_directory}")
        sys.exit(1)

    # Create a list to store full paths of the PCD files
    pcd_files = [os.path.join(input_directory, f) for f in pcd_files]

    points = []
    colors = []

    for pcd_file in pcd_files:
        pcd = o3d.io.read_point_cloud(pcd_file)
        points.append(np.asarray(pcd.points))
        colors.append(np.asarray(pcd.colors) * 255.0)

    merged_points = np.vstack(points)
    merged_colors = np.vstack(colors).astype(np.uint8)

    # Convert RGB values back to a single integer (0xRRGGBB)
    merged_rgb = (merged_colors[:, 0] << 16) + (merged_colors[:, 1] << 8) + merged_colors[:, 2]

    merged_pcd = o3d.geometry.PointCloud()
    merged_pcd.points = o3d.utility.Vector3dVector(merged_points)

    # Create colors array with correct shape and dtype
    colors_array = np.zeros((merged_rgb.shape[0], 3), dtype=np.uint8)
    colors_array[:, 0] = (merged_rgb >> 16) & 0xFF
    colors_array[:, 1] = (merged_rgb >> 8) & 0xFF
    colors_array[:, 2] = merged_rgb & 0xFF

    # Directly assign colors_array to the colors attribute
    merged_pcd.colors = o3d.utility.Vector3dVector(colors_array.astype(np.float64))

    o3d.io.write_point_cloud(output_pcd, merged_pcd, write_ascii=True)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py input_directory output_pcd")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_pcd = sys.argv[2]

    merge_pcd_in_directory(input_directory, output_pcd)

if __name__ == "__main__":
    main()