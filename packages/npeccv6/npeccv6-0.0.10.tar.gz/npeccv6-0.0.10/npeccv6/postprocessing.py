#!/bin/python3
import math
from typing import Any, Dict, List, Tuple

import cv2
import networkx as nx
import numpy as np
import pandas as pd
from skan import Skeleton, summarize
from skan.csr import skeleton_to_csgraph
from skimage.morphology import (remove_small_holes, remove_small_objects,
                                skeletonize)

try:
    # Attempt relative imports (if run as a package module)
    from .utils import setup_logger

except ImportError:
    # Fallback to absolute imports (if run as a standalone script)
    from utils import setup_logger


# Configure logger
logger = setup_logger()


def segment_roots(image: np.ndarray, expected_nr_plants: int) -> np.ndarray:
    """
    The function segments roots from the input image using connected component analysis and size-based filtering.
    It first identifies connected components in the image and removes small objects and small holes.
    Then, it filters the remaining components based on their position and size.
    If the number of segmented roots exceeds the expected number of plants, only the largest ones are retained.
    Finally, the function returns the segmented roots with labeled regions.

    Parameters:
        - image (np.ndarray): An array representing the input image containing plant roots.
        - expected_nr_plants (int): The expected number of plants to be found.

    Returns:
        - np.ndarray: An array representing the segmented roots.

    Example:
        - segmented_roots_image = segment_roots(image = image_to_be_segmented, expected_nr_plants = 5)

    Note:
        - This function assumes that the input image contains plant roots.
        - This function will consider overlaping roots as one singular root.
        - The function will ignore roots smaller than 64 pixels.
    """
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)
    # Get components
    _, labels, stats, _ = cv2.connectedComponentsWithStats(image)

    # Remove objects with area smaller than 64
    removed_small_obj = remove_small_objects(labels, 64)
    removed_small_obj[removed_small_obj != 0] = 1
    removed_small_obj = removed_small_obj.astype(np.uint8)
    _, labels, stats, _ = cv2.connectedComponentsWithStats(removed_small_obj)

    # Make labeles binary
    labels = labels > 0

    # Remove holes with area smalle than 64
    removed_small_holes = remove_small_holes(labels, 64)
    removed_small_holes[removed_small_holes != 0] = 1
    removed_small_holes = removed_small_holes.astype(np.uint8)
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(removed_small_holes)
    # Round the centroids
    centroids = np.round(centroids).astype(int)
    # Combine stats and centroids
    combined_stats = np.hstack((stats, centroids))

    # Add id to clean canvas to only roots
    row_indices = np.arange(len(combined_stats))
    stats_with_id = np.hstack((combined_stats, row_indices.reshape(-1, 1)))

    # Empty list with roots
    roots = []

    # Sort the array
    sorted_stats = stats_with_id[stats_with_id[:, 3].argsort()[::-1]]

    # Define conditions to filter the image
    above_150_condition = sorted_stats[:, 1] > 150
    below_half_y_condition = sorted_stats[:, 1] < (labels.shape[1] / 2)
    combined_condition = above_150_condition & below_half_y_condition

    # Apply the combined condition to filter rows
    filtered_stats = sorted_stats[combined_condition]
    sorted_roots = filtered_stats[filtered_stats[:, 3].argsort()[::-1]]

    # Remove elements whose centroids are below 450
    centroids_below_450 = sorted_roots[:, 6] > 450
    centroids_above_1800 = sorted_roots[:, 6] < 1800
    centroids_condition = centroids_below_450 & centroids_above_1800

    # Keep the roots which meet the centroid condition
    sorted_roots = sorted_roots[centroids_condition]

    # Sort the roots by size in descending order
    sorted_roots = sorted(sorted_roots, key=lambda x: x[4])
    sorted_roots = np.array(sorted_roots)

    # Empty list to keep the good roots
    filtered_roots = []

    # Iterate over all roots
    for i, test_root in enumerate(sorted_roots):
        # Set up the 2 checks
        keep_1 = True
        keep_2 = True
        # Go over all the root bigger than the test root
        for j, root in enumerate(sorted_roots[i + 1 :], start=i + 1):
            # If the roots overlap vertically, failed check
            if root[0] <= test_root[5] <= root[0] + root[2]:
                keep_1 = False
            # If the roots centroids are too close, failed check
            if (
                math.sqrt((root[5] - test_root[5]) ** 2 + (root[6] - test_root[6]) ** 2)
                < 300
            ):
                keep_2 = False
        # If both checks passed, save the root
        if keep_1 and keep_2:
            filtered_roots.append(test_root)

    # Sort the roots by size in descending order and make them into an array
    roots = sorted(filtered_roots, key=lambda x: x[4], reverse=True)
    roots = np.array(roots)

    # Leave only the expected nr of plants based on size and overwrite rest
    if len(roots) > expected_nr_plants:
        roots = roots[:expected_nr_plants, :]

    # Make the mask based on the roots
    mask = np.isin(labels, roots[:, -1])

    # Create the labels/big picture
    labels[~mask] = 0
    roots = roots[roots[:, 0].argsort()]

    try:
        # Get the width and size of the 2nd biggest component
        _, _, width_1, _, size_1, _, _, _ = roots[0]
        # Get the size of the 2nd biggest component
        size_2 = roots[1][5]

        # Check the width
        if width_1 > labels.shape[0] / (expected_nr_plants - 1) and size_1 / 2 > size_2:
            logger.error("Image has overlapping plants!")
            return labels
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    # Check the number of roots
    if len(roots) != expected_nr_plants:
        logger.error(f"Number of detected plants is not {expected_nr_plants}!")
        logger.error(f"Detected: {len(roots)} plants")
        return labels

    # Return the image with the labels and segmented plants
    return labels


