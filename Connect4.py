import numpy as np
import pygame
import sys
import math

GREY = pygame.Color("#242526")
BLUE = pygame.Color("#1357BE")
RED = pygame.Color("#FF6961")
YELLOW = pygame.Color("#FDFD96")
WHITE = pygame.Color("#FFFFFF")
LIGHT_GREY = pygame.Color("#D3D3D3")
NAVY_BLUE = pygame.Color("#27285C")

ROW_COUNT = 6
COLUMN_COUNT = 7

backgroundColor = GREY
gameColor = BLUE
player1Color = RED
player2Color = YELLOW
chipOutlineColor = LIGHT_GREY
turnColor = WHITE

SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)

clock = pygame.time.Clock()
FPS = 60
initial_velocity = 0
gravity = 40  # pixels per second squared
chip_movement_velocity = 50


def create_board():
	board = np.zeros((ROW_COUNT, COLUMN_COUNT))
	return board


def drop_piece(board, row, col, player):
	board[row][col] = player


def is_valid_location(board, col):
	return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r


def print_board(board):
	print(np.flip(board, 0))


def winning_move(board, player):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT):
			if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
				return True

	# Check positively sloped diagonals
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
				return True

	# Check negatively sloped diagonals
	for c in range(COLUMN_COUNT - 3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
				return True


def draw_chip(x, y, player):
	color = player1Color

	if player == 2:
		color = player2Color

	pygame.draw.circle(screen, color, (x, y), RADIUS)
	pygame.draw.circle(screen, chipOutlineColor, (x, y), RADIUS, 5)


def animate_drop(row, col, player):
	x_pos = int(col * SQUARE_SIZE + SQUARE_SIZE / 2)
	y_init_pos = int(SQUARE_SIZE / 2)
	y_final_pos = height - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)
	curr_velocity = initial_velocity

	y_curr_pos = y_init_pos
	while y_curr_pos < y_final_pos:
		draw_board(board)
		draw_chip(x_pos, y_curr_pos, player)
		pygame.display.update()
		curr_velocity += gravity
		y_curr_pos += int(curr_velocity / FPS)
		clock.tick(FPS)

	draw_board(board)


def draw_board(board):
	pygame.draw.rect(screen, backgroundColor, (0, 0, width, SQUARE_SIZE))

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, gameColor, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
			pygame.draw.circle(screen, backgroundColor,
							   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
				draw_chip(int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2), 1)
			elif board[r][c] == 2:
				draw_chip(int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2), 2)
	pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 1

pygame.init()

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

winFont = pygame.font.SysFont("jost700", 75)
turnFont = pygame.font.SysFont("jost700", 20)

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		currPlayer = turn % 2
		currColor = player1Color

		if currPlayer == 0:
			currPlayer += 2
			currColor = player2Color

		pygame.draw.rect(screen, backgroundColor, (0, 0, width, SQUARE_SIZE))
		label = turnFont.render("Turn: " + str(turn), True, turnColor)
		screen.blit(label, (10, 10))

		if event.type == pygame.MOUSEMOTION:
			posx = event.pos[0]
			circlePosX = int(math.floor(posx / SQUARE_SIZE)) * SQUARE_SIZE + SQUARE_SIZE / 2

			if currPlayer == 1:
				draw_chip(circlePosX, int(SQUARE_SIZE / 2), 1)

			else:
				draw_chip(circlePosX, int(SQUARE_SIZE / 2), 2)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			posx = event.pos[0]
			col = int(math.floor(posx / SQUARE_SIZE))

			if is_valid_location(board, col):
				row = get_next_open_row(board, col)

				#animate_drop(row, col, currPlayer)
				drop_piece(board, row, col, currPlayer)

				if winning_move(board, currPlayer):
					game_over = True

				turn += 1

			print_board(board)
			print()

			draw_board(board)

			if game_over:
				label = winFont.render("Player " + str(currPlayer) + " wins!", True, currColor)
				text_rect = label.get_rect(center=(width / 2, 50))
				screen.blit(label, text_rect)
				pygame.display.update()

				pygame.time.wait(3000)

	clock.tick(FPS)
