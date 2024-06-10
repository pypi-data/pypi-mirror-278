import numpy as np
import warnings


def solid_angle(v0, v1, v2, delta_r=1e-6, delta_phi=np.deg2rad(1e-2)):
    """
    Returns the solid angle of a spherical triangle on the unit-sphere.

    Parameters
    ----------
    v0 : np.array(3)
        First vertex of triangle.
    v1 : np.array(3)
        Second vertex of triangle.
    v2 : np.array(3)
        Third vertex of triangle.
    delta_r : float
        Max. accepted deviation from a vertex [v0, v1, v2] to the unit-sphere.
    delta_phi : float
        When all the angles between the vertices are smaller than delta_phi,
        the solid angle is computed with an algorithm for flat, non spherical
        triangles to prevent numerical issues.
    Returns
    -------
    solid angle : float
    """
    v0 = np.array(v0)
    v1 = np.array(v1)
    v2 = np.array(v2)
    norm = np.linalg.norm
    assert np.abs(norm(v0) - 1) <= delta_r
    assert np.abs(norm(v1) - 1) <= delta_r
    assert np.abs(norm(v2) - 1) <= delta_r

    a01 = _angle_between(v0, v1)
    a12 = _angle_between(v1, v2)
    a20 = _angle_between(v2, v0)
    angles_are_small = np.array([a01, a12, a20]) < delta_phi

    if np.all(angles_are_small):
        return _area_of_flat_triangle(v0=v0, v1=v1, v2=v2)
    else:
        if np.any(angles_are_small):
            warnings.warn(
                (
                    "The angles between the spherical triangle are neither "
                    "all small nor are they all large. This might result in "
                    "numerically unstable results. "
                    "When all angles are small it is safe to approximate "
                    "the solid angle with the area of a flat triangle. "
                    "When all angles are large it is safe to approximate "
                    "the solid angle with Girad's algorithm. "
                ),
                RuntimeWarning,
            )
        return _solid_angle_of_spherical_triangle_according_to_girad(
            v0=v0, v1=v1, v2=v2
        )


def _area_of_flat_triangle(v0, v1, v2):
    """
    Returns the area of a flat triangle with vertices v0, v1, and v2.

    Parameters
    ----------
    v0 : np.array(3)
        First vertex of triangle.
    v1 : np.array(3)
        Second vertex of triangle.
    v2 : np.array(3)
        Third vertex of triangle.
    """
    l01 = v1 - v0
    l21 = v1 - v2
    return np.linalg.norm(np.cross(l01, l21)) / 2.0


def _solid_angle_of_spherical_triangle_according_to_girad(v0, v1, v2):
    """
    Returns the solid angle of a spherical triangle on the unit-sphere.

    According to girads theorem:
        solid angle = radius ** 2 * excess-angle
        excess-angle = (alpha + beta + gamma - pi)
        alpha: angle between line(v0, v1) and line(v0, v2)
        beta: angle between line(v1, v0) and line(v1, v2)
        gamma: angle between line(v2, v0) and line(v2, v1)
        v0, v1, v2 are the vertices of the triangle:

    Parameters
    ----------
    v0 : np.array(3)
        First vertex of triangle.
    v1 : np.array(3)
        Second vertex of triangle.
    v2 : np.array(3)
        Third vertex of triangle.
    """
    alpha = _angle_between(_surface_tangent(v0, v1), _surface_tangent(v0, v2))
    beta = _angle_between(_surface_tangent(v1, v0), _surface_tangent(v1, v2))
    gamma = _angle_between(_surface_tangent(v2, v0), _surface_tangent(v2, v1))

    excess_angle = alpha + beta + gamma - np.pi
    return excess_angle


def _angle_between(a, b):
    """
    Returns the angle between the vectors a, and b.

    Parameters
    ----------
    a : 3 floats (list, array, tuple)
        Point 'a' on the unit-sphere.
    b  : 3 floats (list, array, tuple)
        Point 'b' on the unit-sphere.

    Returns
    -------
    angle : float
    """
    dot = np.dot
    norm = np.linalg.norm
    acos = np.arccos
    return acos(dot(a, b) / (norm(a) * norm(b)))


def _surface_tangent(a, b):
    """
    Returns the direction of the great-circle-arc which goes from point a to
    b and is located in point a.

    Parameters
    ----------
    a : 3 floats (list, array, tuple)
        Point 'a' on the unit-sphere.
    b  : 3 floats (list, array, tuple)
        Point 'b' on the unit-sphere.

    Returns
    -------
    tangent : vector dim 3
        Direction-vector perpendicular to a and pointing in the
        great-circle-arc's direction towards b.
    """
    a = np.array(a)
    b = np.array(b)
    ray_support = b
    ray_direction = a
    lam = _ray_parameter_for_closest_distance_to_point(
        support_vector=ray_support,
        direction_vector=ray_direction,
        point=a,
    )
    closest_point = ray_support + lam * ray_direction
    tangent = closest_point - a
    assert np.abs(_angle_between(tangent, a) - np.pi / 2) < 1e-6
    return tangent


def _ray_parameter_for_closest_distance_to_point(
    support_vector, direction_vector, point
):
    """
    Returns the ray-parameter (lambda) which marks the ray's closest position
    to point.

    Ray-equation:
        vec{ray}(lambda) = vec{support_vector} + lambda * vec{direction_vector}

    Parameters
    ----------
    support_vector : 3 floats (list, array, tuple)
        Ray's support vector
    direction_vector : 3 floats (list, array, tuple)
        Ray's direction vector
    point : 3 floats (list, array, tuple)
        The point to estimate the closest point on the ray to.

    Returns
    -------
    lambda : float
        Parameter of ray. See ray-equation.
    """
    d = np.dot(direction_vector, point)
    return d - np.dot(support_vector, direction_vector)
