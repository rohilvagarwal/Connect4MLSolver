import sys
from ProjectConstants import *
from UIElements.Button import Button
from ExtraPages.Menu import draw_menu
from GameLogic.Connect4MLGameLogic import Connect4MLGameLogic
from GameLogic.Connect4GameLogic import Connect4GameLogic

def update_game_state(new_state):
	global gameState
	gameState = new_state

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect 4: ML Solver")

gameOver = False
gameState = "Menu" #ML Solver, Default Game

mlGame = Connect4MLGameLogic(ROW_COUNT, COLUMN_COUNT, "You", "The ML", update_game_state)
defaultGame = Connect4GameLogic(ROW_COUNT, COLUMN_COUNT, "Red", "Yellow", update_game_state)

while not gameOver:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameOver = True

	if gameState == "Menu":
		draw_menu(screen, update_game_state)
	if gameState == "ML Solver":
		mlGame.draw_board(screen)
	if gameState == "Default Game":
		defaultGame.draw_board(screen)

	pygame.display.update()
	clock.tick(FPS)

pygame.quit()
sys.exit()