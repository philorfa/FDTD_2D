import numpy as np
import pandas as pd
import math
from Functions.Fast_Fourier_Transform import Fast_Fourier_Tranform


def Deal_FDTD_Forward(frequency,deltaT,original_measurements,source,NumberOfAntennas):


    measurements = np.reshape(original_measurements,(NumberOfAntennas**2,source.timesteps))
    magnitude,phase = Fast_Fourier_Tranform(measurements,frequency,deltaT,source.magnitude,source.phase)

    mag_background = np.reshape(magnitude,(NumberOfAntennas,NumberOfAntennas))
    pha_background = np.reshape(phase,(NumberOfAntennas,NumberOfAntennas))

    return mag_background,pha_background
