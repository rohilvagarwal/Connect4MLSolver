from ProjectConstants import *
from UIElements.Button import Button
import random

rojWidth = 300
roj = pygame.image.load('UIElements/roj.png').convert_alpha()
scaledRoj = pygame.transform.scale(roj, (rojWidth, rojWidth)).convert_alpha()

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

def draw_about_me(screen, update_game_state):
	global xCurrPos, yInitPos, yCurrPos, yFinalPos, currVelocity, currColor

	board = [[1, 1, 0],
		 [1, 2, 0],
		 [2, 1, 0],
		 [2, 2, 0],
		 [1, 2, 0],
		 [0, 1, 0]]
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
	draw_text_center(screen, WIDTH / 2, SQUARE_SIZE // 2, "About Me", LIGHT_GREY, font40)

	screen.blit(board_layer, (-SQUARE_SIZE // 2, SQUARE_SIZE))
	screen.blit(pygame.transform.flip(board_layer, True, False), (WIDTH - SQUARE_SIZE * 5 // 2, SQUARE_SIZE))

	screen.blit(scaledRoj, (WIDTH / 2 - rojWidth / 2, SQUARE_SIZE * 4 // 3))
	draw_text_center(screen, WIDTH / 2, HEIGHT * 2 // 3, "By Rohil Agarwal", WHITE, font30)
	draw_text_center(screen, WIDTH / 2, HEIGHT * 2 // 3 + SQUARE_SIZE // 2, "I go by roj.", WHITE, font20)
	draw_text_center(screen, WIDTH / 2, HEIGHT - SQUARE_SIZE * 3 // 2, "Github: https://github.com/rohilvagarwal", WHITE, font15)
	draw_text_center(screen, WIDTH / 2, HEIGHT - SQUARE_SIZE * 4 // 3, "LinkedIn: https://www.linkedin.com/in/rohil-ag/", WHITE, font15)

	menuButton = Button(WIDTH // 2, HEIGHT - SQUARE_SIZE // 2, SQUARE_SIZE * 5 // 2, SQUARE_SIZE // 2, font30, SQUARE_SIZE // 10, "Menu")

	if menuButton.draw_and_check_click(screen):
		update_game_state("Menu")