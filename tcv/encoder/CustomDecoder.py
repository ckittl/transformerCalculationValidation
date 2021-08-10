from tcv.calculation.result.GridResultTwoWinding import GridResultTwoWinding
from tcv.calculation.result.GridResultThreeWinding import GridResultThreeWinding


def custom_decode(dct):
    if all(key in dct for key in (
            'v_lv_pu', 'v_ang_lv_degree', 'p_hv_kw', 'q_hv_kvar', 's_hv_kva', 'i_mag_hv_a', 'i_ang_hv_degree',
            'p_lv_kw', 'q_lv_kvar', 's_lv_kva', 'i_mag_lv_a', 'i_ang_lv_degree')):
        # Do custom decode for two winding grid results
        return GridResultTwoWinding(v_lv_pu=dct['v_lv_pu'], v_ang_lv_degree=dct['v_ang_lv_degree'],
                                    p_hv_kw=dct['p_hv_kw'], q_hv_kvar=dct['q_hv_kvar'], s_hv_kva=dct['s_hv_kva'],
                                    i_mag_hv_a=dct['i_mag_hv_a'], i_ang_hv_degree=dct['i_ang_hv_degree'],
                                    p_lv_kw=dct['p_lv_kw'], q_lv_kvar=dct['q_lv_kvar'], s_lv_kva=dct['s_lv_kva'],
                                    i_mag_lv_a=dct['i_mag_lv_a'], i_ang_lv_degree=dct['i_ang_lv_degree'])
    if all(key in dct for key in (
            'v_mv_pu', 'v_ang_mv_degree', 'v_lv_pu', 'v_ang_lv_degree', 'p_hv_kw', 'q_hv_kvar', 's_hv_kva',
            'i_mag_hv_a', 'i_ang_hv_degree', 'p_mv_kw', 'q_mv_kvar', 's_mv_kva', 'i_mag_mv_a', 'i_ang_mv_degree',
            'p_lv_kw', 'q_lv_kvar', 's_lv_kva', 'i_mag_lv_a', 'i_ang_lv_degree')):
        # Do custom decode for three winding grid results
        return GridResultThreeWinding(v_mv_pu=dct['v_mv_pu'], v_ang_mv_degree=dct['v_ang_mv_degree'],
                                      v_lv_pu=dct['v_lv_pu'], v_ang_lv_degree=dct['v_ang_lv_degree'],
                                      p_hv_kw=dct['p_hv_kw'], q_hv_kvar=dct['q_hv_kvar'], s_hv_kva=dct['s_hv_kva'],
                                      i_mag_hv_a=dct['i_mag_hv_a'], i_ang_hv_degree=dct['i_ang_hv_degree'],
                                      p_mv_kw=dct['p_mv_kw'], q_mv_kvar=dct['q_mv_kvar'], s_mv_kva=dct['s_mv_kva'],
                                      i_mag_mv_a=dct['i_mag_mv_a'], i_ang_mv_degree=dct['i_ang_mv_degree'],
                                      p_lv_kw=dct['p_lv_kw'], q_lv_kvar=dct['q_lv_kvar'], s_lv_kva=dct['s_lv_kva'],
                                      i_mag_lv_a=dct['i_mag_lv_a'], i_ang_lv_degree=dct['i_ang_lv_degree'])
    else:
        return dct
