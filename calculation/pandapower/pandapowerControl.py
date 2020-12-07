import decimal
import logging

import datetime as datetime
import pandapower as pp
from numpy.ma import arange

from calculation.pandapower.resultwriter import ResultWriter
from calculation.pandapower.testgrid import test_grid, TapSide


class TransformerTestBench:
    logging.basicConfig(level=logging.INFO)

    if __name__ == '__main__':
        logger = logging.getLogger()

        # --- General information ---
        logger.info("Preparing the general information")
        tapRange = range(-10, 11)  # Range of available tap positions
        pRange = arange(-1, 1,
                        decimal.Decimal(0.1))  # Active power range in terms of dimensionless power from infeed to load

        # Reference system
        v_ref_kv = 0.4
        s_ref_mva = 0.4

        # Loading
        p_nom_mw = decimal.Decimal(0.4)  # Nominal active power of the load

        # --- Preparing the writing of results ---
        logger.info("Preparing to write results")
        datetime = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        writer_tap_hv = ResultWriter('../results/pandapower/', datetime + 'pandapower_tap_hv.csv')
        writer_tap_lv = ResultWriter('../results/pandapower/', datetime + 'pandapower_tap_lv.csv')

        # Iterate through all available tap positions
        for tap_pos in tapRange:
            for p in pRange:
                logger.info("Power flow with tap_pos = %i and p = %.3f p.u. - tap changer on hv side" % (tap_pos, p))
                net = test_grid(tap_pos, p * p_nom_mw, s_ref_mva)
                pp.runpp(net, trafo_model="pi")
                writer_tap_hv.write_result(tap_pos, p, net)

                logger.info("Power flow with tap_pos = %i and p = %.3f p.u. - tap changer on lv side" % (tap_pos, p))
                net = test_grid(tap_pos, p * p_nom_mw, s_ref_mva, TapSide.LV)
                pp.runpp(net, trafo_model="pi")
                writer_tap_lv.write_result(tap_pos, p, net)
        writer_tap_hv.shutdown()
