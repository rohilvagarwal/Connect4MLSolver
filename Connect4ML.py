import sys
from ProjectConstants import *
from GameLogic.Connect4MLGameLogic import Connect4MLGameLogic

screen = pygame.display.set_mode(SIZE)

GAME_QUIT = False

game = Connect4MLGameLogic(ROW_COUNT, COLUMN_COUNT, "The ML", "You")

while not GAME_QUIT:
	GAME_QUIT = game.get_quit()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_QUIT = True

	game.draw_board(screen)

	pygame.display.update()
	clock.tick(FPS)

pygame.quit()
sys.exit()