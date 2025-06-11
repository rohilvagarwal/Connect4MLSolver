# /// script
# dependencies = [
#  "pytmx",
#  "pygame-ce",
#  "pyscroll",
#  "numpy",
#  "math"
# ]
# ///

import asyncio

import sys
from ProjectConstants import *
from platform import window

window.python.config.user_canvas = 0
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect 4: ML Solver")

from ExtraPages.Menu import draw_menu
from ExtraPages.AboutMe import draw_about_me
from GameLogic.Connect4MLGameLogic import Connect4MLGameLogic
from GameLogic.Connect4GameLogic import Connect4GameLogic

def update_game_state(new_state):
	global gameState
	gameState = new_state

mlGame = Connect4MLGameLogic(ROW_COUNT, COLUMN_COUNT, "You", "The ML", update_game_state)
defaultGame = Connect4GameLogic(ROW_COUNT, COLUMN_COUNT, "Red", "Yellow", update_game_state)

gameState = "Menu"  #ML Solver, Default Game


async def main():
	gameOver = False

	while not gameOver:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver = True

		if gameState == "Menu":
			draw_menu(screen, update_game_state)
		elif gameState == "About Me":
			draw_about_me(screen, update_game_state)
		elif gameState == "ML Solver":
			mlGame.draw_board(screen)
		elif gameState == "Default Game":
			defaultGame.draw_board(screen)

		pygame.display.update()
		clock.tick(FPS)
		await asyncio.sleep(0)

	pygame.quit()
	sys.exit()


asyncio.run(main())
