from enum import Enum

import pandapower as pp


class TapSide(Enum):
    """
    Permissible tap side definitions
    """
    HV = "hv"
    LV = "lv"


class TransformerModel(Enum):
    """
    Permissible transformer model types for pandapower
    """
    PI = "pi"
    T = "t"


def test_grid_two_winding(tap_pos=0, p_mw=0.0, sn_mva=0.0, tap_side=TapSide.HV) -> pp.pandapowerNet:
    """
    This methods generates a test grid consisting of a transformer loaded with a only active power load. The
    transformer parameters are taken from real SGB Smit DTTH 630 kVA transformer
    (https://www.sgb-smit.com/fileadmin/user_upload/Downloads/Broschueren/Cast_Resin_Transformers/GT_Technik_UniQ_D.pdf)
    and enhanced by an artificial tap changer

    Parameters:
        tap_pos (int): Current position of the tap changer
        p_mw (float): Current active power consumption of the load
        sn_mva (float): Nominal apparent power to use for calculations
        tap_side (TapSide): Side, at which the transformer's tap changer is installed

    Returns:
        pandapowerNet: A test grid with one transformer and one load
    """
    net = pp.create_empty_network(sn_mva=sn_mva)
    a = pp.create_bus(net, vn_kv=10.)
    b = pp.create_bus(net, vn_kv=.4)
    pp.create_ext_grid(net, bus=a)
    pp.create_transformer_from_parameters(net=net, hv_bus=a, lv_bus=b, sn_mva=.63, vn_hv_kv=10.0, vn_lv_kv=.4,
                                          vkr_percent=1.15873, vk_percent=4.0, pfe_kw=0.0, i0_percent=0.23810,
                                          tap_side=tap_side.value, tap_neutral=0, tap_max=10, tap_min=-10,
                                          tap_step_percent=2.5, tap_step_degree=0., tap_pos=tap_pos, numba=True)
    pp.create_load(net, bus=b, p_mw=p_mw)
    return net


def test_grid_three_winding(tap_pos: int = 0, p_mv_mw: float = 0.0, p_lv_mw: float = 0.0, sn_mva: float = 0.0,
                            with_main_field_losses: bool = False, tap_at_star_point=False) -> pp.pandapowerNet:
    """
    Create a test grid with a three winding transformer as well two loads at it's medium and lower voltage ports.

    Parameters:
        tap_pos (int): Current position of the tap changer
        p_mv_mw (float): Active power loading of the medium voltage port
        p_lv_mw (float): Active power loading of the low voltage port
        sn_mva (float): Nominal apparent power to use for calculations
        with_main_field_losses (bool): Whether or not, main field losses should be considered
        tap_at_star_point (bool): True, if the tap changer is at the star point.

    Returns:
        pandapowerNet: A test grid with one transformer and two loads
    """
    net = pp.create_empty_network(sn_mva=sn_mva)
    node_a = pp.create_bus(net=net, vn_kv=380.0, name="node_a")
    node_b = pp.create_bus(net=net, vn_kv=110.0, name="node_b")
    node_c = pp.create_bus(net=net, vn_kv=30.0, name="node_c")
    pp.create_ext_grid(net, bus=node_a)
    iron_losses_kw = 0.0 if not with_main_field_losses else 1.875
    i0_percent = 0.0 if not with_main_field_losses else 0.25
    pp.create_transformer3w_from_parameters(net=net, hv_bus=node_a, mv_bus=node_b, lv_bus=node_c, vn_hv_kv=380.0,
                                            vn_mv_kv=110.0, vn_lv_kv=30.0, sn_hv_mva=300.0, sn_mv_mva=300.0,
                                            sn_lv_mva=100.0, vk_hv_percent=17.5, vk_mv_percent=18.0, vk_lv_percent=15.5,
                                            vkr_hv_percent=0.15, vkr_mv_percent=0.12, vkr_lv_percent=0.09,
                                            pfe_kw=iron_losses_kw, i0_percent=i0_percent, shift_mv_degree=0.0,
                                            shift_lv_degree=0.0, tap_step_percent=1.5, tap_pos=tap_pos, tap_neutral=0,
                                            tap_min=-10, tap_max=10, name="three_winding_transformer",
                                            tap_at_star_point=tap_at_star_point, tap_side='hv')
    pp.create_load(net, bus=node_b, p_mw=p_mv_mw, name="load_mv")
    pp.create_load(net, bus=node_c, p_mw=p_lv_mw, name="load_lv")
    return net
