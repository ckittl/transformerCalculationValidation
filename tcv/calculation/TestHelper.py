from math import ceil, floor

from numpy import ndarray, arange


def permissible_power_range_lv(s_nom_hv_mva: float = 0.0, s_nom_lv_mva: float = 0.0, p_mv_mw: float = 0.0,
                               p_step_mw: float = 0.0) -> ndarray:
    """
    Determine the permissible power range, that the low voltage load can cover, without violating the rated power of
    the high voltage port together with the medium voltage load. The range is truncated to cover multiples of step
    size around 0 kW.

    Parameters:
        s_nom_hv_mva (float): Rated power of the high voltage port
        s_nom_lv_mva (float): Rated power of the low voltage port
        p_mv_mw (float): Foreseen power consumption at the medium voltage port
        p_step_mw (float): Step size to use, when sweeping over the power range

    Returns:
        power_range (ndarray): Range of active power to sweep
    """
    p_min_mw: float = max(-s_nom_lv_mva, -(p_mv_mw + s_nom_hv_mva))
    p_min_mw = ceil(p_min_mw / p_step_mw) * p_step_mw
    p_max_mw: float = min(s_nom_lv_mva, s_nom_hv_mva - p_mv_mw)
    p_max_mw = floor(p_max_mw / p_step_mw) * p_step_mw

    return arange(p_min_mw, p_max_mw + p_step_mw, p_step_mw)