def calculate_root_length(
    subgraph: nx.Graph, subgraph_edges: pd.DataFrame
) -> Tuple[float, float, int]:
    """
    Calculate the main and lateral root lengths and the destination node of the main root in a subgraph.

    Parameters:
        - subgraph (nx.Graph): The subgraph representing a skeleton.
        - subgraph_edges (pd.DataFrame): The edge data for the subgraph.

    Returns:
        - Tuple[float, float, int]: The main root length, lateral root length, and the destination node of the main root.
    """
    logger.info("Calculating root lengths for a subgraph.")

    # Find the node that corresponds to the lowest value of image-coord-dst-0 and image-coord-src-0
    highest_dst_node = subgraph_edges.loc[
        subgraph_edges["image-coord-dst-0"].idxmin(), "node-id-dst"
    ]
    highest_src_node = subgraph_edges.loc[
        subgraph_edges["image-coord-src-0"].idxmin(), "node-id-src"
    ]

    highest_node = min(highest_dst_node, highest_src_node)
    logger.debug(f"Starting node for root length calculation: {highest_node}")

    # Compute the lengths using single-source shortest path from the chosen node
    lengths = nx.single_source_dijkstra_path_length(
        subgraph, highest_node, weight="branch-distance"
    )

    main_root_length = max(lengths.values())
    main_root_src = highest_node
    main_root_dest = max(lengths, key=lengths.get)

    lateral_root_length = sum(lengths.values()) - main_root_length

    logger.debug(
        f"Main root length: {main_root_length}, Lateral root length: {lateral_root_length}, Main root destination: {main_root_dest}"
    )

    return main_root_length, lateral_root_length, main_root_src, main_root_dest


def calculate_root_lengths(graph: pd.DataFrame) -> Dict[int, Dict[str, float]]:
    """
    Calculate the root lengths for all unique skeleton IDs in the graph.

    Parameters:
        - graph (pd.DataFrame): The edge data for the entire graph.

    Returns:
        - Dict[int, Dict[str, float]]: A dictionary mapping skeleton IDs to their respective root lengths and main root destinations.
    """
    logger.info("Calculating root lengths for all skeletons.")

    unique_values = graph["skeleton-id"].unique()
    results = {}

    for skeleton_id in unique_values:
        logger.info(f"Processing skeleton ID: {skeleton_id}")

        subgraph_edges = graph[graph["skeleton-id"] == skeleton_id]
        subgraph = nx.from_pandas_edgelist(
            subgraph_edges,
            source="node-id-src",
            target="node-id-dst",
            edge_attr="branch-distance",
        )

        (
            main_root_length,
            lateral_root_length,
            main_root_src,
            main_root_dest,
        ) = calculate_root_length(subgraph, subgraph_edges)

        results[skeleton_id] = {
            "main_root_length": main_root_length,
            "lateral_root_length": lateral_root_length,
            "main_root_src": main_root_src,
            "main_root_dest": main_root_dest,
        }

    return results


