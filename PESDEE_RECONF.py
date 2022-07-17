"""
####################################################################################################################
INSTITUTO FEDERAL DO ESPÍRITO SANTO
ENGENHARIA ELÉTRICA - DISTRIBUIÇÃO DE ENERGIA ELÉTRICA

Título da Pesquisa:
Planejamento técnico da expansão de distribuição de energia elétrica multiestágios com
utilização a reconfiguração do alimentador para minimização de custos e perdas

Nome Orientador: Dr. Clainer Bravim Donadel
          email: cdonadel@ifes.edu.br
     Nome Aluno: Fernando Calenzani Muller
         e-mail: fernandocalenzani@gmail.com
####################################################################################################################



####################################################################################################################
INICIO DO ALGORITMO DAGRONFLY ALGORITHM OPTIMIZATION (DAO)
####################################################################################################################
"""

# coding: utf-8
# encoding: utf-8

"""
####################################################################################################################
                                                    BIBLIOTECAS
####################################################################################################################
"""
import matplotlib.pyplot as plt
import numpy as np
import py_dss_interface  # importa o pacode para utilizar as classes no OpenDSS
import random
import pandas as pd
import os
"""
####################################################################################################################
                                            INTERFACE OPENDSS E PYTHON
####################################################################################################################
"""

dss = py_dss_interface.DSSDLL(r"C:\Program Files\OpenDSS")  # OpenDSS objeto com path do OpenDSS local
dss_file = r"C:\PESDEE_123B_RECONF\A1_IEEE123Bus\Master.DSS"
dss.text('compile [{}]'.format(dss_file))
print('-=' * 50)
print("INICIANDO ALGORITMO")
print('-=' * 50)
print('...')

"""
####################################################################################################################
                                                    FUNÇÕES
####################################################################################################################
"""

def search(lista, valor):
    for i in range(0, len(lista)):
        if lista[i] == valor:
            indice = i
            break

    return indice

def MarkElements(Switch, Trafo, Reguladores, Capacitores):
    if (Trafo == 'sim') or (Trafo == 'SIM') or (Trafo == 'S') or (Trafo == 'y') or (Trafo == 'Y') or (
            Trafo == 'yes') or (Trafo == 'YES'):
        dss.text("set markTransformers=Yes TransMarkerCode=17 TransMarkerSize=3")

    if (Reguladores == 'sim') or (Reguladores == 'SIM') or (Reguladores == 'S') or (Reguladores == 'y') or (
            Reguladores == 'Y') or (Reguladores == 'yes') or (Reguladores == 'YES'):
        dss.text("set MarkRegulators = Yes RegMarkerCode = 24 RegMarkerSize = 3")

    if (Capacitores == 'sim') or (Capacitores == 'SIM') or (Capacitores == 'S') or (Capacitores == 'y') or (
            Capacitores == 'Y') or (Capacitores == 'yes') or (Capacitores == 'YES'):
        dss.text("set MarkCapacitors = Yes CapMarkerCode = 38 CapMarkerSize = 3")

    if (Switch == 'sim') or (Switch == 'SIM') or (Switch == 'S') or (Switch == 'y') or (Switch == 'Y') or (
            Switch == 'yes') or (Switch == 'YES'):
        dss.text("AddBusMarker bus=150r color=blue size=3 code=37")
        dss.text("AddBusMarker bus=149  color=blue size=3 code=6")

        dss.text("AddBusMarker bus=13   color=blue size=3 code=37")
        dss.text("AddBusMarker bus=152 color=blue size=3 code=6")

        dss.text("AddBusMarker bus=18 color=blue size=3 code=37")
        dss.text("AddBusMarker bus=135 color=blue size=3 code=6")

        dss.text("AddBusMarker bus=60 color=blue size=3 code=37")
        dss.text("AddBusMarker bus=160 color=blue size=3 code=6")

        dss.text("AddBusMarker bus=97 color=blue size=3 code=37")
        dss.text("AddBusMarker bus=197 color=blue size=3 code=6")

        dss.text("AddBusMarker bus=61 color=blue size=3 code=37")
        dss.text("AddBusMarker bus=61s color=blue size=3 code=6")

        dss.text("AddBusMarker bus=151 color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus=300 color=LtGray size=3 code=6")

        dss.text("AddBusMarker bus=54  color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus=94  color=LtGray size=3 code=6")

        dss.text("AddBusMarker bus=95   color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus=195   color=LtGray size=3 code=6")

        dss.text("AddBusMarker bus=250 color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus=251 color=LtGray size=3 code=6")

        dss.text("AddBusMarker bus=450 color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus=451 color=LtGray size=3 code=6")

        dss.text("AddBusMarker bus=300 color=LtGray size=3 code=37")
        dss.text("AddBusMarker bus = 350 color = LtGray size = 3 code = 6")

def SwitchingElement(Switch_State):
    # Switch Open(1) e Switch Close(2) OPENDSS
    # Switch Open(0) e Switch Close(1)  BDA
    Switch_AllStates = []
    Switch_AllName = []

    dss.swtcontrols_first()
    for i in range(0, len(Switch_State)):

        if Switch_State[i] == 0:
            Switch_State[i] = 1
        elif Switch_State[i] == 1:
            Switch_State[i] = 2

        dss.swtcontrols_write_action(Switch_State[i])
        Switch_AllStates.insert(i, dss.swtcontrols_read_action())
        Switch_AllName.insert(i, dss.swtcontrols_read_name())

        if Switch_AllStates[i] == 1:
            Switch_AllStates[i] = 0
        elif Switch_AllStates[i] == 2:
            Switch_AllStates[i] = 1
        dss.swtcontrols_next()

    return Switch_AllStates

