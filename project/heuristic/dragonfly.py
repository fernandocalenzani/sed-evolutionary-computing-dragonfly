import random
import numpy as np

for ii in range(0, H_Planejamento+1):

    """______________________________________________________________________________________________________________"""
    # DECLARAÇÃO DAS VARIÁVEIS
    """______________________________________________________________________________________________________________"""

    X = np.ones((N, nVar), dtype=np.float64)
    deltaX = np.zeros((N, nVar), dtype=np.float64)
    Food_pos = np.zeros((1, nVar), dtype=np.float64)
    Enemy_pos = np.zeros((1, nVar), dtype=np.float64)
    Fitness = -1 + np.zeros((N, 1), dtype=np.float64)
    Fitness2 = -1 + np.zeros((N, 2), dtype=np.float64)
    S = np.zeros((1, nVar), dtype=np.float64)
    A = np.zeros((1, nVar), dtype=np.float64)
    C = np.zeros((1, nVar), dtype=np.float64)
    F = np.zeros((1, nVar), dtype=np.float64)
    E = np.zeros((1, nVar), dtype=np.float64)
    Enemy_fitness = -np.inf
    Food_fitness = np.inf
    Chaveamento = np.ones((N, nVar), dtype=np.float64)
    CustoTotal = np.zeros((N, 1), dtype=np.float64)
    Food_Line = np.zeros((dss.lines_count(), 1), dtype=np.float64)
    M_Resultado = []
    Convergence_curve = np.zeros((max_iter, Nobjetivos), dtype=np.float64)

    """______________________________________________________________________________________________________________"""
    # 1 - INICIALIZANDO A POPULAÇÃO DE LIBÉLULAS INICIAL: deltaX e X cujo [linhas=Libélulas, colunas=variaveis]
    """______________________________________________________________________________________________________________"""
    for i in range(0, N):
        for j in range(2, nVar):
            if random.uniform(-1, 1) >= 0.5:
                X[i][j] = random.uniform(0, Xmax)
            else:
                X[i][j] = random.uniform(Xmin, 0)
            if random.uniform(-1, 1) >= 0.5:
                deltaX[i][j] = random.uniform(0, Xmax / 10)
            else:
                deltaX[i][j] = random.uniform(Xmin / 10, 0)

    if ii > 0:
        X[0][:] = Best_pos[ii - 1][:]
    else:
        X[0][:] = [5, 5, 5, 5, 5, 5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5]

    """______________________________________________________________________________________________________________"""
    # 2 - INÍCIO DO LOOP DO DAO
    """______________________________________________________________________________________________________________"""
    for iter in range(0, max_iter):

        print('\n' * 25)
        print('EXECUTANDO O BDA PARA IEEE123: Minimização de CUSTO DA EXPANSÃO e PERDAS TÉCNICAS')
        print('_____________________________')
        print('Ano: {} Horizonte Planejamento: {} Expansao Anual(%): {} Nlibelulas:{} max_iter:{} Nchaves:{} '.format(
            ii, H_Planejamento, int(ExpCarga * 100), N, max_iter, dss.swtcontrols_count()))
        print('Loading: {} %'.format(int(iter * 100 / max_iter)))

        """_______________________________________________________________________________________________________"""
        # 3 - INICIALIZANDO OS PESOS s,a,c,f,e,w
        """_______________________________________________________________________________________________________"""

        w = 0.9 - iter * (0.5 / max_iter)
        my_c = 0.1 - iter * (0.1 / (max_iter / 2))
        my_c = my_c/100
        if my_c < 0:
            my_c = 1 / 100

        if iter < (3 * max_iter / 4):
            s = peso * my_c * random.uniform(0, 1)  # coeficiente de separação
            # coeficiente de alinhamento
            a = peso * my_c * random.uniform(0, 1)
            c = peso * my_c * random.uniform(0, 1)  # coeficiente de coesão
            # coeficiente de atração por comida
            f = pesof * random.uniform(0, 1)
            e = my_c  # coeficiente de distração do inimigo

        else:
            s = my_c / iter  # coeficiente de separação
            a = my_c / iter  # coeficiente de alinhamento
            c = my_c / iter  # coeficiente de coesão
            # coeficiente de atração por comida
            f = pesof * random.uniform(0, 1)
            e = my_c / iter  # coeficiente de distração do inimigo

        """_______________________________________________________________________________________________________"""
        # 4 - CALCULO DAS FUNÇÕES OBJETIVO
        """_______________________________________________________________________________________________________"""
        for i in range(0, N):

            Loads_Status = 0
            if STO == 'sim':
                dss.solution_solve()
            else:
                SwitchStates = Float2Int(Binarizacao(X[i][:]))
                Chaveamento[i][:] = SwitchStates
                SwitchingElement(SwitchStates)
                dss.solution_solve()

            """RESTRIÇÕES"""
            # 1) TODAS AS CARGAS DEVEM SER ABASTECIDAS APÓS A RECONFIGURAÇÃO
            # 2) TODAS AS CARGAS DEVEM SER ABASTECIDAS COM PELO MENOS Load_VariacaoPot % DE POTENCIA

            PlanoCondutores, PlanoCusto = PlanoExpansao(
                H_Planejamento, ii, CondutoresAtuais)
            Grandezas_Coletadas = ColetarGrandezas(
                PlanoCondutores, PlanoCusto, CondutoresAtuais)
            Grand_LoadPower = np.copy(Grandezas_Coletadas[4][:])
            Grandezas_Coletadas = list(Grandezas_Coletadas)
            Grandezas_Coletadas.append(X[i][:])

            for j in range(0, len(Grand_LoadPower)):
                if (Load_VariacaoPot * Load_S_kva[j]) > (round(Grand_LoadPower[j][2], 0)):
                    Loads_Status = Loads_Status + 1

            if Loads_Status == 0:
                M_Resultado.insert(len(M_Resultado)+1,
                                   list(Grandezas_Coletadas))

        M_Resultado_rankeada = Ranking(M_Resultado)
        Convergence_curve[iter][0] = M_Resultado_rankeada[0][13]
        Convergence_curve[iter][1] = M_Resultado_rankeada[0][0][0]
        Food_fitness = M_Resultado_rankeada[0][13]
        Food_pos = M_Resultado_rankeada[0][14]
        Food_Line = M_Resultado_rankeada[0][11]
        Enemy_fitness = M_Resultado_rankeada[len(M_Resultado[:])-1][13]
        Enemy_pos = M_Resultado_rankeada[len(M_Resultado[:])-1][14]

        """_______________________________________________________________________________________________________"""
        # 6 - ATUALIZAÇÃO DE S,A,C,F,E e deltaX
        """_______________________________________________________________________________________________________"""
        for i in range(0, N):
            index = 0
            neighbours_no = 0
            Neighbours_X = np.zeros((N, nVar), dtype=np.float64)
            Neighbours_DeltaX = np.zeros((N, nVar), dtype=np.float64)

            # ENCONTRANDO SOLUÇÕES VIZINHAS AS LIBÉLULAS SÃO BINÁRIAS
            for j in range(0, N):
                if i != j:
                    Neighbours_DeltaX[index][:] = np.copy(deltaX[j][:])
                    Neighbours_X[index][:] = np.copy(X[j][:])
                    index = index + 1
                    neighbours_no = neighbours_no + 1

            # SEPARAÇÃO
            S = np.zeros((1, dim), dtype=np.float64)
            for k in range(0, neighbours_no):
                S[0][:] = S[0][:] + X[i][:] - Neighbours_X[k][:]
            S = -S

            # ALINHAMENTO
            A[0][:] = (np.transpose(
                np.sum(np.transpose(Neighbours_DeltaX)))) / neighbours_no

            # COESÃO
            C_temp = (np.transpose(
                np.sum(np.transpose(Neighbours_X)))) / neighbours_no
            C[0][:] = C_temp - X[i][:]

            # ATRAÇÃO POR COMIDA
            F[0][:] = Food_pos - X[i][:]

            # DISTRAÇÃO DO INIMIGO
            E[0][:] = Enemy_pos + X[i][:]

            """___________________________________________________________________________________________________"""
            # 7 - ATUALIZANDO O VETOR DE PASSO DeltaXi
            """___________________________________________________________________________________________________"""

            for j in range(0, dim):

                deltaX[i][j] = np.copy(
                    s * S[0][j] + a * A[0][j] + c * C[0][j] + f * F[0][j] + e * E[0][j] + w * deltaX[i][j])

                if deltaX[i][j] > Xmax:
                    deltaX[i][j] = Xmax
                if deltaX[i][j] < Xmin:
                    deltaX[i][j] = Xmin

                X[i][j] = np.copy(X[i][j] + deltaX[i][j])

                if X[i][j] > Xmax:
                    X[i][j] = Xmax
                if X[i][j] < Xmin:
                    X[i][j] = Xmin

    """___________________________________________________________________________________________________________"""
    # 8 - RECONFIGURANDO O ALIMENTADOR E CALCULANDO GRANDEZAS PARA NOVO ANO
    """___________________________________________________________________________________________________________"""

    Best_pos[ii][:] = Food_pos
    CondutoresAtuais = Food_Line

    # 8.1 - EXECUTANDO TROCA DE CONDUTORES
    for i in range(0, dss.lines_count()):
        CondutoresUtilizados[i][ii] = Food_Line[i][0]

    # 8.2 - MELHOR CONFIGURAÇÃO
    if np.sum(Best_pos[ii][:]) == 0:
        print('Não foram encontradas soluções ótimas!')
        print('Algoritmo finalizado!')
        break

    else:
        Best_pos[ii][:] = np.copy(Float2Int(Binarizacao(Food_pos)))

    #  8.3 - EXPANSÃO DA CARGA E FIM DO PRIMEIRO ANO DE PLANEJAMENTO
    if ii <= (H_Planejamento - 1):
        ExpansaoCarga(1)

    #  8.4 - ATUALIZAÇÃO DOS VALORES DAS CARGAS
    dss.loads_first()
    for i in range(0, dss.loads_count()):
        dss.circuit_setactiveelement(Load_Name[i])
        Load_P_kw[i][0] = dss.loads_read_kw()
        Load_Qkvar[i][0] = dss.loads_read_kvar()
        Load_U_kV[i][0] = dss.loads_read_kv()
        S = ((dss.loads_read_kw()) ** 2 + (dss.loads_read_kvar()) ** 2) ** (1 / 2)
        fp = dss.loads_read_kw() / S
        Load_S_kva[i][0] = S
        Load_fp[i][0] = fp

        dss.loads_next()

    """___________________________________________________________________________________________________________"""
    # 10 - ARMAZENAMENTO DOS DADOS ANUAIS
    """___________________________________________________________________________________________________________"""
    M_Resultado_rankeada.insert(len(M_Resultado_rankeada)+1, Convergence_curve)
    M_Resultado_ano.insert(ii, M_Resultado_rankeada)
