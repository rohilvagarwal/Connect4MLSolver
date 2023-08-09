from ProjectConstants import *
from UIElements.Button import Button
import numpy as np
import random
import math

class Connect4GameLogic:
	def __init__(self, rowCount, columnCount, player1Name, player2Name, update_game_state):
		self.update_game_state = update_game_state

		#design
		self.bgColor = DARK_GREY
		self.boardColor = BLUE
		self.player1Color = RED
		self.player2Color = YELLOW
		self.chipOutlineColor = LIGHT_GREY
		self.textColor = WHITE
		self.menuColor = GREY
		self.gameDividerColor = WHITE
		self.transparentColor = (0, 0, 0, 0)

		#game
		self.rowCount = rowCount
		self.columnCount = columnCount
		self.player1Name = player1Name
		self.player2Name = player2Name

		#game logic
		self.noPlayerNum = 0
		self.player1Num = 1
		self.player2Num = 2

		self.playerColorDict = {
			self.player1Num: self.player1Color,
			self.player2Num: self.player2Color
		}

		self.playerNameDict = {
			self.player1Num: self.player1Name,
			self.player2Num: self.player2Name
		}

		self.gameOver = False
		self.board = np.zeros((rowCount, columnCount))
		self.turn = 1
		self.winnerName = None
		self.firstPlayer = self.player1Num
		self.currPlayer = self.firstPlayer
		self.currColor = self.playerColorDict[self.currPlayer]

		#fonts
		self.winFont = pygame.font.Font("fonts/Jost-700-Bold.otf", 75)
		self.turnFont = pygame.font.Font("fonts/Jost-700-Bold.otf", 20)
		self.menuFont = pygame.font.Font("fonts/Jost-700-Bold.otf", 30)

		#picture imports
		d4 = pygame.image.load("UIElements/d4.png").convert_alpha()
		self.d4resized = pygame.transform.scale(d4, (LOGO_SIZE, LOGO_SIZE)).convert_alpha()

		#animating chip
		self.ifAnimating = False
		self.animatingCol = None
		self.animatingXPos = None
		self.animatingYInitPos = int(SQUARE_SIZE / 2)
		self.animatingYCurrPos = None
		self.animatingYFinalPos = None
		self.animatingCurrVelocity = None

	def restart(self):
		self.gameOver = False
		self.board.fill(self.noPlayerNum)
		self.turn = 1
		self.winnerName = None
		#self.firstPlayer = random.randint(self.player1Num, self.player2Num)
		self.recalculate_curr_player()
		self.ifAnimating = False

	def switch_first_player(self):
		self.firstPlayer = self.player2Num if self.firstPlayer == self.player1Num else self.player1Num

	def recalculate_curr_player(self):
		if self.firstPlayer == self.player1Num:
			self.currPlayer = self.player1Num if self.turn % 2 == 1 else self.player2Num
		else:
			self.currPlayer = self.player2Num if self.turn % 2 == 1 else self.player1Num

		self.currColor = self.playerColorDict[self.currPlayer]

	def if_valid_column(self, col):
		topRow = self.board[self.rowCount - 1][col]
		return topRow == self.noPlayerNum

	def get_next_open_row(self, col):
		for r in range(self.rowCount):
			position = self.board[r][col]
			if np.any(position == self.noPlayerNum):
				return r

	def drop_piece(self, col):
		self.board[self.get_next_open_row(col)][col] = self.currPlayer
		self.turn += 1
		self.recalculate_curr_player()

	def check_game_over(self):
		def winning_move(board, player):
			# Check horizontal locations for win
			for c in range(self.columnCount - 3):
				for r in range(self.rowCount):
					if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
						return True

			# Check vertical locations for win
			for c in range(self.columnCount):
				for r in range(self.rowCount - 3):
					if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
						return True

			# Check positively sloped diagonals
			for c in range(self.columnCount - 3):
				for r in range(self.rowCount - 3):
					if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
						return True

			# Check negatively sloped diagonals
			for c in range(self.columnCount - 3):
				for r in range(3, self.rowCount):
					if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
						return True

		if winning_move(self.board, self.player1Num):
			self.gameOver = True
			self.winnerName = self.player1Name
			self.turn -= 1
		elif winning_move(self.board, self.player2Num):
			self.gameOver = True
			self.winnerName = self.player2Name
			self.turn -= 1
		elif not np.any(self.board == 0):
			self.gameOver = True
			self.turn -= 1

	#ui
	def draw_chip(self, screen, x, y, color, ifOutline):
		pygame.draw.circle(screen, color, (x, y), RADIUS)

		if ifOutline:
			pygame.draw.circle(screen, self.chipOutlineColor, (x, y), RADIUS, 5)

	def draw_background(self, screen):
		pygame.draw.rect(screen, self.bgColor, (0, 0, WIDTH - MENU_WIDTH, HEIGHT))  #Behind Board

		draw_text_right(screen, 55, 20, "Turn:", self.textColor, self.turnFont)
		draw_text_left(screen, 55 + 5, 20, str(self.turn), self.textColor, self.turnFont)

	def draw_board_foreground(self, board_layer):
		#Draw empty spots
		pygame.draw.rect(board_layer, self.boardColor, (0, 0, WIDTH - MENU_WIDTH, HEIGHT - SQUARE_SIZE))  #Board

		for c in range(self.columnCount):
			for r in range(self.rowCount):
				self.draw_chip(board_layer, int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE / 2), self.transparentColor, False)

		#Draw chips on board
		for c in range(self.columnCount):
			for r in range(self.rowCount):
				if self.board[r][c] == self.player1Num:
					self.draw_chip(board_layer, int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(HEIGHT - 2 * SQUARE_SIZE - r * SQUARE_SIZE + SQUARE_SIZE / 2), self.player1Color,
								   True)
				elif self.board[r][c] == self.player2Num:
					self.draw_chip(board_layer, int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(HEIGHT - 2 * SQUARE_SIZE - r * SQUARE_SIZE + SQUARE_SIZE / 2), self.player2Color,
								   True)


	def animate_drop(self, screen, col):
		board_layer = pygame.Surface((WIDTH - MENU_WIDTH, HEIGHT - SQUARE_SIZE)).convert_alpha()
		menu_layer = pygame.Surface((MENU_WIDTH, HEIGHT)).convert_alpha()

		xPos = int(col * SQUARE_SIZE + SQUARE_SIZE / 2)
		yInitPos = int(SQUARE_SIZE / 2)
		yCurrPos = yInitPos
		yFinalPos = HEIGHT - int(self.get_next_open_row(col) * SQUARE_SIZE + SQUARE_SIZE / 2)
		currVelocity = initial_velocity

		while yCurrPos < yFinalPos:
			#Draw Menu
			self.draw_menu(menu_layer)
			screen.blit(menu_layer, (WIDTH - MENU_WIDTH, 0))
			self.draw_menu_items(screen)

			self.draw_background(screen)
			self.draw_chip(screen, xPos, yCurrPos, self.currColor, True)
			self.draw_board_foreground(board_layer)
			screen.blit(board_layer, (0, SQUARE_SIZE))
			self.draw_outlines(screen)
			pygame.display.update()
			currVelocity += gravity
			yCurrPos += int(currVelocity / FPS)
			clock.tick(FPS)

		#Draw Menu
		self.draw_menu(menu_layer)
		screen.blit(menu_layer, (WIDTH - MENU_WIDTH, 0))
		self.draw_menu_items(screen)

		self.draw_background(screen)
		self.draw_chip(screen, xPos, yFinalPos, self.currColor, True)
		self.draw_board_foreground(board_layer)
		screen.blit(board_layer, (0, SQUARE_SIZE))
		pygame.display.update()

	def draw_outlines(self, screen):
		#Draw outlines
		pygame.draw.rect(screen, self.gameDividerColor, (WIDTH - MENU_WIDTH - OUTLINE_WIDTH, 0, OUTLINE_WIDTH, HEIGHT))  #Vertical Outline
		pygame.draw.rect(screen, self.gameDividerColor, (0, SQUARE_SIZE, WIDTH - MENU_WIDTH, OUTLINE_WIDTH))  #Horizontal Outline

	def draw_menu(self, menu_layer):
		pygame.draw.rect(menu_layer, self.menuColor, (0, 0, SQUARE_SIZE * 2, HEIGHT))  #Menu
		menu_layer.blit(self.d4resized, (MENU_WIDTH - LOGO_SIZE, HEIGHT - LOGO_SIZE))  #Logo
		draw_text_center(menu_layer, MENU_WIDTH // 2, SQUARE_SIZE // 2, "Connect 4", self.textColor, self.menuFont)

		pygame.draw.circle(menu_layer, self.playerColorDict[self.firstPlayer], (MENU_WIDTH / 5, 3 * SQUARE_SIZE), RADIUS / 2)
		pygame.draw.circle(menu_layer, self.chipOutlineColor, (MENU_WIDTH / 5, 3 * SQUARE_SIZE), RADIUS / 2, int(5 / 2))
		draw_text_left(menu_layer, MENU_WIDTH / 3, 3 * SQUARE_SIZE, "P1: " + self.playerNameDict[self.firstPlayer], self.textColor, self.turnFont)

		pygame.draw.circle(menu_layer, self.playerColorDict[self.firstPlayer + 1] if self.firstPlayer == self.player1Num else self.playerColorDict[self.firstPlayer - 1], (MENU_WIDTH / 5, SQUARE_SIZE * 7 // 2), RADIUS / 2)
		pygame.draw.circle(menu_layer, self.chipOutlineColor, (MENU_WIDTH / 5, SQUARE_SIZE * 7 // 2), RADIUS / 2, int(5 / 2))
		draw_text_left(menu_layer, MENU_WIDTH / 3, SQUARE_SIZE * 7 // 2, "P2: " + self.playerNameDict[self.firstPlayer + 1] if self.firstPlayer == self.player1Num else "P2: " + self.playerNameDict[self.firstPlayer - 1], self.textColor, self.turnFont)


	def draw_menu_items(self, screen):
		restartButton = Button(WIDTH - MENU_WIDTH / 2, HEIGHT / 4, MENU_WIDTH * 4 / 5, 50, self.menuFont, 10, "Restart")
		switchButton = Button(WIDTH - MENU_WIDTH / 2, HEIGHT / 4 + SQUARE_SIZE * 2 // 3, MENU_WIDTH * 4 / 5, 50, self.menuFont, 10, "Switch P1")
		menuButton = Button(WIDTH - MENU_WIDTH / 2, HEIGHT - SQUARE_SIZE * 4 // 3, MENU_WIDTH * 4 / 5, 50, font30, 10, "Menu")

		if restartButton.draw_and_check_click(screen):
			self.restart()

		if switchButton.draw_and_check_click(screen):
			self.switch_first_player()
			self.restart()

		if menuButton.draw_and_check_click(screen):
			self.update_game_state("Menu")

	def check_if_piece_added(self):
		if ifClicked():
			mouseX, mouseY = pygame.mouse.get_pos()

			if 0 < mouseX < WIDTH - MENU_WIDTH:
				col = int(math.floor(mouseX / SQUARE_SIZE))

				if self.if_valid_column(col):
					return col

		return None


	def draw_board(self, screen):
		board_layer = pygame.Surface((WIDTH - MENU_WIDTH, HEIGHT - SQUARE_SIZE)).convert_alpha()
		menu_layer = pygame.Surface((MENU_WIDTH, HEIGHT)).convert_alpha()

		self.draw_background(screen)

		if not self.gameOver:
			mouseX, mouseY = pygame.mouse.get_pos()

			#Draw Menu
			self.draw_menu(menu_layer)
			screen.blit(menu_layer, (WIDTH - MENU_WIDTH, 0))
			self.draw_menu_items(screen)

			if self.ifAnimating:
				self.draw_chip(screen, self.animatingXPos, self.animatingYCurrPos, self.currColor, True)

				self.animatingCurrVelocity += gravity
				self.animatingYCurrPos += self.animatingCurrVelocity // FPS

				if self.animatingYCurrPos > self.animatingYFinalPos:
					self.ifAnimating = False
					self.drop_piece(self.animatingCol)

			else:
				#Draw hovering chip
				if 0 < mouseX < WIDTH - MENU_WIDTH:
					circlePosX = int(math.floor(mouseX / SQUARE_SIZE)) * SQUARE_SIZE + SQUARE_SIZE / 2
					self.draw_chip(screen, circlePosX, int(SQUARE_SIZE / 2), self.currColor, True)

				#Drop piece if clicked
				columnDropped = self.check_if_piece_added()
				if columnDropped is not None:
					self.ifAnimating = True
					self.animatingCol = columnDropped
					self.animatingXPos = int(columnDropped * SQUARE_SIZE + SQUARE_SIZE / 2)
					self.animatingYInitPos = int(SQUARE_SIZE / 2)
					self.animatingYCurrPos = self.animatingYInitPos
					self.animatingYFinalPos = HEIGHT - int(self.get_next_open_row(columnDropped) * SQUARE_SIZE + SQUARE_SIZE / 2)
					self.animatingCurrVelocity = initial_velocity

			#Board
			self.draw_board_foreground(board_layer)
			screen.blit(board_layer, (0, SQUARE_SIZE))

			self.draw_outlines(screen)

			self.check_game_over()

		else:
			#Board
			self.draw_board_foreground(board_layer)
			screen.blit(board_layer, (0, SQUARE_SIZE))

			self.draw_outlines(screen)

			if self.winnerName is None:
				self.recalculate_curr_player()
				draw_text_center(screen, (WIDTH - MENU_WIDTH) / 2, SQUARE_SIZE / 2, "It is a tie!", self.textColor, self.winFont)
			else:
				self.recalculate_curr_player()
				draw_text_center(screen, (WIDTH - MENU_WIDTH) / 2, SQUARE_SIZE / 2, self.winnerName + " won!", self.currColor, self.winFont)

			#Draw Menu
			self.draw_menu(menu_layer)
			screen.blit(menu_layer, (WIDTH - MENU_WIDTH, 0))
			self.draw_menu_items(screen)

	def print_board(self):
		print(np.flip(self.board, 0))