def ColetarGrandezas(Cabos_Hplanejamento, CustoExpansao, CondutoresAtuais):
    # DECLARANDO AS GRANDEZAS A SEREM COLETADAS
    # ___________________________________________________________________________________________________________________
    Grand_LineCurrent = []
    Grand_Linelosses = []
    Grand_LinePhases = []
    Grand_ElementCurrent = []
    Grand_ElementVoltagepu = []
    Grand_ElementPower = []
    LineNumCond = []
    Grand_LoadPower = np.zeros((len(Load_Name), 4))
    Grand_ChargingCurrent_phaseA = -1 + np.zeros((len(Line_Name), 1), dtype=np.float64)
    Grand_ChargingCurrent_phaseB = -1 + np.zeros((len(Line_Name), 1), dtype=np.float64)
    Grand_ChargingCurrent_phaseC = -1 + np.zeros((len(Line_Name), 1), dtype=np.float64)
    Grand_New_ChargingCurrent_phaseA = -1 + np.zeros((len(Line_Name), 1), dtype=np.float64)
    Grand_New_ChargingCurrent_phaseB = -1 + np.zeros((len(Line_Name), 1), dtype=np.float64)
    Grand_New_ChargingCurrent_phaseC = -1 + np.zeros((len(Line_Name), 1), dtype=np.float64)
    CondutoresCandidatos = -1 + np.zeros((len(Line_Name), 1), dtype=np.float64)
    CustoAnual = np.zeros((len(Line_Name), 1), dtype=np.float64)
    # ___________________________________________________________________________________________________________________
    # CORRENTE NAS LINHAS [A]
    # ___________________________________________________________________________________________________________________
    dss.lines_first()
    for i in range(0, len(Line_Name)):
        dss.circuit_setactiveelement(Line_Name[i])
        Grand_LineCurrent.insert(i, dss.cktelement_currentsmagang())
        Grand_Linelosses.insert(i, dss.cktelement_losses())
        Grand_LinePhases.insert(i, dss.cktelement_nodeorder())
        LineNumCond.insert(i, dss.cktelement_numconductors())

        dss.lines_next()

    # TENSÕES NAS BARRAS [pu]
    # ___________________________________________________________________________________________________________________
    Grand_Voltagepu = dss.circuit_allbusvmagpu()

    # PERDAS TÉCNICAS TOTAIS [kVA]
    # ___________________________________________________________________________________________________________________
    Grand_Losses = dss.circuit_losses()  # Grand_Losses[0]=P  Grand_Losses[1]=Q

    # POTENCIA COMPLEXA TOTAL [kVA]
    # ___________________________________________________________________________________________________________________
    Grand_CircuitPower = dss.circuit_totalpower()

    # POTÊNCIA NAS CARGAS
    # ___________________________________________________________________________________________________________________
    dss.loads_first()
    for i in range(0, len(Load_Name)):
        dss.circuit_setactiveelement(Load_Name[i])
        Grand_ElementCurrent.insert(i, dss.cktelement_currentsmagang())
        Grand_ElementVoltagepu.insert(i, dss.cktelement_voltagesmagang())
        Grand_ElementPower.insert(i, dss.cktelement_powers())

        if (dss.cktelement_numphases()) >= 3:
            Grand_LoadPower[i][0] = Grand_ElementPower[i][0] + Grand_ElementPower[i][2] + Grand_ElementPower[i][4]
            Grand_LoadPower[i][1] = Grand_ElementPower[i][1] + Grand_ElementPower[i][3] + Grand_ElementPower[i][5]
            Grand_LoadPower[i][2] = ((Grand_LoadPower[i][0]) ** 2 + (Grand_LoadPower[i][1]) ** 2) ** (0.5)
            Grand_LoadPower[i][3] = (Grand_LoadPower[i][0]) / (Grand_LoadPower[i][2])

        elif (dss.cktelement_numphases()) < 3:
            Grand_LoadPower[i][0] = Grand_ElementPower[i][0] + Grand_ElementPower[i][2]
            Grand_LoadPower[i][1] = Grand_ElementPower[i][1] + Grand_ElementPower[i][3]
            Grand_LoadPower[i][2] = ((Grand_LoadPower[i][0]) ** 2 + (Grand_LoadPower[i][1]) ** 2) ** (0.5)
            Grand_LoadPower[i][3] = (Grand_LoadPower[i][0]) / (Grand_LoadPower[i][2])

        dss.loads_next()

    # CARREGAMENTO NAS LINHAS
    # __________________________________________________________________________________________________________________
    CondutoresCandidatos = np.copy(CondutoresAtuais)
    for i in range(0, dss.lines_count()):

        # linhas trifásicas cabo phase ABC=336 e Cabo Neutral= 4/0
        if Line_NumPhase[i] == 3:
            if (Grand_LinePhases[i][0] == 1) and (Grand_LinePhases[i][1] == 2) and (Grand_LinePhases[i][2] == 3):
                Grand_ChargingCurrent_phaseA[i][0] = Grand_LineCurrent[i][0] / CondutoresCandidatos[i][0]
                Grand_ChargingCurrent_phaseB[i][0] = Grand_LineCurrent[i][2] / CondutoresCandidatos[i][0]
                Grand_ChargingCurrent_phaseC[i][0] = Grand_LineCurrent[i][4] / CondutoresCandidatos[i][0]

        # linhas bifásicas cabo phase ABC=336 e Cabo Neutral= 4/0
        elif Line_NumPhase[i] == 2:
            if (Grand_LinePhases[i][0] == 1) and (Grand_LinePhases[i][1] == 2):
                Grand_ChargingCurrent_phaseA[i][0] = Grand_LineCurrent[i][0] / CondutoresCandidatos[i][0]
                Grand_ChargingCurrent_phaseB[i][0] = Grand_LineCurrent[i][2] / CondutoresCandidatos[i][0]
            elif (Grand_LinePhases[i][0] == 1) and (Grand_LinePhases[i][1] == 3):
                Grand_ChargingCurrent_phaseA[i][0] = Grand_LineCurrent[i][0] / CondutoresCandidatos[i][0]
                Grand_ChargingCurrent_phaseC[i][0] = Grand_LineCurrent[i][2] / CondutoresCandidatos[i][0]
            elif (Grand_LinePhases[i][0] == 2) and (Grand_LinePhases[i][1] == 3):
                Grand_ChargingCurrent_phaseB[i][0] = Grand_LineCurrent[i][0] / CondutoresCandidatos[i][0]
                Grand_ChargingCurrent_phaseC[i][0] = Grand_LineCurrent[i][2] / CondutoresCandidatos[i][0]

        # linhas monofásicas cabo phase ABC=1/0 e Cabo Neutral= 1/0
        elif Line_NumPhase[i] == 1:
            if (Grand_LinePhases[i][0] == 1):
                Grand_ChargingCurrent_phaseA[i][0] = Grand_LineCurrent[i][0] / CondutoresCandidatos[i][0]
            elif (Grand_LinePhases[i][0] == 2):
                Grand_ChargingCurrent_phaseB[i][0] = Grand_LineCurrent[i][0] / CondutoresCandidatos[i][0]
            elif (Grand_LinePhases[i][0] == 3):
                Grand_ChargingCurrent_phaseC[i][0] = Grand_LineCurrent[i][0] / CondutoresCandidatos[i][0]

    # NOVOS CARREGAMENTOS E CUSTOS
    # __________________________________________________________________________________________________________________
    for i in range(0, dss.lines_count()):

        # linhas trifásicas cabo phase ABC=336 e Cabo Neutral= 4/0
        if Line_NumPhase[i] == 3:
            if (Grand_LinePhases[i][0] == 1) and (Grand_LinePhases[i][1] == 2) and (Grand_LinePhases[i][2] == 3):
                if (Grand_ChargingCurrent_phaseA[i][0] > CarregAdm) or (
                        Grand_ChargingCurrent_phaseB[i][0] > CarregAdm) or (
                        Grand_ChargingCurrent_phaseC[i][0] > CarregAdm):
                    Grand_New_ChargingCurrent_phaseA[i][0] = Grand_LineCurrent[i][0] / Cabos_Hplanejamento[i][2]
                    Grand_New_ChargingCurrent_phaseB[i][0] = Grand_LineCurrent[i][2] / Cabos_Hplanejamento[i][2]
                    Grand_New_ChargingCurrent_phaseC[i][0] = Grand_LineCurrent[i][4] / Cabos_Hplanejamento[i][2]
                    CondutoresCandidatos[i][0] = Cabos_Hplanejamento[i][2]
                    CustoAnual[i][0] = PlanoCusto[i][0]

        # linhas bifásicas cabo phase ABC=336 e Cabo Neutral= 4/0
        elif Line_NumPhase[i] == 2:
            if (Grand_LinePhases[i][0] == 1) and (Grand_LinePhases[i][1] == 2):
                if (Grand_ChargingCurrent_phaseA[i][0] > CarregAdm) or (
                        Grand_ChargingCurrent_phaseB[i][0] > CarregAdm):
                    Grand_New_ChargingCurrent_phaseA[i][0] = Grand_LineCurrent[i][0] / Cabos_Hplanejamento[i][2]
                    Grand_New_ChargingCurrent_phaseB[i][0] = Grand_LineCurrent[i][2] / Cabos_Hplanejamento[i][2]
                    CondutoresCandidatos[i][0] = Cabos_Hplanejamento[i][2]
                    CustoAnual[i][0] = PlanoCusto[i][0]

            elif (Grand_LinePhases[i][0] == 1) and (Grand_LinePhases[i][1] == 3):
                if (Grand_ChargingCurrent_phaseA[i][0] > CarregAdm) or (
                        Grand_ChargingCurrent_phaseC[i][0] > CarregAdm):
                    Grand_New_ChargingCurrent_phaseA[i][0] = Grand_LineCurrent[i][0] / Cabos_Hplanejamento[i][2]
                    Grand_New_ChargingCurrent_phaseC[i][0] = Grand_LineCurrent[i][2] / Cabos_Hplanejamento[i][2]
                    CondutoresCandidatos[i][0] = Cabos_Hplanejamento[i][2]
                    CustoAnual[i][0] = PlanoCusto[i][0]

            elif (Grand_LinePhases[i][0] == 2) and (Grand_LinePhases[i][1] == 3):
                if (Grand_ChargingCurrent_phaseB[i][0] > CarregAdm) or (
                        Grand_ChargingCurrent_phaseC[i][0] > CarregAdm):
                    Grand_New_ChargingCurrent_phaseB[i][0] = Grand_LineCurrent[i][0] / Cabos_Hplanejamento[i][2]
                    Grand_New_ChargingCurrent_phaseC[i][0] = Grand_LineCurrent[i][2] / Cabos_Hplanejamento[i][2]
                    CondutoresCandidatos[i][0] = Cabos_Hplanejamento[i][2]
                    CustoAnual[i][0] = PlanoCusto[i][0]

        # linhas monofásicas cabo phase ABC=1/0 e Cabo Neutral= 1/0
        elif Line_NumPhase[i] == 1:
            if (Grand_LinePhases[i][0] == 1):
                if (Grand_ChargingCurrent_phaseA[i][0] > CarregAdm):
                    Grand_New_ChargingCurrent_phaseA[i][0] = Grand_LineCurrent[i][0] / Cabos_Hplanejamento[i][2]
                    CondutoresCandidatos[i][0] = Cabos_Hplanejamento[i][2]
                    CustoAnual[i][0] = PlanoCusto[i][0]

            elif (Grand_LinePhases[i][0] == 2):
                if (Grand_ChargingCurrent_phaseB[i][0] > CarregAdm):
                    Grand_New_ChargingCurrent_phaseB[i][0] = Grand_LineCurrent[i][0] / Cabos_Hplanejamento[i][2]
                    CondutoresCandidatos[i][0] = Cabos_Hplanejamento[i][2]
                    CustoAnual[i][0] = PlanoCusto[i][0]

            elif (Grand_LinePhases[i][0] == 3):
                if (Grand_ChargingCurrent_phaseC[i][0] > CarregAdm):
                    Grand_New_ChargingCurrent_phaseC[i][0] = Grand_LineCurrent[i][0] / Cabos_Hplanejamento[i][2]
                    CondutoresCandidatos[i][0] = Cabos_Hplanejamento[i][2]
                    CustoAnual[i][0] = PlanoCusto[i][0]

    CustoTotal = np.sum(CustoAnual[:][:])

    return Grand_Losses, \
           Grand_CircuitPower, \
           Grand_Voltagepu, \
           Grand_LineCurrent, \
           Grand_LoadPower, \
           Grand_ChargingCurrent_phaseA, \
           Grand_ChargingCurrent_phaseB, \
           Grand_ChargingCurrent_phaseC, \
           Grand_New_ChargingCurrent_phaseA, \
           Grand_New_ChargingCurrent_phaseB, \
           Grand_New_ChargingCurrent_phaseC, \
           CondutoresCandidatos,\
           CustoAnual,\
           CustoTotal

