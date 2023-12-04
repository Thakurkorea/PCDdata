import sys
import open3d as o3d
import numpy as np
import laspy

def pcd_to_las(input_pcd, output_las):
    # Read the input PCD file
    pcd = o3d.io.read_point_cloud(input_pcd)

    # Extract point coordinates and a single RGB integer value
    points = np.asarray(pcd.points)
    rgb = np.asarray(pcd.colors)  # Assuming the single RGB value is already an integer

    # Convert RGB values to uint16 for laspy
    rgb = rgb.astype(np.uint16)

    # Create LAS file using laspy
    las_outfile = laspy.create(file_version="1.4", point_format=2)
    las_outfile.x = points[:, 0]
    las_outfile.y = points[:, 1]
    las_outfile.z = points[:, 2]

    # Reshape the color values before assigning
    las_outfile.red = (rgb >> 16).reshape(-1)
    las_outfile.green = ((rgb >> 8) & 0xFF).reshape(-1)
    las_outfile.blue = (rgb & 0xFF).reshape(-1)

    # Write the data to the output LAS file
    las_outfile.write(output_las)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py input_pcd output_las")
        sys.exit(1)

    input_pcd = sys.argv[1]
    output_las = sys.argv[2]

    pcd_to_las(input_pcd, output_las)

if __name__ == "__main__":
    main()