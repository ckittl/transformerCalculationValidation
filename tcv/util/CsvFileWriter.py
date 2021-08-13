import csv
import json
import os
import re

import numpy as np

from tcv.encoder import CustomDecoder


def write_three_winding_results(result_json_path: str, csv_file_path: str, p_nom_mv_mw: float, p_nom_lv_mw: float):
    """
    Write the three winding results into a simple, plain csv file

    :param result_json_path: File path to the JSON formatted results
    :param csv_file_path: File path, where the csv file should be written
    :param p_nom_mv_mw: Nominal active power at the medium voltage node
    :param p_nom_lv_mw: Nominal active power at the low voltage node
    """
    if os.path.exists(result_json_path):
        # The result file exists. Read it and use it
        with open(result_json_path, "r") as file_to_read:
            json_string = file_to_read.read()
            results = json.loads(json_string, object_hook=CustomDecoder.custom_decode)

        # Go through the result dict and convert the dict
        csv_results = [_convert_dict(origin_dict, p_nom_mv_mw, p_nom_lv_mw) for origin_dict in results]

        with open(csv_file_path, 'w') as file_to_write:
            writer = csv.DictWriter(file_to_write, csv_results[0].keys())
            writer.writeheader()
            writer.writerows(csv_results)
    else:
        raise IOError("Unable to open result file '%s'." % result_json_path)


def _convert_dict(result_dict: dict, p_nom_mv_mw: float, p_nom_lv_mw: float) -> dict:
    return {
        'tap_pos': result_dict['tap_pos'],
        'p_mv_pu': result_dict['p_mv'] / p_nom_mv_mw,
        'p_lv_pu': result_dict['p_lv'] / p_nom_lv_mw,
        'v_mag_mv_pu': result_dict['result'].v_mv_pu,
        'v_ang_mv_degree': result_dict['result'].v_ang_mv_degree,
        'v_mag_lv_pu': result_dict['result'].v_lv_pu,
        'v_ang_lv_degree': result_dict['result'].v_ang_mv_degree,
    }


def _empty_result(tap_pos: int, p_mv_pu: float, p_lv_pu: float) -> dict:
    """
    Return an empty dummy result in case there is no real result apparent

    :param tap_pos: The current tap changer position
    :param p_mv_pu: The loading at medium voltage port
    :param p_lv_pu: The loading at low voltage port
    """
    return {
        'tap_pos': tap_pos,
        'p_mv_pu': p_mv_pu,
        'p_lv_pu': p_lv_pu,
        'v_mag_mv_pu': 'nan',
        'v_ang_mv_degree': 'nan',
        'v_mag_lv_pu': 'nan',
        'v_ang_lv_degree': 'nan',
    }


def write_for_pgf_surf_plot(p_mv_tick_num: int, p_mv_rated_mw: float, p_lv_tick_num: int, p_lv_rated_mw: float,
                            tap_range: range, result_json_path: str, csv_file_path: str, col_sep: str = ","):
    """
    Prepare and write the given results in a manner, that is needed to plot them within the LaTeX and TikZ library
    pgfplots.

    :param p_mv_tick_num: Amount of ticks along the "p_mv"-axis
    :param p_mv_rated_mw: Rated active power at the medium voltage port
    :param p_lv_tick_num: Amount of ticks along the "p_lv"-axis
    :param p_lv_rated_mw: Rated active power at the low voltage port
    :param tap_range: Range of tap changer positions to consider
    :param result_json_path: File path, where to find the json formatted results
    :param csv_file_path: File path where to place the csv file
    :param col_sep: Column separator when writing to csv files
    """
    if os.path.exists(result_json_path):
        # The result file exists. Read it and use it
        with open(result_json_path, "r") as file_to_read:
            json_string = file_to_read.read()
            results = json.loads(json_string, object_hook=CustomDecoder.custom_decode)

        # Preparing the x and y axis with a meshed grid
        p_mv_range = np.linspace(-1.0, 1.0, p_mv_tick_num)
        p_lv_range = np.linspace(-1.0, 1.0, p_lv_tick_num)

        # Set up a mesh grid for the results
        p_mv_grid, p_lv_grid = np.meshgrid(p_mv_range, p_lv_range)

        # Go through each of the possible tap positions and write a csv file for it
        for tap_pos in tap_range:
            out_file_path = re.sub(pattern="\\.csv$", repl="_pgfplots_tap_%i.csv" % tap_pos, string=csv_file_path)

            # Prepare writing to file
            with open(out_file_path, 'w') as file_to_write:
                file_to_write.write(col_sep.join(
                    ['tap_pos', 'p_mv_pu', 'p_lv_pu', 'v_mag_mv_pu', 'v_ang_mv_degree', 'v_mag_lv_pu',
                     'v_ang_lv_degree']))
                file_to_write.write("\n")

                for block in zip(p_mv_grid, p_lv_grid):
                    for p_mv_pu, p_lv_pu in zip(block[0], block[1]):
                        # Round to the first decimal place
                        p_mv_pu = round(p_mv_pu * 10) / 10
                        p_lv_pu = round(p_lv_pu * 10) / 10

                        p_mv_mw = p_mv_pu * p_mv_rated_mw
                        p_lv_mw = p_lv_pu * p_lv_rated_mw
                        try:
                            result = next(entry for entry in results if
                                          (entry['p_mv'] == p_mv_mw and entry['p_lv'] == p_lv_mw and entry[
                                              'tap_pos'] == tap_pos))
                            csv_dict = _convert_dict(result_dict=result, p_nom_mv_mw=p_mv_rated_mw,
                                                     p_nom_lv_mw=p_lv_rated_mw)
                            file_to_write.write(col_sep.join(map(lambda val: str(val), csv_dict.values())))
                            file_to_write.write("\n")
                        except StopIteration:
                            csv_dict = _empty_result(tap_pos, p_mv_pu, p_lv_pu)
                            file_to_write.write(col_sep.join(map(lambda val: str(val), csv_dict.values())))
                            file_to_write.write("\n")
                        except Exception as e:
                            print("Other error: %s" % e)
                    file_to_write.write("\n")
    else:
        raise IOError("Unable to open result file '%s'." % result_json_path)