def Binarizacao(VetReal):
    VetBin = np.zeros((1, len(VetReal)))

    for l in range(0, len(VetReal)):

        VetBin[0][l] = 1 / (1 + np.exp(-VetReal[l]))

        if VetBin[0][l] >= 0.5:
            VetBin[0][l] = 1
        elif VetBin[0][l] < 0.5:
            VetBin[0][l] = 0

    return VetBin

def Float2Int(Xfloat):
    Xint = []
    Xint.clear()

    for i in range(0, len(Xfloat[0][:])):
        if Xfloat[0][i] == 1:
            Xint.insert(i, 1)
        else:
            Xint.insert(i, 0)

    return Xint
''
def ExpansaoCarga(t):

    Load_P_kw = np.zeros((dss.loads_count(), 1))
    Load_Qkvar = np.zeros((dss.loads_count(), 1))
    Load_S_kva = np.zeros((dss.loads_count(), 1))
    Load_fp = np.zeros((dss.loads_count(), 1))
    Load_U_kV = np.zeros((dss.loads_count(), 1))

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

    dss.loads_first()
    for i in range(0, dss.loads_count()):
        dss.text('Edit Load.{} Bus1={}    Phases={} Conn={}   Model={} kV={}   kW={}  kvar={}'.format(
            Load_Name[i], Load_bus[i], Load_phases[i], Load_Conn[i], Load_model[i], Load_U_kV[i],
            Load_P_kw[i] * (1 + t*ExpCarga), Load_Qkvar[i] * (1 + t*ExpCarga)))

        dss.loads_next()

