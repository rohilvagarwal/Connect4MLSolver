import sys
from ProjectConstants import *
from GameLogic.Connect4GameLogic import Connect4GameLogic

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect 4: Default Game")

GAME_QUIT = False

game = Connect4GameLogic(ROW_COUNT, COLUMN_COUNT, "Red", "Yellow")

while not GAME_QUIT:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_QUIT = True

	game.draw_board(screen)

	pygame.display.update()
	clock.tick(FPS)

pygame.quit()
sys.exit()