
def get_elements(dss):
    name_elements = dss.circuit_allelementnames()
    element_n_phases = []
    element_bus_name = []

    for i in range(0, len(name_elements)):
        dss.circuit_setactiveelement(name_elements[i])
        element_n_phases.insert(i, dss.cktelement_numphases())
        element_bus_name.insert(i, dss.cktelement_read_busnames())

    return dss, name_elements, element_n_phases, element_bus_name
