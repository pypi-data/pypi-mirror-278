# SPDX-License-Identifier: Apache-2.0

"""Morphology synthesis data structures"""
from collections import namedtuple

EndfeetData = namedtuple("EndfeetData", ["ids", "targets", "area_meshes"])

AstrocyteProperties = namedtuple(
    "AstrocyteProperties", ["name", "soma_position", "soma_radius", "microdomain"]
)

SpaceColonizationData = namedtuple("SpaceColonizationData", ["point_cloud"])

EndfeetAttractionData = namedtuple("EndfeetAttractionData", ["targets"])

TNSData = namedtuple("TNSData", ["parameters", "distributions", "context"])

SynthesisInputPaths = namedtuple(
    "SynthesisInputPaths",
    [
        "astrocytes",
        "microdomains",
        "neuronal_connectivity",
        "gliovascular_connectivity",
        "neuroglial_connectivity",
        "tns_parameters",
        "tns_distributions",
        "tns_context",
        "er_data",
        "morphology_directory",
        "endfeet_meshes",
    ],
)
