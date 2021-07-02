from math import cos, radians, sin

from tcv.calculation.result.GridResultThreeWinding import GridResultThreeWinding
from tcv.calculation.powersystemdatamodel.model.NodeResult import NodeResult
from tcv.calculation.powersystemdatamodel.model.Transformer3WResult import Transformer3WResult


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
    v_b_pu, e_b_pu, f_b_pu = _convert_nodal_results(node_result_b)
    v_c_pu, e_c_pu, f_c_pu = _convert_nodal_results(node_result_c)
    s_a_kva, p_a_kw, q_a_kvar, s_b_kva, p_b_kw, q_b_kvar, s_c_kva, p_c_kw, q_c_kvar = _convert_transformer_3w_result(
        hv_node_result=node_result_a, mv_node_result=node_result_b, lv_node_result=node_result_c,
        transformer_result=transformer_result, v_rated_hv=v_rated_hv, v_rated_mv=v_rated_mv, v_rated_lv=v_rated_lv)

    return GridResultThreeWinding(
        v_mv_pu=v_b_pu,
        e_mv_pu=e_b_pu,
        f_mv_pu=f_b_pu,
        v_lv_pu=v_c_pu,
        e_lv_pu=e_c_pu,
        f_lv_pu=f_c_pu,
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


def _convert_nodal_results(node_result: NodeResult) -> (float, float, float):
    """
    Transform the nodal result into cartesian coordinates

    :param node_result: The nodal result received from powersystemdatamodel
    """
    e_pu = node_result.v_mag_pu * cos(radians(node_result.v_ang_degree))
    f_pu = node_result.v_mag_pu * sin(radians(node_result.v_ang_degree))

    return node_result.v_mag_pu, e_pu, f_pu


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
    s_kva = v_nom_kv * v_mag_pu * i_mag_ampere
    s_ang_rad = radians(v_ang_degree - i_ang_degree)
    p_kw = s_kva * cos(s_ang_rad)
    q_kvar = s_kva * sin(s_ang_rad)

    return s_kva, p_kw, q_kvar
