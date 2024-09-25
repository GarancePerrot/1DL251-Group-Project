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
    tot_width_grid = block_size * 4

    height_board_start = (HEIGHT - tot_width_grid) / 2
    height_board_end = HEIGHT - height_board_start
    width_board_start = (WIDTH - tot_width_grid) / 2
    width_board_end = WIDTH - width_board_start

    for x in range(0, 800, block_size):
        pygame.draw.line(screen, BLACK, (x + width_board_start, height_board_start), (x + width_board_start, height_board_end), 2)
        pygame.draw.line(screen, BLACK, (width_board_start, x + height_board_start), (width_board_end, x + height_board_start), 2)

def get_titles(font, title_text, width, screen):
    text = font.render(title_text, True, BLACK, WHITE)

    textRect = text.get_rect()

    textRect.center = (width, 40)

    screen.blit(text, textRect)
    

def get_player_turn():
    return None


def run_game():
    pygame.init()
    pygame.display.set_caption('GROUP-PROJECT')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    title_font1 = pygame.font.Font('freesansbold.ttf', 32)
    title_font2 = pygame.font.Font('freesansbold.ttf', 16)

    screen.fill(WHITE)
    # clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        turn = get_player_turn()

        get_titles(title_font1, "PLAYER ... TURN", 600, screen)

        get_titles(title_font2, "PLAYER 1:s pieces", 140, screen)

        get_titles(title_font2, "PLAYER 2: pieces", 1060, screen)

        draw_rect(screen)

        pygame.display.update() 

        # clock.tick(FPS)

    pygame.quit()
    