def ContracaoCarga(t):

    Load_P_kw = np.zeros((dss.loads_count(), 1))
    Load_Qkvar = np.zeros((dss.loads_count(), 1))
    Load_S_kva = np.zeros((dss.loads_count(), 1))
    Load_fp = np.zeros((dss.loads_count(), 1))
    Load_U_kV = np.zeros((dss.loads_count(), 1))

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

    dss.loads_first()
    for i in range(0, dss.loads_count()):
        dss.text('Edit Load.{} Bus1={}    Phases={} Conn={}   Model={} kV={}   kW={}  kvar={}'.format(
            Load_Name[i], Load_bus[i], Load_phases[i], Load_Conn[i], Load_model[i], Load_U_kV[i],
            Load_P_kw[i] / (1 + t*ExpCarga), Load_Qkvar[i] / (1 + t*ExpCarga)))

        dss.loads_next()

def PlanoExpansao(H_Planejamento,AnoPlanejado,AmpacidadeCondutores):


    """______________________________________________________________________________________________________________"""
    #                                                DEFININDO PLANO DE EXPANSÃO
    """______________________________________________________________________________________________________________"""

    CustoExpansao = np.zeros((dss.lines_count(), 1))
    LineNumCond = []
    Corrente_Hplanejamento = []
    Cabos_Hplanejamento = np.zeros((dss.lines_count(), 3))


    # EXPANSÃO DA DEMANDA DE ENERGIA PARA O HORIZONTE DE PLANEJAMENTO
    ContracaoCarga(AnoPlanejado)
    dss.solution_solve()
    ExpansaoCarga(H_Planejamento)
    dss.solution_solve()

    # COLETA A CORRENTE DAS LINHAS NO HORIZONTE DE PLANEJAMENTO
    dss.lines_first()
    for i in range(0, dss.lines_count()):
        dss.circuit_setactiveelement(Line_Name[i])
        LineNumCond.insert(i, dss.cktelement_numconductors())
        dss.lines_next()

    dss.lines_first()
    for i in range(0, len(Line_Name)):
        dss.circuit_setactiveelement(Line_Name[i])
        Corrente_Hplanejamento.insert(i, dss.cktelement_currentsmagang())

        if (Corrente_Hplanejamento[i][0] / AmpacidadeCondutores[i][0]) > CarregAdm:

            for j in range(0, len(CabosDados[1][:]) - 1):

                if int(round(Corrente_Hplanejamento[i][0], 0)) in range(int(round(CarregAdm * CabosDados[1][j], 0)),
                                                                        int(round(CarregAdm * CabosDados[1][j + 1],
                                                                                  0))):

                    # RECONDUTORAMENTO
                    # __________________________________________________________________________________________________
                    if Corrente_Hplanejamento[i][0] < round(CarregAdm * CabosDados[1][6], 0):

                        # 1 - R: CABOS EM ESTOQUE_______________________________________________________________________
                        for k in range(0, len(Cabos_Retirados)):
                            if (Corrente_Hplanejamento[i][0] < round(CarregAdm * Cabos_Retirados[k][0], 0)) and (
                                    Line_comp[i] <= Cabos_Retirados[k][1]):
                                Cabos_Hplanejamento[i][0] = CondutorOriginal[i][0]
                                Cabos_Hplanejamento[i][1] = Cabos_Retirados[k][0]
                                Cabos_Hplanejamento[i][2] = Cabos_Retirados[k][0]

                                CustoExpansao[i][0] = (Porc_custo_fixo) * (1.60934) * (Line_comp[i]) * \
                                                      (CabosCustosRecond[
                                                          CabosDados[1][:].index(AmpacidadeCondutores[i][0])] \
                                                          [CabosDados[1][:].index(Cabos_Retirados[k][0])])
                                Cabos_Retirados[k][0] = -1
                                break

                        # 2 - R: NOVOS CABOS________________________________________________________________________________
                        if (int(round(Corrente_Hplanejamento[i][0], 0)) in range(
                                int(round(CarregAdm * CabosDados[1][0], 0)),
                                int(round(CarregAdm * CabosDados[1][6], 0)))) and (
                                Cabos_Hplanejamento[i][2] == 0):
                            Cabos_Hplanejamento[i][0] = CondutorOriginal[i][0]
                            Cabos_Hplanejamento[i][1] = CabosDados[1][j + 1]
                            Cabos_Hplanejamento[i][2] = CabosDados[1][j + 1]

                            Cabos_Retirados[i][0] = CondutorOriginal[i][0]
                            Cabos_Retirados[i][1] = Line_comp[i]

                            CustoExpansao[i][0] = (Porc_custo_fixo) * (1.60934) * (Line_comp[i]) * \
                                                  (CabosCustosRecond[CabosDados[1][:].index(AmpacidadeCondutores[i])][
                                                      j + 1]) \
                                                  + (1 - Porc_custo_fixo) * (LineNumCond[i] / 3) * (1.60934) * (
                                                  Line_comp[i]) \
                                                  * (CabosCustosRecond[CabosDados[1][:].index(AmpacidadeCondutores[i])][
                                j + 1])

                    # CONSTRUÇÃO DE NOVA LINHA + RECONDUTORAMENTO
                    # __________________________________________________________________________________________________

                    if Corrente_Hplanejamento[i][0] > round(CarregAdm * CabosDados[1][6], 0):

                        # 1 - R + NL: CABOS EM ESTOQUE__________________________________________________________________
                        for k in range(0, len(Cabos_Retirados)):

                            if (Corrente_Hplanejamento[i][0] < round(
                                    CarregAdm * (Cabos_Retirados[k][0] + CabosDados[1][6]
                                    ), 0)) and (Line_comp[i] <= Cabos_Retirados[k][1])and(i>8):

                                if CondutorOriginal[i][0] == CabosDados[1][4]:
                                    Cabos_Hplanejamento[i][0] = CabosDados[1][4]
                                    Cabos_Hplanejamento[i][1] = CabosDados[1][6]
                                    Cabos_Hplanejamento[i][2] = Cabos_Retirados[k][0] + CabosDados[1][6]
                                    CustoExpansao[i][0] = CabosCustosConstr[0][6] * 1.60934 * Line_comp[i]
                                    break
                                else:

                                    CustoExpansao[i][0] = CabosCustosConstr[0][6] + (Porc_custo_fixo) * (1.60934) * \
                                                          (Line_comp[i]) * (CabosCustosRecond[3][4])
                                    Cabos_Retirados[k][0] = -1
                                    break

                        # 2 - R + NL: NOVOS CABOS_______________________________________________________________________
                        if (Corrente_Hplanejamento[i][0] < round(CarregAdm * (CabosDados[1][j + 1]), 0)) and (
                                Cabos_Hplanejamento[i][2] == 0):
                            Cabos_Retirados[i][0] = CondutorOriginal[i][0]
                            Cabos_Retirados[i][1] = Line_comp[i]

                            Cabos_Hplanejamento[i][0] = CabosDados[1][6]
                            Cabos_Hplanejamento[i][1] = CabosDados[1][j + 1] - CabosDados[1][6]
                            Cabos_Hplanejamento[i][2] = CabosDados[1][j + 1]

                            CustoExpansao[i][0] = 1.60934 * (Line_comp[i]) * (CabosCustosConstr[0][j + 1]) * \
                                                  (1 - Porc_custo_fixo) * LineNumCond[i] / 3 + 1.60934 * (Line_comp[i]) \
                                                  * (CabosCustosConstr[0][j + 1]) * (Porc_custo_fixo)

                    # 3 - CORRENTE MENOR DE 150 A_______________________________________________________________________
                    if Corrente_Hplanejamento[i][0] < CarregAdm * CabosDados[1][0]:

                        # 3.1 - CORRENTE MENOR DE 150 A E CABOS MAIORES DO QUE 150A ____________________________________
                        if CabosDados[1][0] != CondutorOriginal[i][0]:
                            Cabos_Retirados[i][0] = CondutorOriginal[i][0]
                            Cabos_Retirados[i][1] = Line_comp[i]

                            Cabos_Hplanejamento[i][0] = CondutorOriginal[i][0]
                            Cabos_Hplanejamento[i][1] = CabosDados[1][0]
                            Cabos_Hplanejamento[i][2] = CabosDados[1][0]

                            CustoExpansao[i][0] = (Porc_custo_fixo) * (1.60934) * (Line_comp[i]) * \
                                                  (
                                                  CabosCustosRecond[CabosDados[1][:].index(AmpacidadeCondutores[i])][j]) \
                                                  + (1 - Porc_custo_fixo) * (LineNumCond[i] / 3) * (1.60934) * (
                                                  Line_comp[i]) \
                                                  * (
                                                  CabosCustosRecond[CabosDados[1][:].index(AmpacidadeCondutores[i])][j])

                        # 4 - CORRENTE MENOR DE 150 A SEM ALTERAÇÃO_____________________________________________________
                        else:
                            Cabos_Hplanejamento[i][0] = CondutorOriginal[i][0]
                            Cabos_Hplanejamento[i][1] = CabosDados[1][0]
                            Cabos_Hplanejamento[i][2] = CondutorOriginal[i][0]

        # 1 - NÃO EXCEDERAM LIMITE DE CARREGAMENTO______________________________________________________________________
        else:
            Cabos_Hplanejamento[i][0] = AmpacidadeCondutores[i][0]
            Cabos_Hplanejamento[i][1] = 0
            Cabos_Hplanejamento[i][2] = AmpacidadeCondutores[i][0]

            if i >= 122:
                Cabos_Hplanejamento[i][0] = np.inf
                Cabos_Hplanejamento[i][1] = 0
                Cabos_Hplanejamento[i][2] = np.inf

        dss.lines_next()

    # CONTRAÇÃO DA DEMANDA
    ContracaoCarga(H_Planejamento)
    dss.solution_solve()
    ExpansaoCarga(AnoPlanejado)
    dss.solution_solve()


    return Cabos_Hplanejamento, CustoExpansao

