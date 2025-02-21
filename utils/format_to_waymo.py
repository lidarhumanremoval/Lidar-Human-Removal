import os
import numpy as np
import shutil

def organize_npy_files(input_folder, output_folder, intensity_folder):
    """
    Organizes .npy files into timestamped subfolders and creates additional files 
    to match the folders and files format used in Waymo Open Dataset.

    Args:
        input_folder (str): Path to the folder containing the points .npy files.
        output_folder (str): Path to the folder where the output will be organized.
        intensity_folder (str): Path to the folder containing the intensity .npy files.
    """
    try:
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Iterate over all .npy files in the input folder
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".npy") and file_name.startswith("pointcloud_"):
                # Extract the timestamp from the filename
                timestamp = file_name.split("_")[1].replace(".npy", "")

                # Create the subfolder for the timestamp
                subfolder_path = os.path.join(output_folder, timestamp)
                os.makedirs(subfolder_path, exist_ok=True)

                # Define source file path
                source_file_path = os.path.join(input_folder, file_name)

                # Define destination paths
                coord_file_path = os.path.join(subfolder_path, "coord.npy")
                labels_file_path = os.path.join(subfolder_path, "segment.npy")

                # Copy and rename the file to "coord.npy"
                shutil.copy(source_file_path, coord_file_path)

                # Load coord.npy to determine its length
                coord_data = np.load(coord_file_path)
                n = len(coord_data)

                # Create a new .npy file filled with -1
                labels_data = np.full(n, -1, dtype=int)
                np.save(labels_file_path, labels_data)

                print(f"Processed: {file_name} -> {subfolder_path}/coord.npy, segment.npy")

        for file_name in os.listdir(intensity_folder):
            if file_name.endswith(".npy") and file_name.startswith("intensity_"):
                # Extract the timestamp from the filename
                timestamp = file_name.split("_")[1].replace(".npy", "")

                # Create the subfolder for the timestamp
                subfolder_path = os.path.join(output_folder, timestamp)
                os.makedirs(subfolder_path, exist_ok=True)

                # Define source file path
                source_file_path = os.path.join(intensity_folder, file_name)

                # Define destination paths
                strength_file_path = os.path.join(subfolder_path, "strength.npy")

                # Copy and rename the file to "strength.npy"
                shutil.copy(source_file_path, strength_file_path)

                print(f"Processed: {file_name} -> {subfolder_path}/strength.npy")

    except OSError as e:
        print(f"OS error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
input_folder = "./XRE_AI_OUSTER_POINTS_DEC_2024/XRE_AI_20484_1/npy/coord"  # Replace with your input folder path
intensity_folder = "./XRE_AI_OUSTER_POINTS_DEC_2024/XRE_AI_20484_1/npy/strength"  # Replace with your intensity folder path
output_folder = "./XRE_AI_OUSTER_POINTS_DEC_2024/XRE_AI_20484_1/segment-2048-1_with_camera_labels"  # Replace with your output folder path

if __name__ == "__main__":
    organize_npy_files(input_folder, output_folder, intensity_folder)
