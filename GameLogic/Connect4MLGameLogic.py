from ProjectConstants import *
from GameLogic.Connect4GameLogic import Connect4GameLogic
import numpy as np
import math

def ml_drop_piece(board, row, col, player):
	board[row][col] = player


def ml_if_valid_column(board, col, noPlayerNum):
	topRow = board[ROW_COUNT - 1][col]
	return topRow == noPlayerNum


def ml_get_valid_columns(board, noPlayerNum):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if ml_if_valid_column(board, col, noPlayerNum):
			valid_locations.append(col)
	return valid_locations


def ml_get_next_open_row(board, col, noPlayerNum):
	for r in range(ROW_COUNT):
		position = board[r][col]
		if np.any(position == noPlayerNum):
			return r

def ml_winning_move(board, player):
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

def ml_evaluate_window(window, player, mlNum, humanNum):
	score = 0
	opponent = humanNum

	if player == humanNum:
		opponent = mlNum

	if window.count(player) == 4:
		score += 999999
	elif window.count(player) == 3 and window.count(0) == 1:
		score += 5
	elif window.count(player) == 2 and window.count(0) == 2:
		score += 2
	if window.count(opponent) == 3 and window.count(0) == 1:
		score -= 10

	return score

def ml_score_position(board, player, mlNum, humanNum):
	score = 0

	# Check horizontal windows for score
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT):
			window = [board[r][c], board[r][c + 1], board[r][c + 2], board[r][c + 3]]
			score += ml_evaluate_window(window, player, mlNum, humanNum)

	# Check vertical windows for score
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT - 3):
			window = [board[r][c], board[r + 1][c], board[r + 2][c], board[r + 3][c]]
			score += ml_evaluate_window(window, player, mlNum, humanNum)

	# Check positively sloped diagonals windows for score
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT - 3):
			window = [board[r][c], board[r + 1][c + 1], board[r + 2][c + 2], board[r + 3][c + 3]]
			score += ml_evaluate_window(window, player, mlNum, humanNum)

	# Check negatively sloped diagonals windows for score
	for c in range(COLUMN_COUNT - 3):
		for r in range(3, ROW_COUNT):
			window = [board[r][c], board[r - 1][c + 1], board[r - 2][c + 2], board[r - 3][c + 3]]
			score += ml_evaluate_window(window, player, mlNum, humanNum)

	#Center Position Score
	for r in range(ROW_COUNT):
		if board[r][COLUMN_COUNT // 2] == player:
			score += 3

	return score

def ml_is_terminal_node(board, noPlayerNum, mlNum, humanNum):
	return ml_winning_move(board, humanNum) or ml_winning_move(board, mlNum) or len(ml_get_valid_columns(board, noPlayerNum)) == 0

def pick_best_move(board, player, noPlayerNum, mlNum, humanNum):
	valid_locations = ml_get_valid_columns(board, noPlayerNum)
	best_score = -math.inf
	best_col = None
	for col in valid_locations:
		row = ml_get_next_open_row(board, col, noPlayerNum)
		temp_board = board.copy()
		ml_drop_piece(temp_board, row, col, player)
		score = ml_score_position(temp_board, player, mlNum, humanNum)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def ml_minimax(board, depth, alpha, beta, maximizingPlayer, noPlayerNum, mlNum, humanNum):
	valid_locations = ml_get_valid_columns(board, noPlayerNum)
	is_terminal = ml_is_terminal_node(board, noPlayerNum, mlNum, humanNum)
	if depth == 0 or is_terminal:
		if is_terminal:
			if ml_winning_move(board, mlNum):
				return [None, 999999]
			elif ml_winning_move(board, humanNum):
				return [None, -999999]
			else:  # Game is over, no more valid moves
				return [None, 0]

		else:  # Depth is zero
			return [None, ml_score_position(board, mlNum, mlNum, humanNum)]

	if maximizingPlayer:
		value = -math.inf
		column = None
		for col in valid_locations:
			row = ml_get_next_open_row(board, col, noPlayerNum)
			b_copy = board.copy()
			ml_drop_piece(b_copy, row, col, mlNum)
			new_score = ml_minimax(b_copy, depth - 1, alpha, beta, False, noPlayerNum, mlNum, humanNum)[1]
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
			row = ml_get_next_open_row(board, col, noPlayerNum)
			b_copy = board.copy()
			ml_drop_piece(b_copy, row, col, humanNum)
			new_score = ml_minimax(b_copy, depth - 1, alpha, beta, True, noPlayerNum, mlNum, humanNum)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return [column, value]

class Connect4MLGameLogic(Connect4GameLogic):
	def __init__(self, rowCount, columnCount, mlName, humanName):
		super().__init__(rowCount, columnCount, mlName, humanName)
		self.mlName = mlName
		self.humanName = humanName

		self.playerNumDict = {name: num for num, name in self.playerNameDict.items()}

		self.mlNum = self.playerNumDict[self.mlName]
		self.humanNum = self.playerNumDict[self.humanName]

	def draw_board(self, screen):
		board_layer = pygame.Surface((WIDTH - MENU_WIDTH, HEIGHT - SQUARE_SIZE)).convert_alpha()
		menu_layer = pygame.Surface((MENU_WIDTH, HEIGHT)).convert_alpha()

		if not self.gameOver:
			#Draw Menu
			self.draw_menu(menu_layer)
			screen.blit(menu_layer, (WIDTH - MENU_WIDTH, 0))
			self.draw_menu_items(screen)

			#Board
			self.draw_background(screen)
			self.draw_board_foreground(board_layer)
			screen.blit(board_layer, (0, SQUARE_SIZE))

			#if current player is human
			if self.humanNum == self.currPlayer:
				mouseX, mouseY = pygame.mouse.get_pos()

				#Draw hovering chip
				if 0 < mouseX < WIDTH - MENU_WIDTH:
					circlePosX = int(math.floor(mouseX / SQUARE_SIZE)) * SQUARE_SIZE + SQUARE_SIZE / 2
					self.draw_chip(screen, circlePosX, int(SQUARE_SIZE / 2), self.currColor, True)

				#Drop piece if clicked
				columnDropped = self.check_if_piece_added()
				if columnDropped is not None:
					self.animate_drop(screen, columnDropped)
					self.drop_piece(columnDropped)

			#if current player is ML
			else:
				col = ml_minimax(self.board, 5, -math.inf, math.inf, True, self.noPlayerNum, self.mlNum, self.humanNum)[0]
				self.animate_drop(screen, col)
				self.drop_piece(col)

			self.draw_outlines(screen)
			self.check_game_over()

		else:
			#Draw Menu
			self.draw_menu(menu_layer)
			screen.blit(menu_layer, (WIDTH - MENU_WIDTH, 0))

			self.draw_menu_items(screen)

			#Board
			self.draw_background(screen)
			self.draw_board_foreground(board_layer)
			screen.blit(board_layer, (0, SQUARE_SIZE))

			self.draw_outlines(screen)

			if self.winnerName is None:
				self.recalculate_curr_player()
				draw_text_center(screen, (WIDTH - MENU_WIDTH) / 2, SQUARE_SIZE / 2, "It is a tie!", self.textColor, self.winFont)
			else:
				self.recalculate_curr_player()
				draw_text_center(screen, (WIDTH - MENU_WIDTH) / 2, SQUARE_SIZE / 2, self.winnerName + " won!", self.currColor, self.winFont)