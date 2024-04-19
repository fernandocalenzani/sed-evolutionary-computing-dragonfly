import numpy as np


def get_circuit_params(dss):
    load_P_kw = np.zeros((dss.loads_count(), 1))
    load_Qkvar = np.zeros((dss.loads_count(), 1))
    load_S_kva = np.zeros((dss.loads_count(), 1))
    load_fp = np.zeros((dss.loads_count(), 1))
    load_U_kV = np.zeros((dss.loads_count(), 1))
    load_name = []
    load_conn = []
    load_model = []
    load_bus = []
    load_phases = []
    line_name = []
    line_comp = []
    line_code = []
    line_n_phase = []
    cable_original = np.zeros((dss.lines_count(), 1))
    cable_withdrawn = np.zeros((dss.lines_count(), 2))

    return load_P_kw, load_Qkvar, load_S_kva, load_fp, load_U_kV, load_name, load_conn, load_model, load_bus, load_phases, line_name, line_comp, line_code, line_n_phase, cable_original, cable_withdrawn
