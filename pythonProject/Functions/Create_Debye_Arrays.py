import pandas as pd
import numpy as np


def Create_Debye_Arrays(model_number):
    materials = pd.read_csv('Model' + model_number + '/Data/Debye/Materials_Debye_Parameters.csv')
    mask = pd.read_csv('Model' + model_number + '/Data/Debye/Debye_Mask.csv',header=None)
    Debye_EpsDelta = np.empty(mask.shape)
    Debye_EpsInf = np.empty(mask.shape)
    Debye_Sigma_s = np.empty(mask.shape)

    material_codes = materials.Mask_Code

    for i in material_codes:
        indices = np.where(mask == i)
        indices = np.asarray(indices).T

        Debye_EpsDelta[indices[:, 0], indices[:, 1]] = materials.Delta_Epsilon[
            int(np.where(materials.Mask_Code == i)[0])]
        Debye_EpsInf[indices[:, 0], indices[:, 1]] = materials.Epsilon_Infinity[
            int(np.where(materials.Mask_Code == i)[0])]
        Debye_Sigma_s[indices[:, 0], indices[:, 1]] = materials.Sigma_S[int(np.where(materials.Mask_Code == i)[0])]

    pd.DataFrame(Debye_EpsDelta).to_csv('Model' + model_number + '/Data/Debye/Debye_EpsDelta.csv', index=False,
                                        header=False)
    pd.DataFrame(Debye_EpsInf).to_csv('Model' + model_number + '/Data/Debye/Debye_EpsInf.csv', index=False,
                                      header=False)
    pd.DataFrame(Debye_Sigma_s).to_csv('Model' + model_number + '/Data/Debye/Debye_Sigma_s.csv', index=False,
                                       header=False)

    return
