import pygame

pygame.init()

default_display = 320, 240
max_display = pygame.display.Info().current_w, pygame.display.Info().current_h
scale = 1
fullscreen = False

draw_surface = pygame.Surface(default_display)
scale_surface = pygame.Surface(default_display)
game_display = pygame.display.set_mode(default_display)
clock = pygame.time.Clock()


# Functions
def set_display():
    global game_display, scale_surface, draw_surface
    scale_surface = pygame.Surface(get_resolution())
    if fullscreen:
        draw_surface = pygame.Surface(max_display)
        gameDisplay = pygame.display.set_mode(max_display, pygame.FULLSCREEN)
    else:
        draw_surface = pygame.Surface(default_display)
        gameDisplay = pygame.display.set_mode(default_display)
    return


def get_resolution():
    if fullscreen:
        return max_display[0] * scale, max_display[1] * scale
    else:
        return default_display[0] * scale, default_display[1] * scale


# MainLoop
while True:

    # EventHandle
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Buttons
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                scale += 1
                if scale == 4:
                    scale = 1
                set_display()
            if event.key == pygame.K_x:
                fullscreen = not fullscreen
                set_display()
            if event.key == pygame.K_c:
                pass

    # Draw
    draw_surface.fill((255, 255, 255))
    pygame.draw.rect(draw_surface, (0, 0, 0), (50, 50, 50, 50))

    pygame.transform.scale(draw_surface, get_resolution(), scale_surface)

    game_display.blit(scale_surface, (0, 0))

    pygame.display.update()
    clock.tick(60)
