import logging
import os

import powerfactory
from numpy import arange

from calculation.TestHelper import permissible_power_range_lv
from util.SeverityLevel import SeverityLevel

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
log_directory = os.path.join("..", "..", "log")
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
log_file = os.path.join(log_directory, "dpf_three_winding_testbench.log")
file_handler = logging.FileHandler(log_file, 'w')
file_handler.setLevel(level=logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Get the PowerFactory object
dpf = {'app': powerfactory.GetApplication()}
dpf['active_project'] = dpf['app'].GetActiveProject()
dpf['pf_object'] = dpf['app'].GetFromStudyCase("ComLdf")
dpf['app'].PrintPlain("Active Project: %s" % str(dpf['active_project']))
dpf['script'] = dpf['app'].GetCurrentScript()

# Get configuration from script object
err, p_step_pu = dpf['script'].GetInputParameterDouble('p_step')
if err == 1:
    raise ValueError('Unable to load input parameter \"p_step\"')
log(SeverityLevel.INFO, "Your test bench configuration:\n\tp_step: %.2f p.u." % p_step_pu)

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

load_mv = dpf['app'].GetCalcRelevantObjects("load_mv.ElmLod")[0]
load_lv = dpf['app'].GetCalcRelevantObjects("load_lv.ElmLod")[0]
log(SeverityLevel.INFO, "Load at medium voltage port: %s" % str(load_mv))
log(SeverityLevel.INFO, "Load at low voltage port: %s" % str(load_lv))

# Deriving additional information
tap_range = range(tap_min, tap_max + 1)
delta_p_mv = sr_mv_mva * p_step_pu
delta_p_lv = sr_lv_mva * p_step_pu
p_mv_range = arange(-sr_mv_mva, sr_mv_mva + delta_p_mv, delta_p_mv)

# Performing the calculations
log(SeverityLevel.INFO, "Starting the power flow calculations")
for tap_pos in tap_range:
    log(SeverityLevel.INFO, "Sweeping through power consumption for tap position %i." % tap_pos)

    # Sweep through medium voltage power
    for p_mv_mw in p_mv_range:
        log(SeverityLevel.DEBUG, "Setting medium voltage load to %.1f MW" % p_mv_mw)
        load_mv.SetAttribute('plini', p_mv_mw)

        # Determine the permissible power range for the low voltage side
        p_lv_range = permissible_power_range_lv(sr_hv_mva, sr_lv_mva, p_mv_mw, delta_p_lv)

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
            # TODO: Extract all the needed information
# TODO Write results to json file
