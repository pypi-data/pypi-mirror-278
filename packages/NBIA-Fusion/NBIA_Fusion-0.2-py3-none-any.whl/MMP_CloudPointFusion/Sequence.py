import json
import os
from pathlib import Path
from typing import Sequence

import numpy as np
import open3d as o3d

from Scan import Scan
from utils.transform import Transform
from utils.alignment import *


class Sequence:
    def __init__(
        self,
        src_directory: str or None,  # type: ignore
        destination: str,
        master_cameraID: int = 0,
        master_time_tag: int = 1,
    ) -> None:
        """
        Initialize a sequence object.

        Args:
            src_directory (str or None): Path to the directory containing the scans.
            destination (str): Path to the directory where the resulting point cloud will be saved.
            master_cameraID (int, optional): ID of the camera that will be used as a reference for the alignment. Defaults to 0.
            master_time_tag (int, optional): Time tag that will be used as a reference for the alignment. Defaults to 1.
        """
        # TODO: add a check to verify that the src_directory is not empty
        # TODO: add a sequence ID extraction from the src_directory
        # Directories
        self.src_directory = src_directory
        self.destination = destination

        # Scan related variables
        self.scans = []
        self.nb_cameras = 0
        self.master_cameraID = master_cameraID
        self.read_sequence()  # Initiates scans, nb_cameras
        self.nb_scans_total = len(self.scans)
        self.nb_scans_per_camera = self.nb_scans_total // self.nb_cameras
        self.result_scan = None
        self.result_dict = {}
        self.merge_by_camera = []

        # ID and time tag
        self.ID = (
            self.src_directory.rstrip("/").split("/")[-1] if src_directory else None
        )
        self.master_time_tag = master_time_tag

    def read_sequence(self) -> None:
        """Read the sequence directory and create a list of Scan objects.

        This method reads the sequence directory and creates a list of Scan objects
        based on the subfolders and .ply files found in the directory. It also updates
        the maximum camera and scan numbers for the sequence.

        Returns:
            None
        """
        # Initialize maximum camera and scan numbers
        max_camera_num = 0
        max_scan_num = 0

        # Get all subfolders in the source directory
        path = Path(self.src_directory)
        subfolders = [f for f in path.iterdir() if f.is_dir()]

        # Process all .ply files in the sub directories
        for i, subfolder in enumerate(subfolders):
            poses = json.load(open(os.path.join(subfolder, "poses.json")))
            for f in os.listdir(subfolder):
                if f.endswith(".ply"):  # Check if the file is a .ply file
                    # Extract camera and scan numbers from the file name
                    camera_num = i
                    scan_num = int(f[5])

                    # Update maximum camera and scan numbers
                    max_camera_num = max(max_camera_num, camera_num)
                    max_scan_num = max(max_scan_num, scan_num)

                    # Create and process a Scan object for the file
                    scan = Scan(
                        camera=camera_num,
                        time_tag=scan_num,
                        point_cloud_path=os.path.join(subfolder, f),
                        pose=poses[f],
                    )
                    # scan.process()

                    # Add the processed Scan object to the list of scans
                    self.scans.append(scan)

        # Update the Sequence object's attributes
        self.nb_scans_per_camera = max_scan_num + 1
        self.nb_cameras = max_camera_num + 1

    def tracking_processing(self):
        """Process the scans to merge them into a single
        point cloud in the Hanger Coordinate System for each camera

        Returns:
            list: A list of Scan objects, one for each camera (concatenated by cam pcds)
        """
        for scan in self.scans:
            scan.set_point_cloud(self.cam_to_HCS(scan.point_cloud, scan.pose))

        merged_pcds = []
        for cam in range(self.nb_cameras):
            pcds = [
                scan.get_point_cloud()
                for scan in self.scans
                if scan.get_camera() == cam
            ]
            merged_pcd = self.concatenate_point_clouds(pcds)
            # create a Scan object for each camera (time_tag = -1) since it's
            # just to indicate it's the merged point cloud
            self.merge_by_camera.append(Scan(cam, -1, point_cloud=merged_pcd))

        return self.merge_by_camera

    def concatenate_point_clouds(
        self, input: Sequence[o3d.geometry.PointCloud]
    ) -> o3d.geometry.PointCloud:
        """Concatenate a list of point clouds into a single point cloud

        Args:
            input (Sequence[o3d.geometry.PointCloud]): A list of point clouds to be concatenated.

        Returns:
            o3d.geometry.PointCloud: The resulting point cloud, including all the points from the input point clouds.
        """
        merged = o3d.geometry.PointCloud()
        for pcd in input:
            merged += pcd
        return merged

    def cam_to_HCS(self, pcd, pose):
        """Transforms a point cloud from the camera coordinate system to the Hanger Coordinate System

        Args:
            pcd (PointCloud): The point cloud to transform.
            pose (tuple): The pose of the hanger in the form (x, y, z, x_rad, y_rad, z_rad).

        Returns:
            PointCloud: The transformed point cloud in the Hanger Coordinate System.
        """
        pose = Transform.from_parameters(*pose)
        x, y, z, x_rad, y_rad, z_rad = pose.to_parameters()
        pose.set_rotation(x_rad, y_rad * -1, z_rad * -1)
        pose.set_translation(x, y * -1, z * -1)

        pcd.transform(np.linalg.inv(pose.matrix))

        mirror = np.array([[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
        pcd.transform(mirror)

        # This is kinda arbitrary to reach the HCS from the center of the hanger. We will need to measure the real value.
        translation_arbitraire = 0.24
        translation = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, translation_arbitraire],
                [0, 0, 0, 1],
            ]
        )
        pcd.transform(translation)

        return pcd

    def extract_camera_number(filename: str) -> int:
        """
        Extract the camera number from the filename.

        Args:
            filename (str): The filename.

        Returns:
            int: The camera number.
        """
        prefix = filename.split("_")[
            0
        ]  # split the filename at the underscore and take the first part
        camera_number = int(
            prefix.replace("cam", "")
        )  # remove 'cam' and convert the remaining string to an integer
        return camera_number

    def extract_scan_number(filename: str) -> int:
        """
        Extract the scan number from the filename.

        Args:
            filename (str): The filename.

        Returns:
            int: The scan number.
        """
        suffix = filename.split("_")[
            1
        ]  # split the filename at the underscore and take the second part
        scan_number = int(
            suffix.replace(".ply", "").replace("scan", "")
        )  # remove '.ply' and 'scan' and convert the remaining string to an integer
        return scan_number

    def align_processing(self, refine: bool = True):
        """Align the merged point clouds to the master camera.

        This method aligns the merged point clouds to the master camera by performing
        a series of alignment operations. The master camera is defined as the target
        and is painted red. The source scans are aligned to the target scan using the
        align_source_to_target_RANSAC_ICP algorithm. The aligned point clouds are then
        concatenated with the target point cloud to form the final scan.

        Args:
            refine (bool, optional): Flag indicating whether to refine the alignment.
                Defaults to True.

        Returns:
            Scan: The final scan with all aligned point clouds.
        """
        source_scans = []
        # define the master camera as the target and paint it red
        for scan in self.merge_by_camera:
            if scan.get_camera() == self.master_cameraID:
                target_pcd = scan.get_point_cloud()
                target_pcd.paint_uniform_color([1, 0, 0])  # Paint target in red
            else:
                source_scans.append(scan)

        # align the source scans to the target scan
        aligned_sources = []

        for source_scan in source_scans:
            source_pcd = source_scan.get_point_cloud()
            random_color = np.random.rand(3)  # Generate random color
            source_pcd.paint_uniform_color(random_color)  # Paint source in random color
            aligned_source = align_source_to_target_RANSAC_ICP(
                source=source_pcd,
                target=target_pcd,
                voxel_size=20,
                display=False,
                ransac_confidence=0.9999,
                ransac_max_iter=10000,
                refine=refine,
                color=True,
            )
            aligned_sources.append(aligned_source)

        result_pcd = self.concatenate_point_clouds([target_pcd] + aligned_sources)
        self.result_scan = Scan(
            camera=self.master_cameraID, time_tag=-1, point_cloud=result_pcd
        )

        return self.result_scan
