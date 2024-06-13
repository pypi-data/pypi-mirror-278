# SPDX-License-Identifier: Apache-2.0

"""
Handles the spatial point pattern generation and spatial indexing for the cell placement
"""

import numpy
from brain_indexer import SphereIndexBuilder


class SpatialSpherePattern:
    """Data Structure for a sphere collection embedded in space,
    registered in an Rtree index.

    Args:
        max_spheres : int
            Maximum Number of spheres in the pattern.

    Attributes:
        coordinates: 2D array
            Coordinates of the centers of the spheres stored in the pattern
        radii: 1D array
            Respective radii
        index: int
            The current position in the coordinates / radii arrays.
        si: sphere_rtree
            The rtree spatial index data structure
    """

    def __init__(self, max_spheres):
        self._coordinates = numpy.zeros((max_spheres, 3), dtype=numpy.float64)
        self._radii = numpy.zeros(max_spheres, dtype=numpy.float64)

        self._index = 0

        self._si = SphereIndexBuilder.create_empty()

    def __getitem__(self, pos):
        """Get sphere center and radius at position pos"""
        assert pos < self._index
        return self._coordinates[pos], self._radii[pos]

    def __len__(self):
        """Number of elements in the index"""
        return self._index

    @property
    def coordinates(self):
        """Returns a view of the stored coordinates"""
        return self._coordinates[: self._index]

    @property
    def radii(self):
        """Returns a view of the stored radii"""
        return self._radii[: self._index]

    def add(self, position, radius):
        """Add a sphere with index in the pattern and register it in the spatial index
        numpy array positional index is stored as id in RTree object
        """
        self._coordinates[self._index] = position
        self._radii[self._index] = radius

        self._si.insert(centroid=position, radius=radius, id=self._index)
        self._index += 1

    def is_intersecting(self, new_position, new_radius):
        """Checks if the new sphere intersects with another from
        the index. RTree intersection iterator is empty in case of
        no hits which raises a StopIteration exception.

        Args:
            new_position: 1D array
            new_radius: float

        Returns: Bool
            True if there is intersection with another object.
        """
        return not self._si.sphere_empty(new_position, new_radius)

    def distance_to_nearest_neighbor(self, trial_position, max_distance):
        """Return the distance to the nearest centroid within `max_distance`.

        Note, that only neighbours that overlap with the sphere
        `(trial_position, max_distance)` are considered. If there are no
        neighbours within this distance the method returns `np.inf`.
        """

        trial_position = numpy.reshape(trial_position, (3,))

        candidates = self._si.sphere_query(trial_position, max_distance)
        centroids = candidates["centroid"]

        if numpy.size(centroids) > 0:
            return numpy.sqrt(numpy.min(numpy.sum((centroids - trial_position) ** 2, axis=1)))

        return numpy.inf
