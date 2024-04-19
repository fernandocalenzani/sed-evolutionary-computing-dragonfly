def switching_element(dss, switch_state):
    # Switch Open(1) e Switch Close(2) OPENDSS
    # Switch Open(0) e Switch Close(1)  BDA
    switch_all_states = []
    switch_all_names = []

    dss.swtcontrols_first()
    for i in range(0, len(switch_state)):

        if switch_state[i] == 0:
            switch_state[i] = 1
        elif switch_state[i] == 1:
            switch_state[i] = 2

        dss.swtcontrols_write_action(switch_state[i])
        switch_all_states.insert(i, dss.swtcontrols_read_action())
        switch_all_names.insert(i, dss.swtcontrols_read_name())

        if switch_all_states[i] == 1:
            switch_all_states[i] = 0
        elif switch_all_states[i] == 2:
            switch_all_states[i] = 1
        dss.swtcontrols_next()

    return dss
