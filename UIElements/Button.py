from ProjectConstants import *


class Button:
	def __init__(self, centerX, centerY, width, height, font, borderSize, text="empty"):
		self.textColor = WHITE
		self.hoverColor = LIGHT_GREY
		self.backgroundColor = GREY


		#font
		self.font = font

		#text
		self.buttonText = self.font.render(text, True, self.textColor)
		self.textWidth = self.buttonText.get_width()
		self.textHeight = self.buttonText.get_height()
		self.buttonPosition = self.buttonText.get_rect(center=(centerX, centerY))

		#background
		self.buttonBackground = pygame.Rect(0, 0, width, height)
		self.buttonBackground.center = (centerX, centerY)
		self.borderSize = borderSize

	def draw_and_check_click(self, surface):
		pressed = False
		mousePos = pygame.mouse.get_pos()

		#if mouse is on button
		if self.buttonBackground.collidepoint(mousePos):
			pygame.draw.rect(surface, self.textColor, self.buttonBackground, width=self.borderSize)
			pygame.draw.rect(surface, self.hoverColor, self.buttonBackground.inflate(-self.borderSize, -self.borderSize))

			if ifClicked():
				pressed = True

		#if mouse is not on button
		else:
			pygame.draw.rect(surface, self.textColor, self.buttonBackground, width=self.borderSize)
			pygame.draw.rect(surface, self.backgroundColor, self.buttonBackground.inflate(-self.borderSize, -self.borderSize))

		surface.blit(self.buttonText, self.buttonPosition)

		return pressed
