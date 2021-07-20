import json
import logging
import math
import os

import numpy as np
import powerfactory
from numpy import arange

from tcv.calculation.TestHelper import permissible_power_range_lv
from tcv.calculation.result.GridResultThreeWinding import GridResultThreeWinding
from tcv.encoder.DictEncoder import DictEncoder
from tcv.util.SeverityLevel import SeverityLevel

"""
This script controls a DIgSILENT PowerFactory instance with the objective to test the behavior of a modeled three
winding transformer within a three-node test bench.
"""


def log(level: SeverityLevel, msg: str):
    """
    Print log statements as well to the logger, as also to the PowerFactory application

    Args:
        level: Level of the message
        msg: The message itself

    Returns:
        Nothing
    """
    if level == SeverityLevel.ERROR:
        logger.error(msg)
        dpf['app'].PrintError(msg)
    elif level == SeverityLevel.WARNING:
        logger.warning(msg)
        dpf['app'].PrintWarn(msg)
    elif level == SeverityLevel.INFO:
        logger.info(msg)
        dpf['app'].PrintPlain(msg)
    elif level == SeverityLevel.DEBUG:
        logger.debug(msg)


# Set up util
logger = logging.getLogger()
logger.setLevel(level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s - %(message)s')

# Create a file handler
log_directory = os.path.join("..", "..", "..", "log")
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
log_file = os.path.join(log_directory, "dpf_three_winding_testbench.log")
file_handler = logging.FileHandler(log_file, 'w')
file_handler.setLevel(level=logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Prepare information about output file
result_directory = os.path.join("..", "..", "..", "results", "three_winding")
result_file = os.path.join(result_directory, "dpf_withMainFieldLosses.json")

# Get the PowerFactory object
dpf = {'app': powerfactory.GetApplication()}
dpf['active_project'] = dpf['app'].GetActiveProject()
dpf['pf_object'] = dpf['app'].GetFromStudyCase("ComLdf")
dpf['app'].PrintPlain("Active Project: %s" % str(dpf['active_project']))
dpf['script'] = dpf['app'].GetCurrentScript()

# Get configuration from script object
err, p_step_in = dpf['script'].GetInputParameterDouble('p_step')
if err == 1:
    raise ValueError('Unable to load input parameter \"p_step\"')
p_step = int(p_step_in)
log(SeverityLevel.INFO, "Your test bench configuration:\n\tMedium voltage is varied with %i steps" % p_step)

# Get needed information from grid structure
transformer = dpf['app'].GetCalcRelevantObjects("three_winding_transformer.ElmTr3")[0]
transformer_type = transformer.GetAttribute('typ_id')
sr_hv_mva: float = transformer_type.GetAttribute('strn3_h')
sr_mv_mva: float = transformer_type.GetAttribute('strn3_m')
sr_lv_mva: float = transformer_type.GetAttribute('strn3_l')
tap_min: int = transformer_type.GetAttribute('n3tmn_h')
tap_max: int = transformer_type.GetAttribute('n3tmx_h')
log(SeverityLevel.INFO,
    "Transformer model: %s\n\tof type %s\n\t\ts_rated_hv = %.1f MVA\n\t\ts_rated_mv = %.1f MVA\n\t\ts_rated_lv = %.1f "
    "MVA\n\t\ttap = %i..%i" % (
        str(transformer), str(transformer_type), sr_hv_mva, sr_mv_mva, sr_lv_mva, tap_min, tap_max
    ))
log(SeverityLevel.WARNING,
    "Attention, this script assumes, that s_rated_mv <= s_rated_hv and s_rated_lv <= s_rated_hv holds true.")

node_mv = dpf['app'].GetCalcRelevantObjects("node_b.ElmTerm")[0]
load_mv = dpf['app'].GetCalcRelevantObjects("load_mv.ElmLod")[0]
node_lv = dpf['app'].GetCalcRelevantObjects("node_c.ElmTerm")[0]
load_lv = dpf['app'].GetCalcRelevantObjects("load_lv.ElmLod")[0]
log(SeverityLevel.INFO, "Load at medium voltage port: %s" % str(load_mv))
log(SeverityLevel.INFO, "Load at low voltage port: %s" % str(load_lv))

# Deriving additional information
tap_range = range(tap_min, tap_max + 1)
p_mv_range_mw = [round(p_pu * sr_mv_mva) for p_pu in np.linspace(-1.0, 1.0, p_step)]  # Power range @ mv port
p_step_lv_mw = 2 * sr_lv_mva / (p_step - 1)  # Bin width at the lv side

# Performing the calculations
log(SeverityLevel.INFO, "Starting the power flow calculations")
results = []


def _calculate_angle(y: float, x: float) -> float:
    angle = math.atan2(y, x)
    if math.isnan(angle):
        return math.copysign(90.0, y)
    else:
        return math.degrees(angle)


for tap_pos in tap_range:
    log(SeverityLevel.INFO, "Sweeping through power consumption for tap position %i." % tap_pos)
    transformer.SetAttribute('n3tap_h', tap_pos)

    # Sweep through medium voltage power
    for p_mv_mw in p_mv_range_mw:
        log(SeverityLevel.DEBUG, "Setting medium voltage load to %.1f MW" % p_mv_mw)
        load_mv.SetAttribute('plini', p_mv_mw)

        # Determine the permissible power range for the low voltage side
        p_lv_range = permissible_power_range_lv(sr_hv_mva, sr_lv_mva, p_mv_mw, p_step_lv_mw)

        # Sweep through low voltage power
        for p_lv_mw in p_lv_range:
            log(SeverityLevel.DEBUG, "Setting low voltage load to %.1f MW" % p_lv_mw)
            load_lv.SetAttribute('plini', p_lv_mw)

            # Actually perform the power flow calculation
            pfStatus = dpf['pf_object'].Execute()
            if pfStatus != 0:
                log(SeverityLevel.ERROR,
                    "Power flow calculation failed for tap_pos = %i, p_mv = %.3f MW, p_lv = %.3f MW" % (
                        tap_pos, p_mv_mw, p_lv_mw))

            # Collecting all relevant results from simulation
            v_mv_pu = node_mv.GetAttribute("m:u")  # All nodal voltages in p.u.
            e_mv_pu = node_mv.GetAttribute("m:ur")
            f_mv_pu = node_mv.GetAttribute("m:ui")
            v_ang_mv_degree = _calculate_angle(f_mv_pu, e_mv_pu)
            v_lv_pu = node_lv.GetAttribute("m:u")
            e_lv_pu = node_lv.GetAttribute("m:ur")
            f_lv_pu = node_lv.GetAttribute("m:ui")
            v_ang_lv_degree = _calculate_angle(f_lv_pu, e_lv_pu)

            p_hv_kw = transformer.GetAttribute("m:Psum:bushv") * 1000  # Comes in MW
            q_hv_kvar = transformer.GetAttribute("m:Qsum:bushv") * 1000  # Comes in MVAr
            s_hv_kva = transformer.GetAttribute("m:Ssum:bushv") * 1000  # Comes in MVA
            i_mag_hv_a = transformer.GetAttribute("m:I:bushv") * 1000  # Comes in kA
            i_ang_hv_degree = transformer.GetAttribute("m:phii:bushv")  # Comes in degree
            p_mv_kw = transformer.GetAttribute("m:Psum:busmv") * 1000
            q_mv_kvar = transformer.GetAttribute("m:Qsum:busmv") * 1000
            s_mv_kva = transformer.GetAttribute("m:Ssum:busmv") * 1000
            i_mag_mv_a = transformer.GetAttribute("m:I:busmv") * 1000
            i_ang_mv_degree = transformer.GetAttribute("m:phii:busmv")
            p_lv_kw = transformer.GetAttribute("m:Psum:buslv") * 1000
            q_lv_kvar = transformer.GetAttribute("m:Qsum:buslv") * 1000
            s_lv_kva = transformer.GetAttribute("m:Ssum:buslv") * 1000
            i_mag_lv_a = transformer.GetAttribute("m:I:buslv") * 1000
            i_ang_lv_degree = transformer.GetAttribute("m:phii:buslv")

            result = GridResultThreeWinding(v_mv_pu=v_mv_pu, v_ang_mv_degree=v_ang_mv_degree, v_lv_pu=v_lv_pu,
                                            v_ang_lv_degree=v_ang_lv_degree, p_hv_kw=p_hv_kw, q_hv_kvar=q_hv_kvar,
                                            s_hv_kva=s_hv_kva, i_mag_hv_a=i_mag_hv_a, i_ang_hv_degree=i_ang_hv_degree,
                                            p_mv_kw=p_mv_kw, q_mv_kvar=q_mv_kvar, s_mv_kva=s_mv_kva,
                                            i_mag_mv_a=i_mag_mv_a, i_ang_mv_degree=i_ang_mv_degree, p_lv_kw=p_lv_kw,
                                            q_lv_kvar=q_lv_kvar, s_lv_kva=s_lv_kva, i_mag_lv_a=i_mag_lv_a,
                                            i_ang_lv_degree=i_ang_lv_degree)
            results.append({
                'tap_pos': tap_pos,
                'p_mv': p_mv_mw,
                'p_lv': p_lv_mw,
                'result': result
            })

log(SeverityLevel.INFO,
    "Successfully performed %i power flow calculations. Dum results into '%s'." % (len(results), str(result_file)))
if not os.path.exists(result_directory):
    os.makedirs(result_directory)
with open(result_file, "w") as file_to_write_to:
    json.dump(results, file_to_write_to, cls=DictEncoder, indent=2)
