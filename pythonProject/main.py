import pandas as pd
import numpy as np
import os
import glob
import shutil
from Functions import constants
from Functions.Transform_Resolution import Transform_Resolution
from Functions.Resolution_check import Resolution_check
from Functions.Pair_Antennas import Pair_Antennas
from Functions.FDTD_Preprocess import FDTD_Preprocess
from Functions.Gaussian_Pulse import Gaussian_Pulse
from Functions.Fast_Fourier_Transform import Fast_Fourier_Tranform
from Functions.FDTD_2D import FDTD_2D
from Functions.Deal_FDTD_Forward import Deal_FDTD_Forward


class Info:
    def __init__(self, NumberOfPhantom, Resolution, Center_Frequency, frequencies):
        self.NumberOfPhantom = NumberOfPhantom
        self.Resolution = Resolution
        self.Center_Frequency = Center_Frequency
        self.frequencies = frequencies
        self.DeltaX = Resolution / 10 ** 3
        self.DeltaT = (Resolution / 10 ** 3) / (2 * constants.WAVE_VELOCITY)
        self.TauP = None
        self.EpsS = None


class Simulation:
    def __init__(self, timeSteps_coarse, timeSteps_fine, pml_coarse, pml_fine, delay, tauS):
        self.timeSteps_coarse = timeSteps_coarse
        self.timeSteps_fine = timeSteps_fine
        self.pml_coarse = pml_coarse
        self.pml_fine = pml_fine
        self.delay = delay
        self.tauS = tauS


class Debye_Values:
    # We are interested in the area where Debye_Mask is not zero
    def __init__(self, Debye_size_x, Debye_size_y, Debye_Mask, Debye_Eps_Delta, Debye_Eps_Inf, Debye_Sigma_s):
        self.Debye_size_x = Debye_size_x
        self.Debye_size_y = Debye_size_y
        self.Debye_Mask = Debye_Mask
        self.Debye_Eps_Delta = Debye_Eps_Delta
        self.Debye_Eps_Inf = Debye_Eps_Inf
        self.Debye_Sigma_s = Debye_Sigma_s


class Antennas:
    def __init__(self, NumberOfAntennas, x_location, y_location, pairs_index):
        self.NumberOfAntennas = NumberOfAntennas
        self.x_location = x_location
        self.y_location = y_location
        self.pairs_index = pairs_index


class Preparation:
    def __init__(self):
        self.be_x_all = None
        self.be_y_all = None
        self.ce_x_all = None
        self.ce_y_all = None
        self.bh_x_all = None
        self.bh_y_all = None
        self.ch_x_all = None
        self.ch_y_all = None
        self.den_ex = None
        self.den_ey = None
        self.den_hy = None
        self.den_hx = None
        self.Imax = None
        self.Jmax = None
        self.XBB = None
        self.YBB = None
        self.bbSize = None
        self.bbox_exterior_mask_extend = None


class Pulse:
    def __init__(self, source, timesteps):
        self.source = source
        self.timesteps = timesteps
        self.magnitude = None
        self.phase = None


