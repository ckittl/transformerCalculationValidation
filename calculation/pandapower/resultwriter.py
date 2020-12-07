import logging
import os
import csv
from math import cos, sin, atan, pi, sqrt


class ResultWriter:
    """
    This class serves as a result writer for pandapower's power flow results to a csv file. As the pandapower results
    are given in a different format then what we need, this class also takes care of converting the results into the
    correct form
    """

    logger = logging.getLogger()
    file = None
    csv_writer = None
    header = [
        'tap_pos',
        'p_set_pu',
        'e_pu',
        'f_pu',
        'v_pu',
        'i_mag_hv_a',
        'i_ang_hv_degree',
        'i_mag_lv_a',
        'i_ang_lv_degree',
        'p_hv_kw',
        'q_hv_kvar',
        's_hv_kva',
        'p_lv_kw',
        'q_lv_kvar',
        's_lv_kva',
    ]

    def __init__(self, rel_path="", file_name=""):
        # Prepare the output file by setting up all directories
        os.makedirs(os.path.relpath(rel_path), exist_ok=True)
        self.file = open(rel_path + file_name, 'wt', newline='')
        try:
            self.csv_writer = csv.writer(self.file)
            self.csv_writer.writerow(self.header)
        except Exception as e:
            self.logger.error("Error during writing of head line")
            self.file.close()
            raise e

    def write_result(self, tap_pos=0, p_pu=0.0, net=None):
        """
        This method calculates the desired results and writes them to the previously defined file
        """
        # Nodal voltages at the low voltage node of the transformer
        v_pu = net.res_bus.vm_pu[1]
        e_pu = v_pu * cos(net.res_bus.va_degree[1] / 180 * pi)  # Real part of nodal voltage
        f_pu = v_pu * sin(net.res_bus.va_degree[1] / 180 * pi)  # Imaginary part of nodal voltage

        # Power at high voltage node
        p_hv_kw = net.res_trafo.p_hv_mw * 1000.0
        q_hv_kvar = net.res_trafo.q_hv_mvar * 1000.0
        s_hv_kva = sqrt(pow(p_hv_kw, 2) + pow(q_hv_kvar, 2))

        # Current at high voltage node
        i_mag_hv_a = net.res_trafo.i_hv_ka[0] * 1000.0  # Port current at high voltage node
        i_ang_hv_degree = self.__calc_current_angle(p_hv_kw, q_hv_kvar, 0.0)

        # Power at low voltage node
        p_lv_kw = net.res_trafo.p_lv_mw * 1000.0
        q_lv_kvar = net.res_trafo.q_lv_mvar * 1000.0
        s_lv_kva = sqrt(pow(p_lv_kw, 2) + pow(q_lv_kvar, 2))

        # Current at high voltage node
        i_mag_lv_a = net.res_trafo.i_lv_ka[0] * 1000.0  # Port current at high voltage node
        phi_v_lv_degree = atan(f_pu / e_pu) / pi * 180.0
        i_ang_lv_degree = self.__calc_current_angle(p_lv_kw, q_lv_kvar, phi_v_lv_degree)

        # Prepare the csv row and write it to file
        row = [
            tap_pos,  # Current tap position
            "%0.1f" % p_pu,  # Chosen loading in p.u.
            "%0.12f" % e_pu,  # Low voltage nodal voltage - real part
            "%0.12f" % f_pu,  # Low voltage nodal voltage - imaginary part
            "%0.12f" % v_pu,  # Low voltage nodal voltage - magnitude
            "%0.12f" % i_mag_hv_a,  # High voltage port current - magnitude
            "%0.12f" % i_ang_hv_degree,  # High voltage port current - angle
            "%0.12f" % i_mag_lv_a,  # Low voltage port current - magnitude
            "%0.12f" % i_ang_lv_degree,  # Low voltage port current - angle
            "%0.9f" % p_hv_kw,  # High voltage port active power
            "%0.9f" % q_hv_kvar,  # High voltage port reactive power
            "%0.9f" % s_hv_kva,  # High voltage port apparent power
            "%0.9f" % p_lv_kw,  # Low voltage port active power
            "%0.9f" % q_lv_kvar,  # Low voltage port reactive power
            "%0.9f" % s_lv_kva  # High voltage port apparent power
        ]
        try:
            self.csv_writer.writerow(row)
        except Exception as e:
            self.logger.error("Error during writing of result for tap_pos = %i and p = %.3f" % (tap_pos, p_pu))
            self.file.close()
            raise e

    @staticmethod
    def __calc_current_angle(p=0.0, q=0.0, phi_v_degree=0.0):
        """
        Method to calc the current's angle based on the given active and reactive power, as well as the equivalent
        nodal voltage current. You have to make sure, that p and q are given in the same units

        The arctangent "only" calculates the angle between the complex current and it's real part. This means, that
        i = Complex(i_real, i_imag) and i' = Comples(-i_real, -i_imag) will lead to the same angle. However, for
        power system simulation, the absolute orientation in the complex plain with regard to the positive real axis
        is of interest. Therefore, additional 180° are added, if the real part of the current is negative.

        Parameters:
            p (double): Active power
            q (double): Reactive power
            phi_v_degree (double): Nodal voltage angle in degrees

        Returns:
            double: Current angle in degrees
        """
        if (p >= 0.0).bool():
            phi_s_degree = atan(q / p) / pi * 180.0
        else:
            phi_s_degree = atan(q / p) / pi * 180.0 + 180.0
        return phi_v_degree - phi_s_degree

    def shutdown(self):
        """
        Shuts down the writer (closing the result file)
        """
        self.file.close()
