from ProjectConstants import *
from Connect4GameLogic import Connect4GameLogic

screen = pygame.display.set_mode(SIZE)

GAME_QUIT = False

game = Connect4GameLogic(ROW_COUNT, COLUMN_COUNT, "Player 1", "Player 2")

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