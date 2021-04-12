from calculation.pandapower.GridResult import GridResult


def custom_decode(dct):
    if all(key in dct for key in (
            'v_pu', 'e_pu', 'f_pu', 'p_hv_kw', 'q_hv_kvar', 's_hv_kva', 'i_mag_hv_a', 'i_ang_hv_degree', 'p_lv_kw',
            'q_lv_kvar',
            's_lv_kva', 'i_mag_lv_a', 'i_ang_lv_degree')):
        # Do custom decode
        return GridResult(dct['e_pu'], dct['f_pu'], dct['v_pu'], dct['p_hv_kw'], dct['q_hv_kvar'], dct['s_hv_kva'],
                          dct['i_mag_hv_a'], dct['i_ang_hv_degree'], dct['p_lv_kw'], dct['q_lv_kvar'], dct['s_lv_kva'],
                          dct['i_mag_lv_a'], dct['i_ang_lv_degree'])
    else:
        return dct
