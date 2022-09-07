import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage


def heatmap2d(arr: np.ndarray):
    plt.imshow(arr, cmap='viridis')
    plt.colorbar()
    plt.show()


def Transform_Resolution(phantom, antennas_setup, Debye_model):
    multiplication_factor = phantom.Resolution / 0.5

    antennas_setup.x_location = np.rint(antennas_setup.x_location / multiplication_factor)
    antennas_setup.y_location = np.rint(antennas_setup.y_location / multiplication_factor)

    Debye_model.Debye_size_x = int(Debye_model.Debye_size_x / multiplication_factor)
    Debye_model.Debye_size_y = int(Debye_model.Debye_size_y / multiplication_factor)

    # Debye_model.Debye_Mask = cv2.resize(np.array(Debye_model.Debye_Mask),(Debye_model.Debye_size_x,Debye_model.Debye_size_y),interpolation=cv2.INTER_NEAREST)
    # #heatmap2d(Debye_model.Debye_Mask)
    # Debye_model.Debye_Eps_Delta = cv2.resize(np.array(Debye_model.Debye_Eps_Delta),(Debye_model.Debye_size_x,Debye_model.Debye_size_y),interpolation=cv2.INTER_NEAREST)
    # Debye_model.Debye_Eps_Inf = cv2.resize(np.array(Debye_model.Debye_Eps_Inf),(Debye_model.Debye_size_x,Debye_model.Debye_size_y),interpolation=cv2.INTER_NEAREST)
    # Debye_model.Debye_Sigma_s = cv2.resize(np.array(Debye_model.Debye_Sigma_s),(Debye_model.Debye_size_x,Debye_model.Debye_size_y),interpolation=cv2.INTER_NEAREST)

    Debye_model.Debye_Mask = scipy.ndimage.zoom(np.array(Debye_model.Debye_Mask), 1 / multiplication_factor, order=0)
    Debye_model.Debye_Eps_Delta = scipy.ndimage.zoom(np.array(Debye_model.Debye_Eps_Delta), 1 / multiplication_factor,
                                                     order=0)
    Debye_model.Debye_Eps_Inf = scipy.ndimage.zoom(np.array(Debye_model.Debye_Eps_Inf), 1 / multiplication_factor,
                                                   order=0)
    Debye_model.Debye_Sigma_s = scipy.ndimage.zoom(np.array(Debye_model.Debye_Sigma_s), 1 / multiplication_factor,
                                                   order=0)
    return
