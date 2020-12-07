import pandapower as pp
from enum import Enum


class TapSide(Enum):
    """
    Permissible tap side definitions
    """
    HV = "hv"
    LV = "lv"


def test_grid(tap_pos=0, p_mw=0.0, sn_mva=0.0, tap_side=TapSide.HV) -> pp.pandapowerNet:
    """
    This methods generates a test grid consisting of a transformer loaded with a only active power load. The
    transformer parameters are taken from real SGB Smit DTTH 630 kVA transformer
    (https://www.sgb-smit.com/fileadmin/user_upload/Downloads/Broschueren/Cast_Resin_Transformers/GT_Technik_UniQ_D.pdf)
    and enhanced by an artificial tap changer

    Parameters:
        tap_pos (int): Current position of the tap changer
        p_mw (double): Current active power consumption of the load
        sn_mva (double): Nominal apparent power to use for calculations
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
                                          tap_step_percent=2.5, tap_step_degree=0., tap_pos=tap_pos)
    pp.create_load(net, bus=b, p_mw=p_mw)
    return net
