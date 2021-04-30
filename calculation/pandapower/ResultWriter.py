import csv
import util
import os

from calculation.result.GridResultTwoWinding import GridResultTwoWinding


class ResultWriter:
    """
    This class serves as a result writer for pandapower's power flow results to a csv file. As the pandapower results
    are given in a different format then what we need, this class also takes care of converting the results into the
    correct form
    """

    logger = util.getLogger()
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

    def write_result(self, tap_pos: int = 0, p_pu: float = 0.0, result: GridResultTwoWinding = None):
        """
        This method writes the given result to the file.
        
        Parameters:
            tap_pos (int): Tap position, with which the result has been obtained
            p_pu (float): Relative active power, with which the result has been obtained
            result (GridResultTwoWinding): Container class, that holds all results of interest
        """
        # Prepare the csv row and write it to file
        row = [
            tap_pos,  # Current tap position
            "%0.1f" % p_pu,  # Chosen loading in p.u.
            "%0.12f" % result.e_pu,  # Low voltage nodal voltage - real part
            "%0.12f" % result.f_pu,  # Low voltage nodal voltage - imaginary part
            "%0.12f" % result.v_pu,  # Low voltage nodal voltage - magnitude
            "%0.12f" % result.i_mag_hv_a,  # High voltage port current - magnitude
            "%0.12f" % result.i_ang_hv_degree,  # High voltage port current - angle
            "%0.12f" % result.i_mag_lv_a,  # Low voltage port current - magnitude
            "%0.12f" % result.i_ang_lv_degree,  # Low voltage port current - angle
            "%0.9f" % result.p_hv_kw,  # High voltage port active power
            "%0.9f" % result.q_hv_kvar,  # High voltage port reactive power
            "%0.9f" % result.s_hv_kva,  # High voltage port apparent power
            "%0.9f" % result.p_lv_kw,  # Low voltage port active power
            "%0.9f" % result.q_lv_kvar,  # Low voltage port reactive power
            "%0.9f" % result.s_lv_kva  # High voltage port apparent power
        ]
        try:
            self.csv_writer.writerow(row)
        except Exception as e:
            self.logger.error("Error during writing of result for tap_pos = %i and p = %.3f" % (tap_pos, p_pu))
            self.file.close()
            raise e

    def shutdown(self):
        """
        Shuts down the writer (closing the result file)
        """
        self.file.close()
