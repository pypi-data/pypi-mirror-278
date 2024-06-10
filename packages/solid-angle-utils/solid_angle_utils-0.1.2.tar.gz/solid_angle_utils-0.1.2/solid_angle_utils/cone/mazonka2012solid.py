import numpy as np
from . import cone


def intersection_of_two_cones(
    half_angle_one_rad,
    half_angle_two_rad,
    angle_between_cones,
    epsilon_rad=np.deg2rad(1 / 100),
):
    """
    Returns the intersecting solid angle of two cones.
    Algorithm by Mazonka, Oleg.

    Parameters
    ----------
    half_angle_one_rad : float
        First cone's half angle
    half_angle_two_rad : float
        Second cone's half angle
    angle_between_cones : float
        Angle between axis of the two cones.
    epsilon_rad : float
        Critical angle to use approximations instead.

    Returns
    -------
    solid angle : float
        The intersecting solid angle ot two cones.

    Reference
    ---------
    @article{mazonka2012solid,
        title={
            Solid angle of conical surfaces, polyhedral cones,
            and intersecting spherical caps
        },
        author={Mazonka, Oleg},
        journal={arXiv preprint arXiv:1205.1396},
        year={2012}
    }
    """
    result, _ = _intersection_of_two_cones_with_debug(
        half_angle_one_rad=half_angle_one_rad,
        half_angle_two_rad=half_angle_two_rad,
        angle_between_cones=angle_between_cones,
        epsilon_rad=epsilon_rad,
    )
    return result


def _intersection_of_two_cones_with_debug(
    half_angle_one_rad,
    half_angle_two_rad,
    angle_between_cones,
    epsilon_rad,
):
    assert epsilon_rad >= 0.0
    assert angle_between_cones >= 0.0
    assert half_angle_one_rad >= 0.0
    assert half_angle_two_rad >= 0.0

    PI = np.pi

    if half_angle_one_rad > half_angle_two_rad:
        theta1 = half_angle_one_rad
        theta2 = half_angle_two_rad
    else:
        theta2 = half_angle_one_rad
        theta1 = half_angle_two_rad

    alpha = angle_between_cones

    # this check is not metioned, but my foo is not strong enough to make
    # the mentioned cases work without this.
    if alpha > half_angle_one_rad + half_angle_two_rad:
        return (0.0, "no overlap")

    # case 4.4.2 Inverted cones
    if theta1 > PI / 2:
        return (
            _cone(theta2)
            - _cone_segment(
                thetaA=PI - theta1,
                thetaB=theta2,
                alpha=PI - alpha,
            ),
            "4.4.2 Inverted cones",
        )

    # case 4.4.3 Co-directed cone
    if alpha < epsilon_rad:
        return (min([_cone(theta1), _cone(theta2)]), "4.4.3 Co-directed cone")

    # case 4.4.4 Counter-directed cones
    if alpha > PI - epsilon_rad:
        omega1 = _cone_segment(
            thetaA=theta1,
            thetaB=theta2,
            alpha=alpha,
        )
        omega2 = _cone_segment(
            thetaA=theta2,
            thetaB=theta1,
            alpha=alpha,
        )
        if omega1 + omega2 < 4 * PI:
            return (
                omega1 + omega2,
                "4.4.4 Counter-directed cones, omega1 + omega2 < 4 * PI",
            )
        else:
            return (0.0, "4.4.4 Counter-directed cones, else")

    # case 4.4.5 Narrow cone
    if 0.0 < theta2 < epsilon_rad:
        gamma2 = alpha - theta1
        if gamma2 > theta2:
            return (0.0, "4.4.5 Narrow cone, gamma2 > theta2")
        elif gamma2 < -theta2:
            return (_cone(theta2), "4.4.5 Narrow cone, gamma2 < -theta2")
        else:
            return (
                _cone(theta2) * (gamma2 + theta2) / (2 * theta2),
                "4.4.5 Narrow cone, else",
            )

    # 4.4.6 two hemispheres
    if theta1 > PI / 2 - epsilon_rad and theta2 > PI / 2 - epsilon_rad:
        return (2.0 * (PI - alpha), "4.4.6 two hemispheres")

    """
    # case 4.4.7 one hemisphere
    if theta1 > PI / 2 - epsilon_rad:
        return (
            _cone_segment(
                thetaA=theta2,
                thetaB=theta1,
                alpha=alpha - PI / 2,
            ),
            "4.4.7 one hemisphere",
        )
    """

    return (
        _cone_segment(
            thetaA=theta1,
            thetaB=theta2,
            alpha=alpha,
        )
        + _cone_segment(
            thetaA=theta2,
            thetaB=theta1,
            alpha=alpha,
        ),
        "default",
    )


def _cone(theta):
    # Eq 47
    return cone.solid_angle(half_angle_rad=theta)


def _cone_segment(thetaA, thetaB, alpha):
    cos = np.cos
    sin = np.sin
    acos = np.arccos
    sq = np.sqrt

    # Eq 48
    ty = cos(thetaB) - cos(alpha) * cos(thetaA)
    tx = sin(alpha) * cos(thetaA)

    # Eq 49
    cos_phi = _limiting((ty * cos(thetaA)) / (tx * sin(thetaA)))

    # Eq 50
    cos_beta = _limiting(ty / (sin(thetaA) * sq(tx**2 + ty**2)))

    phi = acos(cos_phi)
    beta = acos(cos_beta)

    # Eq 45
    segment_solid_angle = 2.0 * (beta - phi * cos(thetaA))
    return segment_solid_angle


def _limiting(x, start=-1.0, stop=1.0):
    # Eq 51
    if x > stop:
        return stop
    elif x < start:
        return start
    else:
        return x
