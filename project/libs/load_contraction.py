import numpy as np


def load_contraction(
    dss,
    t,
    load_name,
    load_bus,
    load_phases,
    load_conn,
    load_model,
    load_expansion
):

    load_P_kw = np.zeros((dss.loads_count(), 1))
    load_Qkvar = np.zeros((dss.loads_count(), 1))
    load_S_kva = np.zeros((dss.loads_count(), 1))
    load_fp = np.zeros((dss.loads_count(), 1))
    load_U_kV = np.zeros((dss.loads_count(), 1))

    dss.loads_first()
    for i in range(0, dss.loads_count()):
        dss.circuit_setactiveelement(load_name[i])
        load_P_kw[i][0] = dss.loads_read_kw()
        load_Qkvar[i][0] = dss.loads_read_kvar()
        load_U_kV[i][0] = dss.loads_read_kv()
        S = ((dss.loads_read_kw()) ** 2 + (dss.loads_read_kvar()) ** 2) ** (1 / 2)
        fp = dss.loads_read_kw() / S
        load_S_kva[i][0] = S
        load_fp[i][0] = fp

        dss.loads_next()

    dss.loads_first()
    for i in range(0, dss.loads_count()):
        dss.text('Edit Load.{} Bus1={}    Phases={} Conn={}   Model={} kV={}   kW={}  kvar={}'.format(
            load_name[i], load_bus[i], load_phases[i], load_conn[i], load_model[i], load_U_kV[i],
            load_P_kw[i] / (1 + t*load_expansion), load_Qkvar[i] / (1 + t*load_expansion)))

        dss.loads_next()

    return dss, load_P_kw, load_Qkvar, load_S_kva, load_fp, load_U_kV
