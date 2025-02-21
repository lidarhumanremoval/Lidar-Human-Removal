import open3d as o3d
import os
import time
from typing import List

"""Simple pcd viewer to visualize point clouds sequence in a folder"""

FILE_PATH = "./ouster_ai_5/pcd"
UNIFORM_COLOR = True
COLOR = [0.5, 0.5, 0.5]  # gray color
SLEEP_TIME = 0.005
VIS_TRANSFORM = [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]] 


def get_pcd_files(file_path: str) -> List[str]:
    """Get a sorted list of .pcd files in the given directory."""
    pcd_files = [f for f in os.listdir(file_path) if f.endswith('.pcd')]
    pcd_files.sort()
    return pcd_files


def visualize_pcd_files(pcd_files: List[str], file_path: str, uniform_color: bool, color: List[float], sleep_time: float):
    """Visualize the point cloud files."""
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    for pcd_file in pcd_files:
        pcd = o3d.io.read_point_cloud(os.path.join(file_path, pcd_file))
        print(f"Visualizing {pcd_file}")
        pcd.transform(VIS_TRANSFORM)
        if uniform_color:
            pcd.paint_uniform_color(color)
        vis.add_geometry(pcd)
        vis.poll_events()
        vis.update_renderer()
        time.sleep(sleep_time)
        vis.remove_geometry(pcd, False)

    vis.destroy_window()


def main():
    pcd_files = get_pcd_files(FILE_PATH)
    visualize_pcd_files(pcd_files, FILE_PATH, UNIFORM_COLOR, COLOR, SLEEP_TIME)


if __name__ == "__main__":
    main()