# SPDX-License-Identifier: Apache-2.0

""" Facade classes for NGV connectivity
"""

# pylint: disable = no-name-in-module

import logging

import numpy as np
import pandas as pd

from archngv.building.connectivity.detail.gliovascular_generation.graph_connect import (
    domains_to_vasculature,
)
from archngv.building.connectivity.detail.gliovascular_generation.graph_reachout import strategy
from archngv.building.connectivity.detail.gliovascular_generation.graph_targeting import (
    create_targets,
)
from archngv.building.connectivity.detail.gliovascular_generation.surface_intersection import (
    surface_intersect,
)

L = logging.getLogger(__name__)


def _vasculature_annotation_from_edges(vasculature, edge_indices):
    edge_properties = vasculature.edge_properties
    return (
        edge_properties.loc[edge_indices, "section_id"].to_numpy(dtype=np.int64),
        edge_properties.loc[edge_indices, "segment_id"].to_numpy(dtype=np.int64),
    )


def _create_point_sampling_on_vasculature_skeleton(vasculature, graph_targeting_params):
    positions, edge_indices = create_targets(
        vasculature.points, vasculature.edges, graph_targeting_params
    )

    L.info("STEP 1: Generation of potential targets completed.")
    L.info("%s potential targets generated.", len(positions))
    L.debug("Parameters: %s", graph_targeting_params)
    L.debug("Positions: %s\nVasculature Edges: %s", positions, edge_indices)

    L.info("STEP 2: Connection of astrocytes with vasculature started.")

    beg_radii, end_radii = 0.5 * vasculature.segment_diameters
    radii = np.min((beg_radii[edge_indices], end_radii[edge_indices]), axis=0)

    section_ids, segment_ids = _vasculature_annotation_from_edges(vasculature, edge_indices)

    return pd.DataFrame(
        {
            "x": positions[:, 0],
            "y": positions[:, 1],
            "z": positions[:, 2],
            "r": radii,
            "edge_index": edge_indices,
            "vasculature_section_id": section_ids,
            "vasculature_segment_id": segment_ids,
        }
    )


def generate_gliovascular(cell_ids, astrocytic_positions, astrocytic_domains, vasculature, params):
    """For each astrocyte id find the connections to the vasculature

    Args:
        cell_ids: array[int, (N,)]
        astrocyte_positions: array[float, (N, 3)]
        astrocytic_domains: Microdomains
        vasculature: Vasculature
        params: gliovascular parameters dict

    Returns:
        endfeet_positions: array[float, (M, 3)]
        graph_positions: array[float, (M, 3)]
        endfeet_to_astrocyte_mapping: array[int, (M,)]
        endfeet_to_vasculature_mapping: array[int, (M, 2)]
            section_id, segment_id for each endfoot
    """
    L.info("STEP 1: Generating potential targets...")
    skeleton_seeds = _create_point_sampling_on_vasculature_skeleton(
        vasculature, params["graph_targeting"]
    )

    L.info("STEP 2: Connecting astrocytes with vasculature skeleton graph...")
    astrocyte_skeleton_pairs = domains_to_vasculature(
        cell_ids,
        strategy(params["connection"]["reachout_strategy"]),
        skeleton_seeds,
        astrocytic_domains,
        params["connection"],
    )

    L.info("STEP 3: Mapping from graph points to vasculature surface...")
    (
        endfeet_positions,
        endfeet_astrocyte_edges,
        endfeet_vasculature_edge_indices,
    ) = surface_intersect(
        astrocytic_positions, skeleton_seeds, astrocyte_skeleton_pairs, vasculature
    )

    # translate the vasculature edge indices to section and segment ids
    section_ids, segment_ids = _vasculature_annotation_from_edges(
        vasculature, endfeet_vasculature_edge_indices
    )
    endfeet_to_vasculature = np.column_stack((section_ids, segment_ids))

    return (endfeet_positions, endfeet_astrocyte_edges, endfeet_to_vasculature)


def generate_gliovascular_edge_properties(astrocytes, astrocytic_domains, vasculature, params):
    """Generate edge population edge population source/target ids and properties."""
    (
        endfoot_surface_positions,
        endfeet_to_astrocyte_mapping,
        endfeet_to_vasculature_mapping,
    ) = generate_gliovascular(
        cell_ids=np.arange(len(astrocytes), dtype=np.int64),
        astrocytic_positions=astrocytes.positions,
        astrocytic_domains=astrocytic_domains,
        vasculature=vasculature,
        params=params,
    )

    assert (
        len(endfeet_to_astrocyte_mapping)
        == len(endfeet_to_vasculature_mapping)
        == len(endfoot_surface_positions)
    )

    # get the section/segment ids and use them to get the vasculature node ids
    vasculature_properties = vasculature.edge_properties.loc[:, ["section_id", "segment_id"]]
    vasculature_properties["index"] = vasculature_properties.index
    vasculature_properties = vasculature_properties.set_index(["section_id", "segment_id"])

    indices = pd.MultiIndex.from_arrays(endfeet_to_vasculature_mapping.T)
    vasculature_ids = vasculature_properties.loc[indices, "index"].to_numpy()

    properties = {
        "endfoot_id": np.arange(len(endfeet_to_astrocyte_mapping), dtype=np.uint64),
        "endfoot_surface_x": endfoot_surface_positions[:, 0].astype(np.float32),
        "endfoot_surface_y": endfoot_surface_positions[:, 1].astype(np.float32),
        "endfoot_surface_z": endfoot_surface_positions[:, 2].astype(np.float32),
        "vasculature_section_id": endfeet_to_vasculature_mapping[:, 0].astype(np.uint32),
        "vasculature_segment_id": endfeet_to_vasculature_mapping[:, 1].astype(np.uint32),
    }

    return endfeet_to_astrocyte_mapping, vasculature_ids, properties
