import pygame as pg
from button import Button
from sqlFunctions import *
from player import Player
from enemies import Boss, Skullie, Blob

pg.init()

# Create game window
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
WINDOW = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Helga')

# Load initial art assets
from art import *

# Create Buttons
NG_BUTTON = Button(350, 400, NEW_GAME)
C_BUTTON = Button(350, 480, CONTINUE)
O_BUTTON = Button(350, 560, OPTIONS)
LOAD1_BUTTON = Button(30, 35, LOAD_P1)
LOAD2_BUTTON = Button(30, 276, LOAD_P2)
LOAD3_BUTTON = Button(30, 521, LOAD_P3)

# Set framerate
clock = pg.time.Clock()
FPS = 30

# Create or load database for save files 
start_db() 

# Define player variables
join_size = 64
join_scale = 2
join_offset = [14, 15]
join_data = [join_size, join_scale, join_offset]
join_animation_steps = [1, 1, 1, 1, 1]

# Define enemy variables
blob_size = 32
skullie_size = 16
blob_scale = 4
skullie_scale = 8
blob_offset = [9, 10]
skullie_offset = [4, 7]
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
enemy_data = [empty_data, blob_data, skullie_data, boss_data]
enemy_animation_steps = [empty_animations, blob_animation_steps, skullie_animation_steps, boss_animation_steps]
enemy_spritesheets = [EMPTY_SPRITESHEET, BLOB_SPRITESHEET, SKULLIE_SPRITESHEET, BOSS_SPRITESHEET]
enemy_locations = [None, 2, 1, 0, 2, 0, 1, 2, 3, 1] # Blob is 1 [2, 6, 9] and Skullie is 2 [1, 4, 7]
defeated = [None, False, False, True, False, True, False, False, True, False]
loaded = [None, False, False, True, False, True, False, False, True, False]

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
    run, title, state, boss_defeated = True, True, "main_menu", False
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
            if NG_BUTTON.draw(WINDOW):
                print("New Game")
                state = "new_game"
            if C_BUTTON.draw(WINDOW):
                print("Continue")
                state = "continue"
            if O_BUTTON.draw(WINDOW):
                print("Options")
                state = "options"
            

        # Handle new game scenario
        if state == "new_game":
            WINDOW.blit(NEW_SAVE, (0, 0))
            saves = find_saves()

            # Detect save data
            if saves:
                number_of_saves = len(saves)
            else:
                print("Zero save data.")

            # Detect which save file to write on/over
            if LOAD1_BUTTON.draw(WINDOW):
                if not saves:
                    new_save()
                else:
                    replace_save(1)
                state = "main"
            if LOAD2_BUTTON.draw(WINDOW):
                if not saves:
                    new_save()
                else:
                    if number_of_saves > 1:
                        replace_save(2)
                    else:
                        new_save()
                state = "main"
            if LOAD3_BUTTON.draw(WINDOW):
                if not saves:
                    new_save()
                else:
                    if number_of_saves > 2:
                        replace_save(3)
                    else:
                        new_save()
                state = "main"
            new_game = True


        # Handle load game
        if state == "continue":
            WINDOW.blit(LOAD, (0, 0))
            if LOAD1_BUTTON.draw(WINDOW):
                load_data = load_file(1)
                state = "main"
            if LOAD2_BUTTON.draw(WINDOW):
                load_data = load_file(2)
                state = "main"
            if LOAD3_BUTTON.draw(WINDOW):
                load_data = load_file(3)
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
            blob = Blob(1, 200, 310, enemy_data, enemy_spritesheets, enemy_animation_steps, enemy_locations)
            skullie = Skullie(2, 200, 310, enemy_data, enemy_spritesheets, enemy_animation_steps, enemy_locations) 
            final_boss = Boss(3, 400, 100, enemy_data, enemy_spritesheets, enemy_animation_steps, enemy_locations)

        # When playing game
        if state == "playing":

            # Update environment
            current_tile = player_1.update_tiles(WINDOW, current_tile, TILE_LIST, SCREEN_WIDTH, SCREEN_HEIGHT)

            # Update player
            player_1.update_animations()
            player_1.draw(WINDOW)
            player_1.move(current_tile, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW, skullie, blob, final_boss) 
            draw_health_bar(player_1.health, 20, 20, 1)

            # Create enemies on this tile
            if not defeated[current_tile]:

                # Make more enemies if any are left after killing one
                if (not defeated[1] or not defeated[4] or not defeated[7]) and not loaded[current_tile]:
                    skullie = Skullie(2, 200, 310, enemy_data, enemy_spritesheets, enemy_animation_steps, enemy_locations)
                    loaded[current_tile] = True
                if (not defeated[2] or not defeated[6] or not defeated[9]) and not loaded[current_tile]: # Blob is enemy #1 [tiles 2, 6, 9] and Skullie is 2 [1, 4, 7]
                    blob = Blob(1, 200, 310, enemy_data, enemy_spritesheets, enemy_animation_steps, enemy_locations)
                    loaded[current_tile] = True


                # Handle updates of blob
                if current_tile in [2, 6, 9] and not defeated[current_tile]:
                    blob.update_animations()
                    blob.draw(WINDOW)
                    blob.move(current_tile, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW, player_1)
                    # And mark as dead
                    if not blob.defeated():
                        print("I'm dead blobby!")
                        print(current_tile)
                        defeated[current_tile] = True

                # Handle updates of Skullie
                if current_tile in [1, 4, 7] and not defeated[current_tile]:
                    skullie.update_animations()
                    skullie.draw(WINDOW)
                    skullie.move(current_tile, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW, player_1)
                    # And mark as dead
                    if not skullie.defeated():
                        print(current_tile)
                        print("Killing blow on skullie's head!")
                        defeated[current_tile] = True


            # Create boss battle
            if current_tile == 8 and not boss_defeated:
                final_boss.update_animations()
                final_boss.draw(WINDOW)
                final_boss.move(3, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW, player_1)
                draw_health_bar(final_boss.health, 110, 720, 2)
                if not final_boss.defeated():
                    boss_defeated = True


            # If victory
            if defeated[1] and defeated[2] and defeated[4] and defeated[6] and defeated[7] and defeated[9] and boss_defeated:
                draw_text('Victory!', victory_font, (255, 0, 0), int(SCREEN_WIDTH / 2 - 185), int(SCREEN_HEIGHT) / 3)
            if not player_1.defeated():
                draw_text('Game Over!', victory_font, (255, 0, 0), int(SCREEN_WIDTH / 2 - 300), int(SCREEN_HEIGHT) / 3)

            # # If loaded all tiles, but not defeated - FOR TESTING
            # if loaded[1] and loaded[2] and loaded[4] and loaded[6] and loaded[7] and loaded[9] and not (defeated[1] and defeated[2] and defeated[4] and defeated[6] and defeated[7] and defeated[9]):
            #     loaded[1] = defeated[1]
            #     loaded[2] = defeated[2]
            #     loaded[4] = defeated[4]
            #     loaded[6] = defeated[6]
            #     loaded[7] = defeated[7]
            #     loaded[9] = defeated[9]

        # Update screen
        pg.display.update()
    
    pg.quit()

if __name__ == "__main__":
    main()