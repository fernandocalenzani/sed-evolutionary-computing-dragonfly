import numpy as np


def collect_measurements(dss, load_names, line_names, planned_cables, expansion_cost, current_conductors, line_phase_count, administrative_load, planned_cost):
    grand_line_current = []
    grand_line_losses = []
    grand_line_phases = []
    grand_element_current = []
    grand_element_voltage_pu = []
    grand_element_power = []
    line_num_cond = []
    grand_load_power = np.zeros((len(load_names), 4))
    grand_charging_current_phase_a = -1 + \
        np.zeros((len(line_names), 1), dtype=np.float64)
    grand_charging_current_phase_b = -1 + \
        np.zeros((len(line_names), 1), dtype=np.float64)
    grand_charging_current_phase_c = -1 + \
        np.zeros((len(line_names), 1), dtype=np.float64)
    grand_new_charging_current_phase_a = -1 + \
        np.zeros((len(line_names), 1), dtype=np.float64)
    grand_new_charging_current_phase_b = -1 + \
        np.zeros((len(line_names), 1), dtype=np.float64)
    grand_new_charging_current_phase_c = -1 + \
        np.zeros((len(line_names), 1), dtype=np.float64)
    candidate_conductors = -1 + \
        np.zeros((len(line_names), 1), dtype=np.float64)
    annual_costs = np.zeros((len(line_names), 1), dtype=np.float64)

    dss.lines_first()
    for i in range(len(line_names)):
        dss.circuit_setactiveelement(line_names[i])
        grand_line_current.insert(i, dss.cktelement_currentsmagang())
        grand_line_losses.insert(i, dss.cktelement_losses())
        grand_line_phases.insert(i, dss.cktelement_nodeorder())
        line_num_cond.insert(i, dss.cktelement_numconductors())
        dss.lines_next()

    grand_voltage_pu = dss.circuit_allbusvmagpu()
    grand_losses = dss.circuit_losses()
    grand_circuit_power = dss.circuit_totalpower()

    dss.loads_first()
    for i in range(len(load_names)):
        dss.circuit_setactiveelement(load_names[i])
        grand_element_current.insert(i, dss.cktelement_currentsmagang())
        grand_element_voltage_pu.insert(i, dss.cktelement_voltagesmagang())
        grand_element_power.insert(i, dss.cktelement_powers())

        if dss.cktelement_numphases() >= 3:
            grand_load_power[i][0] = grand_element_power[i][0] + \
                grand_element_power[i][2] + grand_element_power[i][4]
            grand_load_power[i][1] = grand_element_power[i][1] + \
                grand_element_power[i][3] + grand_element_power[i][5]
        else:
            grand_load_power[i][0] = grand_element_power[i][0] + \
                grand_element_power[i][2]
            grand_load_power[i][1] = grand_element_power[i][1] + \
                grand_element_power[i][3]

        grand_load_power[i][2] = np.sqrt(
            grand_load_power[i][0] ** 2 + grand_load_power[i][1] ** 2)
        grand_load_power[i][3] = grand_load_power[i][0] / \
            grand_load_power[i][2]
        dss.loads_next()

    candidate_conductors = np.copy(current_conductors)
    for i in range(dss.lines_count()):
        if line_phase_count[i] == 3:
            if grand_line_phases[i][0] == 1 and grand_line_phases[i][1] == 2 and grand_line_phases[i][2] == 3:
                grand_charging_current_phase_a[i][0] = grand_line_current[i][0] / \
                    candidate_conductors[i][0]
                grand_charging_current_phase_b[i][0] = grand_line_current[i][2] / \
                    candidate_conductors[i][0]
                grand_charging_current_phase_c[i][0] = grand_line_current[i][4] / \
                    candidate_conductors[i][0]
        elif line_phase_count[i] == 2:
            if grand_line_phases[i][0] == 1 and grand_line_phases[i][1] == 2:
                grand_charging_current_phase_a[i][0] = grand_line_current[i][0] / \
                    candidate_conductors[i][0]
                grand_charging_current_phase_b[i][0] = grand_line_current[i][2] / \
                    candidate_conductors[i][0]
            elif grand_line_phases[i][0] == 1 and grand_line_phases[i][1] == 3:
                grand_charging_current_phase_a[i][0] = grand_line_current[i][0] / \
                    candidate_conductors[i][0]
                grand_charging_current_phase_c[i][0] = grand_line_current[i][2] / \
                    candidate_conductors[i][0]
            elif grand_line_phases[i][0] == 2 and grand_line_phases[i][1] == 3:
                grand_charging_current_phase_b[i][0] = grand_line_current[i][0] / \
                    candidate_conductors[i][0]
                grand_charging_current_phase_c[i][0] = grand_line_current[i][2] / \
                    candidate_conductors[i][0]

    for i in range(dss.lines_count()):
        if line_phase_count[i] == 3:
            if grand_line_phases[i][0] == 1 and grand_line_phases[i][1] == 2 and grand_line_phases[i][2] == 3:
                if grand_charging_current_phase_a[i][0] > administrative_load or grand_charging_current_phase_b[i][0] > administrative_load or grand_charging_current_phase_c[i][0] > administrative_load:
                    grand_new_charging_current_phase_a[i][0] = grand_line_current[i][0] / \
                        planned_cables[i][2]
                    grand_new_charging_current_phase_b[i][0] = grand_line_current[i][2] / \
                        planned_cables[i][2]
                    grand_new_charging_current_phase_c[i][0] = grand_line_current[i][4] / \
                        planned_cables[i][2]
                    candidate_conductors[i][0] = planned_cables[i][2]
                    annual_costs[i][0] = planned_cost[i][0]

        elif line_phase_count[i] == 2:
            if grand_line_phases[i][0] == 1 and grand_line_phases[i][1] == 2:
                if grand_charging_current_phase_a[i][0] > administrative_load or grand_charging_current_phase_b[i][0] > administrative_load:
                    grand_new_charging_current_phase_a[i][0] = grand_line_current[i][0] / \
                        planned_cables[i][2]
                    grand_new_charging_current_phase_b[i][0] = grand_line_current[i][2] / \
                        planned_cables[i][2]
                    candidate_conductors[i][0] = planned_cables[i][2]
                    annual_costs[i][0] = planned_cost[i][0]

            elif grand_line_phases[i][0] == 1 and grand_line_phases[i][1] == 3:
                if grand_charging_current_phase_a[i][0] > administrative_load or grand_charging_current_phase_c[i][0] > administrative_load:
                    grand_new_charging_current_phase_a[i][0] = grand_line_current[i][0] / \
                        planned_cables[i][2]
                    grand_new_charging_current_phase_c[i][0] = grand_line_current[i][2] / \
                        planned_cables[i][2]
                    candidate_conductors[i][0] = planned_cables[i][2]
                    annual_costs[i][0] = planned_cost[i][0]

            elif grand_line_phases[i][0] == 2 and grand_line_phases[i][1] == 3:
                if grand_charging_current_phase_b[i][0] > administrative_load or grand_charging_current_phase_c[i][0] > administrative_load:
                    grand_new_charging_current_phase_b[i][0] = grand_line_current[i][0] / \
                        planned_cables[i][2]
                    grand_new_charging_current_phase_c[i][0] = grand_line_current[i][2] / \
                        planned_cables[i][2]
                    candidate_conductors[i][0] = planned_cables[i][2]
                    annual_costs[i][0] = planned_cost[i][0]

        elif line_phase_count[i] == 1:
            if grand_line_phases[i][0] == 1:
                if grand_charging_current_phase_a[i][0] > administrative_load:
                    grand_new_charging_current_phase_a[i][0] = grand_line_current[i][0] / \
                        planned_cables[i][2]
                    candidate_conductors[i][0] = planned_cables[i][2]
                    annual_costs[i][0] = planned_cost[i][0]

            elif grand_line_phases[i][0] == 2:
                if grand_charging_current_phase_b[i][0] > administrative_load:
                    grand_new_charging_current_phase_b[i][0] = grand_line_current[i][0] / \
                        planned_cables[i][2]
                    candidate_conductors[i][0] = planned_cables[i][2]
                    annual_costs[i][0] = planned_cost[i][0]

            elif grand_line_phases[i][0] == 3:
                if grand_charging_current_phase_c[i][0] > administrative_load:
                    grand_new_charging_current_phase_c[i][0] = grand_line_current[i][0] / \
                        planned_cables[i][2]
                    candidate_conductors[i][0] = planned_cables[i][2]
                    annual_costs[i][0] = planned_cost[i][0]

    total_cost = np.sum(annual_costs[:][:])

    return grand_losses, grand_circuit_power, grand_voltage_pu, grand_line_current, grand_load_power, grand_charging_current_phase_a, grand_charging_current_phase_b, grand_charging_current_phase_c, grand_new_charging_current_phase_a, grand_new_charging_current_phase_b, grand_new_charging_current_phase_c, candidate_conductors, annual_costs, total_cost
