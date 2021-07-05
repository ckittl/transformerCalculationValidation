from datetime import timedelta
from uuid import UUID

from typing import List

from tcv.calculation.powersystemdatamodel import ResultConverter
from tcv.calculation.powersystemdatamodel.model.TimeSeriesResult import TimeSeriesResult
from tcv.exception.ResultCollectionException import ResultCollectionException


def collect(base_directory: str, node_a: UUID, node_b: UUID, node_c: UUID, load_mv: UUID, load_lv: UUID,
            v_rated_hv: float, v_rated_mv: float, v_rated_lv: float, tap_pos: int) -> List[dict]:
    """
    Collects together all results and brings them into the form, that is used for result comparison

    :param base_directory: The base directory, where the time series results can be found
    :param node_a: Unique identifier of the highest voltage node
    :param node_b: Unique identifier of the medium voltage node
    :param node_c: Unique identifier of the low voltage node
    :param load_mv: Unique identifier of the medium voltage load
    :param load_lv: Unique identifier of the low voltage node
    :param v_rated_hv: Rated voltage magnitude of the highest voltage node
    :param v_rated_mv: Rated voltage magnitude of the medium voltage node
    :param v_rated_lv: Rated voltage magnitude of the low voltage node
    :param tap_pos: Current position of the tap changer
    """
    # Read in all results
    time_series_result = TimeSeriesResult(base_directory=base_directory)

    # Map time step onto power consumption
    time_to_power = _map_time_to_power(time_series_result.load_results, load_mv, load_lv)

    # Map time step onto power flow results
    time_to_pf = _map_time_to_power_flow_result(time_series_result.node_results,
                                                time_series_result.transformer_3w_results, node_a, node_b, node_c,
                                                v_rated_hv, v_rated_mv, v_rated_lv)

    # Bring together both results
    results = []
    for time_step in time_to_power.keys():
        p_mv_mw, p_lv_mw = time_to_power[time_step]
        # Match with the power flow result one tick ahead, because of SIMONA's logic
        pf_time = time_step + timedelta(seconds=1)
        grid_result = time_to_pf[pf_time]

        results.append({
                'tap_pos': tap_pos,
                'p_mv': p_mv_mw,
                'p_lv': p_lv_mw,
                'result': grid_result
            })

    return results


def _map_time_to_power(load_results: dict, load_mv: UUID, load_lv: UUID) -> dict:
    """
    Map the time series time steps to induced powers at the ports

    :param load_results: The dictionary from time_step to a list of load results
    :param load_mv: Unique identifier of the medium voltage load
    :param load_lv: Unique identifier of the low voltage load
    """
    time_to_power: dict = {}
    for time_step in load_results.keys():
        powers = load_results[time_step]
        if len(powers) == 2:
            # The result contains power in kW
            p_mv_mw = next(result.p * 1e3 for result in powers if result.input_model == load_mv)
            p_lv_mw = next(result.p * 1e3 for result in powers if result.input_model == load_lv)

            time_to_power[time_step] = (p_mv_mw, p_lv_mw)
        else:
            raise ResultCollectionException("I need two power results, but found %i.", len(powers))
    return time_to_power


def _map_time_to_power_flow_result(node_results: dict, transformer_results: dict, node_a: UUID, node_b: UUID,
                                   node_c: UUID, v_rated_hv: float, v_rated_mv: float, v_rated_lv: float) -> dict:
    """
    Determine the mapping from simulation time step to power flow result

    :param node_results: Mapping from time step to node results
    :param transformer_results: Mapping from time step to transformer results
    :param node_a: Unique identifier of the highest voltage node
    :param node_b: Unique identifier of the medium voltage node
    :param node_c: Unique identifier of the low voltage node
    :param v_rated_hv: Rated voltage magnitude of the highest voltage node
    :param v_rated_mv: Rated voltage magnitude of the medium voltage node
    :param v_rated_lv: Rated voltage magnitude of the low voltage node
    """
    time_to_power_flow_result = dict()
    for time_step in node_results.keys():
        node_result_a = next(result for result in node_results[time_step] if result.input_model == node_a)
        node_result_b = next(result for result in node_results[time_step] if result.input_model == node_b)
        node_result_c = next(result for result in node_results[time_step] if result.input_model == node_c)
        transformer_result = next(result for result in transformer_results[time_step])

        power_flow_result = ResultConverter.to_three_winding_result(node_result_a=node_result_a,
                                                                    node_result_b=node_result_b,
                                                                    node_result_c=node_result_c,
                                                                    transformer_result=transformer_result,
                                                                    v_rated_hv=v_rated_hv, v_rated_mv=v_rated_mv,
                                                                    v_rated_lv=v_rated_lv)
        time_to_power_flow_result[time_step] = power_flow_result
    return time_to_power_flow_result
