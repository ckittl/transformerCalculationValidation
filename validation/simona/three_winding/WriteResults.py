from datetime import datetime

from tcv.util import CsvFileWriter

# ##### A result writing routine for three winding transformer results #####

# ----- Write the results, that can be used for plotting ----
json_result_file = "../../../results/three_winding/simona_withMainFieldLosses.json"
csv_result_file = "../../../csv/three_winding/%s_simona.csv" % datetime.strftime(datetime.now(), "%Y%m%d")

CsvFileWriter.write_three_winding_results(result_json_path=json_result_file, csv_file_path=csv_result_file,
                                          p_nom_mv_mw=300.0, p_nom_lv_mw=100.0)

CsvFileWriter.write_for_pgf_surf_plot(p_mv_tick_num=11, p_mv_rated_mw=300.0, p_lv_tick_num=11, p_lv_rated_mw=100.0,
                                      tap_range=range(-10, 11), result_json_path=json_result_file,
                                      csv_file_path=csv_result_file, col_sep=",")