def Ranking(M_Resultado):

    M_resultado_rankeada = []
    M_Custos = []
    for i in range(0,len(M_Resultado[:])):
       M_Custos.insert(i, M_Resultado[i][13])

    M_Custos_ordenada = sorted(M_Custos)
    M_Custos.index(M_Custos[0])

    for i in range(0,len(M_Custos)):
        M_resultado_rankeada.insert(i,M_Resultado[M_Custos.index(M_Custos_ordenada[i])])

    return M_resultado_rankeada

"""
####################################################################################################################
                                            PARÂMETROS DA SIMULAÇÃO
####################################################################################################################
"""


"""_____________________________________________________________________________________________________________________"""
# PARAMETROS GERAIS
"""_____________________________________________________________________________________________________________________"""
STO              = 'nao'   # simular SISTEMA TESTE ORIGINAL
N                = 25      # Número de libélulas (solucões) iniciais
CarregAdm        = 0.66    # Carregamento Admissível nas linhas
Load_VariacaoPot = 0.95    # % da potencia da carga que deve ser atendida
ExpCarga         = 0.07    # % em que a potencia das cargas crescem anualmente
H_Planejamento   = 3       # Horizonte em anos do planejamento
Porc_custo_fixo  = 0.35    # porcentagem de custo fixo da expansão
max_iter         = 50      # Número máximo de iterações
Xmax             = +5      # Valor máximo que a sigmoide pode assumir
Xmin             = -5      # Valor mínimo que a sigmoide pode assumir
peso             = +1      # % do peso dos parametros s,a,c
pesof            = +2      # % do peso do parametro f
salvar           = 'sim'
Nobjetivos       = 2
"""_____________________________________________________________________________________________________________________"""
# PARAMETROS DO CIRCUITO
"""_____________________________________________________________________________________________________________________"""
NameElements = dss.circuit_allelementnames()
Element_numphases = []
Element_busname = []
U_barras = dss.circuit_allbusvmag()

