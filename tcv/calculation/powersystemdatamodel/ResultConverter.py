from math import cos, radians, sin, sqrt

from tcv.calculation.powersystemdatamodel.model.NodeResult import NodeResult
from tcv.calculation.powersystemdatamodel.model.Transformer2WResult import Transformer2WResult
from tcv.calculation.powersystemdatamodel.model.Transformer3WResult import Transformer3WResult
from tcv.calculation.result.GridResultThreeWinding import GridResultThreeWinding
from tcv.calculation.result.GridResultTwoWinding import GridResultTwoWinding


def to_three_winding_result(node_result_a: NodeResult, node_result_b: NodeResult, node_result_c: NodeResult,
                            transformer_result: Transformer3WResult, v_rated_hv: float, v_rated_mv: float,
                            v_rated_lv: float) -> GridResultThreeWinding:
    """
    Converts the given SIMONA result models into the commonly shared data for comparison of results of one operation
    point

    :param node_result_a: Nodal result for the highest voltage node
    :param node_result_b: Nodal result for the medium voltage node
    :param node_result_c: Nodal result for the lowest voltage node
    :param transformer_result: Result for the transformer
    :param v_rated_hv: Rated nodal voltage at highest voltage port
    :param v_rated_mv: Rated nodal voltage at medium voltage port
    :param v_rated_lv: Rated nodal voltage at lowest voltage port
    """
    s_a_kva, p_a_kw, q_a_kvar, s_b_kva, p_b_kw, q_b_kvar, s_c_kva, p_c_kw, q_c_kvar = _convert_transformer_3w_result(
        hv_node_result=node_result_a, mv_node_result=node_result_b, lv_node_result=node_result_c,
        transformer_result=transformer_result, v_rated_hv=v_rated_hv, v_rated_mv=v_rated_mv, v_rated_lv=v_rated_lv)

    return GridResultThreeWinding(
        v_mv_pu=node_result_b.v_mag_pu,
        v_ang_mv_degree=node_result_b.v_ang_degree,
        v_lv_pu=node_result_c.v_mag_pu,
        v_ang_lv_degree=node_result_c.v_ang_degree,
        p_hv_kw=p_a_kw,
        q_hv_kvar=q_a_kvar,
        s_hv_kva=s_a_kva,
        i_mag_hv_a=transformer_result.i_a_mag_ampere,
        i_ang_hv_degree=transformer_result.i_a_ang_degree,
        p_mv_kw=p_b_kw,
        q_mv_kvar=q_b_kvar,
        s_mv_kva=s_b_kva,
        i_mag_mv_a=transformer_result.i_b_mag_ampere,
        i_ang_mv_degree=transformer_result.i_b_ang_degree,
        p_lv_kw=p_c_kw,
        q_lv_kvar=q_c_kvar,
        s_lv_kva=s_c_kva,
        i_mag_lv_a=transformer_result.i_c_mag_ampere,
        i_ang_lv_degree=transformer_result.i_c_ang_degree
    )


def _convert_transformer_3w_result(hv_node_result: NodeResult, mv_node_result: NodeResult, lv_node_result: NodeResult,
                                   transformer_result: Transformer3WResult, v_rated_hv: float, v_rated_mv: float,
                                   v_rated_lv: float) -> (
        float, float, float, float, float, float, float, float, float):
    """
    Calculate the transformer port powers

    :param hv_node_result: Result of the highest voltage node
    :param mv_node_result: Result of the medium voltage node
    :param lv_node_result: Result of the lowest voltage node
    :param transformer_result: Result of the transformer
    :param v_rated_hv: Rated voltage of the highest voltage port
    :param v_rated_mv: Rated voltage of the medium voltage port
    :param v_rated_lv: Rated voltage of the lowest voltage port
    """
    s_a_kva, p_a_kw, q_a_kvar = _calculate_power(hv_node_result.v_mag_pu, hv_node_result.v_ang_degree,
                                                 transformer_result.i_a_mag_ampere, transformer_result.i_a_ang_degree,
                                                 v_rated_hv)
    s_b_kva, p_b_kw, q_b_kvar = _calculate_power(mv_node_result.v_mag_pu, mv_node_result.v_ang_degree,
                                                 transformer_result.i_b_mag_ampere, transformer_result.i_b_ang_degree,
                                                 v_rated_mv)
    s_c_kva, p_c_kw, q_c_kvar = _calculate_power(lv_node_result.v_mag_pu, lv_node_result.v_ang_degree,
                                                 transformer_result.i_c_mag_ampere, transformer_result.i_c_ang_degree,
                                                 v_rated_lv)
    return s_a_kva, p_a_kw, q_a_kvar, s_b_kva, p_b_kw, q_b_kvar, s_c_kva, p_c_kw, q_c_kvar


