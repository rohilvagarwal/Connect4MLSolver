import numpy as np
import pygame
from pygame.locals import *
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
	board = np.zeros((ROW_COUNT, COLUMN_COUNT))
	return board


def drop_piece(board, row, col, piece):
	board[row][col] = piece


def is_valid_location(board, col):
	return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r


def print_board(board):
	print(np.flip(board, 0))


def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT - 3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
				return True


def animate_drop(row, col, piece):
	x_pos = int(col * SQUARESIZE + SQUARESIZE / 2)
	y_init_pos = int(SQUARESIZE / 2)
	y_final_pos = height - int(row * SQUARESIZE + SQUARESIZE / 2)
	curr_velocity = initial_velocity

	if piece == 1:
		color = RED
	else:
		color = YELLOW

	y_curr_pos = y_init_pos
	while y_curr_pos < y_final_pos:
		pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
		draw_board(board)
		pygame.draw.circle(screen, color, (x_pos, y_curr_pos), RADIUS)
		pygame.display.update()
		curr_velocity += gravity
		y_curr_pos += int(curr_velocity / FPS)
		clock.tick(FPS)

	draw_board(board)


def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (
					int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
			elif board[r][c] == 2:
				pygame.draw.circle(screen, YELLOW, (
					int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
	pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
clock = pygame.time.Clock()
initial_velocity = 0
velocity = 500  # pixels per second
gravity = 40  # pixels per second squared

FPS = 60

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
			else:
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			turn += 1
			pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

			# Ask for Player 1 Input
			if turn % 2 == 1:
				posx = event.pos[0]
				col = int(math.floor(posx / SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					animate_drop(row, col, 1)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40, 10))
						game_over = True


			# # Ask for Player 2 Input
			else:
				posx = event.pos[0]
				col = int(math.floor(posx / SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					animate_drop(row, col, 2)
					drop_piece(board, row, col, 2)

					if winning_move(board, 2):
						label = myfont.render("Player 2 wins!!", 1, YELLOW)
						screen.blit(label, (40, 10))
						game_over = True

			print_board(board)
			print()

			draw_board(board)

			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)

	clock.tick(FPS)
