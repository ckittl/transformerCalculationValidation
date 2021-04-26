from math import ceil, floor, cos, pi, sin, sqrt, atan

import pandapower as pp
from numpy import arange, ndarray

from calculation.pandapower.GridResultThreeWinding import GridResultThreeWinding
from calculation.pandapower.TestBench import TestBench, __calc_current_angle
from calculation.pandapower.TestGrid import test_grid_three_winding


def extract_results(net: pp.pandapowerNet = None) -> GridResultThreeWinding:
    """
    Extract results of interest from provided pandapower net

    Parameters:
        net (pandapowerNet): pandapower's net model, additionally carrying results of last simulation

    Returns:
        GridResultThreeWinding: A container class holding all information of interest
    """
    # --- Medium voltage node ---
    # Nodal voltage
    v_mv_pu = net.res_bus.vm_pu[1]
    e_mv_pu = v_mv_pu * cos(net.res_bus.va_degree[1] / 180 * pi)  # Real part of nodal voltage
    f_mv_pu = v_mv_pu * sin(net.res_bus.va_degree[1] / 180 * pi)  # Imaginary part of nodal voltage

    # Power
    p_mv_kw = net.res_trafo3w.p_mv_mw[0] * 1000.0
    q_mv_kvar = net.res_trafo3w.q_lv_mvar[0] * 1000.0
    s_mv_kva = sqrt(pow(p_mv_kw, 2) + pow(q_mv_kvar, 2))

    # Current at high voltage node
    i_mag_mv_a = net.res_trafo3w.i_mv_ka[0] * 1000.0
    phi_v_mv_degree = atan(f_mv_pu / e_mv_pu) / pi * 180.0
    i_ang_mv_degree = __calc_current_angle(p_mv_kw, q_mv_kvar, phi_v_mv_degree)

    # --- Medium voltage node ---
    # Nodal voltage
    v_lv_pu = net.res_bus.vm_pu[2]
    e_lv_pu = v_lv_pu * cos(net.res_bus.va_degree[2] / 180 * pi)  # Real part of nodal voltage
    f_lv_pu = v_lv_pu * sin(net.res_bus.va_degree[2] / 180 * pi)  # Imaginary part of nodal voltage

    # Power
    p_lv_kw = net.res_trafo3w.p_lv_mw[0] * 1000.0
    q_lv_kvar = net.res_trafo3w.q_lv_mvar[0] * 1000.0
    s_lv_kva = sqrt(pow(p_lv_kw, 2) + pow(q_lv_kvar, 2))

    # Current
    i_mag_lv_a = net.res_trafo3w.i_mv_ka[0] * 1000.0
    phi_v_lv_degree = atan(f_lv_pu / e_lv_pu) / pi * 180.0
    i_ang_lv_degree = __calc_current_angle(p_lv_kw, q_lv_kvar, phi_v_lv_degree)

    # --- High voltage node ---
    # Power
    p_hv_kw = net.res_trafo3w.p_hv_mw[0] * 1000.0
    q_hv_kvar = net.res_trafo3w.q_hv_mvar[0] * 1000.0
    s_hv_kva = sqrt(pow(p_hv_kw, 2) + pow(q_hv_kvar, 2))

    # Current
    i_mag_hv_a = net.res_trafo3w.i_hv_ka[0] * 1000.0
    i_ang_hv_degree = __calc_current_angle(p_hv_kw, q_hv_kvar, 0.0)

    return GridResultThreeWinding(v_mv_pu=v_mv_pu, e_mv_pu=e_mv_pu, f_mv_pu=f_mv_pu, v_lv_pu=v_lv_pu, e_lv_pu=e_lv_pu,
                                  f_lv_pu=f_lv_pu, p_hv_kw=p_hv_kw, q_hv_kvar=q_hv_kvar, s_hv_kva=s_hv_kva,
                                  i_mag_hv_a=i_mag_hv_a, i_ang_hv_degree=i_ang_hv_degree, p_mv_kw=p_mv_kw,
                                  q_mv_kvar=q_mv_kvar, s_mv_kva=s_mv_kva, i_mag_mv_a=i_mag_mv_a,
                                  i_ang_mv_degree=i_ang_mv_degree, p_lv_kw=p_lv_kw, q_lv_kvar=q_lv_kvar,
                                  s_lv_kva=s_lv_kva, i_mag_lv_a=i_mag_lv_a, i_ang_lv_degree=i_ang_lv_degree)


