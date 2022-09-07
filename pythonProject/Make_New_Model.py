from Functions.Create_Model_File import Create_Model_File
from Functions.Materials import Materials
from Functions.Make_Mask import Make_Mask
from Functions.Set_Antennas_Position1 import Set_Antennas_Position
from Functions.Create_Debye_Arrays import Create_Debye_Arrays
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.ndimage


def heatmap2d(arr: np.ndarray):
    plt.imshow(arr, cmap='viridis')
    plt.colorbar()
    plt.show()


if __name__ == '__main__':
    NumberOfModel = Create_Model_File()
    Materials(NumberOfModel)
    print("Wait Until Materials File is Saved")
    time.sleep(10)

    height_grid = int(input("Please Select height of grid:"))
    width_grid = int(input("Please Select width of grid:"))

    mask = Make_Mask(height_grid, width_grid, NumberOfModel)

    resolution = int(
        input("Please Select resolution of image(Enter one value k and image will always be a square (k,k):"))
    # mask = cv2.resize(np.array(mask), (resolution, resolution), interpolation=cv2.INTER_CUBIC)
    mask = scipy.ndimage.zoom(mask, (resolution / height_grid, resolution / width_grid), order=0)
    mask1 = pd.DataFrame(mask)
    mask1.to_csv("Model" + NumberOfModel + "/Data/Debye/Debye_Mask.csv", header=False, index=False)

    number_of_antennas = int(input("Time to place the antennas!!\nPlease select the number of antennas: "))
    antennas_position = Set_Antennas_Position(mask, NumberOfModel, number_of_antennas)

    frequencies = list(map(int, input("Please enter frequencies(MHz) separated with comma: (e.g 1,2,3):").split(",")))
    frequencies = [element * 10 ** 6 for element in frequencies]
    df = pd.DataFrame(frequencies)
    df.to_csv("Model" + NumberOfModel + "/Data/frequencies.csv", header=False, index=False)

    print("\nFinally enter some simulation Parameters")
    delay = float(input('Delay: '))
    pml_coarse = int(input("Pml_coarse: "))
    pml_fine = int(input("Pml_fine: "))
    tauS = float(input("TauS: "))
    timeSteps_coarse = int(input("timeSteps_coarse: "))
    timeSteps_fine = int(input("timeSteps_fine: "))

    data = {'Delay': [delay], 'Pml_coarse': [pml_coarse], 'Pml_fine': [pml_fine], 'TauS': [tauS],
            'timeSteps_coarse': [timeSteps_coarse], 'timeSteps_fine': [timeSteps_fine]}
    parameters = pd.DataFrame(data)
    parameters.to_csv('Model' + NumberOfModel + '\Data\Simulation_Parameters.csv', index=False, header=True)

    Create_Debye_Arrays(NumberOfModel)
