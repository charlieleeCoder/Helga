import pygame as pg

class Player():
    def __init__(self, x, y, data, sprite_sheet, animation_steps): 
        self.flip = False
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0 = idle, etc.
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pg.time.get_ticks()   # or not?
        self.up, self.down, self.left, self.right = False, False, False, False
        self.attacking = False
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self._defeated = False
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

    def move(self, current_tile, screen_width, screen_height, surface, enemy_list, boss): # target variable needs adding back in
        SPEED = 15
        self.dx = 0
        self.dy = 0

        # get key presses
        key = pg.key.get_pressed()

        # Can only perform other actions if not attacking or dead
        if self.health <= 0:   
            self.health = 0   
            self._defeated = True   
            self.update_action(7)

        # If still alive
        if not self._defeated:

            # Movement
            if key[pg.K_a]:          
                self.dx = -SPEED
                self.left = True
                self.flip = True
                self.right, self.up, self.down = False, False, False
            elif key[pg.K_d]:
                self.dx = SPEED
                self.right = True
                self.flip = False
                self.left, self.up, self.down = False, False, False
            elif key[pg.K_w]:             
                self.dy = -SPEED
                self.up = True
                self.left, self.right, self.down = False, False, False
            elif key[pg.K_s]:
                self.dy = SPEED
                self.down = True
                self.left, self.right, self.up = False, False, False
            # Attack
            elif key[pg.K_SPACE]:
                if self.attack_cooldown == 0:
                    self.attacking = True
                    self.left, self.right = False, False
                    self.attack(current_tile, surface, enemy_list, boss)
                    # self.attack_type = 5
                    self.attack_cooldown = 22
            else:
                self.left, self.right, self.attacking = False, False, False
        

        # Ensure player stays within outer boundary
        if self.rect.left + self.dx < 0 and current_tile % 3 == 1:
            self.dx = 0 - self.rect.left
        if self.rect.right + self.dx > screen_width and current_tile % 3 == 0:
            self.dx = screen_width - self.rect.right
        if self.rect.bottom + self.dy > screen_height and current_tile < 4:
            self.dy = screen_height - self.rect.bottom
        if self.rect.top + self.dy < 0 and current_tile > 6:
            self.dy = 0 - self.rect.top

        # Update player position
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Apply attack cool down
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    # handle animation updates
    def update_animations(self):
        animation_cooldown =  100 # Time in miliseconds between frames
        self.image = self.animation_list[self.action][self.frame_index]

        # check what action the player is performing
        if self.left:
            self.update_action(2) 
        elif self.right: 
            self.update_action(2) 
        elif self.down and self.dy != 0:
            self.update_action(2) 
        elif self.up and self.dy != 0:
            self.update_action(2) 

        # Expand bitmap list for other animation cycles
        elif self.hit:
            self.update_action(5) # getting hit
        elif self.attacking:
            self.update_action(1) # attacking
        else:
            self.update_action(0) # 0:idle

        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
        # if the player is dead then end the animation_list
            if self._defeated ==  True:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                self.hit = False

    def attack(self, current_tile, surface, enemy_list, boss):     # pg.Rect((x, y, 64, 96))
        # Player orientation
        if self.up or self.down:
            self.y_tilt = True
        else:
            self.y_tilt = False
        fix_x_pos = self.left * 1.5 * self.rect.width # If facing left, start the hitbox further left (-x)
        fix_y_pos = self.up * 1.5 * self.rect.height + ((self.rect.centery - self.rect.y) / 2) # If facing up, start the hitbox further up (-y) and also don't start hitbox at top of sprite but 3/4
        
        # Horizontal versus vertical attacks
        narrow_attacks = self.y_tilt * self.rect.width
        tall_attacks = self.rect.height * self.y_tilt
        attacking_rect = pg.Rect(self.rect.centerx - fix_x_pos, self.rect.centery - fix_y_pos, 1.5 * self.rect.width - narrow_attacks, self.rect.height / 2 + tall_attacks)

        # Attack which target
        try:
            if attacking_rect.colliderect(enemy_list[current_tile].rect):
                enemy_list[current_tile].health -= 15
                enemy_list[current_tile].hit = True
                pg.draw.rect(surface, (0, 255, 0), attacking_rect)     
        except AttributeError: 
            pass
        # Deal with variable lag
        try:
            if attacking_rect.colliderect(boss.rect):
                boss.health -= 12
                boss.hit = True
                pg.draw.rect(surface, (0, 255, 0), attacking_rect)
        except AttributeError: 
            pass

    def update_action(self, new_action):
        # check if the new action is different to previous one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

    def draw(self, surface):
        img = pg.transform.flip(self.image, self.flip, False)
        # pg.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

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
            self._defeated = True
        return self._defeated


