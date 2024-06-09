import open3d as o3d
from utils.alignment import crop_bbox
from Sequence import Sequence
import torch
import numpy as np


def process_point_clouds(
    bbox_w_rack: tuple,
    bbox_wo_rack: tuple,
    src_directory: str = "MMP-CloudPointFusion/exemple_bidon",
    output_folder: str = "",
    display: bool = True,
):
    """
    Process point clouds by performing fusion, tracking, alignment, cropping, and outlier removal.

    This function performs the following steps:
    1. Loads a sequence of point clouds from a specified path.
    2. Performs tracking processing on the sequence.
    3. Defines a bounding box to crop the point clouds with a rack.
    4. Visualizes the original point clouds with the coordinate frame.
    5. Crops the background of each point cloud using the defined bounding box.
    6. Visualizes the cropped point clouds with the coordinate frame.
    7. Aligns the point clouds using a specified alignment method.
    8. Visualizes the aligned point clouds with the coordinate frame.
    9. Defines a bounding box to crop the point clouds without the rack.
    10. Crops the rack from the aligned point cloud using the defined bounding box.
    11. Visualizes the cropped point cloud without the rack with the coordinate frame.
    12. Removes outliers from the point cloud using statistical outlier removal.
    13. Visualizes the point cloud after outlier removal with the coordinate frame.

    Parameters:
    - display (bool): Flag to control whether to display the point clouds or not. Default is True.
    - bbox_w_rack (tuple): Bounding box coordinates for cropping the point clouds with the rack. Default is (-0.75, 0.75, -0.50, 0.5, -1.25, 0.4).
    - bbox_wo_rack (tuple): Bounding box coordinates for cropping the point clouds without the rack. Default is (-0.75, 0.75, -0.50, 0.5, -1.25, 0.1).
    - src_directory (str): Path to the directory containing the point cloud files. Default is "MMP-CloudPointFusion/exemple_bidon".
    - output_folder (str): Path to the directory where the processed point clouds will be saved. Default is an empty string.
    """

    s = Sequence(src_directory=src_directory, destination=output_folder)
    s.tracking_processing()  # align all the scan by camera using the pose estimation provided by the tracker

    coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=0.3, origin=[0, 0, 0]
    )
    for scan in s.merge_by_camera:
        pcd = scan.get_point_cloud()
        # paint blue
        pcd.paint_uniform_color([0, 0, 1])
        if display:
            o3d.visualization.draw_geometries([pcd, coordinate_frame])

        # crop the background
        crop_bbox(scan, *bbox_w_rack)
        if display:
            o3d.visualization.draw_geometries([scan.point_cloud, coordinate_frame])

    for i, scan in enumerate(s.merge_by_camera):

        # Step 1: Read the PLY file
        point_cloud = scan.point_cloud
        point_cloud_np = np.asarray(point_cloud.points)
        # Step 2: Convert to PyTorch tensor
        point_cloud_tensor = torch.from_numpy(point_cloud_np)

        # Step 3: Save to PTH file
        torch.save(point_cloud_tensor, f"scan{i}.pth")

    # Align the point clouds
    result = s.align_processing(refine=True)

    if display:
        o3d.visualization.draw_geometries([result.point_cloud, coordinate_frame])

    # crop the rack
    crop_bbox(result, *bbox_wo_rack)
    if display:
        o3d.visualization.draw_geometries([result.point_cloud, coordinate_frame])

    # Remove outliers from the point cloud using statistical outlier removal
    cl, ind = result.point_cloud.remove_statistical_outlier(
        nb_neighbors=20, std_ratio=1.5
    )
    result.point_cloud = result.point_cloud.select_by_index(ind)
    if display:
        o3d.visualization.draw_geometries([result.point_cloud, coordinate_frame])


if __name__ == "__main__":
    # exemple avec display
    process_point_clouds(
        display=True,
        bbox_w_rack=(-0.75, 0.75, -0.50, 0.5, -1.25, 0.4),
        bbox_wo_rack=(-0.75, 0.75, -0.50, 0.5, -1.25, 0.1),
        src_directory="MMP-CloudPointFusion/exemple_bidon",
        output_folder="",
    )
