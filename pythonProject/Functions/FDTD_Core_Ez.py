import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)


def FDTD_Core_Ez(Hy, Hx, CA, CB, Kd, Jd, prepared, Ez_c, psi_Ezx, DeltaX, psi_Ezy, Beta_d, dt):
    Ez_former = Ez_c.copy()
    temp_Hy = np.diff(Hy[:, 1::], 1, 0)
    temp_Hx = -1 * np.diff(Hx[1::, :], 1, 1)

    ######## Update main field of Ez ########
    Ez_c = np.multiply(CA, Ez_c) + np.multiply(CB, (
            np.multiply(temp_Hy, prepared.den_ex) + np.multiply(temp_Hx, prepared.den_ey) - 0.5 * (1 + Kd) * Jd))

    ######## Update pml of Ez in x direction ########
    psi_Ezx = np.multiply(prepared.be_x_all, psi_Ezx) + np.multiply(prepared.ce_x_all, temp_Hy) / DeltaX

    ######## Update pml of Ez in y direction ########

    psi_Ezy = np.multiply(prepared.be_y_all, psi_Ezy) + np.multiply(prepared.ce_y_all, temp_Hx) / DeltaX

    Ez_c = Ez_c + np.multiply(CB, psi_Ezx + psi_Ezy)
    Jd = Kd * Jd + np.multiply(Beta_d, (Ez_c - Ez_former)) / dt
    return Ez_c, Jd, psi_Ezx, psi_Ezy
