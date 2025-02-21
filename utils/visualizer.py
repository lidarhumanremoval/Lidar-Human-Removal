from open3d.geometry import LineSet, PointCloud
from open3d.visualization import VisualizerWithKeyCallback
from open3d.utility import Vector3dVector, Vector2iVector
import numpy as np
import glob
import matplotlib.pyplot as plt
import argparse
import os

# Constants
POINT_SIZE = 5
KEY_NEXT_FRAME = ord("D")
KEY_PREV_FRAME = ord("A")
COLORMAP = plt.get_cmap("bwr")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Visualize point cloud sequence with frame control (keys: A,D).")
    parser.add_argument(
        "segment_path", 
        type=str, 
        help="Path to the segment directory containing point cloud folders in the Waymo Open Dataset format."
    )
    return parser.parse_args()

def load_frame(index, folders, pcd, colormap):
    """Load point cloud and color data for a given frame index."""
    try:
        points = np.load(os.path.join(folders[index], "coord.npy"))
        pcd.points = Vector3dVector(points)
        print(f"Loading frame at {folders[index]}")
        
        segment_path = os.path.join(folders[index], "segment.npy")
        if os.path.exists(segment_path):
            val = np.load(segment_path)
            if np.max(val) != np.min(val):
                val_norm = (val - np.min(val)) / (np.max(val) - np.min(val))
                colors = colormap(val_norm)[:, :3]
            else:
                colors = colormap(val)[:, :3]
            pcd.colors = Vector3dVector(colors)
        else:
            pcd.colors = Vector3dVector(np.zeros((len(points), 3)))
        
        vis.update_geometry(pcd)
    except Exception as e:
        print(f"Error loading frame {index}: {e}")

def next_frame(vis):
    """Callback function to load the next frame."""
    global frame_index
    if frame_index < len(folders) - 1:
        frame_index += 1
        load_frame(frame_index, folders, pcd, COLORMAP)
        vis.poll_events()
        vis.update_renderer()
    else:
        print("Reached last frame.")

def prev_frame(vis):
    """Callback function to load the previous frame."""
    global frame_index
    if frame_index > 0:
        frame_index -= 1
        load_frame(frame_index, folders, pcd, COLORMAP)
        vis.poll_events()
        vis.update_renderer()
    else:
        print("Reached first frame.")

if __name__ == "__main__":
    args = parse_arguments()

    # Load paths for each time step
    folders = sorted(glob.glob(os.path.join(args.segment_path, '*')))

    # Initialize Open3D visualizer with key callback functionality
    vis = VisualizerWithKeyCallback()
    vis.create_window()


    # Set point size
    render_option = vis.get_render_option()
    render_option.point_size = POINT_SIZE

    # Load the first frame and initialize point cloud
    initial_points = np.load(os.path.join(folders[0], "coord.npy"))
    pcd = PointCloud()
    pcd.points = Vector3dVector(initial_points)

    # Load initial scalar values for coloring
    initial_val_path = os.path.join(folders[0], "segment.npy")
    if os.path.exists(initial_val_path):
        initial_val = np.load(initial_val_path)
        if np.max(initial_val) != np.min(initial_val):
            initial_val_norm = (initial_val - np.min(initial_val)) / (np.max(initial_val) - np.min(initial_val))
            colors = COLORMAP(initial_val_norm)[:, :3]
        else:
            colors = COLORMAP(initial_val)[:, :3]
        pcd.colors = Vector3dVector(colors)
    else:
        pcd.colors = Vector3dVector(np.zeros((len(initial_points), 3)))

    # Add the initial point cloud to the visualizer
    vis.add_geometry(pcd)

    # Global frame index
    frame_index = 0

    # Register key callbacks
    vis.register_key_callback(KEY_NEXT_FRAME, next_frame)  # Press "D" to go to the next frame
    vis.register_key_callback(KEY_PREV_FRAME, prev_frame)  # Press "A" to go to the previous frame

    # Start the visualizer
    vis.run()
    vis.destroy_window()
