import pygame
import random
from tkinter import messagebox

# Initialize Pygame
pygame.init()

# Define colors
color_white = (255, 255, 255)
color_black = (0, 0, 0)

# Define the window size
window_width = 800
window_height = 800
rows = 6  # creating a 6x6 matrix with rows and columns
columns = 6
card_width = window_width // columns
card_height = window_height // rows

# Create the screen
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Virtual Matching Game")

# Define the font
font = pygame.font.Font(None, 60)

# Load the images from the "Images_vmg" folder
def load_images():
    images = []
    for i in range(1, 19):
        img = pygame.image.load(f"Images_vmg/{i}.jpg")
        img = pygame.transform.scale(img, (card_width, card_height))
        images.append(img)
    images *= 2  # duplicate the images to create pairs
    random.shuffle(images)
    return images

# Create a class for the cards to use
class Card:
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect
        self.flipped = False
        self.matched = False

# Create the cards
def create_cards(images):
    cards = []
    for row in range(rows):
        for col in range(columns):
            x = col * card_width  # calculate the x position
            y = row * card_height  # calculate the y position
            rect = pygame.Rect(x, y, card_width, card_height)  # create a rectangle for the card
            card = Card(images.pop(), rect)
            cards.append(card)
    return cards

# Draw the grid of cards
def draw_cards(cards):
    for card in cards:
        if card.flipped or card.matched:
            screen.blit(card.image, card.rect)  # display the card image
        else:
            pygame.draw.rect(screen, color_white, card.rect)  # draw a white rectangle
            pygame.draw.rect(screen, color_black, card.rect, 2)  # draw a black border around the rectangle

# Draw the buttons for playing and quitting, defining their sizes
def draw_button(text, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)  # create the button rectangle
    pygame.draw.rect(screen, color_black, button_rect)
    text_surface = font.render(text, True, color_white)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return button_rect

# Main game loop
def game_loop():
    images = load_images()
    cards = create_cards(images)
    running = True
    selected_cards = []
    matched_pairs = 0
    clock = pygame.time.Clock()
    show_time = 1000  # time in milliseconds to show the cards
    flip_time = None  # time to flip the cards

    while running:
        screen.fill(color_black)
        
        # Instructions to handle the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # exit the loop
            elif event.type == pygame.MOUSEBUTTONDOWN and flip_time is None:
                pos = pygame.mouse.get_pos()  # get the mouse position
                for card in cards:
                    if card.rect.collidepoint(pos) and not card.flipped and len(selected_cards) < 2:
                        card.flipped = True  # flip the card
                        selected_cards.append(card)  # add the card to the selected list
                        if len(selected_cards) == 2:
                            if selected_cards[0].image != selected_cards[1].image:
                                flip_time = pygame.time.get_ticks() + show_time  # control the flip time
                            else:
                                selected_cards[0].matched = True  # mark the card as matched
                                selected_cards[1].matched = True
                                selected_cards = []  # reset the selected list
                                matched_pairs += 1  # increment the pair count

        # Flip cards if not a match after showing for a time
        if flip_time and pygame.time.get_ticks() >= flip_time:
            for card in selected_cards:
                card.flipped = False  # flip the cards
            selected_cards = []  # reset the list
            flip_time = None  # reset the flip time

        draw_cards(cards)
        pygame.display.update()  # update the screen

        # Show message when all pairs are found
        if matched_pairs == 18:
            messagebox.showinfo('You Won', 'Congratulations, your memory is extraordinary!')
            return True

        clock.tick(30)

# Start screen
def start_screen():
    running = True
    while running:
        screen.fill(color_white)  # fill the screen with white
        play_button = draw_button("Play", window_width // 2 - 100, window_height // 2 - 90, 200, 60)  # draw the play button
        quit_button = draw_button("Quit", window_width // 2 - 100, window_height // 2 + 10, 200, 60)  # draw the quit button
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # exit the loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    if not game_loop():
                        running = False
                elif quit_button.collidepoint(event.pos):
                    running = False

        pygame.display.update()
    pygame.quit()

# Run the game
if __name__ == "__main__":
    start_screen()
