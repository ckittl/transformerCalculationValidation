import pytest

from tcv.calculation.powersystemdatamodel import ResultConverter
from tcv.calculation.powersystemdatamodel.model.NodeResult import NodeResult
from tcv.calculation.powersystemdatamodel.model.Transformer3WResult import Transformer3WResult


def test_correct_conversion():
    """
    Tests the valid conversion of a SIMONA result to the commonly shared result class for comparison
    """

    # Preparing input data
    node_result_a = NodeResult(v_mag_pu=1.0, v_ang_degree=0.0)
    node_result_b = NodeResult(v_mag_pu=1.01, v_ang_degree=15.0)
    node_result_c = NodeResult(v_mag_pu=0.98, v_ang_degree=20.0)
    transformer_result = Transformer3WResult(
        i_a_mag_ampere=10.0,
        i_a_ang_degree=5.0,
        i_b_mag_ampere=5.0,
        i_b_ang_degree=20.0,
        i_c_mag_ampere=7.5,
        i_c_ang_degree=10.0
    )

    v_rated_a = 380.0
    v_rated_b = 110.0
    v_rated_c = 30.0

    # Calculating expected values
    s_a_kva = 3800.0
    p_a_kw = 3785.53985
    q_a_kvar = -331.19182
    s_b_kva = 555.5
    p_b_kw = 553.38615
    q_b_kvar = -48.41502
    s_c_kva = 220.5
    p_c_kw = 217.15011
    q_c_kvar = 38.28942

    # Checking the right values
    actual = ResultConverter.to_three_winding_result(node_result_a=node_result_a, node_result_b=node_result_b,
                                                     node_result_c=node_result_c, transformer_result=transformer_result,
                                                     v_rated_hv=v_rated_a, v_rated_mv=v_rated_b, v_rated_lv=v_rated_c)

    assert actual.s_hv_kva == pytest.approx(s_a_kva, 1e-5)
    assert actual.s_mv_kva == pytest.approx(s_b_kva, 1e-5)
    assert actual.s_lv_kva == pytest.approx(s_c_kva, 1e-5)

    assert actual.p_hv_kw == pytest.approx(p_a_kw, 1e-5)
    assert actual.p_mv_kw == pytest.approx(p_b_kw, 1e-5)
    assert actual.p_lv_kw == pytest.approx(p_c_kw, 1e-5)

    assert actual.q_hv_kvar == pytest.approx(q_a_kvar, 1e-5)
    assert actual.q_mv_kvar == pytest.approx(q_b_kvar, 1e-5)
    assert actual.q_lv_kvar == pytest.approx(q_c_kvar, 1e-5)

    assert actual.i_mag_hv_a == pytest.approx(transformer_result.i_a_mag_ampere, 1e-5)
    assert actual.i_mag_mv_a == pytest.approx(transformer_result.i_b_mag_ampere, 1e-5)
    assert actual.i_mag_lv_a == pytest.approx(transformer_result.i_c_mag_ampere, 1e-5)

    assert actual.i_ang_hv_degree == pytest.approx(transformer_result.i_a_ang_degree, 1e-5)
    assert actual.i_ang_mv_degree == pytest.approx(transformer_result.i_b_ang_degree, 1e-5)
    assert actual.i_ang_lv_degree == pytest.approx(transformer_result.i_c_ang_degree, 1e-5)
