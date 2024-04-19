path_to_save_results = r'C:\PESDEE_123B_RECONF\Resultado'
dss_file = r"C:\PESDEE_123B_RECONF\A1_IEEE123Bus\Master.DSS"
opendss_path = r"C:\PESDEE_123B_RECONF\A1_IEEE123Bus\Master.DSS"

parameters = {
    "STO": 'nao',  # Simulate Original Test System
    "n_dragonflies": 25,  # Number of initial dragonflies (solutions)
    "loadMax": 0.66,  # Admissible loading on lines
    "load_variation_power": 0.95,  # Percentage of load power to be met
    "load_expansion": 0.07,  # Percentage by which loads power grows annually
    "h_planning": 3,  # Planning horizon in years
    "fixed_cost_percent": 0.35,  # Percentage of fixed cost of expansion
    "max_iter": 50,  # Maximum number of iterations
    "x_max": +5,  # Maximum value the sigmoid can assume
    "x_min": -5,  # Minimum value the sigmoid can assume
    "weight": +1,  # Percentage of weight for parameters s, a, c
    "weight_f": +2,  # Percentage of weight for parameter f
    "save_result": 'sim',  # Whether to save results
    "n_objective": 2  # Number of objectives
}