# ENCONTRANDO O NOME DA BARRA E O NUMERO DE FASES
for i in range(0, len(NameElements)):
    dss.circuit_setactiveelement(NameElements[i])
    Element_numphases.insert(i, dss.cktelement_numphases())
    Element_busname.insert(i, dss.cktelement_read_busnames())

"""_____________________________________________________________________________________________________________________"""
# DECLARAÇÕES DAS VARIÁVEIS
"""_____________________________________________________________________________________________________________________"""
Load_P_kw = np.zeros((dss.loads_count(), 1))
Load_Qkvar = np.zeros((dss.loads_count(), 1))
Load_S_kva = np.zeros((dss.loads_count(), 1))
Load_fp = np.zeros((dss.loads_count(), 1))
Load_U_kV = np.zeros((dss.loads_count(), 1))
Load_Name = []
Load_Conn = []
Load_model = []
oad_bus = []
Load_phases = []
Line_Name = []
Line_comp = []
Line_Code = []
Line_NumPhase = []
CondutorOriginal = np.zeros((dss.lines_count(), 1))
Cabos_Retirados = np.zeros((dss.lines_count(), 2))

"""_____________________________________________________________________________________________________________________"""
# PARAMETROS DOS CABOS DO ALIMENTADOR  [AMPACIDADE A | CUSTO R$/km]
"""_____________________________________________________________________________________________________________________"""
CabosDados = [['CAA1', 'CAA2', 'CAA3', 'CAA4', 'CAA5', 'CAA6', 'CAA7',
               'CAA7+CAA1', 'CAA7+CAA2', 'CAA7+CAA6', 'CAA7+CAA7',],  # CABOS[0][:]NOME       CABO
              [150.00, 250.00, 350.00, 400.00, 500.00, 600.00, 790.00, 1390, 1580]]  # CABOS[1][:]AMPACIDADE CABO

CabosCustosRecond = [[0, 40200, 64700, 70000, 101400, 132900, 194900],
                     [0, 0.000, 52500, 61200,  87400, 115400, 176400],
                     [0, 0.000, 0.000, 50700,  75200,  92700, 157900],
                     [0, 0.000, 0.000, 0.000,  61200,  78700, 139400],
                     [0, 0.000, 0.000, 0.000,  0.000,  66500, 120900],
                     [0, 0.000, 0.000, 0.000,  0.000,  0.000, 102900]]

CabosCustosConstr = [[35000, 52500, 73500, 87400, 117200, 148700, 213400, 251100, 315800]]

"""_____________________________________________________________________________________________________________________"""
# PARAMETROS DAS CARGAS
"""_____________________________________________________________________________________________________________________"""