if __name__ == '__main__':

    ## Type Resolution and repeat until input is mulitple of 0.5(mm) ##
    Resolution = Resolution_check()
    NumberOfPhantom = input("Please choose a kind of brain phantom (1~999):")
    Center_Frequency = int(input('Please choose a center frequency(Ghz):')) * 1000000000
    frequencies = pd.read_csv('Model' + NumberOfPhantom + '/Data/frequencies.csv', header=None)

    ## Create basic phantom object ##
    phantom = Info(NumberOfPhantom, Resolution, Center_Frequency, np.array(frequencies[0], dtype=float))

    ## Create object with basic simulation parameters ##
    simulation_parameters = pd.read_csv('Model' + phantom.NumberOfPhantom + '/Data/Simulation_Parameters.csv').iloc[0]
    experiment_parameters = Simulation(simulation_parameters.timeSteps_coarse,
                                       simulation_parameters.timeSteps_fine,
                                       simulation_parameters.Pml_coarse,
                                       simulation_parameters.Pml_fine,
                                       simulation_parameters.Delay,
                                       simulation_parameters.TauS)


    antennas_location = pd.read_csv('Model' + phantom.NumberOfPhantom + '/Data/Antennas_Location.csv')
    x = np.array(antennas_location.x, dtype=float)
    y = np.array(antennas_location.y, dtype=float)
    antenna_pairs = Pair_Antennas(x, y)

    # create Dataframe with all combinations ie 0,1/0,2/0,3 etc
    antennas_setup = Antennas(len(x), x, y, antenna_pairs)


    debye_mask = pd.read_csv('Model' + phantom.NumberOfPhantom + '/Data/Debye/Debye_Mask.csv', header=None)
    debye_epsdelta = pd.read_csv('Model' + phantom.NumberOfPhantom + '/Data/Debye/Debye_EpsDelta.csv', header=None)
    debye_epsinf = pd.read_csv('Model' + phantom.NumberOfPhantom + '/Data/Debye/Debye_EpsInf.csv', header=None)
    debye_sigmas = pd.read_csv('Model' + phantom.NumberOfPhantom + '/Data/Debye/Debye_Sigma_s.csv', header=None)
    Debye_model = Debye_Values(debye_epsdelta.shape[0], debye_epsdelta.shape[1], debye_mask, debye_epsdelta,
                               debye_epsinf,
                               debye_sigmas)

    # Fixes debye grid location and antennas location
    Transform_Resolution(phantom, antennas_setup, Debye_model)

    print("------------- The Number of Antennas is ", antennas_setup.NumberOfAntennas, " -------------")

    ## Complete Load_FDTD_material_2d
    materials = pd.read_csv('Model' + phantom.NumberOfPhantom + '/Data/Debye/Materials_Debye_Parameters.csv')
    phantom.TauP = materials['Relaxation_Time'].iloc[np.where(materials.Name == 'Immer')][0]
    phantom.EpsS = materials['Epsilon_Infinity'].iloc[np.where(materials.Name == 'Immer')][0] + \
                   materials['Delta_Epsilon'].iloc[np.where(materials.Name == 'Immer')][0]

    preparetion = Preparation()
    FDTD_Preprocess(phantom, experiment_parameters, Debye_model, antennas_setup, preparetion)

    source, optimized_timesteps = Gaussian_Pulse(phantom, experiment_parameters, Debye_model)
    gaussian_source = Pulse(source, optimized_timesteps)

    magnitude, phase = Fast_Fourier_Tranform(source, phantom.Center_Frequency, phantom.DeltaT, 0, 0)
    gaussian_source.magnitude = magnitude
    gaussian_source.phase = phase

    original_measurements = FDTD_2D(preparetion, Debye_model, phantom, antennas_setup, gaussian_source)
    if not glob.glob('Model' + phantom.NumberOfPhantom + '/Data/FDTD_Results'):
        os.makedirs('Model' + phantom.NumberOfPhantom + '/Data/FDTD_Results')
    else:
            shutil.rmtree('Model' + phantom.NumberOfPhantom + '/Data/FDTD_Results')
            os.makedirs('Model' + phantom.NumberOfPhantom + '/Data/FDTD_Results')

    np.save('Model' + phantom.NumberOfPhantom + '/Data/FDTD_Results/original_measurements.npy', original_measurements)

    print("Starting to deal with the simulated data")

    Calibrated_Magnitude = np.zeros(
        (antennas_setup.NumberOfAntennas, antennas_setup.NumberOfAntennas, len(phantom.frequencies)))
    Calibrated_Phase = np.zeros(
        (antennas_setup.NumberOfAntennas, antennas_setup.NumberOfAntennas, len(phantom.frequencies)))
    for i in range(len(phantom.frequencies)):
        mag_background, pha_background = Deal_FDTD_Forward(float(phantom.frequencies[i]), phantom.DeltaT,
                                                           original_measurements, gaussian_source,
                                                           antennas_setup.NumberOfAntennas)

        Calibrated_Phase[:, :, i] = pha_background  # rad
        Calibrated_Magnitude[:, :, i] = 20 * np.log10(mag_background)  # dB

    np.save('Model' + phantom.NumberOfPhantom + '/Data/FDTD_Results/Calibrated_Magnitude.npy', Calibrated_Magnitude)
    np.save('Model' + phantom.NumberOfPhantom + '/Data/FDTD_Results/Calibrated_Phase.npy', Calibrated_Phase)