def to_two_winding_result(node_result_a: NodeResult, node_result_b: NodeResult, transformer_result: Transformer2WResult,
                          v_rated_hv: float, v_rated_lv: float) -> GridResultTwoWinding:
    """
    Converts the given SIMONA result models into the commonly shared data for comparison of results of one operation
    point

    :param node_result_a: Nodal result for the highest voltage node
    :param node_result_b: Nodal result for the medium voltage node
    :param transformer_result: Result for the transformer
    :param v_rated_hv: Rated nodal voltage at highest voltage port
    :param v_rated_lv: Rated nodal voltage at lowest voltage port
    """
    s_a_kva, p_a_kw, q_a_kvar, s_b_kva, p_b_kw, q_b_kvar = _convert_transformer_2w_result(hv_node_result=node_result_a,
                                                                                          lv_node_result=node_result_b,
                                                                                          transformer_result=transformer_result,
                                                                                          v_rated_hv=v_rated_hv,
                                                                                          v_rated_lv=v_rated_lv)

    return GridResultTwoWinding(
        v_lv_pu=node_result_b.v_mag_pu,
        v_ang_lv_degree=node_result_b.v_ang_degree,
        p_hv_kw=p_a_kw,
        q_hv_kvar=q_a_kvar,
        s_hv_kva=s_a_kva,
        i_mag_hv_a=transformer_result.i_a_mag_ampere,
        i_ang_hv_degree=transformer_result.i_a_ang_degree,
        p_lv_kw=p_b_kw,
        q_lv_kvar=q_b_kvar,
        s_lv_kva=s_b_kva,
        i_mag_lv_a=transformer_result.i_b_mag_ampere,
        i_ang_lv_degree=transformer_result.i_b_ang_degree
    )


def _convert_transformer_2w_result(hv_node_result: NodeResult, lv_node_result: NodeResult,
                                   transformer_result: Transformer2WResult, v_rated_hv: float, v_rated_lv: float) -> (
        float, float, float, float, float, float):
    """
    Calculate the transformer port powers

    :param hv_node_result: Result of the highest voltage node
    :param lv_node_result: Result of the lowest voltage node
    :param transformer_result: Result of the transformer
    :param v_rated_hv: Rated voltage of the highest voltage port
    :param v_rated_lv: Rated voltage of the lowest voltage port
    """
    s_a_kva, p_a_kw, q_a_kvar = _calculate_power(hv_node_result.v_mag_pu, hv_node_result.v_ang_degree,
                                                 transformer_result.i_a_mag_ampere,
                                                 transformer_result.i_a_ang_degree,
                                                 v_rated_hv)
    s_b_kva, p_b_kw, q_b_kvar = _calculate_power(lv_node_result.v_mag_pu, lv_node_result.v_ang_degree,
                                                 transformer_result.i_b_mag_ampere,
                                                 transformer_result.i_b_ang_degree,
                                                 v_rated_lv)
    return s_a_kva, p_a_kw, q_a_kvar, s_b_kva, p_b_kw, q_b_kvar


def _calculate_power(v_mag_pu: float, v_ang_degree: float, i_mag_ampere: float, i_ang_degree: float,
                     v_nom_kv: float) -> (float, float, float):
    """
    Calculate the power at a transformers node

    :param v_mag_pu: Magnitude of the port current
    :param v_ang_degree: Angle of the port current
    :param i_mag_ampere: Magnitude of the port current
    :param i_ang_degree: Angle of the port current
    :param v_nom_kv: Nominal voltage to apply
    """
    s_kva = sqrt(3) * v_nom_kv * v_mag_pu * i_mag_ampere
    s_ang_rad = radians(v_ang_degree - i_ang_degree)
    p_kw = s_kva * cos(s_ang_rad)
    q_kvar = s_kva * sin(s_ang_rad)

    return s_kva, p_kw, q_kvar
