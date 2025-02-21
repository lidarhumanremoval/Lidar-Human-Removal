import numpy as np
import os
import open3d as o3d

from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2
from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr

def save_to_pcd(points, filename):
    """
    Save the point cloud to a PCD file using Open3D.
    """
    folder = os.path.dirname(filename)
    os.makedirs(folder, exist_ok=True)
    
    points = np.array(points)
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(filename, pc)
    print(f"Point cloud saved to {filename}")

def save_to_npy(data, filename):
    """
    Save the data to a NPY file using NumPy.
    """
    folder = os.path.dirname(filename)
    os.makedirs(folder, exist_ok=True)

    np.save(filename, data)
    print(f"Data saved to {filename}")

def main():
    file_path = "./ouster_ai_5/"

    with Reader(file_path) as reader:
        for connection in reader.connections:
            print(connection.topic, connection.msgtype)
        
        for data in reader.messages():
            points = []
            intensities = []
            timestamp = data[1]
            blob = data[2]
            if connection.topic == '/ouster_points':
                msg_raw = deserialize_cdr(blob, connection.msgtype)
                msg = PointCloud2(
                    header=msg_raw.header,
                    height=msg_raw.height,
                    width=msg_raw.width,
                    fields=msg_raw.fields,
                    is_bigendian=msg_raw.is_bigendian,
                    point_step=msg_raw.point_step,
                    row_step=msg_raw.row_step,
                    data=msg_raw.data,
                    is_dense=msg_raw.is_dense
                )

                for point in sensor_msgs.point_cloud2.read_points(msg, skip_nans=True):
                    points.append(point[0:3])  # keep only x, y, z
                    intensities.append(point[3])  # keep only intensity
                
                intensities = np.array(intensities).reshape(-1, 1)

                save_to_pcd(points, os.path.join(file_path, f"pcd/pointcloud_{timestamp}.pcd"))
                save_to_npy(points, os.path.join(file_path, f"npy/coord/pointcloud_{timestamp}.npy"))
                save_to_npy(intensities, os.path.join(file_path, f"npy/strength/intensity_{timestamp}.npy"))

    print(f"Successfully saved {len(points)} points")

if __name__ == "__main__":
    main()