class ThreeWindingTestBench(TestBench):
    def __init__(self):
        super().__init__()

    def calculate(self, tap_min: int = -10, tap_max: int = 10, s_nom_hv_mva: float = 300.0, s_nom_mv_mva: float = 300.0,
                  s_nom_lv_mva: float = 100.0, p_step_pu: float = 0.1, v_ref_kv: float = 380.0,
                  s_ref_mva: float = 300.0,
                  tap_at_star_point: bool = False) -> list:
        """
        Iterate over tap positions, medium and low voltage power consumption and perform the power flow calculation.

        Parameters:
            tap_min (int): Minimum tap position of the transformer
            tap_max (int): Maximum tap position of the transformer
            s_nom_hv_mva (float): Nominal apparent power at the high voltage node
            s_nom_mv_mva (float): Nominal apparent power at the medium voltage node
            s_nom_lv_mva (float): Nominal apparent power at the low voltage node
            p_step_pu (float): Step size to sweep over power range with respect to the nominal voltage of the port
            v_ref_kv (float): Reference voltage of the calculation
            s_ref_mva (float): Reference apparent power of the calculation
            tap_at_star_point (bool): True, if the tap changer is located at the transformers star point
        """
        # --- General information ---
        tap_range: range = range(tap_min, tap_max + 1)
        p_step_mv_mva: float = s_nom_mv_mva * p_step_pu
        p_step_lv_mva: float = s_nom_lv_mva * p_step_pu
        self.logger.info(
            ("Starting to calculate grid with pandapower. Parameters: tap = %i...%i, reference = %.2f MVA @ %.2f kV, " %
             (tap_min, tap_max, s_ref_mva, v_ref_kv)) + "tap changer is" + (
                " " if tap_at_star_point else " not ") + "at star point")

        # --- Prepare the output dictionary ---
        out = []

        # --- Iterate through tap positions ---
        for tap_pos in tap_range:
            # --- Iterate over medium voltage load ---
            for p_mv_mw in arange(-s_nom_mv_mva, s_nom_mv_mva + p_step_mv_mva, p_step_mv_mva):
                # --- Figure out permissible power range for low voltage load and iterate over it
                p_lv_range_mw: ndarray = ThreeWindingTestBench.__permissible_power_range_lv(s_nom_hv_mva, s_nom_lv_mva,
                                                                                            p_mv_mw,
                                                                                            p_step_lv_mva)
                self.logger.debug(
                    "Power range for low voltage load is from %.2f...%.2f MW (medium voltage load is at %.2f MW)" % (
                        min(p_lv_range_mw), max(p_lv_range_mw), p_mv_mw))

                for p_lv_mw in p_lv_range_mw:
                    self.logger.debug(
                        "Perform power flow calculation with the following parameters:\n\ttap pos = %i\n\tp_mv_mw = "
                        "%.2f MW\n\tp_lv_mw = %.2f MW" % (tap_pos, p_mv_mw, p_lv_mw))
                    net = test_grid_three_winding(tap_pos=tap_pos, p_mv_mw=p_mv_mw, p_lv_mw=p_lv_mw, sn_mva=s_ref_mva,
                                                  with_iron_losses=False, tap_at_star_point=tap_at_star_point)
                    pp.runpp(net)

                    # Extract the result of this model run
                    result = extract_results(net)

                    # Register the results
                    out.append({'tap_pos': tap_pos, 'p_mv': p_mv_mw, 'p_lv': p_lv_mw, 'result': result})
                # --- Register the results to mv loop ---
        return out

    @staticmethod
    def __permissible_power_range_lv(s_nom_hv_mva: float = 0.0, s_nom_lv_mva: float = 0.0, p_mv_mw: float = 0.0,
                                     p_step_mw: float = 0.0) -> ndarray:
        """
        Determine the permissible power range, that the low voltage load can cover, without violating the rated power of
        the high voltage port together with the medium voltage load. The range is truncated to cover multiples of step
        size around 0 kW.

        Parameters:
            s_nom_hv_mva (float): Rated power of the high voltage port
            s_nom_lv_mva (float): Rated power of the low voltage port
            p_mv_mw (float): Foreseen power consumption at the medium voltage port
            p_step_mw (float): Step size to use, when sweeping over the power range

        Returns:
            power_range (ndarray): Range of active power to sweep
        """
        p_min_mw: float = max(-s_nom_lv_mva, -(p_mv_mw + s_nom_hv_mva))
        p_min_mw = ceil(p_min_mw / p_step_mw) * p_step_mw
        p_max_mw: float = min(s_nom_lv_mva, s_nom_hv_mva - p_mv_mw)
        p_max_mw = floor(p_max_mw / p_step_mw) * p_step_mw

        return arange(p_min_mw, p_max_mw + p_step_mw, p_step_mw)
