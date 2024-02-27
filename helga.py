# Required modules
import pygame as pg
from button import Button
from sqlFunctions import *
from player import Player
from enemies import Boss, Skullie, Blob
from random import choice, randint

# Start PyGame
pg.init()

# Create game window
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
WINDOW = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Helga')

# Load initial art assets
from art import *

# Create Buttons
NG_BUTTON = Button(350, 400, NEW_GAME, 'new_game')
C_BUTTON = Button(350, 480, CONTINUE, 'continue')
O_BUTTON = Button(350, 560, OPTIONS, 'options')
BUTTONS = [NG_BUTTON, C_BUTTON, O_BUTTON]

# Manage saves
LOAD1_BUTTON = Button(30, 35, LOAD_P1)
LOAD2_BUTTON = Button(30, 276, LOAD_P2)
LOAD3_BUTTON = Button(30, 521, LOAD_P3)
LOADS = [LOAD1_BUTTON, LOAD2_BUTTON, LOAD3_BUTTON]

# Set framerate
clock = pg.time.Clock()
FPS = 30

# Create or load database for save files 
start_db() 

# Define player variables
join_size = 56
join_scale = 4 
join_offset = [20,26] # [14, 15]
join_data = [join_size, join_scale, join_offset]
join_animation_steps = [6, 8, 8, 8, 8, 4, 8, 4, 8, 3, 3]

# Define enemy size variables
blob_size = 32
blob_scale = 4
skullie_scale = 8
skullie_size = 16

# Adjust pixel overlay
blob_offset = [9, 10]
skullie_offset = [4, 7]

# Establish variables to pass to instance
blob_data = [blob_size, blob_scale, blob_offset]
skullie_data = [skullie_size, skullie_scale, skullie_offset]
blob_animation_steps = [4, 4]
skullie_animation_steps = [4, 4]

# Define boss variables
boss_size = 32
boss_scale = 8
boss_offset = [4, 5]
boss_data = [boss_size, boss_scale, boss_offset]
boss_animation_steps = [4, 5]

# Empty 
empty_size, empty_scale = 32, 1
empty_offset = [0, 0]
empty_animations = [1]
empty_data = [empty_size, empty_scale, empty_offset]

# Enemy grouped variables
enemy_data = [blob_data, skullie_data, boss_data]
enemy_animation_steps = [blob_animation_steps, skullie_animation_steps, boss_animation_steps]
enemy_spritesheets = [BLOB_SPRITESHEET, SKULLIE_SPRITESHEET, BOSS_SPRITESHEET]

# Create random enemy locations in tiles 1-9
defeated = [choice([0, 1]) for _ in range(10)]
defeated[0] = 1

# Define font
victory_font = pg.font.Font('Fonts\RockwellNova.ttf', 100)

# Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    WINDOW.blit(img, (x, y))

# Create Player
player_1 = Player(200, 310, join_data, JOIN_SPRITESHEET, join_animation_steps) # Tweak animation deets as new ones are added

# Update Screen
def draw_window():
    WINDOW.fill(255, 255, 255)

# Update Screen 
def load_tile(tile, TILE_LIST):
    tilename = TILE_LIST[(tile)]
    WINDOW.blit(tilename, (0,0))

# function for drawing health bar
def draw_health_bar(health, x, y, multiplier):
    ratio = health / 100
    pg.draw.rect(WINDOW, (0, 0, 0), (x - 2, y - 2, 400 * multiplier + 6, 36))
    pg.draw.rect(WINDOW, (255, 0, 0), (x, y, 400 * multiplier, 30))
    pg.draw.rect(WINDOW, (0, 255, 0), (x, y, 400 * ratio, 30))

