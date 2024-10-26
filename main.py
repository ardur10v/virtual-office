import pygame
import sys
import pyaudio

# Initialize Pygame
pygame.init()

# Set up display dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Avatar with Mute/Unmute and Speaking Indicator")

# Load images
bg_image = pygame.image.load('./office.png').convert()
bg_image = pygame.transform.scale(bg_image, (width, height))
avatar_image = pygame.image.load('./avatar.png').convert_alpha()

# Scale the avatar image
scaled_avatar_image = pygame.transform.scale(avatar_image, (200, 200))

# Load mute/unmute icons and set icon position
mute_icon = pygame.image.load('./mute.webp').convert_alpha()
unmute_icon = pygame.image.load('./unmute.jpg').convert_alpha()
icon_size = (40, 40)
mute_icon = pygame.transform.scale(mute_icon, icon_size)
unmute_icon = pygame.transform.scale(unmute_icon, icon_size)
icon_position = (width - icon_size[0] - 10, 10)  # Top-right corner

# Load speaking indicator icon
speaking_icon = pygame.image.load('./speaking.png').convert_alpha()
speaking_icon = pygame.transform.scale(speaking_icon, (50, 50))  # Adjust size as needed

# Set initial mute state
is_muted = True

# Set up microphone input
p = pyaudio.PyAudio()

# Define audio stream (initially closed)
def open_stream():
    return p.open(format=pyaudio.paInt16,
                  channels=1,
                  rate=44100,
                  input=True,
                  frames_per_buffer=1024)

stream = None  # Initialize stream variable

def toggle_audio():
    global is_muted, stream
    if is_muted:
        stream = open_stream()  # Open the audio stream for input
    else:
        if stream is not None:
            stream.stop_stream()
            stream.close()
            stream = None
    is_muted = not is_muted

# Avatar class definition
class Avatar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = scaled_avatar_image
        self.rect = self.image.get_rect(center=(400, 300))
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < height:
            self.rect.y += 5

# Create sprite groups
all_sprites = pygame.sprite.Group()
avatar = Avatar()
all_sprites.add(avatar)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if the mute/unmute icon is clicked
            if icon_position[0] <= mouse_pos[0] <= icon_position[0] + icon_size[0] and \
               icon_position[1] <= mouse_pos[1] <= icon_position[1] + icon_size[1]:
                toggle_audio()  # Toggle microphone audio

    # Update all sprites
    all_sprites.update()

    # Draw background image and sprites
    screen.blit(bg_image, (0, 0))
    all_sprites.draw(screen)

    # Draw mute/unmute icon
    if is_muted:
        screen.blit(mute_icon, icon_position)
    else:
        screen.blit(unmute_icon, icon_position)

    # Draw speaking indicator above the avatar if unmuted
    if not is_muted:
        # Position the speaking indicator just above the avatar
        speaking_position = (avatar.rect.centerx - speaking_icon.get_width() // 2, avatar.rect.top - speaking_icon.get_height())
        screen.blit(speaking_icon, speaking_position)

    # Refresh the display
    pygame.display.flip()

# Clean up
if stream is not None:
    stream.stop_stream()
    stream.close()
p.terminate()

pygame.quit()
sys.exit()
