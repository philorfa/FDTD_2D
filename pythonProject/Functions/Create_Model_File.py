import glob
import os
import shutil


def Create_Model_File():
    flag = True
    while flag:
        Number = input("Please enter a number for your new Head Model:")
        if not glob.glob("Model" + Number):
            os.makedirs("Model" + Number + "\Data\Debye")
            flag = False
        else:
            overwrite = input("Model already exists, do you want to overwrite folder? [y/n]")
            if (overwrite == "y") or (overwrite == "Y"):
                shutil.rmtree("Model" + Number)
                os.makedirs("Model" + Number + "\Data\Debye")
                flag = False
    return Number
