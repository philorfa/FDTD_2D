import pandas as pd
from IPython.core.display_functions import display


def Materials(Number):
    print("\n!!!!Preview of available Materials!!!!\n")

    mat1 = [0, 'Immer', 6.566, 16.86, 0.3231, 1.4288e-10]
    mat2 = [1, 'Glycerine', 6.566, 16.86, 0.3231, 1.4288e-10]
    mat3 = [2, 'Brain', 35, 5, 0.147, None]
    mat4 = [3, 'CSF', 18.28, 44.71, 0.0782, None]
    mat5 = [4, 'Plastic', 3.5, 0, 0.0055, None]

    materials = []
    materials.append(mat1)
    materials.append(mat2)
    materials.append(mat3)
    materials.append(mat4)
    materials.append(mat5)
    materials = pd.DataFrame(materials, columns=['Mask_Code', 'Name', 'Epsilon_Infinity', 'Delta_Epsilon', 'Sigma_S',
                                                 'Relaxation_Time'])
    display(materials.to_string())

    flag = True
    while flag:
        extra_material = input("\nDo you want to add a new material? [y/n]")
        if extra_material == 'y' or extra_material == 'Y':
            mask_code = int(input("Mask Code: "))
            name = input("Name: ")
            Epsilon_Infinity = float(input("Epsilon Infinity: "))
            Delta_Epsilon = float(input("Delta Epsilon: "))
            Sigma_S = float(input("Sigma S:"))
            Relaxation_Time = float(input("Relaxation Time:"))
            materials.loc[materials.shape[0]] = [mask_code, name, Epsilon_Infinity, Delta_Epsilon, Sigma_S, Relaxation_Time]
            display(materials)
        else:
            flag = False

    materials.to_csv(r'C:\Users\philo\OneDrive\Υπολογιστής\DBIM_Exp\pythonProject\Model' + Number + '\Data\Debye\Materials_Debye_Parameters.csv',
        index=False, header=True)
    print("!!!! Feel free to modify file Model" + Number + "\Data\Debye\Materials_Debye_Parameters.csv !!!!")
    return
