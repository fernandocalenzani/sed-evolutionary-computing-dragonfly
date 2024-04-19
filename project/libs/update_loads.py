def update_load_params(dss, load_P_kw, load_Qkvar, load_name, load_conn, load_U_kV, load_model, load_bus_params, load_S_kva, load_fp, load_phases):
    for i in range(0, dss.loads_count()):
        load_P_kw[i][0] = dss.loads_read_kw()
        load_Qkvar[i][0] = dss.loads_read_kvar()
        load_name.insert(i, dss.loads_read_name())
        load_conn.insert(i, dss.loads_read_isdelta())
        load_U_kV[i][0] = dss.loads_read_kv()
        load_model.insert(i, dss.loads_read_model())
        S = ((dss.loads_read_kw()) ** 2 + (dss.loads_read_kvar()) ** 2) ** (1 / 2)
        fp = dss.loads_read_kw() / S
        load_S_kva[i][0] = S
        load_fp[i][0] = fp

        dss.circuit_setactiveelement(load_name[i])
        load_phases.insert(i, dss.cktelement_numphases())
        dss.loads_next()

    return dss, load_P_kw, load_Qkvar, load_name, load_conn, load_U_kV, load_model, load_bus_params, load_S_kva, load_fp, load_phases
