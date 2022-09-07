def Resolution_check():
    flag = True
    while flag:
        resolution = float(input("Please enter a new coarse resolution on a mulitple of 0.5(mm):"))
        if not (resolution % 0.5):
            return resolution
