import os
import json
import numpy as np
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)

def update_labels_from_json(labels_json_path: str, names_json_path: str, output_folder: str) -> None:
    """
    Updates labels.npy files to add human class labels based on the labels JSON and names JSON.

    Args:
        labels_json_path (str): Path to the JSON file containing label information.
        names_json_path (str): Path to the JSON file mapping frame indices to filenames.
        output_folder (str): Path to the output folder.
    """
    try:
        labels_data = load_json(labels_json_path)
        names_data = load_json(names_json_path)

        for frame in labels_data.get("frames", []):
            frame_index = str(frame["index"])
            if frame_index not in names_data:
                logging.warning(f"Frame index {frame_index} not found in names JSON. Skipping.")
                continue

            timestamp = names_data[frame_index].split("_")[1].replace(".pcd", "")
            labels_file_path = os.path.join(output_folder, timestamp, "segment.npy")

            if not os.path.exists(labels_file_path):
                logging.warning(f"Labels file not found for timestamp {timestamp}. Skipping.")
                continue

            labels = np.load(labels_file_path)
            labels = np.where(labels == 6, -1, labels)

            for figure in frame.get("figures", []):
                object_key = figure.get("objectKey")
                if object_key:
                    object_data = next((obj for obj in labels_data.get("objects", []) if obj["key"] == object_key), None)
                    if object_data:
                        class_title = object_data.get("classTitle", "").lower()
                        class_value = 6 if class_title == "human" else -1

                        indices = figure["geometry"]["indices"]
                        labels[indices] = class_value

            np.save(labels_file_path, labels)
            logging.info(f"Updated labels for timestamp {timestamp}.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    labels_json_path = "./XRE_AI_OUSTER_POINTS_DEC_2024/XRE_AI_20484_1/labels1_corr/annotation.json"
    names_json_path = "./XRE_AI_OUSTER_POINTS_DEC_2024/XRE_AI_20484_1/labels1_corr/frame_pointcloud_map.json"
    output_folder = "./XRE_AI_OUSTER_POINTS_DEC_2024/XRE_AI_20484_1/segment-2048-1_with_camera_labels"
    update_labels_from_json(labels_json_path, names_json_path, output_folder)
