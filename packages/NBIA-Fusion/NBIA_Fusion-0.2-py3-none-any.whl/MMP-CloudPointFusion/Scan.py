import open3d
import numpy as np


class Scan:
    def __init__(
        self,
        camera: int,
        time_tag: int,
        point_cloud_path: str = None,
        point_cloud: open3d.geometry.PointCloud = None,
        pose: np.ndarray = None,
    ) -> None:
        """Object representation of a 3D scan.
        Compose of the scan info and the point cloud data.

        Args:
            camera (int): Camera ID (two scans with the same camera ID have been taken by the same camera)
            time_tag (int): Time tag of the scan (two scans with the same time tag have been taken at the same time)
            point_cloud_path (str, optional): Path to the point cloud file. Defaults to None.
            point_cloud (open3d.geometry.PointCloud, optional): Point cloud object. Defaults to None.
            pose (np.ndarray, optional): Pose of the scan. Defaults to None.
        """
        self.camera = camera
        self.time_tag = time_tag
        self.ID = f"CAM<{self.camera}>_SCAN<{self.time_tag}>"
        self.pose = pose
        if point_cloud is None:
            self.point_cloud = open3d.io.read_point_cloud(point_cloud_path)
        else:
            self.point_cloud = point_cloud

    def get_ID(self) -> str:
        """Get the ID of the scan.

        Returns:
            str: The ID of the scan.
        """
        return self.ID

    def get_camera(self) -> int:
        """Get the camera ID of the scan.

        Returns:
            int: The camera ID of the scan.
        """
        return self.camera

    def get_time_tag(self) -> int:
        """Get the time tag of the scan.

        Returns:
            int: The time tag of the scan.
        """
        return self.time_tag

    def get_point_cloud(self) -> open3d.geometry.PointCloud:
        """Get the point cloud of the scan.

        Returns:
            open3d.geometry.PointCloud: The point cloud of the scan.
        """
        return self.point_cloud

    def set_point_cloud(self, point_cloud: open3d.geometry.PointCloud) -> None:
        """Set the point cloud of the scan.

        Args:
            point_cloud (open3d.geometry.PointCloud): The point cloud to set.
        """
        self.point_cloud = point_cloud

    def get_pose(self) -> np.ndarray:
        """Get the pose of the scan.

        Returns:
            np.ndarray: The pose of the scan.
        """
        return self.pose

    def info(self) -> None:
        """Print the information of the scan."""
        print(f"Scan ID: {self.ID}")

    # def process(self):
    #     self.point_cloud = crop_and_center(self.point_cloud)