def write_for_pgf_line_plot(p_lv_tick_num: int, p_lv_rated_mw: float, tap_range: range, result_json_path: str,
                            csv_file_path: str, col_sep: str = ","):
    """
    Prepare and write the given results in a manner, that is needed to plot them within the LaTeX and TikZ library
    pgfplots.

    :param p_lv_tick_num: Amount of ticks along the "p_lv"-axis
    :param p_lv_rated_mw: Rated active power at the low voltage port
    :param tap_range: Range of tap changer positions to consider
    :param result_json_path: File path, where to find the json formatted results
    :param csv_file_path: File path where to place the csv file
    :param col_sep: Column separator when writing to csv files
    """
    if os.path.exists(result_json_path):
        # The result file exists. Read it and use it
        with open(result_json_path, "r") as file_to_read:
            json_string = file_to_read.read()
            results = json.loads(json_string, object_hook=CustomDecoder.custom_decode)

        # Preparing the x and y axis with a meshed grid
        p_lv_range = np.linspace(-1.0, 1.0, p_lv_tick_num)

        # Go through each of the possible tap positions and write a csv file for it
        for tap_pos in tap_range:
            out_file_path = re.sub(pattern="\\.csv$", repl="_pgfplots_tap_%i.csv" % tap_pos, string=csv_file_path)

            # Prepare writing to file
            with open(out_file_path, 'w') as file_to_write:
                file_to_write.write(col_sep.join(['tap_pos', 'p_lv_pu', 'v_mag_lv_pu', 'v_ang_lv_degree']))
                file_to_write.write("\n")

                for p_lv_pu in p_lv_range:
                    # Round to kW-precision places
                    p_lv_mw = round(p_lv_pu * p_lv_rated_mw * 1e3) / 1e3
                    try:
                        result = next(
                            entry for entry in results if (entry['p_lv'] == p_lv_mw and entry['tap_pos'] == tap_pos))
                        csv_dict = _convert_dict_two_winding(result_dict=result, p_nom_lv_mw=p_lv_rated_mw)
                        file_to_write.write(col_sep.join(map(lambda val: str(val), csv_dict.values())))
                        file_to_write.write("\n")
                    except StopIteration:
                        csv_dict = _empty_result_two_winding(tap_pos, p_lv_pu)
                        file_to_write.write(col_sep.join(map(lambda val: str(val), csv_dict.values())))
                        file_to_write.write("\n")
                    except Exception as e:
                        print("Other error: %s" % e)
    else:
        raise IOError("Unable to open result file '%s'." % result_json_path)


def _convert_dict_two_winding(result_dict: dict, p_nom_lv_mw: float) -> dict:
    return {
        'tap_pos': result_dict['tap_pos'],
        'p_lv_pu': round(result_dict['p_lv'] / p_nom_lv_mw * 10) / 10,
        'v_mag_lv_pu': result_dict['result'].v_lv_pu,
        'v_ang_lv_degree': result_dict['result'].v_ang_lv_degree,
    }


def _empty_result_two_winding(tap_pos: int, p_lv_pu: float) -> dict:
    """
    Return an empty dummy result in case there is no real result apparent

    :param tap_pos: The current tap changer position
    :param p_lv_pu: The loading at low voltage port
    """
    return {
        'tap_pos': tap_pos,
        'p_lv_pu': p_lv_pu,
        'v_mag_lv_pu': 'nan',
        'v_ang_lv_degree': 'nan',
    }
