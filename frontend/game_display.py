# TEST FEEL FREE TO DELETE ONLY FOR FOLDER STRUCTURE
import pygame

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('GROUP-PROJECT')

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill((0, 0, 0))

        pygame.display.flip() 
    pygame.quit()