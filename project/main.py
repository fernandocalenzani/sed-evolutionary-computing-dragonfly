import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from config.bus import load_bus_params
from config.cables import cable_costs_const, cable_params, cables_costs_recond
from config.general import parameters, path_to_save_results
from libs.collect_metrics import collect_measurements
from libs.decimal2binary import to_binary
from libs.float2int import float2Int
from libs.get_circuit_params import get_circuit_params
from libs.get_elements import get_elements
from libs.load_expansion import increase_power_in_loads
from libs.mark_elements import mark_elements
from libs.opendss import dss
from libs.plan_expansion import calculate_expansion_plan
from libs.ranking import ranking
from libs.save_result import save_annual_results
from libs.search import search
from libs.swithing_elements import switching_element
from libs.update_lines import update_line_params
from libs.update_loads import update_load_params

##########################################################################################
# PARÂMETROS DA SIMULAÇÃO

# General Parameters
STO = parameters["STO"]
n_dragonflies = parameters["n_dragonflies"]
load_max = parameters["load_max"]
load_variation_power = parameters["load_variation_power"]
load_expansion = parameters["load_expansion"]
h_planning = parameters["h_planning"]
fixed_cost_percent = parameters["fixed_cost_percent"]
max_iter = parameters["max_iter"]
x_max = parameters["x_max"]
x_min = parameters["x_min"]
weight = parameters["weight"]
weight_f = parameters["weight_f"]
save_result = parameters["save_result"]
n_objective = parameters["n_objective"]

# Circuit parameters
dss, name_elements, element_n_phases, element_bus_name = get_elements(dss)

# vars
load_P_kw, load_Qkvar, load_S_kva, load_fp, load_U_kV, load_name, load_conn, load_model, load_bus, load_phases, line_name, line_comp, line_code, line_n_phase, cable_original, cable_withdrawn = get_circuit_params(
    dss)


dss.loads_first()

dss, load_P_kw, load_Qkvar, load_name, load_conn, load_U_kV, load_model, load_bus_params, load_S_kva, load_fp, load_phases = update_load_params(
    dss, load_P_kw, load_Qkvar, load_name, load_conn, load_U_kV, load_model, load_bus_params, load_S_kva, load_fp, load_phases)

# PARAMETROS DAS LINHAS
dss.lines_first()
line_name, line_comp, line_code, line_n_phase, cable_original = update_line_params(
    dss, line_name, line_comp, line_code, line_n_phase, cable_original)


cable_currently = cable_original

# DECLARAÇÕES DAS SWITCHS
switch_names, switch_all_states, switch_states = dss.swtcontrols_allnames(), [], []


"""
##########################################################################################
                                INICIO DO ALGORITMO
                            DRAGONFLY ALGORITHM OPTIMIZATION

##########################################################################################"""
# PARÂMETROS DE ENTRADA
n_var = len(switch_names)
dim = n_var

# DECLARAÇÕES DAS VARIAVEIS DO DAO
best_pos = np.zeros((h_planning+1, n_var), dtype=np.int)
cable_used = np.zeros((dss.lines_count(), h_planning+1))
resultado_year = []

