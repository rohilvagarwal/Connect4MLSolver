from ProjectConstants import *
from UIElements.Button import Button
import numpy as np
import random


def menu_button(centerX, centerY, text):
	return Button(centerX=centerX, centerY=centerY, width=2.5 * SQUARE_SIZE, height=WIDTH * 0.05, font=font30, borderSize=10, text=text)


def draw_chip(screen, x, y, color, ifOutline):
	pygame.draw.circle(screen, color, (x, y), RADIUS)

	if ifOutline:
		pygame.draw.circle(screen, LIGHT_GREY, (x, y), RADIUS, 5)

xCurrPos = random.choice([SQUARE_SIZE * 2, SQUARE_SIZE * 7])
yInitPos = SQUARE_SIZE // 2
yCurrPos = yInitPos
yFinalPos = 2 * HEIGHT
currVelocity = initial_velocity
currColor = random.choice([RED, YELLOW])


def draw_menu(screen, update_game_state):
	global xCurrPos, yInitPos, yCurrPos, yFinalPos, currVelocity, currColor

	board = np.array(
		[[1, 1, 0],
		 [1, 2, 0],
		 [2, 1, 0],
		 [2, 2, 0],
		 [1, 2, 0],
		 [0, 1, 0]]
	)
	player1Num = 1
	player2Num = 2

	player1Color = RED
	player2Color = YELLOW

	pygame.draw.rect(screen, DARK_GREY, (0, 0, WIDTH, HEIGHT))

	board_layer = pygame.Surface((3 * SQUARE_SIZE, HEIGHT - SQUARE_SIZE)).convert_alpha()

	#Draw empty spots
	pygame.draw.rect(board_layer, BLUE, (0, 0, WIDTH, HEIGHT - SQUARE_SIZE))  #Board

	for c in range(len(board[0])):
		for r in range(len(board)):
			draw_chip(board_layer, int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE / 2), (0, 0, 0, 0), False)

	#Draw chips on board
	for c in range(len(board[0])):
		for r in range(len(board)):
			if board[r][c] == player1Num:
				draw_chip(board_layer, int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(HEIGHT - 2 * SQUARE_SIZE - r * SQUARE_SIZE + SQUARE_SIZE / 2),
						  player1Color,
						  True)
			elif board[r][c] == player2Num:
				draw_chip(board_layer, int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(HEIGHT - 2 * SQUARE_SIZE - r * SQUARE_SIZE + SQUARE_SIZE / 2),
						  player2Color,
						  True)

	pygame.draw.rect(screen, BLUE, (SQUARE_SIZE * 5 // 2, SQUARE_SIZE, WIDTH - 5 * SQUARE_SIZE, HEIGHT - SQUARE_SIZE))

	#draw animating chip
	draw_chip(screen, xCurrPos, yCurrPos, currColor, True)

	screen.blit(board_layer, (-SQUARE_SIZE // 2, SQUARE_SIZE))
	screen.blit(pygame.transform.flip(board_layer, True, False), (WIDTH - SQUARE_SIZE * 5 // 2, SQUARE_SIZE))

	if yCurrPos > yFinalPos:
		xCurrPos = random.choice([SQUARE_SIZE * 2, SQUARE_SIZE * 7])
		yCurrPos = yInitPos
		currVelocity = initial_velocity
		currColor = random.choice([RED, YELLOW])

	currVelocity += gravity // 2
	yCurrPos += int(currVelocity / FPS)

	#title background
	pygame.draw.rect(screen, DARK_GREY, (0, 0, WIDTH, SQUARE_SIZE))

	#draw title
	draw_text_center(screen, WIDTH / 2, SQUARE_SIZE // 3, "Connect 4 Remastered: ML-Powered Solver", LIGHT_GREY, font40)
	draw_text_center(screen, WIDTH / 2, SQUARE_SIZE * 4 / 5, "By Rohil Agarwal", LIGHT_GREY, font20)


	kinematics = menu_button(WIDTH // 2, 2 * SQUARE_SIZE, "ML Solver")
	circularMotion = menu_button(WIDTH // 2, 3 * SQUARE_SIZE, "Default Game")
	aboutMe = menu_button(WIDTH // 2, HEIGHT - SQUARE_SIZE, "About Me")

	#draw button and check if clicked
	if kinematics.draw_and_check_click(screen):
		update_game_state("ML Solver")

	if circularMotion.draw_and_check_click(screen):
		update_game_state("Default Game")

	if aboutMe.draw_and_check_click(screen):
		update_game_state("aboutMe")

	pygame.draw.rect(screen, WHITE, (0, SQUARE_SIZE, WIDTH, OUTLINE_WIDTH))  #Horizontal Outline
