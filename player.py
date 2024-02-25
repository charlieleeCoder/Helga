import pygame as pg

class Player():
    def __init__(self, x, y, data, sprite_sheet, animation_steps): 
        self.size = data[0]
        self.image_scale = data [1]
        self.offset = data [2]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0 = idle, etc.
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pg.time.get_ticks()   # or not?
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.attacking = False
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True
        self.rect = pg.Rect((x, y, 64, 96))
        self.current_tile = 3
        self.y_tilt = False

    def load_images(self, sprite_sheet, animation_steps):
        
        # extract images from sprite_sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pg.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, current_tile, screen_width, screen_height, surface, skullies, blobs, boss): # target variable needs adding back in
        SPEED = 15
        dx = 0
        dy = 0

        # get key presses
        key = pg.key.get_pressed()

        # Can only perform other actions if not attacking or dead
        if self.health <= 0:   
            self.health = 0   
            self.alive = False   
            # self.update_action(6)

        if not self.attacking and self.alive:

            # Check keyboard input
            if key[pg.K_a]:          # movement
                dx = -SPEED
                self.left = True
                self.right, self.up, self.down = False, False, False
            if key[pg.K_d]:
                dx = SPEED
                self.right = True
                self.left, self.up, self.down = False, False, False
            if key[pg.K_w]:             
                dy = -SPEED
                self.up = True
                self.left, self.right, self.down = False, False, False
            if key[pg.K_s]:
                dy = SPEED
                self.down = True
                self.left, self.right, self.up = False, False, False

            # Attack
            if key[pg.K_SPACE]:
                if self.attack_cooldown == 0:
                    self.attacking = True
                    self.attack(current_tile, surface, skullies, blobs, boss)
                    self.attack_type = 5
                    self.attack_cooldown = 22
            self.attacking = False

        # Ensure player stays within outer boundary
        if self.rect.left + dx < 0 and current_tile % 3 == 1:
            dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width and current_tile % 3 == 0:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height and current_tile < 4:
            dy = screen_height - self.rect.bottom
        if self.rect.top + dy < 0 and current_tile > 6:
            dy = 0 - self.rect.top

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

        # Apply attack cool down
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    # handle animation updates
    def update_animations(self):
        animation_cooldown =  100 # Time in miliseconds between frames
        self.image = self.animation_list[self.action][self.frame_index]

        # check what action the player is performing
        if self.left == True:
            self.update_action(2) # 1: left
        elif self.down == True:
            self.update_action(0) # 2: down
        elif self.up == True:
            self.update_action(1) # 3: up
        elif self.right == True: 
            self.update_action(3) # 4 right
        # elif self.hit == True:
            # self.update_action(5) # getting hit
        # elif self.attacking == True:
            # self.update_action(6) # attacking
        # else:
            # self.update_action(4) # 0:idle

        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
    # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
        # if the player is dead then end the animation_list
            if self.alive ==  False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                self.hit = False

    def attack(self, current_tile, surface, skullies, blobs, boss):     # pg.Rect((x, y, 64, 96))
        if self.up or self.down:
            self.y_tilt = True
        else:
            self.y_tilt = False
        fix_x_pos = self.left * 1.5 * self.rect.width # If facing left, start the hitbox further left (-x)
        fix_y_pos = self.up * 1.5 * self.rect.height + ((self.rect.centery - self.rect.y) / 2) # If facing up, start the hitbox further up (-y) and also don't start hitbox at top of sprite but 3/4
        narrow_attacks = self.y_tilt * self.rect.width
        tall_attacks = self.rect.height * self.y_tilt
        attacking_rect = pg.Rect(self.rect.centerx - fix_x_pos, self.rect.centery - fix_y_pos, 1.5 * self.rect.width - narrow_attacks, self.rect.height / 2 + tall_attacks)
        if current_tile == 1 and attacking_rect.colliderect(skullies[0].rect):
            skullies[0].health -= 15
            print("Ha!")
            skullies[0].hit = True
            pg.draw.rect(surface, (0, 255, 0), attacking_rect)
        if current_tile == 4 and attacking_rect.colliderect(skullies[1].rect):
            skullies[1].health -= 15
            print("Ha!")
            skullies[1].hit = True
            pg.draw.rect(surface, (0, 255, 0), attacking_rect)
        if current_tile == 7 and attacking_rect.colliderect(skullies[2].rect):
            skullies[2].health -= 15
            print("Ha!")
            skullies[2].hit = True
            pg.draw.rect(surface, (0, 255, 0), attacking_rect)
        if current_tile == 2 and attacking_rect.colliderect(blobs[0].rect):
            blobs[0].health -= 15
            print("Ha!")
            blobs[0].hit = True
            pg.draw.rect(surface, (0, 255, 0), attacking_rect)       
        if current_tile == 6 and attacking_rect.colliderect(blobs[1].rect):
            blobs[1].health -= 15
            print("Ha!")
            blobs[1].hit = True
            pg.draw.rect(surface, (0, 255, 0), attacking_rect)     
        if current_tile == 9 and attacking_rect.colliderect(blobs[2].rect):
            blobs[2].health -= 15
            print("Ha!")
            blobs[2].hit = True
            pg.draw.rect(surface, (0, 255, 0), attacking_rect)     
        if attacking_rect.colliderect(boss.rect):
            boss.health -= 15
            print("Ha!")
            boss.hit = True
            pg.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        # check if the new action is different to previous one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

    def draw(self, surface):
        # pg.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(self.image, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def update_tiles(self, WINDOW, current_tile, TILE_LIST, SCREEN_WIDTH, SCREEN_HEIGHT):
        tilename = TILE_LIST[(current_tile)]
        WINDOW.blit(tilename, (0,0))
        if self.rect.x > SCREEN_WIDTH and current_tile % 3 != 0:
            current_tile += 1
            self.rect.x = 10
        elif self.rect.x < 0 and current_tile % 3 != 1:
            current_tile -= 1
            self.rect.x = SCREEN_WIDTH - 10
        if self.rect.y > SCREEN_HEIGHT and current_tile > 3:
            current_tile -= 3
            self.rect.y = 10
        elif self.rect.y < 0 and current_tile < 7:
            current_tile += 3
            self.rect.y = SCREEN_HEIGHT - 10
        return current_tile

    def defeated(self):
        if self.health <= 0:
            self.alive = False
            # print("Noooo!")
        return self.alive


