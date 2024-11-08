import pygame

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pixelated 9-Slice Button Example")

# Define Colors
WHITE = (255, 255, 255)

# 9-Slice rendering function with pixel scaling
def render_9slice(image, rect, corner_size):
    # Define the regions of the 9-slice
    w, h = image.get_size()
    slices = {
        "top_left": image.subsurface((0, 0, corner_size, corner_size)),
        "top": image.subsurface((corner_size, 0, w - 2 * corner_size, corner_size)),
        "top_right": image.subsurface((w - corner_size, 0, corner_size, corner_size)),
        "left": image.subsurface((0, corner_size, corner_size, h - 2 * corner_size)),
        "center": image.subsurface((corner_size, corner_size, w - 2 * corner_size, h - 2 * corner_size)),
        "right": image.subsurface((w - corner_size, corner_size, corner_size, h - 2 * corner_size)),
        "bottom_left": image.subsurface((0, h - corner_size, corner_size, corner_size)),
        "bottom": image.subsurface((corner_size, h - corner_size, w - 2 * corner_size, corner_size)),
        "bottom_right": image.subsurface((w - corner_size, h - corner_size, corner_size, corner_size)),
    }

    # Draw the slices onto the target rect
    screen.blit(slices["top_left"], (rect.x, rect.y))
    screen.blit(pygame.transform.scale(slices["top"], (rect.width - 2 * corner_size, corner_size)), (rect.x + corner_size, rect.y))
    screen.blit(slices["top_right"], (rect.x + rect.width - corner_size, rect.y))

    screen.blit(pygame.transform.scale(slices["left"], (corner_size, rect.height - 2 * corner_size)), (rect.x, rect.y + corner_size))
    screen.blit(pygame.transform.scale(slices["center"], (rect.width - 2 * corner_size, rect.height - 2 * corner_size)), (rect.x + corner_size, rect.y + corner_size))
    screen.blit(pygame.transform.scale(slices["right"], (corner_size, rect.height - 2 * corner_size)), (rect.x + rect.width - corner_size, rect.y + corner_size))

    screen.blit(slices["bottom_left"], (rect.x, rect.y + rect.height - corner_size))
    screen.blit(pygame.transform.scale(slices["bottom"], (rect.width - 2 * corner_size, corner_size)), (rect.x + corner_size, rect.y + rect.height - corner_size))
    screen.blit(slices["bottom_right"], (rect.x + rect.width - corner_size, rect.y + rect.height - corner_size))

# Button Class with 9-Slice Pixelated Support and Multiple States
class Button:
    def __init__(self, x, y, width, height, text='', text_color=(255, 255, 255), corner_size=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 32)
        self.enabled = True  # Button is enabled by default
        self.corner_size = corner_size

        # Load images for different states
        self.image_normal = pygame.image.load("button.png").convert_alpha()
        self.image_highlighted = pygame.image.load("button_highlighted.png").convert_alpha()
        self.image_disabled = pygame.image.load("button_disabled.png").convert_alpha()
    
    def draw(self, screen):
        # Determine which image to display based on state
        if not self.enabled:
            image = self.image_disabled
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            image = self.image_highlighted
        else:
            image = self.image_normal
        
        # Draw the 9-slice image with pixel scaling
        render_9slice(image, self.rect, self.corner_size)

        # Draw the text on top of the button
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        # Check if the button is enabled and if a position is within the button's rectangle
        return self.enabled and self.rect.collidepoint(pos)

    def set_enabled(self, enabled):
        # Enable or disable the button
        self.enabled = enabled

# Main game loop
running = True
button = Button(300, 250, 200, 50, text="Click Me!")

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_clicked(event.pos):
                print("Button clicked!")
                button.set_enabled(False)  # Disable button after clicking

    # Draw button
    button.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()
