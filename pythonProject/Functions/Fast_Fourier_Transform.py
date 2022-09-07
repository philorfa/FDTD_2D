import math
import numpy as np
from numpy import matlib


def Fast_Fourier_Tranform(source, center_frequency, deltaT, ref_mag, ref_pha):
    omega = 2 * math.pi * center_frequency

    if isinstance(source, list):
        n = np.asarray(source).shape[0]
    else:
        n = np.asarray(source).shape[1]

    # Re=source*cos((0:n-1)'*omegas*delT)/n*2;
    Re1 = [math.cos(i * omega * deltaT) for i in range(n)]
    Re = source @ np.array(Re1).T / n * 2

    # Im=source*sin((0:n-1)'*omegas*delT)/n*2;
    Im1 = [math.sin(i * omega * deltaT) for i in range(n)]
    Im = source @ np.array(Im1).T / n * 2

    if ref_mag == 0 and ref_pha == 0:
        magnitude = math.sqrt(Re ** 2 + Im ** 2)
        phase = - math.atan2(Im, Re)
    else:
        temp_ref = np.matlib.repmat(ref_pha, np.asarray(source).shape[0], 1)
        magnitude = np.sqrt(np.power(Re, 2) + np.power(Im, 2))/ref_mag
        phase = np.expand_dims(-np.arctan2(Im, Re),1) - temp_ref
    return magnitude, phase
