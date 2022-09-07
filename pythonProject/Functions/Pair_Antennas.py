from Functions import constants
import pandas as pd
import numpy as np


def Pair_Antennas(x, y):
    data = {'x': x, 'y': y}
    df = pd.DataFrame(data)
    duplicate = df[df.duplicated()]
    if duplicate.empty:
        print("Not duplicate Antennas (pass test)")

    pairs = pd.DataFrame(columns=['FirstAntennaIndex', 'SecondAntennaIndex'])
    index = 0
    for i in range(len(x) + 1):
        for j in range(i + 1, len(x)):
            pairs.loc[index] = [i, j]
            index += 1

    return pairs
