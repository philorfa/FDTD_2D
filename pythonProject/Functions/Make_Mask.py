import pygame
import pandas as pd
import numpy as np


def Make_Mask(height, width, model_number):
    df = pd.read_csv('Model' + model_number + '/Data/Debye/Materials_Debye_Parameters.csv')
    Number_of_Colors = len(df)

    colors = np.empty(11, dtype=object)
    colors[0] = ['WHITE', (255, 255, 255)]
    colors[1] = ['BLACK', (0, 0, 0)]
    colors[2] = ['GREEN', (0, 255, 0)]
    colors[3] = ['RED', (255, 0, 0)]
    colors[4] = ['BLUE', (55, 55, 255)]
    colors[5] = ['YELLOW', (255, 255, 0)]
    colors[6] = ['ORANGE', (255, 128, 0)]
    colors[7] = ['LIGHTBLUE', (51, 255, 255)]
    colors[8] = ['LIGHTGREY', (210, 210, 210)]
    colors[9] = ['BROWN', (153, 76, 0)]
    colors[10] = ['GOLD', (153, 153, 0)]

    # This sets the WIDTH and HEIGHT of each grid location
    SCREEN_WIDTH = 1500
    SCREEN_HEIGHT = 700
    NUMBER_OF_X_CELLS = width
    NUMBER_OF_Y_CELLS = height
    HEIGHT = round(SCREEN_HEIGHT/NUMBER_OF_Y_CELLS)-1
    WIDTH = round(SCREEN_WIDTH/NUMBER_OF_X_CELLS)-1



    # This sets the margin between each cell
    MARGIN = 1

    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    grid = []
    for row in range(NUMBER_OF_X_CELLS):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(NUMBER_OF_Y_CELLS):
            grid[row].append(0)  # Append a cell

    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    scale=1
    flag=False
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.display.flip()

    # Set title of screen
    pygame.display.set_caption(colors[0][0] + " - Material: " + df.iloc[0]["Name"])

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    color_code = 0

    while not done:
        pos = pygame.mouse.get_pos()
        column = pos[0] // (WIDTH + MARGIN)
        row = pos[1] // (HEIGHT + MARGIN)
        text = colors[color_code][0] + " - Material: " + df.iloc[color_code]["Name"] + " - ({},{})".format(row,column)
        pygame.display.set_caption(text)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    color_code = (color_code + 1) % Number_of_Colors
                    #text = colors[color_code][0] + " - Material: " + df.iloc[color_code]["Name"]
                    #pygame.display.set_caption(text)
                    scale=scale+1
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif pygame.mouse.get_pressed()[0]:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                grid[row][column] = color_code
                print("Click ", pos, "Grid coordinates: ", row, column)

        # Set the screen background
        BLACK = (0,0,0)
        screen.fill(BLACK)

        # Draw the grid
        for row in range(NUMBER_OF_X_CELLS):
            for column in range(NUMBER_OF_Y_CELLS):
                pygame.draw.rect(screen,
                                 colors[grid[row][column]][1],
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])


        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
    return grid
