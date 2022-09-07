import sys
import time

import numpy as np
from numpy import matlib

from Functions import constants
from Functions.FDTD_Core_Ez import FDTD_Core_Ez
from Functions.FDTD_Core_H import FDTD_Core_H

np.set_printoptions(threshold=sys.maxsize)


def FDTD_2D(prepared, Debye_model, phantom, antennas_setup, gaussian_source):

    ############################

    eps_s = np.zeros((prepared.Imax, prepared.Jmax))
    eps_inf = np.zeros((prepared.Imax, prepared.Jmax))
    sigma_s = np.zeros((prepared.Imax, prepared.Jmax))
    ############################
    ############################
    k = 0
    for i in prepared.XBB:
        l = 0
        for j in prepared.YBB:
            eps_inf[i, j] = Debye_model.Debye_Eps_Inf[k, l]
            eps_s[i, j] = Debye_model.Debye_Eps_Inf[k, l] + Debye_model.Debye_Eps_Delta[k, l]
            sigma_s[i, j] = Debye_model.Debye_Sigma_s[k, l]
            l = l + 1
        k = k + 1

    ############################
    # Material Settings #
    # To the area that matches pml material we set dielectric properties of air,
    ############################

    X_pml_min = min(prepared.XBB)
    X_pml_max = max(prepared.XBB) + 1
    Y_pml_min = min(prepared.YBB)
    Y_pml_max = max(prepared.YBB) + 1

    ############################
    # Epsilon - Infinity
    # pml_area
    # Corners(Left and Up, Right and Down, Right and Up, Left and Down)
    #########-------------------#########
    #########-------------------#########
    #########-------------------#########
    #########-------------------#########
    #  -------------------------------------
    #  -------------------------------------
    #  -------------------------------------
    #  -------------------------------------
    #########-------------------#########
    #########-------------------#########
    #########-------------------#########
    #########-------------------#########

    eps_inf[0:X_pml_min, 0:Y_pml_min] = Debye_model.Debye_Eps_Inf[0, 0]
    eps_inf[X_pml_max::, Y_pml_max::] = Debye_model.Debye_Eps_Inf[-1, -1]
    eps_inf[0:X_pml_min, Y_pml_max::] = Debye_model.Debye_Eps_Inf[0, -1]
    eps_inf[X_pml_max::, 0:Y_pml_min] = Debye_model.Debye_Eps_Inf[-1, 0]

    # area betwwen two corners
    #####################################
    #####################################
    #####################################
    #####################################
    #########-------------------#########
    #########-------------------#########
    #########-------------------#########
    #########-------------------#########
    #####################################
    #####################################
    #####################################
    #####################################

    # x-direction
    eps_inf[prepared.XBB, 0:Y_pml_min] = np.matlib.repmat(np.expand_dims(Debye_model.Debye_Eps_Inf[:, 0], axis=1), 1,
                                                          Y_pml_min)
    eps_inf[prepared.XBB, Y_pml_max::] = np.matlib.repmat(np.expand_dims(Debye_model.Debye_Eps_Inf[:, -1], axis=1), 1,
                                                          prepared.Jmax - Y_pml_max)
    # y-direction

    eps_inf[0:X_pml_min, prepared.YBB] = np.matlib.repmat(np.expand_dims(Debye_model.Debye_Eps_Inf[0, :], axis=0),
                                                          X_pml_min, 1)
    eps_inf[X_pml_max::, prepared.YBB] = np.matlib.repmat(np.expand_dims(Debye_model.Debye_Eps_Inf[-1, :], axis=0),
                                                          prepared.Imax - X_pml_max, 1)

    ############################
    # Epsilon - Sigma

    Eps_s = Debye_model.Debye_Eps_Inf + Debye_model.Debye_Eps_Delta
    # pml_area

    eps_s[0:X_pml_min, 0:Y_pml_min] = Eps_s[0, 0]
    eps_s[X_pml_max::, Y_pml_max::] = Eps_s[-1, -1]
    eps_s[0:X_pml_min, Y_pml_max::] = Eps_s[0, -1]
    eps_s[X_pml_max::, 0:Y_pml_min] = Eps_s[-1, 0]

    # x-direction
    eps_s[prepared.XBB, 0:Y_pml_min] = np.matlib.repmat(np.expand_dims(Eps_s[:, 0], axis=1), 1,
                                                        Y_pml_min)
    eps_s[prepared.XBB, Y_pml_max::] = np.matlib.repmat(np.expand_dims(Eps_s[:, -1], axis=1), 1,
                                                        prepared.Jmax - Y_pml_max)

    # y-direction

    eps_s[0:X_pml_min, prepared.YBB] = np.matlib.repmat(np.expand_dims(Eps_s[0, :], axis=0),
                                                        X_pml_min, 1)
    eps_s[X_pml_max::, prepared.YBB] = np.matlib.repmat(np.expand_dims(Eps_s[-1, :], axis=0),
                                                        prepared.Imax - X_pml_max, 1)

    ############################
    # Sigma-S

    # pml_area

    sigma_s[0:X_pml_min, 0:Y_pml_min] = Debye_model.Debye_Sigma_s[0, 0]
    sigma_s[X_pml_max::, Y_pml_max::] = Debye_model.Debye_Sigma_s[-1, -1]
    sigma_s[0:X_pml_min, Y_pml_max::] = Debye_model.Debye_Sigma_s[0, -1]
    sigma_s[X_pml_max::, 0:Y_pml_min] = Debye_model.Debye_Sigma_s[-1, 0]

    # x-direction
    sigma_s[prepared.XBB, 0:Y_pml_min] = np.matlib.repmat(np.expand_dims(Debye_model.Debye_Sigma_s[:, 0], axis=1), 1,
                                                          Y_pml_min)
    sigma_s[prepared.XBB, Y_pml_max::] = np.matlib.repmat(np.expand_dims(Debye_model.Debye_Sigma_s[:, -1], axis=1), 1,
                                                          prepared.Jmax - Y_pml_max)

    # y-direction

    sigma_s[0:X_pml_min, prepared.YBB] = np.matlib.repmat(np.expand_dims(Debye_model.Debye_Sigma_s[0, :], axis=0),
                                                          X_pml_min, 1)
    sigma_s[X_pml_max::, prepared.YBB] = np.matlib.repmat(np.expand_dims(Debye_model.Debye_Sigma_s[-1, :], axis=0),
                                                          prepared.Imax - X_pml_max, 1)

    #################
    # FILL IN UPDATING COEFFICIENTS
    ################

    Kd = (2 * phantom.TauP - phantom.DeltaT) / (2 * phantom.TauP + phantom.DeltaT)
    Beta_d = (2 * constants.AIR_PERMITTIVITY * (eps_s - eps_inf) * phantom.DeltaT) / (2 * phantom.TauP + phantom.DeltaT)
    DA = 1.0
    DB = (phantom.DeltaT / constants.AIR_PERMEABILITY)
    CA = (2 * constants.AIR_PERMITTIVITY * eps_inf - sigma_s * phantom.DeltaT + Beta_d) / (
            2 * constants.AIR_PERMITTIVITY * eps_inf + sigma_s * phantom.DeltaT + Beta_d)

    CA = CA[1:prepared.Imax - 1, 1:prepared.Jmax - 1]
    CB = 2 * phantom.DeltaT / (2 * constants.AIR_PERMITTIVITY * eps_inf + sigma_s * phantom.DeltaT + Beta_d)
    CB = CB[1:prepared.Imax - 1, 1: prepared.Jmax - 1]
    Beta_d = Beta_d[1:prepared.Imax - 1, 1: prepared.Jmax - 1]

    # for saving phasors inside FDTD observation bounding box
    numFreqs = 1
    E_fields_rec_dom_mag = np.zeros((antennas_setup.NumberOfAntennas, prepared.bbSize, numFreqs))
    E_fields_rec_dom_pha = np.zeros((antennas_setup.NumberOfAntennas, prepared.bbSize, numFreqs))

    # for saving phasors at the antennas in FDTD

    antObs_data_test = np.zeros(
        (antennas_setup.NumberOfAntennas, antennas_setup.NumberOfAntennas, gaussian_source.timesteps))
    # t_iE = [i for i in range(1,prepared.Imax)] # parameter for updating function E
    # t_jE = [i for i in range(1,prepared.Jmax)] # parameter for updating function E
    print("> Forward solver ... FDTD is running")
    start_timer = time.time()
    for antenna_source in range(antennas_setup.NumberOfAntennas):
    #for antenna_source in range(1):
        timer = time.time()

        ################## INITIALIZE VALUES FOR FIELDS ##################

        Ez = np.zeros((prepared.Imax, prepared.Jmax))
        Hx = np.zeros((prepared.Imax - 1, prepared.Jmax - 1))
        Hy = np.zeros((prepared.Imax - 1, prepared.Jmax - 1))
        Jd = np.zeros((prepared.Imax - 2, prepared.Jmax - 2))

        ################## CPML ##################

        psi_Ezx = np.zeros((prepared.Imax - 2, prepared.Jmax - 2))
        psi_Ezy = np.zeros((prepared.Imax - 2, prepared.Jmax - 2))
        psi_Hx = np.zeros((prepared.Imax - 1, prepared.Jmax - 1))
        psi_Hy = np.zeros((prepared.Imax - 1, prepared.Jmax - 1))

        ################## temp storage for saving data inside observation bounding box ##################

        temp_E_fields_imag = np.zeros((prepared.bbSize, numFreqs))
        temp_E_fields_real = np.zeros((prepared.bbSize, numFreqs))

        for i in range(gaussian_source.timesteps):
        #for i in range(7):
            Hx, Hy, psi_Hx, psi_Hy = FDTD_Core_H(Ez, DA, Hx, DB, psi_Hx, phantom.DeltaX, Hy, psi_Hy, prepared)
            Ez[1:prepared.Imax - 1, 1:prepared.Jmax - 1], Jd, psi_Ezx, psi_Ezy = FDTD_Core_Ez(Hy, Hx, CA, CB, Kd, Jd, prepared,
                                                      Ez[1:prepared.Imax - 1, 1:prepared.Jmax - 1], psi_Ezx,
                                                      phantom.DeltaX, psi_Ezy, Beta_d, phantom.DeltaT)

            ######### Source Update with pulse #########
            Ez[int(antennas_setup.x_location[antenna_source]), int(antennas_setup.y_location[antenna_source])] = \
                Ez[int(antennas_setup.x_location[antenna_source]), int(antennas_setup.y_location[antenna_source])] + \
                gaussian_source.source[i]

            ######### observe field data at every obstime_ds timesteps #########

            #bboxObs_data = Ez[tuple([prepared.bbox_exterior_mask_extend[0], prepared.bbox_exterior_mask_extend[1]])]

            for j in range(len(antennas_setup.x_location)):
                antObs_data_test[antenna_source, j, i] = Ez[antennas_setup.x_location[j], antennas_setup.y_location[j]]
                #print(antObs_data_test[antenna_source, j, i],end = ' ')
                # if(i==gaussian_source.timesteps-1):
                #     print(antObs_data_test[antenna_source, j, i], end=' ')


            ######### Computing frequency - domain quantities by FFT #########
            # temp_E_fields_imag = np.squeeze(temp_E_fields_imag) + bboxObs_data * math.sin(
            #     2 * math.pi * phantom.Center_Frequency * i * phantom.DeltaT)
            # temp_E_fields_real = np.squeeze(temp_E_fields_real) + bboxObs_data * math.cos(
            #     2 * math.pi * phantom.Center_Frequency * i * phantom.DeltaT)

        print("Antenna N.", antenna_source + 1, " runtime: ", time.time() - timer, " seconds")

        ######## convert observations to phasors and normalize by source ########

        # temp_E_fields_imag = temp_E_fields_imag / (gaussian_source.timesteps / 2)
        # temp_E_fields_real = temp_E_fields_real / (gaussian_source.timesteps / 2)
        #
        # E_fields_rec_dom_mag[antenna_source, :, :] = np.expand_dims(
        #     np.sqrt(np.power(temp_E_fields_imag, 2) + np.power(temp_E_fields_real, 2)), 1) / np.matlib.repmat(
        #     gaussian_source.magnitude, prepared.bbSize, 1)
        #
        # E_fields_rec_dom_pha[antenna_source, :, :] = np.expand_dims(
        #     -numpy.arctan2(temp_E_fields_imag, temp_E_fields_real), 1) - np.matlib.repmat(gaussian_source.phase,
        #                                                                                   prepared.bbSize, 1)

        # mag, pha = Fast_Fourier_Tranform(np.reshape(antObs_data_test, (antennas_setup.NumberOfAntennas ** 2, gaussian_source.timesteps)), phantom.Center_Frequency, phantom.DeltaT, gaussian_source.magnitude, gaussian_source.phase)
        # receivedFields_mag = np.reshape(mag, (antennas_setup.NumberOfAntennas, antennas_setup.NumberOfAntennas, numFreqs))
        # receivedFields_pha = np.reshape(pha, (antennas_setup.NumberOfAntennas,antennas_setup.NumberOfAntennas, numFreqs))

    print("> FDTD completed ... Total Running Time: ",time.time() - start_timer ," seconds")

    return antObs_data_test