# INICIO DO ALGORITMO
for ii in range(0, h_planning+1):

    # DECLARAÇÃO DAS VARIÁVEIS
    x_position = np.ones((n_dragonflies, n_var), dtype=np.float64)
    delta_x = np.zeros((n_dragonflies, n_var), dtype=np.float64)
    food_pos = np.zeros((1, n_var), dtype=np.float64)
    enemy_pos = np.zeros((1, n_var), dtype=np.float64)
    S = np.zeros((1, n_var), dtype=np.float64)
    A = np.zeros((1, n_var), dtype=np.float64)
    C = np.zeros((1, n_var), dtype=np.float64)
    F = np.zeros((1, n_var), dtype=np.float64)
    E = np.zeros((1, n_var), dtype=np.float64)
    enemy_fitness = -np.inf
    food_fitness = np.inf
    switching = np.ones((n_dragonflies, n_var), dtype=np.float64)

    food_line = np.zeros((dss.lines_count(), 1), dtype=np.float64)
    result = []
    convergence_curve = np.zeros((max_iter, n_objective), dtype=np.float64)

    # 1 - INICIALIZANDO A POPULAÇÃO DE LIBÉLULAS INICIAL: delta_x e x_position cujo [linhas=Libélulas, colunas=variaveis]

    for i in range(0, n_dragonflies):
        for j in range(2, n_var):
            if random.uniform(-1, 1) >= 0.5:
                x_position[i][j] = random.uniform(0, x_max)
            else:
                x_position[i][j] = random.uniform(x_min, 0)
            if random.uniform(-1, 1) >= 0.5:
                delta_x[i][j] = random.uniform(0, x_max / 10)
            else:
                delta_x[i][j] = random.uniform(x_min / 10, 0)

    if ii > 0:
        x_position[0][:] = best_pos[ii - 1][:]
    else:
        x_position[0][:] = [5, 5, 5, 5, 5, 5, -
                            5, -5, -5, -5, -5, -5, -5, -5, -5, -5]

    # 2 - INÍCIO DO LOOP DO DAO

    for iterator in range(0, max_iter):

        print('\n' * 25)
        print('Ano: {} Horizonte Planejamento: {} Expansao Anual(%): {} Nlibelulas:{} max_iter:{} Nchaves:{} '.format(
            ii, h_planning, int(load_expansion * 100), n_dragonflies, max_iter, dss.swtcontrols_count()))
        print('Loading: {} %'.format(int(iterator * 100 / max_iter)))

        # 3 - INICIALIZANDO OS PESOS s,a,c,f,e,w
        w = 0.9 - iterator * (0.5 / max_iter)
        my_c = 0.1 - iterator * (0.1 / (max_iter / 2))
        my_c = my_c/100
        if my_c < 0:
            my_c = 1 / 100

        if iterator < (3 * max_iter / 4):
            s = weight * my_c * random.uniform(0, 1)
            a = weight * my_c * random.uniform(0, 1)
            c = weight * my_c * random.uniform(0, 1)
            f = weight_f * random.uniform(0, 1)
            e = my_c

        else:
            s = my_c / iterator
            a = my_c / iterator
            c = my_c / iterator
            f = weight_f * random.uniform(0, 1)
            e = my_c / iterator

        # 4 - CALCULO DAS FUNÇÕES OBJETIVO
        for i in range(0, n_dragonflies):

            loads_status = 0
            if STO == 'sim':
                dss.solution_solve()
            else:
                SwitchStates = float2Int(to_binary(x_position[i][:]))
                switching[i][:] = SwitchStates
                dss = switching_element(SwitchStates)
                dss.solution_solve()

            """RESTRIÇÕES"""
            # 1) TODAS AS CARGAS DEVEM SER ABASTECIDAS APÓS A RECONFIGURAÇÃO
            # 2) TODAS AS CARGAS DEVEM SER ABASTECIDAS COM PELO MENOS load_variation_power % DE POTENCIA

            cables_plan, costs_plan = calculate_expansion_plan(
                h_planning,
                ii,
                cable_currently,
                dss,
                load_name,
                line_name,
                line_comp,
                load_max,
                cable_params,
                cable_withdrawn,
                cable_original,
                cables_costs_recond,
                cable_costs_const,
                fixed_cost_percent,
                load_bus,
                load_phases,
                load_conn,
                load_model,
                load_expansion
            )

            metrics_collected = collect_measurements(
                cables_plan, costs_plan, cable_currently)

            metric_load_power = np.copy(metrics_collected[4][:])

            metrics_collected = list(metrics_collected)

            metrics_collected.append(x_position[i][:])

            for j in range(0, len(metric_load_power)):
                if (load_variation_power * load_S_kva[j]) > (round(metric_load_power[j][2], 0)):
                    loads_status = loads_status + 1

            if loads_status == 0:
                result.insert(len(result)+1,
                              list(metrics_collected))

        result_ranking = ranking(result)
        convergence_curve[iterator][0] = result_ranking[0][13]
        convergence_curve[iterator][1] = result_ranking[0][0][0]
        food_fitness = result_ranking[0][13]
        food_pos = result_ranking[0][14]
        food_line = result_ranking[0][11]
        enemy_fitness = result_ranking[len(result[:])-1][13]
        enemy_pos = result_ranking[len(result[:])-1][14]

        # 6 - ATUALIZAÇÃO DE S,A,C,F,E e delta_x
        for i in range(0, n_dragonflies):
            index = 0
            neighbours_no = 0
            neighbours_x = np.zeros((n_dragonflies, n_var), dtype=np.float64)
            neighbours_delta_x = np.zeros(
                (n_dragonflies, n_var), dtype=np.float64)

            # ENCONTRANDO SOLUÇÕES VIZINHAS AS LIBÉLULAS SÃO BINÁRIAS
            for j in range(0, n_dragonflies):
                if i != j:
                    neighbours_delta_x[index][:] = np.copy(delta_x[j][:])
                    neighbours_x[index][:] = np.copy(x_position[j][:])
                    index = index + 1
                    neighbours_no = neighbours_no + 1

            # SEPARAÇÃO
            S = np.zeros((1, dim), dtype=np.float64)
            for k in range(0, neighbours_no):
                S[0][:] = S[0][:] + x_position[i][:] - neighbours_x[k][:]
            S = -S

            # ALINHAMENTO
            A[0][:] = (np.transpose(
                np.sum(np.transpose(neighbours_delta_x)))) / neighbours_no

            # COESÃO
            C_temp = (np.transpose(
                np.sum(np.transpose(neighbours_x)))) / neighbours_no
            C[0][:] = C_temp - x_position[i][:]

            # ATRAÇÃO POR COMIDA
            F[0][:] = food_pos - x_position[i][:]

            # DISTRAÇÃO DO INIMIGO
            E[0][:] = enemy_pos + x_position[i][:]

            # 7 - ATUALIZANDO O VETOR DE PASSO DeltaXi
            for j in range(0, dim):

                delta_x[i][j] = np.copy(
                    s * S[0][j] + a * A[0][j] + c * C[0][j] + f * F[0][j] + e * E[0][j] + w * delta_x[i][j])

                if delta_x[i][j] > x_max:
                    delta_x[i][j] = x_max
                if delta_x[i][j] < x_min:
                    delta_x[i][j] = x_min

                x_position[i][j] = np.copy(x_position[i][j] + delta_x[i][j])

                if x_position[i][j] > x_max:
                    x_position[i][j] = x_max
                if x_position[i][j] < x_min:
                    x_position[i][j] = x_min

    # 8 - RECONFIGURANDO O ALIMENTADOR E CALCULANDO GRANDEZAS PARA NOVO ANO
    best_pos[ii][:] = food_pos
    cable_currently = food_line

    # 8.1 - EXECUTANDO TROCA DE CONDUTORES
    for i in range(0, dss.lines_count()):
        cable_used[i][ii] = food_line[i][0]

    # 8.2 - MELHOR CONFIGURAÇÃO
    if np.sum(best_pos[ii][:]) == 0:
        print('Não foram encontradas soluções ótimas!')
        print('Algoritmo finalizado!')
        break

    else:
        best_pos[ii][:] = np.copy(float2Int(to_binary(food_pos)))

    #  8.3 - EXPANSÃO DA CARGA E FIM DO PRIMEIRO ANO DE PLANEJAMENTO
    if ii <= (h_planning - 1):
        dss, load_P_kw, load_Qkvar, load_S_kva, load_fp, load_U_kV = increase_power_in_loads(
            1)

    #  8.4 - ATUALIZAÇÃO DOS VALORES DAS CARGAS
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

    # 10 - SAVING YEARLY RESULTS
    result_ranking.insert(len(result_ranking)+1, convergence_curve)
    resultado_year.insert(ii, result_ranking)


save_annual_results(resultado_year, load_S_kva, load_fp,
                    cable_withdrawn, save_result, path_to_save_results)
