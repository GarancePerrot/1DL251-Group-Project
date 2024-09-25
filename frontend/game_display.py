# TEST FEEL FREE TO DELETE ONLY FOR FOLDER STRUCTURE
import pygame

################### SETTINGS #######################
WIDTH = 1200
HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
####################################################

def draw_rect(screen):
    block_size = 160
    height_board_start = 100
    height_board_end = 740
    width_board_start = 280
    width_board_end = 920

    for x in range(0, 800, block_size):
        pygame.draw.line(screen, BLACK, (x + 280, height_board_start), (x + 280, height_board_end), 2)
        pygame.draw.line(screen, BLACK, (width_board_start, x + 100), (width_board_end, x + 100), 2)



def run_game():
    pygame.init()
    pygame.display.set_caption('GROUP-PROJECT')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        screen.fill(WHITE)
    
        draw_rect(screen)

        pygame.display.update() 

        # clock.tick(FPS)

    pygame.quit()
    