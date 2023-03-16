import numpy as np
import pygame
import sys
import math

#1 is AI, 2 is Human
AI = 1
HUMAN = 2

DARK_GREY = pygame.Color("#242526")
BLUE = pygame.Color("#1357BE")
RED = pygame.Color("#FF6961")
YELLOW = pygame.Color("#FDFD96")
WHITE = pygame.Color("#FFFFFF")
LIGHT_GREY = pygame.Color("#D3D3D3")
NAVY_BLUE = pygame.Color("#27285C")
GREEN = pygame.Color("#77DD77")
DARK_PURPLE = pygame.Color("#301934")
GREY = pygame.Color("#4c4c4c")

ROW_COUNT = 6
COLUMN_COUNT = 7

backgroundColor = DARK_GREY
gameColor = BLUE
AIcolor = RED
humanColor = YELLOW
chipOutlineColor = LIGHT_GREY
turnColor = WHITE
menuColor = GREY
outlineColor = WHITE

SQUARE_SIZE = 100
WIDTH = COLUMN_COUNT * SQUARE_SIZE + 2 * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
SIZE = (WIDTH, HEIGHT)
RADIUS = int(SQUARE_SIZE / 2 - 5)
OUTLINE_WIDTH = 3
LOGO_SIZE = 100

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
	topRow = board[ROW_COUNT - 1][col]
	return topRow == 0


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

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT - 3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
				return True


def evaluate_window(window, player):
	score = 0
	opponent = HUMAN

	if player == HUMAN:
		opponent = AI

	if window.count(player) == 4:
		score += math.inf
	elif window.count(player) == 3 and window.count(0) == 1:
		score += 5
	elif window.count(player) == 2 and window.count(0) == 2:
		score += 2

	if window.count(opponent) == 3 and window.count(0) == 1:
		score -= 4

	return score


def score_position(board, player):
	score = 0

	# Check horizontal windows for score
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT):
			window = [board[r][c], board[r][c + 1], board[r][c + 2], board[r][c + 3]]
			score += evaluate_window(window, player)

	# Check vertical windows for score
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT - 3):
			window = [board[r][c], board[r + 1][c], board[r + 2][c], board[r + 3][c]]
			score += evaluate_window(window, player)

	# Check positively sloped diagonals windows for score
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT - 3):
			window = [board[r][c], board[r + 1][c + 1], board[r + 2][c + 2], board[r + 3][c + 3]]
			score += evaluate_window(window, player)

	# Check negatively sloped diagonals windows for score
	for c in range(COLUMN_COUNT - 3):
		for r in range(3, ROW_COUNT):
			window = [board[r][c], board[r - 1][c + 1], board[r - 2][c + 2], board[r - 3][c + 3]]
			score += evaluate_window(window, player)

	#Center Position Score
	for r in range(ROW_COUNT):
		if board[r][COLUMN_COUNT // 2] == player:
			score += 3

	return score


def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations


def is_terminal_node(board):
	return winning_move(board, HUMAN) or winning_move(board, AI) or len(get_valid_locations(board)) == 0


def pick_best_move(board, player):
	valid_locations = get_valid_locations(board)
	best_score = -math.inf
	best_col = None
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, player)
		score = score_position(temp_board, player)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col


def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI):
				return [None, math.inf]
			elif winning_move(board, HUMAN):
				return [None, -math.inf]
			else:  # Game is over, no more valid moves
				return [None, 0]

		else:  # Depth is zero
			return [None, score_position(board, AI)]

	if maximizingPlayer:
		value = -math.inf
		column = None
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI)
			new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return [column, value]

	else:  # Minimizing player
		value = math.inf
		column = None
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, HUMAN)
			new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return [column, value]


def draw_chip(x, y, player):
	color = AIcolor

	if player == 2:
		color = humanColor

	pygame.draw.circle(screen, color, (x, y), RADIUS)
	pygame.draw.circle(screen, chipOutlineColor, (x, y), RADIUS, 5)


def animate_drop(row, col, player):
	x_pos = int(col * SQUARE_SIZE + SQUARE_SIZE / 2)
	y_init_pos = int(SQUARE_SIZE / 2)
	y_final_pos = HEIGHT - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)
	curr_velocity = initial_velocity

	y_curr_pos = y_init_pos
	while y_curr_pos < y_final_pos:
		draw_board(board, turn)
		label = turnFont.render("Turn: " + str(turn), True, turnColor)
		screen.blit(label, (10, 10))
		draw_chip(x_pos, y_curr_pos, player)
		pygame.display.update()
		curr_velocity += gravity
		y_curr_pos += int(curr_velocity / FPS)
		clock.tick(FPS)

	draw_board(board)


