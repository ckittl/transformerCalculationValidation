import datetime as datetime
from math import cos, pi, sin, sqrt, atan

import numpy as np
import pandapower
import pandapower as pp
from numpy.ma import arange

from tcv.calculation.pandapower.TestGrid import TapSide, TransformerModel, test_grid_two_winding
from tcv.calculation.result.GridResultTwoWinding import GridResultTwoWinding
from tcv.calculation.pandapower import ResultWriter
from tcv.calculation.pandapower.TestBench import TestBench, __calc_current_angle


def extract_results(net: pandapower.pandapowerNet = None):
    """
    Extract results of interest from provided pandapower net

    Parameters:
        net (pandapowerNet): pandapower's net model, additionally carrying results of last simulation

    Returns:
        GridResultTwoWinding: A container class holding all information of interest
    """
    # Nodal voltages at the low voltage node of the transformer
    v_pu = net.res_bus.vm_pu[1]
    v_ang_degree = net.res_bus.va_degree[1]

    # Power at high voltage node
    p_hv_kw = net.res_trafo.p_hv_mw[0] * 1000.0
    q_hv_kvar = net.res_trafo.q_hv_mvar[0] * 1000.0
    s_hv_kva = sqrt(pow(p_hv_kw, 2) + pow(q_hv_kvar, 2))

    # Current at high voltage node
    i_mag_hv_a = net.res_trafo.i_hv_ka[0] * 1000.0  # Port current at high voltage node
    i_ang_hv_degree = __calc_current_angle(p_hv_kw, q_hv_kvar, 0.0)

    # Power at low voltage node
    p_lv_kw = net.res_trafo.p_lv_mw[0] * 1000.0
    q_lv_kvar = net.res_trafo.q_lv_mvar[0] * 1000.0
    s_lv_kva = sqrt(pow(p_lv_kw, 2) + pow(q_lv_kvar, 2))

    # Current at high voltage node
    i_mag_lv_a = net.res_trafo.i_lv_ka[0] * 1000.0  # Port current at high voltage node
    i_ang_lv_degree = __calc_current_angle(p_lv_kw, q_lv_kvar, v_ang_degree)

    return GridResultTwoWinding(v_lv_pu=v_pu, v_ang_lv_degree=v_ang_degree, p_hv_kw=p_hv_kw, q_hv_kvar=q_hv_kvar,
                                s_hv_kva=s_hv_kva, i_mag_hv_a=i_mag_hv_a, i_ang_hv_degree=i_ang_hv_degree,
                                p_lv_kw=p_lv_kw, q_lv_kvar=q_lv_kvar, s_lv_kva=s_lv_kva, i_mag_lv_a=i_mag_lv_a,
                                i_ang_lv_degree=i_ang_lv_degree)


class TwoWindingTestBench(TestBench):

    def __init__(self):
        super().__init__()

    def calculate(self, tap_min=-10, tap_max=10, p_min=-1.0, p_max=1.0, s_nom_mva: float = 0.63, p_step: int = 21,
                  v_ref_kv=0.4, s_ref_mva=0.4, tap_side=TapSide.LV, transformer_model=TransformerModel.PI):
        """
        Performs a series of power flow calculations with pandapower and the transformer test bench. It iterates through
        all permissible tap positions and further sweeps the range of permissible power infeed or consumption.
        The results are extracted from pandapower grid model and collected within a dictionary. Keys are the string
        representation of the tap position, whereas values are a list of tuples with relative active power and the
        result object.

        Parameters:
            tap_min (int): Minimum permissible tap position
            tap_max (int): Maximum permissible tap position
            p_min (float): Minimum permissible active power (negative = infeed) in p.u.
            p_max (float): Maximum permissible active power (negative = infeed) in p.u.
            s_nom_mva (float): Nominal power of the load in MW
            p_step (float): Amount of ticks along active power axis
            v_ref_kv (float): Nominal voltage of the reference system in kV
            s_ref_mva (float): Nominal apparent power of the reference system in MVA
            tap_side (TapSide): Position of the tap changer
            transformer_model (TapModel): Type of model to use for calculation
        """
        # --- General information ---
        self.logger.info(
            "Starting to calculate grid with pandapower. Parameters: tap = %i...%i, p = (%.2f...%.2f)*%.2f MW, "
            "reference = %.2f MVA @ %.2f kV, tap side = %s" %
            (tap_min, tap_max, p_min, p_max, s_nom_mva, s_ref_mva, v_ref_kv, tap_side))
        self.logger.info("Preparing the general information")
        tap_range = range(tap_min, tap_max + 1)  # Range of available tap positions
        p_range = [round(p_pu * s_nom_mva * 1000) / 1000 for p_pu in
                   np.linspace(-1.0, 1.0, p_step)]  # Power range @ mv port

        # --- Prepare the output dictionary ---
        out = []

        # --- Iterate through all available tap positions ---
        tap_pos: int
        for tap_pos in tap_range:
            for p in p_range:
                # Perform the calculation
                self.logger.debug(
                    "Power flow with tap position = %i and p = %.3f p.u. (%3.f MW)" % (
                        tap_pos, p, p * s_nom_mva))
                net = test_grid_two_winding(tap_pos, p * s_nom_mva, s_ref_mva, tap_side)
                pp.runpp(net, trafo_model=transformer_model.value)

                # Extract the result of this model run
                result = extract_results(net)

                # Register the results
                out.append({'tap_pos': tap_pos, 'p_lv': p, 'result': result})

        return out
