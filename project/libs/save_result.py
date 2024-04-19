import os

import numpy as np
import pandas as pd


def save_annual_results(resultado_year, load_S_kva, load_fp, cable_withdrawn, save_result, save_path):
    resultado_year = list(resultado_year)
    resultado_year.insert(len(resultado_year)+1,
                          np.concatenate((load_S_kva, load_fp)))
    resultado_year.insert(len(resultado_year)+2, cable_withdrawn)

    if save_result == 'yes':
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        dados = resultado_year
        dt = pd.DataFrame(data=dados)
        dt.to_csv(os.path.join(save_path, 'yearly_result.csv'))
