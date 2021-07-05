class GridResultThreeWinding:
    """
    Class to hold information about the results of interest of a power flow calculation obtained with pandapower
    """
    v_mv_pu: float = 0.0
    e_mv_pu: float = 0.0
    f_mv_pu: float = 0.0
    v_lv_pu: float = 0.0
    e_lv_pu: float = 0.0
    f_lv_pu: float = 0.0
    p_hv_kw: float = 0.0
    q_hv_kvar: float = 0.0
    s_hv_kva: float = 0.0
    i_mag_hv_a: float = 0.0
    i_ang_hv_degree: float = 0.0
    p_mv_kw: float = 0.0
    q_mv_kvar: float = 0.0
    s_mv_kva: float = 0.0
    i_mag_mv_a: float = 0.0
    i_ang_mv_degree: float = 0.0
    p_lv_kw: float = 0.0
    q_lv_kvar: float = 0.0
    s_lv_kva: float = 0.0
    i_mag_lv_a: float = 0.0
    i_ang_lv_degree: float = 0.0

    def __init__(self, v_mv_pu: float = 0.0, e_mv_pu: float = 0.0, f_mv_pu: float = 0.0, v_lv_pu: float = 0.0,
                 e_lv_pu: float = 0.0, f_lv_pu: float = 0.0, p_hv_kw: float = 0.0, q_hv_kvar: float = 0.0,
                 s_hv_kva: float = 0.0, i_mag_hv_a: float = 0.0, i_ang_hv_degree: float = 0.0, p_mv_kw: float = 0.0,
                 q_mv_kvar: float = 0.0, s_mv_kva: float = 0.0, i_mag_mv_a: float = 0.0, i_ang_mv_degree: float = 0.0,
                 p_lv_kw: float = 0.0, q_lv_kvar: float = 0.0, s_lv_kva: float = 0.0, i_mag_lv_a: float = 0.0,
                 i_ang_lv_degree: float = 0.0):
        """
        Constructor for the class

        Parameters:
            e_mv_pu (float): Real part of complex nodal voltage at transformers medium voltage node (in p.u.)
            f_mv_pu (float): Imaginary part of complex nodal voltage at transformers medium voltage node (in p.u.)
            v_mv_pu (float): Voltage magnitude at transformers medium voltage node (in p.u.)
            e_lv_pu (float): Real part of complex nodal voltage at transformers low voltage node (in p.u.)
            f_lv_pu (float): Imaginary part of complex nodal voltage at transformers low voltage node (in p.u.)
            v_lv_pu (float): Voltage magnitude at transformers low voltage node (in p.u.)
            p_hv_kw (float): Active power at high voltage port (in kW)
            q_hv_kvar (float): Reactive power at high voltage port (in kVAr)
            s_hv_kva (float): Apparent power at high voltage port (in kVA)
            i_mag_hv_a (float): Port current magnitude at high voltage port (in A)
            i_ang_hv_degree (float): Port current angle at high voltage port (in °)
            p_mv_kw (float): Active power at medium voltage port (in kW)
            q_mv_kvar (float): Reactive power at medium voltage port (in kVAr)
            s_mv_kva (float): Apparent power at medium voltage port (in kVA)
            i_mag_mv_a (float): Port current magnitude at medium voltage port (in A)
            i_ang_mv_degree (float): Port current angle at medium voltage port (in °)
            p_lv_kw (float): Active power at low voltage port (in kW)
            q_lv_kvar (float): Reactive power at low voltage port (in kVAr)
            s_lv_kva (float): Apparent power at low voltage port (in kVA)
            i_mag_lv_a (float): Port current magnitude at high voltage port (in A)
            i_ang_lv_degree (float): Port current angle at low voltage port (in °)
        """
        self.v_mv_pu = v_mv_pu
        self.e_mv_pu = e_mv_pu
        self.f_mv_pu = f_mv_pu
        self.v_lv_pu = v_lv_pu
        self.e_lv_pu = e_lv_pu
        self.f_lv_pu = f_lv_pu
        self.p_hv_kw = p_hv_kw
        self.q_hv_kvar = q_hv_kvar
        self.s_hv_kva = s_hv_kva
        self.i_mag_hv_a = i_mag_hv_a
        self.i_ang_hv_degree = i_ang_hv_degree
        self.p_mv_kw = p_mv_kw
        self.q_mv_kvar = q_mv_kvar
        self.s_mv_kva = s_mv_kva
        self.i_mag_mv_a = i_mag_mv_a
        self.i_ang_mv_degree = i_ang_mv_degree
        self.p_lv_kw = p_lv_kw
        self.q_lv_kvar = q_lv_kvar
        self.s_lv_kva = s_lv_kva
        self.i_mag_lv_a = i_mag_lv_a
        self.i_ang_lv_degree = i_ang_lv_degree

    def __str__(self):
        return "GridResultThreeWinding{p_mv=%.4f, p_lv=%.3f, v_mv=%.3f, v_lv=%.3f}" % (
        self.p_mv_kw, self.p_lv_kw, self.v_mv_pu, self.v_lv_pu)
