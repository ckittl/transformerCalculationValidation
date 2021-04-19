import logging
import os
from math import copysign, atan, pi


def __calc_current_angle(p: float = 0.0, q: float = 0.0, phi_v_degree: float = 0.0):
    """
    Method to calc the current's angle based on the given active and reactive power, as well as the equivalent
    nodal voltage current. You have to make sure, that p and q are given in the same units

    The arctangent "only" calculates the angle between the complex current and it's real part. This means, that
    i = Complex(i_real, i_imag) and i' = Comples(-i_real, -i_imag) will lead to the same angle. However, for
    power system simulation, the absolute orientation in the complex plain with regard to the positive real axis
    is of interest. Therefore, additional 180° are added, if the real part of the current is negative.

    Parameters:
        p (float): Active power
        q (float): Reactive power
        phi_v_degree (float): Nodal voltage angle in degrees

    Returns:
        float: Current angle in degrees
    """
    if p == 0.0:
        if q == 0.0:
            # Active and reactive power are zero. Thus assume it's angle is zero.
            phi_s_degree = 0.0
        else:
            # Active power is zero, but reactive power not. Therefore, the angle is +/- 180°
            phi_s_degree = copysign(180.0, q)
    elif p >= 0.0:
        phi_s_degree = atan(q / p) / pi * 180.0
    else:
        phi_s_degree = atan(q / p) / pi * 180.0 + 180.0
    return phi_v_degree - phi_s_degree


class TestBench:

    def __init__(self):
        # --- Set up the logging ---
        self.logger = logging.getLogger()
        self.logger.setLevel(level=logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s - %(message)s')

        # Create a file handler
        log_directory = os.path.join("..", "..", "..", "log")
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        log_file = os.path.join(log_directory, "test_bench.log")
        file_handler = logging.FileHandler(log_file, 'w')
        file_handler.setLevel(level=logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level=logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