# Game loop
def main():
    run, title, state, boss_defeated, potion = True, True, "main_menu", False, True
    while run:
        
        # Implement number of refreshes a second
        clock.tick(FPS)

        # Check for window being closed and close title screen with spacebar
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    title = False

        # While on title screen
        if title:
            WINDOW.blit(TITLE, (0, 0))

        # Handle main menu screen
        elif state == "main_menu": 
            WINDOW.blit(MENU, (0, 0))
            for button in BUTTONS:
                if button.draw(WINDOW):
                    state = button.state

        # Handle new game scenario
        if state == "new_game":
            WINDOW.blit(NEW_SAVE, (0, 0))
            saves = find_saves()

            # Detect save data
            if saves:
                number_of_saves = len(saves)
            else:
                number_of_saves = 0

            # Detect which save file to write on/over
            for index, save_slot in enumerate(LOADS):
                if save_slot.draw(WINDOW):
                    if not saves:
                        new_save()
                    elif number_of_saves > index:
                        replace_save(index+1)
                    else:
                        new_save()
                    state = "main"
                    new_game = True

        # Handle load game
        if state == "continue":
            WINDOW.blit(LOAD, (0, 0))
            for index, load_button in enumerate(LOADS):
                if load_button.draw(WINDOW):
                    load_data = load_file(index+1)
                    state = "main"
                    new_game = False

        # Handle options
        if state == "options":  
            draw_window()     

        # Else draw main game
        if state == "main":
            if new_game == True:
                current_tile = 3
                load_tile(current_tile, TILE_LIST)
                state = "playing"
            else:
                current_tile = load_data[0][2]
                load_tile(current_tile, TILE_LIST)
                state = "playing"
            
            #Create enemy instances
            enemy_choice = [Blob, Skullie]
            enemy_list = []
            for tile in defeated:
                if tile == 0:
                    enemy_list.append(choice(enemy_choice)(200, 310, enemy_data, enemy_spritesheets, enemy_animation_steps))
                else:
                    enemy_list.append(None)
            final_boss = Boss(400, 100, enemy_data, enemy_spritesheets, enemy_animation_steps)

            # Potion 
            potion_location = randint(1,9)

        # When playing game
        if state == "playing":

            # Update environment
            current_tile = player_1.update_tiles(WINDOW, current_tile, TILE_LIST, SCREEN_WIDTH, SCREEN_HEIGHT)

            # Update player
            player_1.update_animations()
            player_1.draw(WINDOW)
            player_1.move(current_tile, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW, enemy_list, final_boss) 
            draw_health_bar(player_1.health, 20, 20, 1)

            # Handle updates of enemies
            if defeated[current_tile] == 0 and enemy_list[current_tile]:
                enemy_list[current_tile].update_animations()
                enemy_list[current_tile].draw(WINDOW)
                enemy_list[current_tile].move(current_tile, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW, player_1)
                # And mark as dead
                if enemy_list[current_tile].defeated():
                    defeated[current_tile] = 1

            # Create one-off potion 
            if current_tile == potion_location and potion == True:
                potion_rect = pg.Rect((400, 300, 64, 64)) # x, y, x_size, y_size
                # pg.draw.rect(WINDOW, (0, 255, 0), potion_rect) # Testing for allignment
                WINDOW.blit(POTION, (400, 300))
                if potion_rect.colliderect(player_1.rect):
                    player_1.health += 30
                    potion = False
                    if player_1.health > 100:
                        player_1.health = 100

            # Create boss battle
            defeated_total = 0
            for tile in defeated:
                defeated_total += tile
            if defeated_total >= 8 and not boss_defeated and current_tile == 8:
                final_boss.update_animations()
                final_boss.draw(WINDOW)
                final_boss.move(3, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW, player_1)
                draw_health_bar(final_boss.health, 110, 720, 2)
                if final_boss.defeated():
                    boss_defeated = True

            # If victory
            if boss_defeated:
                draw_text('Victory!', victory_font, (255, 0, 0), int(SCREEN_WIDTH / 2 - 185), int(SCREEN_HEIGHT) / 3)
            if player_1.defeated():
                draw_text('Game Over!', victory_font, (255, 0, 0), int(SCREEN_WIDTH / 2 - 300), int(SCREEN_HEIGHT) / 3)

        # Update screendddd
        pg.display.update()
    
    pg.quit()

if __name__ == "__main__":
    main()