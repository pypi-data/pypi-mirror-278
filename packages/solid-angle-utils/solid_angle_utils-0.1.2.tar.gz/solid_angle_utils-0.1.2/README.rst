#################
Solid Angle Utils
#################
|TestStatus| |PyPiStatus| |BlackStyle|

A python-package to help with solid angles.

*******
install
*******

.. code:: bash

    pip install solid_angle_utils


**************************
simple conversion of units
**************************

Inspired by ``numpy`` ``rad2deg`` and ``deg2rad``.

.. code:: python

    import solid_angle_utils

    a_sr = solid_angle_utils.squaredeg2sr(10)
    print(a)
    0.0030461741978670856

    a_sqdeg = solid_angle_utils.sr2squaredeg(a_sr)
    print(a_sqdeg)
    10.0


*****
Cones
*****

Convert solid angle to half angle, and the other way around.

.. code:: python

    import solid_angle_utils

    cone_sa = solid_angle_utils.cone.solid_angle(half_angle_rad=0.1)
    0.031389755322205774

    cone_ha = solid_angle_utils.cone.half_angle(solid_angle_sr=cone_sa)
    0.0999999

    solid_angle_utils.cone.half_angle_space(0, 0.1, 3)
    array([0.        , 0.07069594, 0.1       ])


*********
Triangles
*********

Estimate the solid angle of a spherical triangle.

.. code:: python

    import solid_angle_utils
    import numpy as np

    x, y, z = np.eye(3)
    full_sphere_solid_angle = 4 * np.pi

    triangle_solid_angle = solid_angle_utils.triangle.solid_angle(
        v0=x, v1=y, v2=z
    )

    print("Expect 1/8: ", triangle_solid_angle/full_sphere_solid_angle)




.. |BlackStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |TestStatus| image:: https://github.com/cherenkov-plenoscope/solid_angle_utils/actions/workflows/test.yml/badge.svg?branch=main
    :target: https://github.com/cherenkov-plenoscope/solid_angle_utils/actions/workflows/test.yml

.. |PyPiStatus| image:: https://img.shields.io/pypi/v/solid_angle_utils
    :target: https://pypi.org/project/solid_angle_utils
