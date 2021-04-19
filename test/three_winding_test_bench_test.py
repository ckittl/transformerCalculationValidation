from numpy import arange
from numpy.testing import assert_array_equal

from calculation.pandapower.ThreeWindingTestBench import ThreeWindingTestBench


def test_lv_power_range_not_truncated():
    """
    Test, if the permissible range is given back correctly, if there is no need to truncate anything
    """
    expected = arange(-100.0, 110.0, 10.0)
    # You need to do some naming tricks to access the private method
    actual = ThreeWindingTestBench()._ThreeWindingTestBench__permissible_power_range_lv(s_nom_hv_mva=300.0,
                                                                                        s_nom_lv_mva=100.0,
                                                                                        p_mv_mw=0.0,
                                                                                        p_step_mw=10.0)
    assert_array_equal(actual, expected)


def test_lv_power_range_truncated_lower():
    """
    Test, if the permissible range is given back correctly, if the lower end needs for truncation
    """
    expected = arange(-50.0, 110.0, 10.0)
    # You need to do some naming tricks to access the private method
    actual = ThreeWindingTestBench()._ThreeWindingTestBench__permissible_power_range_lv(s_nom_hv_mva=300.0,
                                                                                        s_nom_lv_mva=100.0,
                                                                                        p_mv_mw=-250.0,
                                                                                        p_step_mw=10.0)
    assert_array_equal(actual, expected)


def test_lv_power_range_truncated_lower_off_grid():
    """
    Test, if the permissible range is given back correctly, if the lower end needs for truncation. Additionally, the
    range is adjusted to meet a multiple of step size around zero
    """
    expected = arange(-50.0, 110.0, 10.0)
    # You need to do some naming tricks to access the private method
    actual = ThreeWindingTestBench()._ThreeWindingTestBench__permissible_power_range_lv(s_nom_hv_mva=300.0,
                                                                                        s_nom_lv_mva=100.0,
                                                                                        p_mv_mw=-245.0,
                                                                                        p_step_mw=10.0)
    assert_array_equal(actual, expected)


def test_lv_power_range_truncated_upper():
    """
    Test, if the permissible range is given back correctly, if the upper end needs for truncation
    """
    expected = arange(-100.0, 60.0, 10.0)
    # You need to do some naming tricks to access the private method
    actual = ThreeWindingTestBench()._ThreeWindingTestBench__permissible_power_range_lv(s_nom_hv_mva=300.0,
                                                                                        s_nom_lv_mva=100.0,
                                                                                        p_mv_mw=250.0,
                                                                                        p_step_mw=10.0)
    assert_array_equal(actual, expected)


def test_lv_power_range_truncated_upper_off_grid():
    """
    Test, if the permissible range is given back correctly, if the upper end needs for truncation. Additionally, the
    range is adjusted to meet a multiple of step size around zero
    """
    expected = arange(-100.0, 60.0, 10.0)
    # You need to do some naming tricks to access the private method
    actual = ThreeWindingTestBench()._ThreeWindingTestBench__permissible_power_range_lv(s_nom_hv_mva=300.0,
                                                                                        s_nom_lv_mva=100.0,
                                                                                        p_mv_mw=245.0,
                                                                                        p_step_mw=10.0)
    assert_array_equal(actual, expected)


def test_lv_power_range_truncated_both():
    """
    Test, if the permissible range is given back correctly, if the low voltage power range is in general bigger than
    allowed
    """
    expected = arange(-400.0, 210.0, 10.0)
    # You need to do some naming tricks to access the private method
    actual = ThreeWindingTestBench()._ThreeWindingTestBench__permissible_power_range_lv(s_nom_hv_mva=300.0,
                                                                                        s_nom_lv_mva=500.0,
                                                                                        p_mv_mw=100.0,
                                                                                        p_step_mw=10.0)
    assert_array_equal(actual, expected)


def test_lv_power_range_truncated_both_off_grid():
    """
    Test, if the permissible range is given back correctly, if the low voltage power range is in general bigger than
    allowed. Additionally, the range is adjusted to meet a multiple of step size around zero
    """
    expected = arange(-400.0, 200.0, 10.0)
    # You need to do some naming tricks to access the private method
    actual = ThreeWindingTestBench()._ThreeWindingTestBench__permissible_power_range_lv(s_nom_hv_mva=300.0,
                                                                                        s_nom_lv_mva=500.0,
                                                                                        p_mv_mw=105.0,
                                                                                        p_step_mw=10.0)
    assert_array_equal(actual, expected)
