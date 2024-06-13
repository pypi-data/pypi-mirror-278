import numpy

from archngv.spatial import utils as _ut
from archngv.utils.ngons import vectorized_triangle_normal


def test_are_normals_backward():
    points = numpy.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])

    face_vertices = numpy.array([[3, 1, 0], [2, 1, 0], [2, 3, 0], [2, 3, 1]])

    face_normals = numpy.array(
        [
            [0.0, 0.0, -1.0],
            [0.0, -1.0, -0.0],
            [-1.0, 0.0, 0.0],
            [0.57735027, 0.57735027, 0.57735027],
        ]
    )

    centroid = numpy.mean(points, axis=0)

    assert not numpy.any(_ut.are_normals_backward(centroid, points, face_vertices, face_normals))


def test_make_normals_outwards():
    def calc_normals(points, triangles):
        v1s = points[triangles[:, 1]] - points[triangles[:, 0]]
        v2s = points[triangles[:, 2]] - points[triangles[:, 0]]

        normals = vectorized_triangle_normal(v1s, v2s)

        return normals

    points = numpy.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])
    old_triangles = numpy.array([[3, 1, 0], [2, 1, 0], [2, 3, 0], [2, 3, 1]])
    old_normals = calc_normals(points, old_triangles)

    centroid = numpy.mean(points, axis=0)

    new_triangles = _ut.make_normals_outward(centroid, points, old_triangles)
    new_normals = calc_normals(points, new_triangles)

    msg = [
        "{} {} {} {}".format(row1, val1, row2, val2)
        for row1, val1, row2, val2 in zip(old_triangles, old_normals, new_triangles, new_normals)
    ]

    msg = "\n" + "\n".join(msg)

    are_backward = _ut.are_normals_backward(centroid, points, new_triangles, new_normals)

    msg += "\n{}\n".format(are_backward)
    assert not numpy.any(are_backward), msg
