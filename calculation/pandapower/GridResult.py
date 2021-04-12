class GridResult:
    """
    Class to hold information about the results of interest of a power flow calculation obtained with pandapower
    """
    v_pu = 0.0
    e_pu = 0.0
    f_pu = 0.0
    p_hv_kw = 0.0
    q_hv_kvar = 0.0
    s_hv_kva = 0.0
    i_mag_hv_a = 0.0
    i_ang_hv_degree = 0.0
    p_lv_kw = 0.0
    q_lv_kvar = 0.0
    s_lv_kva = 0.0
    i_mag_lv_a = 0.0
    i_ang_lv_degree = 0.0

    def __init__(self, e_pu=0.0, f_pu=0.0, v_pu=0.0, p_hv_kw=0.0, q_hv_kvar=0.0, s_hv_kva=0.0, i_mag_hv_a=0.0,
                 i_ang_hv_degree=0.0, p_lv_kw=0.0, q_lv_kvar=0.0, s_lv_kva=0.0,
                 i_mag_lv_a=0.0, i_ang_lv_degree=0.0):
        """
        Constructor for the class

        Parameters:
            e_pu (float): Real part of complex nodal voltage at transformers low voltage node (in p.u.)
            f_pu (float): Imaginary part of complex nodal voltage at transformers low voltage node (in p.u.)
            v_pu (float): Voltage magnitude at transformers low voltage node (in p.u.)
            p_hv_kw (float): Active power at high voltage port (in kW)
            q_hv_kvar (float): Reactive power at high voltage port (in kVAr)
            s_hv_kva (float): Apparent power at high voltage port (in kVA)
            i_mag_hv_a (float): Port current magnitude at low voltage port (in A)
            i_ang_hv_degree (float): Port current angle at low voltage port (in °)
            p_lv_kw (float): Active power at low voltage port (in kW)
            q_lv_kvar (float): Reactive power at low voltage port (in kVAr)
            s_lv_kva (float): Apparent power at low voltage port (in kVA)
            i_mag_lv_a (float): Port current magnitude at high voltage port (in A)
            i_ang_lv_degree (float): Port current angle at low voltage port (in °)
        """
        self.v_pu = v_pu
        self.e_pu = e_pu
        self.f_pu = f_pu
        self.p_hv_kw = p_hv_kw
        self.q_hv_kvar = q_hv_kvar
        self.s_hv_kva = s_hv_kva
        self.i_mag_hv_a = i_mag_hv_a
        self.i_ang_hv_degree = i_ang_hv_degree
        self.p_lv_kw = p_lv_kw
        self.q_lv_kvar = q_lv_kvar
        self.s_lv_kva = s_lv_kva
        self.i_mag_lv_a = i_mag_lv_a
        self.i_ang_lv_degree = i_ang_lv_degree