def mark_landmarks(
    image: Any,
    nodes_summary: pd.DataFrame,
    main_root_src: List[int],
    main_root_dest: List[int],
) -> Any:
    """
    Marks landmarks on the image based on node coordinates extracted from the skeleton summary DataFrame.

    Parameters:
        - image (Any): The image on which to draw the landmarks.
        - nodes_summary (pd.DataFrame): DataFrame containing summary of skeleton nodes.
        - main_root_src (List[int]): List of node IDs for main root sources.
        - main_root_dest (List[int]): List of node IDs for main root destinations.

    Returns:
        Any: The image with landmarks drawn on it.
    """
    logger.info("Marking landmarks on the image.")

    image = np.clip(image * 300, 0, 255).astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    # Define colors
    blue = (255, 0, 0)
    red = (0, 0, 255)
    green = (0, 255, 0)

    # Extract, lateral roots, and junctions from the summary
    lateral_roots = nodes_summary.loc[
        nodes_summary["branch-type"] == 1, "node-id-dst"
    ].tolist()
    junctions = nodes_summary.loc[
        nodes_summary["branch-type"] == 2, "node-id-src"
    ].tolist()

    # Remove main_root_src and main_root_dest from list to mark as junction or lateral tip
    for src, dest in zip(main_root_src, main_root_dest):
        if src in junctions:
            junctions.remove(src)
        if dest in junctions:
            junctions.remove(dest)
        if src in lateral_roots:
            lateral_roots.remove(src)
        if dest in lateral_roots:
            lateral_roots.remove(dest)

    # Draw main roots
    for src, dest in zip(main_root_src, main_root_dest):
        for node in [src, dest]:
            # Define if the start/end is branch or endpoint and act accordingly
            if node in nodes_summary["node-id-src"].values:
                coord = nodes_summary.loc[
                    nodes_summary["node-id-src"] == node, ["coord-src-0", "coord-src-1"]
                ].values[0]
            elif node in nodes_summary["node-id-dst"].values:
                coord = nodes_summary.loc[
                    nodes_summary["node-id-dst"] == node, ["coord-dst-0", "coord-dst-1"]
                ].values[0]
            image = cv2.circle(image, (int(coord[1]), int(coord[0])), 15, blue, 5)

    # Draw lateral roots
    for node in lateral_roots:
        coord = nodes_summary.loc[
            nodes_summary["node-id-dst"] == node, ["coord-dst-0", "coord-dst-1"]
        ].values[0]
        image = cv2.circle(image, (int(coord[1]), int(coord[0])), 15, red, 5)

    # Draw junctions
    for node in junctions:
        coord = nodes_summary.loc[
            nodes_summary["node-id-src"] == node, ["coord-src-0", "coord-src-1"]
        ].values[0]
        image = cv2.circle(image, (int(coord[1]), int(coord[0])), 15, green, 5)

    return image


def process_image_for_roots(
    image: np.ndarray, expected_nr_plants: int = 5
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Processes an image to segment roots, calculate root lengths, and mark landmarks.

    Parameters:
        - image (np.ndarray): Mask of the roots.
        - expected_nr_plants (int): expected number of plants withing the petri dish

    Returns:
        - Tuple[pd.DataFrame, np.ndarray]: A DataFrame with root lengths and the image with landmarks.
    """

    # Segment roots from the image
    segmented_roots = segment_roots(image, expected_nr_plants)

    # Create root skeletons and supparize them
    root_skeleton = skeletonize(segmented_roots)
    summary = summarize(Skeleton(root_skeleton))

    # Calculate root lengths
    root_lengths = calculate_root_lengths(summary)

    # Create a summary DataFrame for nodes
    nodes_summary = pd.DataFrame(summary)

    # Extract main root source and destination IDs
    main_root_src = [info["main_root_src"] for info in root_lengths.values()]
    main_root_dest = [info["main_root_dest"] for info in root_lengths.values()]

    # Mark landmarks on the original image
    marked_image = mark_landmarks(image, nodes_summary, main_root_src, main_root_dest)

    root_tip_coords = []

    for node_id in main_root_dest:
        coords = nodes_summary[nodes_summary["node-id-dst"] == node_id][
            ["coord-dst-0", "coord-dst-1"]
        ].values.tolist()
        root_tip_coords.extend(coords)

    return root_lengths, root_tip_coords, marked_image
