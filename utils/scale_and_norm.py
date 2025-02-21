import os
import numpy as np

def scale_and_normalize_sequence(input_dir, output_dir, scales, strength_max):
    """
    Scale coordinates and normalize strength values in point cloud data.

    Args:
        input_dir (str): Path to the input directory containing the point cloud sequence.
        output_dir (str): Path to the output directory to save processed data.
        scales (list): List of scaling factors to apply to the coordinates.
        strength_max (float): Maximum expected strength value for normalization.
    """
    input_filename = input_dir.split("/")[-1]
    for scale in scales:
        scale_output_dir = os.path.join(output_dir, f"{input_filename}_scaled_{scale}_norm_{strength_max}")
        os.makedirs(scale_output_dir, exist_ok=True)

        for subfolder in os.listdir(input_dir):
            subfolder_path = os.path.join(input_dir, subfolder)
            output_subfolder_path = os.path.join(scale_output_dir, subfolder)

            if os.path.isdir(subfolder_path):
                os.makedirs(output_subfolder_path, exist_ok=True)

                # Load the .npy files
                coord_path = os.path.join(subfolder_path, "coord.npy")
                strength_path = os.path.join(subfolder_path, "strength.npy")
                segment_path = os.path.join(subfolder_path, "segment.npy")

                coord = np.load(coord_path)
                strength = np.load(strength_path)
                segment = np.load(segment_path)

                # Apply scaling to coordinates
                coord_scaled = coord * scale

                # Remove outliers and normalize strength
                strength_clipped = np.clip(strength, 0, strength_max)
                strength_normalized = strength_clipped / strength_max

                # Save the processed data
                np.save(os.path.join(output_subfolder_path, "coord.npy"), coord_scaled)
                np.save(os.path.join(output_subfolder_path, "strength.npy"), strength_normalized)
                np.save(os.path.join(output_subfolder_path, "segment.npy"), segment)

if __name__ == "__main__":
    # Example usage
    input_directory = "./ouster_ai_1/segment-1_with_camera_labels"  # Replace with your input directory path
    output_directory = "./all_120_240/xplore_all_sm_120/all_in" 
    scales = [1.1]  # List of scaling factors to apply to the coordinates
    strength_max = 120  # Maximum expected strength value for normalization

    # Process the sequence
    scale_and_normalize_sequence(input_directory, output_directory, scales, strength_max)
