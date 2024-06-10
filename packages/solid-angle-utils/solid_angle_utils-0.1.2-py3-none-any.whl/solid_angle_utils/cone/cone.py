import numpy as np


def solid_angle(half_angle_rad):
    """
    Returns cone's solid_angle in sr.
    """
    cap_hight = 1.0 - np.cos(half_angle_rad)
    return 2.0 * np.pi * cap_hight


def half_angle(solid_angle_sr):
    """
    Returns cone's half-angle in rad.
    """
    cap_hight = solid_angle_sr / (2.0 * np.pi)
    return np.arccos(-cap_hight + 1.0)


def half_angle_space(start_half_angle_rad, stop_half_angle_rad, num):
    """
    Returns the half-angles of cones where every next larger cone has the same
    additional amount of solid angle.

    So this is a linear spacing in the cone's solid angles.
    """
    return half_angle(
        np.linspace(
            start=solid_angle(start_half_angle_rad),
            stop=solid_angle(stop_half_angle_rad),
            num=num,
        )
    )
