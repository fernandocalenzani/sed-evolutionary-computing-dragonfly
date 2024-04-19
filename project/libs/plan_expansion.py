import numpy as np
from libs.load_contraction import load_contraction
from libs.load_expansion import increase_power_in_loads


def calculate_expansion_plan(
        h_planning, year_planned, cables_ampacity, dss, load_name, line_name, line_comp, load_max, cable_params, cable_withdrawn, cable_original, cables_costs_recond, cable_costs_const, fixed_cost_percent, load_bus, load_phases, load_conn, load_model, load_expansion):

    # DEFININDO PLANO DE EXPANSÃO

    expansion_costs = np.zeros((dss.lines_count(), 1))
    line_n_cables = []
    i_h_planning = []
    cables_h_planning = np.zeros((dss.lines_count(), 3))

    # EXPANSÃO DA DEMANDA DE ENERGIA PARA O HORIZONTE DE PLANEJAMENTO
    dss, load_P_kw, load_Qkvar, load_S_kva, load_fp, load_U_kV = load_contraction(
        dss, year_planned, load_name, load_bus, load_phases, load_conn, load_model, load_expansion)
    dss.solution_solve()

    dss, load_P_kw, load_Qkvar, load_S_kva, load_fp, load_U_kV = increase_power_in_loads(
        dss, load_name, load_bus, load_phases, load_conn, load_model, load_expansion, h_planning)
    dss.solution_solve()

    # COLETA A CORRENTE DAS LINHAS NO HORIZONTE DE PLANEJAMENTO
    dss.lines_first()
    for i in range(0, dss.lines_count()):
        dss.circuit_setactiveelement(line_name[i])
        line_n_cables.insert(i, dss.cktelement_numconductors())
        dss.lines_next()

    dss.lines_first()
    for i in range(0, len(line_name)):
        dss.circuit_setactiveelement(line_name[i])
        i_h_planning.insert(i, dss.cktelement_currentsmagang())

        if (i_h_planning[i][0] / cables_ampacity[i][0]) > load_max:

            for j in range(0, len(cable_params[1][:]) - 1):

                if int(round(i_h_planning[i][0], 0)) in range(int(round(load_max * cable_params[1][j], 0)),
                                                              int(round(load_max * cable_params[1][j + 1],
                                                                        0))):

                    # RECONDUTORAMENTO
                    if i_h_planning[i][0] < round(load_max * cable_params[1][6], 0):

                        # 1 - R: CABOS EM ESTOQUE
                        for k in range(0, len(cable_withdrawn)):
                            if (i_h_planning[i][0] < round(load_max * cable_withdrawn[k][0], 0)) and (
                                    line_comp[i] <= cable_withdrawn[k][1]):
                                cables_h_planning[i][0] = cable_original[i][0]
                                cables_h_planning[i][1] = cable_withdrawn[k][0]
                                cables_h_planning[i][2] = cable_withdrawn[k][0]

                                expansion_costs[i][0] = (fixed_cost_percent) * (1.60934) * (line_comp[i]) * \
                                    (cables_costs_recond[
                                        cable_params[1][:].index(cables_ampacity[i][0])]
                                     [cable_params[1][:].index(cable_withdrawn[k][0])])
                                cable_withdrawn[k][0] = -1
                                break

                        # 2 - R: NOVOS CABOS
                        if (int(round(i_h_planning[i][0], 0)) in range(
                                int(round(load_max * cable_params[1][0], 0)),
                                int(round(load_max * cable_params[1][6], 0)))) and (
                                cables_h_planning[i][2] == 0):
                            cables_h_planning[i][0] = cable_original[i][0]
                            cables_h_planning[i][1] = cable_params[1][j + 1]
                            cables_h_planning[i][2] = cable_params[1][j + 1]

                            cable_withdrawn[i][0] = cable_original[i][0]
                            cable_withdrawn[i][1] = line_comp[i]

                            expansion_costs[i][0] = (fixed_cost_percent) * (1.60934) * (line_comp[i]) * \
                                (cables_costs_recond[cable_params[1][:].index(cables_ampacity[i])][
                                    j + 1]) \
                                + (1 - fixed_cost_percent) * (line_n_cables[i] / 3) * (1.60934) * (
                                line_comp[i]) \
                                * (cables_costs_recond[cable_params[1][:].index(cables_ampacity[i])][
                                    j + 1])

                    # CONSTRUÇÃO DE NOVA LINHA + RECONDUTORAMENTO
                    if i_h_planning[i][0] > round(load_max * cable_params[1][6], 0):

                        # 1 - R + NL: CABOS EM ESTOQUE
                        for k in range(0, len(cable_withdrawn)):

                            if (i_h_planning[i][0] < round(
                                    load_max * (cable_withdrawn[k][0] + cable_params[1][6]
                                                ), 0)) and (line_comp[i] <= cable_withdrawn[k][1]) and (i > 8):

                                if cable_original[i][0] == cable_params[1][4]:
                                    cables_h_planning[i][0] = cable_params[1][4]
                                    cables_h_planning[i][1] = cable_params[1][6]
                                    cables_h_planning[i][2] = cable_withdrawn[k][0] + \
                                        cable_params[1][6]
                                    expansion_costs[i][0] = cable_costs_const[0][6] * \
                                        1.60934 * line_comp[i]
                                    break
                                else:

                                    expansion_costs[i][0] = cable_costs_const[0][6] + (fixed_cost_percent) * (1.60934) * \
                                        (line_comp[i]) * \
                                        (cables_costs_recond[3][4])
                                    cable_withdrawn[k][0] = -1
                                    break

                        # 2 - R + NL: NOVOS CABOS
                        if (i_h_planning[i][0] < round(load_max * (cable_params[1][j + 1]), 0)) and (
                                cables_h_planning[i][2] == 0):
                            cable_withdrawn[i][0] = cable_original[i][0]
                            cable_withdrawn[i][1] = line_comp[i]

                            cables_h_planning[i][0] = cable_params[1][6]
                            cables_h_planning[i][1] = cable_params[1][j +
                                                                      1] - cable_params[1][6]
                            cables_h_planning[i][2] = cable_params[1][j + 1]

                            expansion_costs[i][0] = 1.60934 * (line_comp[i]) * (cable_costs_const[0][j + 1]) * \
                                (1 - fixed_cost_percent) * line_n_cables[i] / 3 + 1.60934 * (line_comp[i]) \
                                * (cable_costs_const[0][j + 1]) * (fixed_cost_percent)

                    # 3 - CORRENTE MENOR DE 150 A
                    if i_h_planning[i][0] < load_max * cable_params[1][0]:

                        # 3.1 - CORRENTE MENOR DE 150 A E CABOS MAIORES DO QUE 150A
                        if cable_params[1][0] != cable_original[i][0]:
                            cable_withdrawn[i][0] = cable_original[i][0]
                            cable_withdrawn[i][1] = line_comp[i]

                            cables_h_planning[i][0] = cable_original[i][0]
                            cables_h_planning[i][1] = cable_params[1][0]
                            cables_h_planning[i][2] = cable_params[1][0]

                            expansion_costs[i][0] = (fixed_cost_percent) * (1.60934) * (line_comp[i]) * \
                                (
                                cables_costs_recond[cable_params[1][:].index(cables_ampacity[i])][j]) \
                                + (1 - fixed_cost_percent) * (line_n_cables[i] / 3) * (1.60934) * (
                                line_comp[i]) \
                                * (
                                cables_costs_recond[cable_params[1][:].index(cables_ampacity[i])][j])

                        # 4 - CORRENTE MENOR DE 150 A SEM ALTERAÇÃO
                        else:
                            cables_h_planning[i][0] = cable_original[i][0]
                            cables_h_planning[i][1] = cable_params[1][0]
                            cables_h_planning[i][2] = cable_original[i][0]

        # 1 - NÃO EXCEDERAM LIMITE DE CARREGAMENTO
        else:
            cables_h_planning[i][0] = cables_ampacity[i][0]
            cables_h_planning[i][1] = 0
            cables_h_planning[i][2] = cables_ampacity[i][0]

            if i >= 122:
                cables_h_planning[i][0] = np.inf
                cables_h_planning[i][1] = 0
                cables_h_planning[i][2] = np.inf

        dss.lines_next()

    # CONTRAÇÃO DA DEMANDA
    dss, load_P_kw, load_Qkvar, load_S_kva, load_fp, load_U_kV = load_contraction(
        dss, h_planning, load_name, load_bus, load_phases, load_conn, load_model, load_expansion)

    dss.solution_solve()

    dss, load_P_kw, load_Qkvar, load_S_kva, load_fp, load_U_kV = increase_power_in_loads(
        dss, load_name, load_bus, load_phases, load_conn, load_model, load_expansion, year_planned)
    dss.solution_solve()

    return cables_h_planning, expansion_costs