dss.loads_first()
for i in range(0, dss.loads_count()):
    Load_P_kw[i][0] = dss.loads_read_kw()
    Load_Qkvar[i][0] = dss.loads_read_kvar()
    Load_Name.insert(i, dss.loads_read_name())
    Load_Conn.insert(i, dss.loads_read_isdelta())
    Load_U_kV[i][0] = dss.loads_read_kv()
    Load_model.insert(i, dss.loads_read_model())
    Load_bus = ['1.1', '2.2', '4.3', '5.3', '6.3', '7.1', '9.1', '10.1', '11.1', '12.2', '16.3', '17.3', '19.1', '20.1',
                '22.2', '24.3', '28.1', '29.1', '30.3', '31.3', '32.3', '33.1', '34.3', '35.1.2', '37.1', '38.2',
                '39.2', '41.3', '42.1', '43.2', '45.1', '46.1', '47', '48', '49.1', '49.2', '49.3', '50.3', '51.1',
                '52.1', '53.1', '55.1', '56.2', '58.2', '59.2', '60.1', '62.3', '63.1', '64.2', '65.1.2', '65.2.3',
                '65.3.1', '66.3', '68.1', '69.1', '70.1', '71.1', '73.3', '74.3', '75.3', '76.1.2', '76.2.3', '76.3.1',
                '77.2', '79.1', '80.2', '82.1', '83.3', '84.3', '85.3', '86.2', '87.2', '88.1', '90.2', '92.3', '94.1',
                '95.2', '96.2', '98.1', '99.2', '100.3', '102.3', '103.3', '104.3', '106.2', '107.2', '109.1', '111.1',
                '112.1', '113.1', '114.1']
    S = ((dss.loads_read_kw()) ** 2 + (dss.loads_read_kvar()) ** 2) ** (1 / 2)
    fp = dss.loads_read_kw() / S
    Load_S_kva[i][0] = S
    Load_fp[i][0] = fp

    dss.circuit_setactiveelement(Load_Name[i])
    Load_phases.insert(i, dss.cktelement_numphases())
    dss.loads_next()

"""_____________________________________________________________________________________________________________________"""
# PARAMETROS DAS LINHAS
"""_____________________________________________________________________________________________________________________"""

dss.lines_first()
for i in range(0, dss.lines_count()):
    Line_Name.insert(i, dss.lines_read_name())
    Line_comp.insert(i, dss.lines_read_length())
    Line_Code.insert(i, dss.lines_read_linecode())
    Line_NumPhase.insert(i, dss.lines_read_phases())

    if (Line_Code[i] == '1') or (Line_Code[i] == '2') or (Line_Code[i] == '3') or (Line_Code[i] == '4') or (
            Line_Code[i] == '5') or (Line_Code[i] == '6'):
        CondutorOriginal[i][0]=500

    elif (Line_Code[i] == '7') or (Line_Code[i] == '8'):
        CondutorOriginal[i][0]=500

    elif (Line_Code[i] == '9') or (Line_Code[i] == '10') or (Line_Code[i] == '11'):
        CondutorOriginal[i][0]=150

    elif (Line_Code[i] == '12'):
        CondutorOriginal[i][0]=500

    else:
        CondutorOriginal[i][0]=np.inf


    dss.lines_next()

CondutoresAtuais = CondutorOriginal

# DECLARAÇÕES DAS SWITCHS
Switch_Names = dss.swtcontrols_allnames()
Switch_AllStates = []
Switch_State = []


"""
########################################################################################################################

                                            INICIO DO ALGORITMO
                                     DRAGONFLY ALGORITHM OPTIMIZATION
                                            
########################################################################################################################
"""


"""_____________________________________________________________________________________________________________________"""
# PARÂMETROS DE ENTRADA DA
"""_____________________________________________________________________________________________________________________"""
nVar  = len(Switch_Names)  # Número de Switches do Alimentados menos a chave da subestação
dim   = nVar

"""_____________________________________________________________________________________________________________________"""
# DECLARAÇÕES DAS VARIAVEIS DO DAO
"""_____________________________________________________________________________________________________________________"""
Best_pos = np.zeros((H_Planejamento+1, nVar), dtype=np.int)
CondutoresUtilizados = np.zeros((dss.lines_count(),H_Planejamento+1))
M_Resultado_ano = []


"""_____________________________________________________________________________________________________________________"""
#                                                     INICIO DO ALGORITMO
"""_____________________________________________________________________________________________________________________"""