def draw_top():
	pygame.draw.rect(screen, backgroundColor, (0, 0, WIDTH - 2 * SQUARE_SIZE, SQUARE_SIZE))
	label = turnFont.render("Turn: " + str(turn), True, turnColor)
	screen.blit(label, (10, 10))
	pygame.draw.rect(screen, outlineColor, (WIDTH - 2 * SQUARE_SIZE - OUTLINE_WIDTH, 0, OUTLINE_WIDTH, SQUARE_SIZE))  #Vertical Outline


def draw_board(board, turn=None):
	if turn is None:
		pygame.draw.rect(screen, backgroundColor, (0, 0, WIDTH - 2 * SQUARE_SIZE, SQUARE_SIZE))  #Top
	else:
		draw_top()

	pygame.draw.rect(screen, menuColor, (WIDTH - 2 * SQUARE_SIZE, 0, SQUARE_SIZE * 2, HEIGHT))  #Menu

	pygame.draw.rect(screen, gameColor, (0, SQUARE_SIZE, WIDTH - 2 * SQUARE_SIZE, HEIGHT - SQUARE_SIZE))  #Board
	pygame.draw.rect(screen, outlineColor, (0, SQUARE_SIZE, WIDTH - 2 * SQUARE_SIZE, OUTLINE_WIDTH))  #Horizontal Outline
	pygame.draw.rect(screen, outlineColor, (WIDTH - 2 * SQUARE_SIZE - OUTLINE_WIDTH, 0, OUTLINE_WIDTH, HEIGHT))  #Vertical Outline

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.circle(screen, backgroundColor,
							   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == AI:
				draw_chip(int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2), AI)
			elif board[r][c] == HUMAN:
				draw_chip(int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2), HUMAN)

	#pygame.draw.rect(screen, outlineColor, (0, SQUARE_SIZE, WIDTH - 2 * SQUARE_SIZE, OUTLINE_WIDTH))
	screen.blit(d4resized, (WIDTH - LOGO_SIZE, HEIGHT - LOGO_SIZE))
	pygame.display.update()


pygame.init()
screen = pygame.display.set_mode(SIZE)

d4 = pygame.image.load("d4.png").convert_alpha()
d4resized = pygame.transform.scale(d4, (LOGO_SIZE, LOGO_SIZE)).convert_alpha()

board = create_board()
print_board(board)
draw_board(board)

game_over = False
turn = 1

pygame.display.update()

winFont = pygame.font.SysFont("jost700", 75)
turnFont = pygame.font.SysFont("jost700", 20)

while not game_over:
	if turn % 2 == 0:
		currPlayer = HUMAN
		currColor = humanColor
	else:
		currPlayer = AI
		currColor = AIcolor

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		draw_top()

		if currPlayer == HUMAN:
			if event.type == pygame.MOUSEMOTION:
				posx = event.pos[0]

				if posx < WIDTH - 2 * SQUARE_SIZE:
					circlePosX = int(math.floor(posx / SQUARE_SIZE)) * SQUARE_SIZE + SQUARE_SIZE / 2
					draw_chip(circlePosX, int(SQUARE_SIZE / 2), HUMAN)

			pygame.display.update()

			if event.type == pygame.MOUSEBUTTONDOWN:
				posx = event.pos[0]

				if posx < WIDTH - 2 * SQUARE_SIZE:
					col = int(math.floor(posx / SQUARE_SIZE))

					if is_valid_location(board, col):
						row = get_next_open_row(board, col)

						animate_drop(row, col, HUMAN)
						drop_piece(board, row, col, HUMAN)

						if winning_move(board, HUMAN):
							game_over = True

						turn += 1

					print_board(board)
					print()

					draw_board(board, turn)

	if currPlayer == AI and not game_over:
		col = minimax(board, 5, -math.inf, math.inf, True)[0]
		#pygame.time.wait(500)
		row = get_next_open_row(board, col)
		animate_drop(row, col, AI)
		drop_piece(board, row, col, AI)

		if winning_move(board, AI):
			game_over = True

		print_board(board)
		turn += 1
		draw_board(board, turn)

		if game_over:
			playerName = None

			if currPlayer == 1:
				playerName = "The AI"
			else:
				playerName = "You"
			label = winFont.render(playerName + " won!", True, currColor)
			text_rect = label.get_rect(center=((WIDTH - 2 * SQUARE_SIZE) / 2, 50))
			screen.blit(label, text_rect)
			pygame.display.update()

			pygame.time.wait(3000)

	clock.tick(FPS)
