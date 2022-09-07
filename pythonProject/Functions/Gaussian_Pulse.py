#####
# Gaussian Modelled Sine Pulse
#####

import math
import matplotlib.pyplot as pp


def Gaussian_Pulse(phantom, experiment_parameters, Debye_model):
    band = 2 * (10 ** 9)
    fmin = int(phantom.Center_Frequency) - band
    fmax = int(phantom.Center_Frequency) + band
    omega = math.pi * (fmin + fmax)
    Ts = 2 * 2 / (math.pi * (fmax - fmin))

    Gauss_limit = 1 * (10 ** -5)
    Nc = math.ceil((Ts / phantom.DeltaT) * math.sqrt(-1 * math.log(Gauss_limit)))

    Opt_Timesteps_temp = math.ceil(
        2 * Nc * 1.5 + max(Debye_model.Debye_size_x, Debye_model.Debye_size_y * math.sqrt(2) * 5))
    Opt_Timesteps = int(min(Opt_Timesteps_temp, experiment_parameters.timeSteps_fine))

    print("The Optimized TimeSteps is", Opt_Timesteps)

    N = [i for i in range(Opt_Timesteps)]
    arg = [(i - Nc) * phantom.DeltaT / Ts for i in N]

    source1 = [math.exp(-1 * i ** 2) for i in arg]
    source2 = [math.sin(omega * i * phantom.DeltaT) for i in N]

    source = [i * j for i, j in zip(source1, source2)]

    # pp.plot(source)
    # pp.show()

    return source, Opt_Timesteps
