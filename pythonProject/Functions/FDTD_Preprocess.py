import math
import numpy as np
from numpy import matlib
from Functions import constants
import sys

np.set_printoptions(threshold=sys.maxsize)


def FDTD_Preprocess(phantom, expreriment_parameters, Debye_model, antennas_setup, preparation):
    dt = phantom.DeltaT
    pml_size = int(expreriment_parameters.pml_coarse)
    dimX = int(Debye_model.Debye_size_x)
    dimY = int(Debye_model.Debye_size_y)

    Imax = dimX + 2 * pml_size
    Jmax = dimY + 2 * pml_size

    preparation.Imax = Imax
    preparation.Jmax = Jmax

    XBB = [i for i in range(pml_size, Imax - pml_size)]
    YBB = [i for i in range(pml_size, Jmax - pml_size)]

    preparation.XBB = XBB
    preparation.YBB = YBB

    exterior_indices = np.where(Debye_model.Debye_Mask == 0)
    preparation.bbSize = len(exterior_indices[0])

    # We create a new area where we have inserted pml, so we want to move the head into the right position, so the air is moved
    # (pml coarse) points with direction diagonally right

    exterior_indices_with_pml_x = [element + pml_size for element in exterior_indices[0]]
    exterior_indices_with_pml_y = [element + pml_size for element in exterior_indices[1]]
    preparation.bbox_exterior_mask_extend = (exterior_indices_with_pml_x, exterior_indices_with_pml_y)

    # next fix the position of the antennas, we add to each position pml_coarse points

    antennas_setup.x_location = list(map(int, antennas_setup.x_location + pml_size))
    antennas_setup.y_location = list(map(int, antennas_setup.y_location + pml_size))

    # SET PML PARAMETERS

    eta = math.sqrt(constants.AIR_PERMEABILITY / (constants.AIR_PERMITTIVITY * phantom.EpsS))
    poly_m = 3  # polynomial order for pml grading
    alpha_m = 1.0
    sig_opt = 0.8 * (poly_m + 1.0) / (eta * phantom.DeltaX)
    sig_x_max = sig_opt
    sig_y_max = sig_x_max
    alpha_x_max = 0.03  # 0.24
    alpha_y_max = alpha_x_max
    kappa_x_max = 1.0  # 2.0
    kappa_y_max = kappa_x_max

    ########## FDTD parameters for E and H fields ##########
    ### !!!!!!!!!!!!!!!! E field exists on DT but H field exists on DT/2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    ## E-field

    # x-dir

    be_x = np.zeros((pml_size, 1))
    ce_x = np.zeros((pml_size, 1))
    alphae_x_PML = np.zeros((pml_size, 1))
    sige_x_PML = np.zeros((pml_size, 1))
    kappae_x_PML = np.zeros((pml_size, 1))

    # y-dir

    be_y = np.zeros((pml_size, 1))
    ce_y = np.zeros((pml_size, 1))
    alphae_y_PML = np.zeros((pml_size, 1))
    sige_y_PML = np.zeros((pml_size, 1))
    kappae_y_PML = np.zeros((pml_size, 1))

    ## H-field
    # x-dir

    bh_x = np.zeros((pml_size - 1, 1))
    ch_x = np.zeros((pml_size - 1, 1))
    alphah_x_PML = np.zeros((pml_size - 1, 1))
    sigh_x_PML = np.zeros((pml_size - 1, 1))
    kappah_x_PML = np.zeros((pml_size - 1, 1))

    # y-dir

    bh_y = np.zeros((pml_size - 1, 1))
    ch_y = np.zeros((pml_size - 1, 1))
    alphah_y_PML = np.zeros((pml_size - 1, 1))
    sigh_y_PML = np.zeros((pml_size - 1, 1))
    kappah_y_PML = np.zeros((pml_size - 1, 1))

    # Denominators for the update equations

    den_ex = np.zeros((Imax, Jmax))
    den_hx = np.zeros((Imax - 1, Jmax - 1))
    den_ey = np.zeros((Imax, Jmax))
    den_hy = np.zeros((Imax - 1, Jmax - 1))

    # SET CMPL PARAMETERS IN EACH DIRECTION

    # x-dir
    for i in range(pml_size):
        sige_x_PML[i] = sig_x_max * ((pml_size - (i + 1)) / (pml_size - 1.0)) ** poly_m
        alphae_x_PML[i] = alpha_x_max * (((i + 1) - 1.0) / (pml_size - 1.0)) ** alpha_m
        kappae_x_PML[i] = 1.0 + (kappa_x_max - 1.0) * ((pml_size - (i + 1)) / (pml_size - 1.0)) ** poly_m
        be_x[i] = math.exp(
            -(sige_x_PML[i] / kappae_x_PML[i] + alphae_x_PML[i]) * dt / constants.AIR_PERMITTIVITY)
        if (sige_x_PML[i] == 0.0) and (alphae_x_PML[i] == 0.0) and (i == pml_size - 1):
            ce_x[i] = 0.0
        else:
            ce_x[i] = sige_x_PML[i] * (be_x[i] - 1.0) / (
                    sige_x_PML[i] + kappae_x_PML[i] * alphae_x_PML[i]) / kappae_x_PML[i]

    for i in range(pml_size - 1):
        sigh_x_PML[i] = sig_x_max * ((pml_size - (i + 1) - 0.5) / (pml_size - 1.0)) ** poly_m
        alphah_x_PML[i] = alpha_x_max * (((i + 1) - 0.5) / (pml_size - 1.0)) ** alpha_m
        kappah_x_PML[i] = 1.0 + (kappa_x_max - 1.0) * ((pml_size - (i + 1) - 0.5) / (pml_size - 1.0)) ** poly_m
        bh_x[i] = math.exp(
            -(sigh_x_PML[i] / kappah_x_PML[i] + alphah_x_PML[i]) * dt / constants.AIR_PERMITTIVITY);
        ch_x[i] = sigh_x_PML[i] * (bh_x[i] - 1.0) / (sigh_x_PML[i] + kappah_x_PML[i] * alphah_x_PML[i]) / \
                  kappah_x_PML[i]

    # y -dir

    for j in range(pml_size):
        sige_y_PML[j] = sig_y_max * ((pml_size - (j + 1)) / (pml_size - 1.0)) ** poly_m
        alphae_y_PML[j] = alpha_y_max * (((j + 1) - 1) / (pml_size - 1.0)) ** alpha_m
        kappae_y_PML[j] = 1.0 + (kappa_y_max - 1.0) * ((pml_size - (j + 1)) / (pml_size - 1.0)) ** poly_m
        be_y[j] = math.exp(
            -(sige_y_PML[j] / kappae_y_PML[j] + alphae_y_PML[j]) * dt / constants.AIR_PERMITTIVITY)
        if (sige_y_PML[j] == 0.0) and (alphae_y_PML[j] == 0.0) and (j == pml_size - 1):
            ce_y[j] = 0.0
        else:
            ce_y[j] = sige_y_PML[j] * (be_y[j] - 1.0) / (
                    sige_y_PML[j] + kappae_y_PML[j] * alphae_y_PML[j]) / kappae_y_PML[j]

    for j in range(pml_size - 1):
        sigh_y_PML[j] = sig_y_max * ((pml_size - (j + 1) - 0.5) / (pml_size - 1.0)) ** poly_m
        alphah_y_PML[j] = alpha_y_max * (((j + 1) - 0.5) / (pml_size - 1.0)) ** alpha_m
        kappah_y_PML[j] = 1.0 + (kappa_y_max - 1.0) * ((pml_size - (j + 1) - 0.5) / (pml_size - 1.0)) ** poly_m
        bh_y[j] = math.exp(
            -(sigh_y_PML[j] / kappah_y_PML[j] + alphah_y_PML[j]) * dt / constants.AIR_PERMITTIVITY)
        ch_y[j] = sigh_y_PML[j] * (bh_y[j] - 1.0) / (sigh_y_PML[j] + kappah_y_PML[j] * alphah_y_PML[j]) / \
                  kappah_y_PML[j]

    # FILL IN DENOMINATORS FOR FIELD UPDATES

    ii = pml_size - 2
    for i in range(Imax - 1):
        if i <= pml_size - 2:
            den_hx[i, :] = 1.0 / (kappah_x_PML[i] * phantom.DeltaX)
        elif i >= Imax - pml_size:
            den_hx[i, :] = 1.0 / (kappah_x_PML[ii] * phantom.DeltaX)
            ii = ii - 1
        else:
            den_hx[i, :] = 1.0 / phantom.DeltaX

    jj = pml_size - 2
    for j in range(Jmax - 1):
        if j <= pml_size - 2:
            den_hy[:, j] = 1.0 / (kappah_y_PML[j] * phantom.DeltaX)
        elif j >= Jmax - pml_size:
            den_hy[:, j] = 1.0 / (kappah_y_PML[jj] * phantom.DeltaX)
            jj = jj - 1
        else:
            den_hy[:, j] = 1.0 / phantom.DeltaX

    ii = pml_size - 1
    for i in range(Imax):
        if i <= pml_size - 1:
            den_ex[i, :] = 1.0 / (kappae_x_PML[i] * phantom.DeltaX)
        elif i >= Imax - pml_size:
            den_ex[i, :] = 1.0 / (kappae_x_PML[ii] * phantom.DeltaX)
            ii = ii - 1
        else:
            den_ex[i, :] = 1.0 / phantom.DeltaX

    jj = pml_size - 1
    for j in range(Jmax):
        if j <= pml_size - 1:
            den_ey[:, j] = 1.0 / (kappae_y_PML[j] * phantom.DeltaX)
        elif j >= Jmax - pml_size:
            den_ey[:, j] = 1.0 / (kappae_y_PML[jj] * phantom.DeltaX)
            jj = jj - 1
        else:
            den_ey[:, j] = 1.0 / phantom.DeltaX

    # temp value for computing

    preparation.den_ex = den_ex[1:Imax - 1, 1:Jmax - 1]  # 218x218
    preparation.den_ey = den_ey[1:Imax - 1, 1:Jmax - 1]  # 218x218
    preparation.den_hx = den_hx
    preparation.den_hy = den_hy

    be_x_all_temp = np.expand_dims(
        np.concatenate((np.squeeze(be_x[1:]), np.zeros(Imax - 2 * pml_size), np.squeeze(be_x[1:][::-1]))),
        axis=1)
    preparation.be_x_all = np.matlib.repmat(be_x_all_temp, 1, Jmax - 2)  # 218x218

    ce_x_all_temp = np.expand_dims(
        np.concatenate((np.squeeze(ce_x[1:]), np.zeros(Imax - 2 * pml_size), np.squeeze(ce_x[1:][::-1]))),
        axis=1)

    preparation.ce_x_all = np.matlib.repmat(ce_x_all_temp, 1, Jmax - 2)  # 218x218

    be_y_all_temp = np.expand_dims(
        np.concatenate((np.squeeze(be_y[1:]), np.zeros(Jmax - 2 * pml_size), np.squeeze(be_y[1:][::-1]))),
        axis=0)

    preparation.be_y_all = np.matlib.repmat(be_y_all_temp, Imax - 2, 1)  # 218x218

    ce_y_all_temp = np.expand_dims(
        np.concatenate((np.squeeze(ce_y[1:]), np.zeros(Jmax - 2 * pml_size), np.squeeze(ce_y[1:][::-1]))),
        axis=0)

    preparation.ce_y_all = np.matlib.repmat(ce_y_all_temp, Imax - 2, 1)  # 218x218

    ###########

    bh_x_all_temp = np.expand_dims(
        np.concatenate((np.squeeze(bh_x), np.zeros((Imax - 1) - 2 * (pml_size - 1)), np.squeeze(bh_x[::-1]))),
        axis=1)

    preparation.bh_x_all = np.matlib.repmat(bh_x_all_temp, 1, Jmax - 1)  # 219x219

    ch_x_all_temp = np.expand_dims(
        np.concatenate((np.squeeze(ch_x), np.zeros(Imax - 1 - 2 * (pml_size - 1)), np.squeeze(ch_x[::-1]))),
        axis=1)

    preparation.ch_x_all = np.matlib.repmat(ch_x_all_temp, 1, Jmax - 1)  # 219x219

    bh_y_all_temp = np.expand_dims(
        np.concatenate((np.squeeze(bh_y), np.zeros(Jmax - 1 - 2 * (pml_size - 1)), np.squeeze(bh_y[::-1]))),
        axis=0)

    preparation.bh_y_all = np.matlib.repmat(bh_y_all_temp, Imax - 1, 1)  # 219x219

    ch_y_all_temp = np.expand_dims(
        np.concatenate((np.squeeze(ch_y), np.zeros(Jmax - 1 - 2 * (pml_size - 1)), np.squeeze(ch_y[::-1]))),
        axis=0)

    preparation.ch_y_all = np.matlib.repmat(ch_y_all_temp, Imax - 1, 1)  # 219x219

    return
