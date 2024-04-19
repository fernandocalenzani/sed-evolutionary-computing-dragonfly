import numpy as np


def update_line_params(dss, line_name, line_comp, line_code, line_n_phase, cable_original):
    for i in range(0, dss.lines_count()):
        line_name.insert(i, dss.lines_read_name())
        line_comp.insert(i, dss.lines_read_length())
        line_code.insert(i, dss.lines_read_linecode())
        line_n_phase.insert(i, dss.lines_read_phases())

        if (line_code[i] == '1') or (line_code[i] == '2') or (line_code[i] == '3') or (line_code[i] == '4') or (
                line_code[i] == '5') or (line_code[i] == '6'):
            cable_original[i][0] = 500

        elif (line_code[i] == '7') or (line_code[i] == '8'):
            cable_original[i][0] = 500

        elif (line_code[i] == '9') or (line_code[i] == '10') or (line_code[i] == '11'):
            cable_original[i][0] = 150

        elif (line_code[i] == '12'):
            cable_original[i][0] = 500

        else:
            cable_original[i][0] = np.inf

        dss.lines_next()

    return dss, line_name, line_comp, line_code, line_n_phase, cable_original
