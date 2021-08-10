class GridResultTwoWinding:
    """
    Class to hold information about the results of interest of a power flow calculation obtained with pandapower
    """
    v_lv_pu: float = 0.0
    v_ang_lv_degree: float = 0.0
    p_hv_kw: float = 0.0
    q_hv_kvar: float = 0.0
    s_hv_kva: float = 0.0
    i_mag_hv_a: float = 0.0
    i_ang_hv_degree: float = 0.0
    p_lv_kw: float = 0.0
    q_lv_kvar: float = 0.0
    s_lv_kva: float = 0.0
    i_mag_lv_a: float = 0.0
    i_ang_lv_degree: float = 0.0

    def __init__(self, v_lv_pu: float = 0.0, v_ang_lv_degree: float = 0.0, p_hv_kw: float = 0.0, q_hv_kvar: float = 0.0,
                 s_hv_kva: float = 0.0, i_mag_hv_a: float = 0.0, i_ang_hv_degree: float = 0.0, p_lv_kw: float = 0.0,
                 q_lv_kvar: float = 0.0, s_lv_kva: float = 0.0, i_mag_lv_a: float = 0.0, i_ang_lv_degree: float = 0.0):
        """
        Constructor for the class

        Parameters:
            v_lv_pu (float): Voltage magnitude at transformers low voltage node (in p.u.)
            v_ang_lv_degree (float): Angle of the nodal voltage (in degree)
            p_hv_kw (float): Active power at high voltage port (in kW)
            q_hv_kvar (float): Reactive power at high voltage port (in kVAr)
            s_hv_kva (float): Apparent power at high voltage port (in kVA)
            i_mag_hv_a (float): Port current magnitude at high voltage port (in A)
            i_ang_hv_degree (float): Port current angle at high voltage port (in °)
            p_lv_kw (float): Active power at low voltage port (in kW)
            q_lv_kvar (float): Reactive power at low voltage port (in kVAr)
            s_lv_kva (float): Apparent power at low voltage port (in kVA)
            i_mag_lv_a (float): Port current magnitude at high voltage port (in A)
            i_ang_lv_degree (float): Port current angle at low voltage port (in °)
        """

        self.v_lv_pu = v_lv_pu
        self.v_ang_lv_degree = v_ang_lv_degree
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


def __str__(self):
    string = "GridResultTwoWinding{p_lv=%.3f, v_lv=%.3f}" % (
        self.p_lv_kw, self.v_lv_pu)
    return string


def subtract(lhs: GridResultTwoWinding, rhs: GridResultTwoWinding) -> GridResultTwoWinding:
    """
    Builds the difference between two results

    :param lhs: The left hand side
    :param rhs: The right hand side
    """
    return GridResultTwoWinding(
        v_lv_pu=lhs.v_lv_pu - rhs.v_lv_pu,
        v_ang_lv_degree=lhs.v_ang_lv_degree - rhs.v_ang_lv_degree,
        p_hv_kw=lhs.p_hv_kw - rhs.p_hv_kw,
        q_hv_kvar=lhs.q_hv_kvar - rhs.q_hv_kvar,
        s_hv_kva=lhs.s_hv_kva - rhs.s_hv_kva,
        i_mag_hv_a=lhs.i_mag_hv_a - rhs.i_mag_hv_a,
        i_ang_hv_degree=lhs.i_ang_hv_degree - rhs.i_ang_hv_degree,
        p_lv_kw=lhs.p_lv_kw - rhs.p_lv_kw,
        q_lv_kvar=lhs.q_lv_kvar - rhs.q_lv_kvar,
        s_lv_kva=lhs.s_lv_kva - rhs.s_lv_kva,
        i_mag_lv_a=lhs.i_mag_lv_a - rhs.i_mag_lv_a,
        i_ang_lv_degree=lhs.i_ang_lv_degree - rhs.i_ang_lv_degree
    )
