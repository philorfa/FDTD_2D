import numpy as np
import sys


np.set_printoptions(threshold=sys.maxsize)


def FDTD_Core_H(Ez, DA, Hx, DB, psi_Hx, deltaX, Hy, psi_Hy, prepared):
    temp_Ezx = -1 * np.diff(Ez[:-1, :], 1, 1)
    temp_Ezy = np.diff(Ez[:, :-1], 1, 0)

    Hx = DA * Hx + DB * (np.multiply(temp_Ezx, prepared.den_hy))
    psi_Hx = np.multiply(prepared.bh_y_all, psi_Hx) + np.multiply(prepared.ch_y_all, temp_Ezx) / deltaX
    Hx = Hx + DB * psi_Hx

    Hy = DA * Hy + DB * (np.multiply(temp_Ezy, prepared.den_hx))
    psi_Hy = np.multiply(prepared.bh_x_all, psi_Hy) + np.multiply(prepared.ch_x_all, temp_Ezy) / deltaX
    Hy = Hy + DB * psi_Hy

    return Hx, Hy, psi_Hx, psi_Hy