for ii in range(0, H_Planejamento+1):

    """_________________________________________________________________________________________________________________"""
    # DECLARAÇÃO DAS VARIÁVEIS
    """_________________________________________________________________________________________________________________"""

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

    """_________________________________________________________________________________________________________________"""
    # 1 - INICIALIZANDO A POPULAÇÃO DE LIBÉLULAS INICIAL: deltaX e X cujo [linhas=Libélulas, colunas=variaveis]
    """_________________________________________________________________________________________________________________"""
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

    """_________________________________________________________________________________________________________________"""
    # 2 - INÍCIO DO LOOP DO DAO
    """_________________________________________________________________________________________________________________"""
    for iter in range(0, max_iter):

        print('\n' * 25)
        print('EXECUTANDO O BDA PARA IEEE123: Minimização de CUSTO DA EXPANSÃO e PERDAS TÉCNICAS')
        print('_____________________________')
        print('Ano: {} Horizonte Planejamento: {} Expansao Anual(%): {} Nlibelulas:{} max_iter:{} Nchaves:{} '.format(
            ii, H_Planejamento, int(ExpCarga * 100), N, max_iter, dss.swtcontrols_count()))
        print('Loading: {} %'.format(int(iter * 100 / max_iter)))

        """__________________________________________________________________________________________________________"""
        # 3 - INICIALIZANDO OS PESOS s,a,c,f,e,w
        """__________________________________________________________________________________________________________"""

        w = 0.9 - iter * (0.5 / max_iter)
        my_c = 0.1 - iter * (0.1 / (max_iter / 2))
        my_c = my_c/100
        if my_c < 0:
            my_c = 1 / 100

        if iter < (3 * max_iter / 4):
            s = peso * my_c * random.uniform(0, 1)  # coeficiente de separação
            a = peso * my_c * random.uniform(0, 1)  # coeficiente de alinhamento
            c = peso * my_c * random.uniform(0, 1)  # coeficiente de coesão
            f = pesof * random.uniform(0, 1)  # coeficiente de atração por comida
            e = my_c  # coeficiente de distração do inimigo

        else:
            s = my_c / iter  # coeficiente de separação
            a = my_c / iter  # coeficiente de alinhamento
            c = my_c / iter  # coeficiente de coesão
            f = pesof * random.uniform(0, 1)  # coeficiente de atração por comida
            e = my_c / iter  # coeficiente de distração do inimigo

        """__________________________________________________________________________________________________________"""
        # 4 - CALCULO DAS FUNÇÕES OBJETIVO
        """__________________________________________________________________________________________________________"""
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

            PlanoCondutores, PlanoCusto = PlanoExpansao(H_Planejamento,ii,CondutoresAtuais)
            Grandezas_Coletadas = ColetarGrandezas(PlanoCondutores, PlanoCusto, CondutoresAtuais)
            Grand_LoadPower = np.copy(Grandezas_Coletadas[4][:])
            Grandezas_Coletadas = list(Grandezas_Coletadas)
            Grandezas_Coletadas.append(X[i][:])

            for j in range(0, len(Grand_LoadPower)):
                if (Load_VariacaoPot * Load_S_kva[j]) > (round(Grand_LoadPower[j][2], 0)):
                    Loads_Status = Loads_Status + 1

            if Loads_Status == 0:
                M_Resultado.insert(len(M_Resultado)+1, list(Grandezas_Coletadas))


        M_Resultado_rankeada = Ranking(M_Resultado)
        Convergence_curve[iter][0] = M_Resultado_rankeada[0][13]
        Convergence_curve[iter][1] = M_Resultado_rankeada[0][0][0]
        Food_fitness = M_Resultado_rankeada[0][13]
        Food_pos = M_Resultado_rankeada[0][14]
        Food_Line = M_Resultado_rankeada[0][11]
        Enemy_fitness = M_Resultado_rankeada[len(M_Resultado[:])-1][13]
        Enemy_pos = M_Resultado_rankeada[len(M_Resultado[:])-1][14]

        """__________________________________________________________________________________________________________"""
        # 6 - ATUALIZAÇÃO DE S,A,C,F,E e deltaX
        """__________________________________________________________________________________________________________"""
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
            A[0][:] = (np.transpose(np.sum(np.transpose(Neighbours_DeltaX)))) / neighbours_no

            # COESÃO
            C_temp = (np.transpose(np.sum(np.transpose(Neighbours_X)))) / neighbours_no
            C[0][:] = C_temp - X[i][:]

            # ATRAÇÃO POR COMIDA
            F[0][:] = Food_pos - X[i][:]

            # DISTRAÇÃO DO INIMIGO
            E[0][:] = Enemy_pos + X[i][:]

            """______________________________________________________________________________________________________"""
            # 7 - ATUALIZANDO O VETOR DE PASSO DeltaXi
            """______________________________________________________________________________________________________"""

            for j in range(0, dim):

                deltaX[i][j] = np.copy(s * S[0][j] + a * A[0][j] + c * C[0][j] + f * F[0][j] + e * E[0][j] + w * deltaX[i][j])

                if deltaX[i][j] > Xmax:
                    deltaX[i][j] = Xmax
                if deltaX[i][j] < Xmin:
                    deltaX[i][j] = Xmin

                X[i][j] = np.copy(X[i][j] + deltaX[i][j])

                if X[i][j] > Xmax:
                    X[i][j] = Xmax
                if X[i][j] < Xmin:
                    X[i][j] = Xmin

    """______________________________________________________________________________________________________________"""
    # 8 - RECONFIGURANDO O ALIMENTADOR E CALCULANDO GRANDEZAS PARA NOVO ANO
    """______________________________________________________________________________________________________________"""

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

    """______________________________________________________________________________________________________________"""
    # 10 - ARMAZENAMENTO DOS DADOS ANUAIS
    """______________________________________________________________________________________________________________"""
    M_Resultado_rankeada.insert(len(M_Resultado_rankeada)+1,Convergence_curve)
    M_Resultado_ano.insert(ii,M_Resultado_rankeada)




"""__________________________________________________________________________________________________________________"""


"""
.
.
.
"""

"""
########################################################################################################################

                                                        RESULTADOS FINAIS
                                                        PLANO EXPANSÃO IEEE 123
                                                        COM RECONFIGURAÇÃO

########################################################################################################################
"""

M_Resultado_ano = list(M_Resultado_ano)
M_Resultado_ano.insert(len(M_Resultado_ano)+1,np.concatenate((Load_S_kva,Load_fp)))
M_Resultado_ano.insert(len(M_Resultado_ano)+2,Cabos_Retirados)

if salvar=='sim':
    Nsim = open("C:\PESDEE_123B_RECONF\Resultado\Simulacao.txt","r")
    Nsim = Nsim.read()
    newpath = r'C:\PESDEE_123B_RECONF\Resultado\SIM_{}'.format(Nsim)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # EXPORTANTO DADOS  CONDUTORES RETIRADOS
    dados = M_Resultado_ano
    dt = pd.DataFrame(data=dados)
    dt.to_csv(newpath+''+'\Resultados_Anuais.csv')


print('-=' * 30)
print('Algoritmo executado com exito!')
print('-=' * 30)

"""
########################################################################################################################
                                                        FIM
########################################################################################################################
"""
