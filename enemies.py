import pygame as pg

class Enemy():
    def __init__(self, enemy_type, x, y, data, sprite_sheet, animation_steps, enemy_locations): 
        self.enemy_type = enemy_type
        self.size = data[self.enemy_type][0]
        self.image_scale = data[self.enemy_type][1]
        self.offset = data[self.enemy_type][2]
        self.animation_list = self.load_images(sprite_sheet[self.enemy_type], animation_steps[self.enemy_type])
        self.action = 0 # 0 = idle, etc.
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pg.time.get_ticks()   # or not?
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.attacking = False
        self.hit = False
        self.health = 50
        self.alive = True
        self.rect = pg.Rect((x, y, 64, 64))
        self.loop = 0
        self.attack_cooldown = 0


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

    def move(self, current_tile, screen_width, screen_height, surface, target): # target variable needs adding in
        SPEED = 20
        dx = 0
        dy = 0
        # print(self.health)

        # Can only perform other actions if not attacking or dead
        if self.health <= 0:   
            self.health = 0   
            print("This cruel world!") 
        #     self.defeated(current_tile)  

        if not self.attacking and self.alive:
            # Check keyboard input
            if self.loop == 0:          # movement
                dx = -SPEED
                self.left = True
                self.right, self.up, self.down = False, False, False
            if self.loop == 4:
                dx = SPEED
                self.right = True
                self.left, self.up, self.down = False, False, False
            if self.loop == 8:             
                dy = -SPEED
                self.up = True
                self.left, self.right, self.down = False, False, False
            if self.loop == 12:
                dy = SPEED
                self.down = True
                self.left, self.right, self.up = False, False, False

            # Attack
            if self.health != 50 and self.health != 200:
                if self.attack_cooldown == 0:
                    self.attacking = True
                    self.attack(surface, target)
                    self.attack_cooldown = 22

        # Ensure enemy stays within outer boundary
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

        # Apply loop of actions
        if self.loop < 16:
            self.loop += 1
        else:
            self.loop = 0

        # handle animation updates
    def update_animations(self):
        animation_cooldown =  100 # Time in miliseconds between frames
        self.image = self.animation_list[self.action][self.frame_index]

        # check what action the player is performing
        # if self.left == True:
            # self.update_action(2) # 1: left
        if self.down == True and self.attacking == False:
            self.update_action(0) # 2: down
        # elif self.up == True:
            # self.update_action(1) # 3: up
        # elif self.right == True: 
            # self.update_action(3) # 4 right
        # elif self.hit == True:
            # self.update_action(5) # getting hit
        if self.attacking == True:
            self.update_action(1) # attacking
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

    def update_action(self, new_action):
        # check if the new action is different to previous one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

    def draw(self, surface):
        if self.alive:
            # pg.draw.rect(surface, (255, 0, 0), self.rect)
            surface.blit(self.image, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def defeated(self):
        if self.health <= 0:
            self.alive = False
            # print("Gaaahh!")
        else:
            self.alive = True
        return self.alive

    def attack(self, surface, target):     # pg.Rect((x, y, 64, 96))
        if self.up or self.down:
            self.y_tilt = True
        else:
            self.y_tilt = False
        fix_x_pos = self.left * 1.5 * self.rect.width # If facing left, start the hitbox further left (-x)
        fix_y_pos = self.up * 1.5 * self.rect.height + ((self.rect.centery - self.rect.y) / 2) # If facing up, start the hitbox further up (-y) and also don't start hitbox at top of sprite but 3/4
        narrow_attacks = self.y_tilt * self.rect.width / 2
        tall_attacks = self.rect.height * self.y_tilt
        attacking_rect = pg.Rect(self.rect.centerx - fix_x_pos, self.rect.centery - fix_y_pos, 1.5 * self.rect.width - narrow_attacks, self.rect.height / 2 + tall_attacks)
        if attacking_rect.colliderect(target.rect):
            target.health -= 8
            print("Gotcha!")
            target.hit = True
            pg.draw.rect(surface, (0, 255, 0), attacking_rect)

class Blob(Enemy):
    def __init__(self, enemy_type, x, y, data, sprite_sheet, animation_steps, enemy_locations):
        super().__init__(enemy_type, x, y, data, sprite_sheet, animation_steps, enemy_locations)
        self.health = 50
        self.alive = True
        self.enemy_type = 1
        self.image_scale = data[1][1]
        self.offset = data[1][2]
        self.animation_list = self.load_images(sprite_sheet[1], animation_steps[1])

class Skullie(Enemy):
    def __init__(self, enemy_type, x, y, data, sprite_sheet, animation_steps, enemy_locations):
        super().__init__(enemy_type, x, y, data, sprite_sheet, animation_steps, enemy_locations)
        self.health = 50
        self.alive = True
        self.enemy_type = 2
        self.image_scale = data[1][1]
        self.offset = data[2][2]
        self.animation_list = self.load_images(sprite_sheet[2], animation_steps[2])

class Boss(Enemy):
    def __init__(self, enemy_type, x, y, data, sprite_sheet, animation_steps, enemy_locations):
        super().__init__(enemy_type, x, y, data, sprite_sheet, animation_steps, enemy_locations)
        self.health = 200
        self.rect = pg.Rect((x, y, 192, 192))
        self.enemy_type = 3
        self.image_scale = data[3][1]
        self.offset = data[3][2]
        self.animation_list = self.load_images(sprite_sheet[3], animation_steps[3])



