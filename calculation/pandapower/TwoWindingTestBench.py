import datetime as datetime
from math import cos, pi, sin, sqrt, atan

import pandapower
import pandapower as pp
from numpy.ma import arange

from calculation.pandapower.GridResultTwoWinding import GridResultTwoWinding
from calculation.pandapower.ResultWriter import ResultWriter
from calculation.pandapower.TestBench import TestBench, __calc_current_angle
from calculation.pandapower.TestGrid import test_grid_two_winding, TapSide, TransformerModel


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
    e_pu = v_pu * cos(net.res_bus.va_degree[1] / 180 * pi)  # Real part of nodal voltage
    f_pu = v_pu * sin(net.res_bus.va_degree[1] / 180 * pi)  # Imaginary part of nodal voltage

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
    phi_v_lv_degree = atan(f_pu / e_pu) / pi * 180.0
    i_ang_lv_degree = __calc_current_angle(p_lv_kw, q_lv_kvar, phi_v_lv_degree)

    return GridResultTwoWinding(e_pu=e_pu, f_pu=f_pu, v_pu=v_pu, p_hv_kw=p_hv_kw, q_hv_kvar=q_hv_kvar, s_hv_kva=s_hv_kva,
                                i_mag_hv_a=i_mag_hv_a,
                                i_ang_hv_degree=i_ang_hv_degree, p_lv_kw=p_lv_kw, q_lv_kvar=q_lv_kvar, s_lv_kva=s_lv_kva,
                                i_mag_lv_a=i_mag_lv_a, i_ang_lv_degree=i_ang_lv_degree)


class TwoWindingTestBench(TestBench):

    def __init__(self):
        super().__init__()

    def calculate(self, tap_min=-10, tap_max=10, p_min=-1.0, p_max=1.0, p_nom_mw=0.4, p_step_size: float = 0.1,
                  v_ref_kv=0.4, s_ref_mva=0.4,
                  tap_side=TapSide.LV, transformer_model=TransformerModel.PI):
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
            p_nom_mw (float): Nominal power of the load in MW
            p_step_size (float): Step size to use for sweeping over the range of active power
            v_ref_kv (float): Nominal voltage of the reference system in kV
            s_ref_mva (float): Nominal apparent power of the reference system in MVA
            tap_side (TapSide): Position of the tap changer
            transformer_model (TapModel): Type of model to use for calculation
        """
        # --- General information ---
        self.logger.info(
            "Starting to calculate grid with pandapower. Parameters: tap = %i...%i, p = (%.2f...%.2f)*%.2f MW, "
            "reference = %.2f MVA @ %.2f kV, tap side = %s" %
            (tap_min, tap_max, p_min, p_max, p_nom_mw, s_ref_mva, v_ref_kv, tap_side))
        self.logger.info("Preparing the general information")
        tap_range = range(tap_min, tap_max + 1)  # Range of available tap positions
        p_range = arange(p_min, p_max + p_step_size,
                         p_step_size)  # Active power range in terms of dimensionless power from infeed to load

        # --- Prepare the output dictionary ---
        out = {}

        # --- Iterate through all available tap positions ---
        tap_pos: int
        for tap_pos in tap_range:
            out[str(tap_pos)] = []
            for p in p_range:
                # Perform the calculation
                self.logger.debug(
                    "Power flow with tap position = %i and p = %.3f p.u. (%3.f MW)" % (
                        tap_pos, p, p * p_nom_mw))
                net = test_grid_two_winding(tap_pos, p * p_nom_mw, s_ref_mva, tap_side)
                pp.runpp(net, trafo_model=transformer_model.value)

                # Extract the result of this model run
                result = extract_results(net)

                # Register the results
                out[str(tap_pos)].append({'p': p, 'result': result})

        return out

    def __write_results(self, base_directory: str = "", file_name_suffix: str = "",
                        time_stamp_pattern: str = "%Y%m%d-%H%M", results: dict = None):
        """
        Iterates over a dictionary of results and writes the content to a file. The file name pattern is
        '<date_time_string of now>_<file_name_suffix>.csv'.

        Parameters:
            base_directory (str): The base directory, where the file shall be placed
            file_name_suffix (str): Suffix of the file name, giving it a meaning
            time_stamp_pattern (str): Pattern, on how to convert the current date time to a string
            results (dict): Dictionary mapping the tap position to a list of tuples (active power and result class
                            object)
        """
        # Set up the writer
        date_time_string = datetime.datetime.now().strftime(time_stamp_pattern)
        file_name = date_time_string + '_' + file_name_suffix + '.csv'
        self.logger.debug("Writing results to file '%s' in directory '%s'." % (file_name, base_directory))

        writer = ResultWriter(base_directory, date_time_string)
        for key in results.keys():
            tap_pos = int(key)
            for value in results[key]:
                p_pu = value[0]  # The first entry is the active power in p.u.
                result = value[1]
                writer.write_result(tap_pos, p_pu, result)
        writer.shutdown()
