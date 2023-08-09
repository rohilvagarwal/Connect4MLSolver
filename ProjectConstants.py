import pygame

pygame.init()
clock = pygame.time.Clock()
FPS = 60
initial_velocity = 0
gravity = 40  # pixels per second squared
chip_movement_velocity = 50

#clicking mechanism
ifMouseDownEarlier = False

def ifClicked():
	global ifMouseDownEarlier

	if pygame.mouse.get_pressed()[0] == 1:
		if not ifMouseDownEarlier:
			ifMouseDownEarlier = True
			#print("Yes")
			return True
	else:
		ifMouseDownEarlier = False

	return False


ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARE_SIZE = 100
WIDTH = COLUMN_COUNT * SQUARE_SIZE + 2 * SQUARE_SIZE
MENU_WIDTH = 2 * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
SIZE = (WIDTH, HEIGHT)
RADIUS = int(SQUARE_SIZE / 2 - 5)
OUTLINE_WIDTH = 3
LOGO_SIZE = 100

#Colors
DARK_GREY = pygame.Color("#242526")
BLUE = pygame.Color("#1357BE")
RED = pygame.Color("#FF6961")
YELLOW = pygame.Color("#FDFD96")
LIGHT_GREY = pygame.Color("#D3D3D3")
WHITE = pygame.Color("#FFFFFF")
GREY = pygame.Color("#4c4c4c")

#10, 20, 25, 30, 70
font15 = pygame.font.Font("fonts/Jost-700-Bold.otf", 15)
font20 = pygame.font.Font("fonts/Jost-700-Bold.otf", 20)
font30 = pygame.font.Font("fonts/Jost-700-Bold.otf", 30)
font40 = pygame.font.Font("fonts/Jost-700-Bold.otf", 40)


def draw_text_center(screen, centerX, centerY, text, color, font):
	text = font.render(text, True, color)
	text_rect = text.get_rect(center=(centerX, centerY))
	screen.blit(text, text_rect)


def draw_text_left(screen, leftX, centerY, text, color, font):
	text = font.render(text, True, color)
	text_rect = text.get_rect(left=leftX, centery=centerY)
	screen.blit(text, text_rect)


def draw_text_right(screen, rightX, centerY, text, color, font):
	text = font.render(text, True, color)
	text_rect = text.get_rect(right=rightX, centery=centerY)
	screen.blit(text, text_rect)