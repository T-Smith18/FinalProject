"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
From:
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
 
Explanation video: http://youtu.be/BCxWJgN4Nnc
 
"""
#Week 1: Created Project Proposal
# Week 2: Made jumping circle
# Week 3: Swapped template to one more suitable for project,read and broke and undid different parts, figured out how to use custom graphics 
import pygame
from constants import *

class Game:
    def __init__(self):
        # initialize program
        pygame.init()
        self.size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Boss Fight")
        self.clock = pygame.time.Clock()
        self.load_data()
        self.running = True

    def load_data(self):
        # Load data files
        self.background = pygame.image.load("FinalProject/resources/graphics/Forestbg.png")
        self.spritesheet = Spritesheet("FinalProject/resources/graphics/Hero.gif")
        self.ghostsprites = Spritesheet("FinalProject/resources/graphics/ghost.png")
    
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    
    def new(self):
        # Start a new game
        # Add empty sprite lists 
        self.active_sprite_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.boss_list = pygame.sprite.Group()
        
        # Add Player and Boss
        self.player = Player(self, 340, SCREEN_HEIGHT)
        self.active_sprite_list.add(self.player)
        self.boss = Boss(self, 800, SCREEN_HEIGHT)
        self.active_sprite_list.add(self.boss)
        self.boss_list.add(self.boss)

        #Add Health Bar
        self.player_hp = Health(self, 15, 15, 30)
        self.active_sprite_list.add(self.player_hp)

        # Add platforms        #(height, width, x, y)
        platform = Platform(210, 20,   0, 530)
        self.active_sprite_list.add(platform)
        self.platform_list.add(platform)
        platform = Platform(210, 20, 200, 400)
        self.active_sprite_list.add(platform)
        self.platform_list.add(platform)
        platform = Platform(210, 20, 600, 300)
        self.active_sprite_list.add(platform)
        self.platform_list.add(platform)
        self.run()
    
    def update(self):
        # Game Loop - Update
        self.active_sprite_list.update()
        self.player.update()
        self.player_hp.track_health()
    
    def events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.go_left()
                if event.key == pygame.K_d:
                    self.player.go_right()
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_p:
                    #disables attacking while running or jumping
                    if self.player.running == True or self.player.jumping == True:
                        pass
                    else:
                        self.player.go_punch()

 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_d and self.player.change_x > 0:
                    self.player.stop()
                if event.key ==pygame.K_p:
                     self.player.stop_punch()


    
    def draw(self):
        # Game Loop - Draw
        self.screen.blit(self.background, (0, 0))
        self.active_sprite_list.draw(self.screen)
        pygame.display.flip()

    def show_start_screen(self):
        # Show start screen
        pass

    def show_game_over_screen(self):
        # Show game over screen
        pass

class Spritesheet:
    # Class for loading and parsing sprite sheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename)

    def get_image(self, x, y, width, height):
        # Grab an image out of a larger sprite sheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # Call the parent's constructor
        super().__init__()
       
        # Creates Player image
        self.game = game 
        
        self.running = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames[self.current_frame]
        self.change_x = 0
        self.change_y = 0
        self.punching = False
        self.attack = 50
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        if y > SCREEN_HEIGHT - self.rect.height:
            y = SCREEN_HEIGHT - self.rect.height
        self.rect.y = y
    
    #this is a function for storing the positions of a sprite
    #within a spritesheet
    def load_images(self):
        # (x,y,height of sprite, width of sprite)
        self.idle_frames = [self.game.spritesheet.get_image(  0, 0, 46, 50)]
        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
        self.run_frames_r = [self.game.spritesheet.get_image(0, 150, 46, 50),
                             self.game.spritesheet.get_image(46, 150, 46, 50),
                             self.game.spritesheet.get_image(92, 150, 46, 50),
                             self.game.spritesheet.get_image(138,  150, 46, 50),
                             self.game.spritesheet.get_image(  184, 150, 46, 50),
                             self.game.spritesheet.get_image( 230, 150, 46, 50),
                             self.game.spritesheet.get_image(276, 150, 46, 50),
                             self.game.spritesheet.get_image(322, 150, 46, 50)]
        self.run_frames_l = []
        for frame in self.run_frames_r:
            frame.set_colorkey(BLACK)
            self.run_frames_l.append(pygame.transform.flip(frame,True,False))
        self.jump_frames = [self.game.spritesheet.get_image(276, 0, 46, 50)]
        for frame in self.jump_frames:
            frame.set_colorkey(BLACK)
        self.punching_frames = [self.game.spritesheet.get_image(92,0,46,50),
                                self.game.spritesheet.get_image(138,0,46,50),
                                self.game.spritesheet.get_image(184,0,46,50),
                                self.game.spritesheet.get_image(230,0,46,50)]
        for frame in self.punching_frames:
            frame.set_colorkey(BLACK)
 
    def update(self):
        # Gravity
        self.calc_grav()

        if self.change_x == 0 or self.jumping == True:
            self.running = False
        else:
            self.running = True

        # Move left/right
        self.rect.x += self.change_x
        
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH
            
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.game.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.game.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
            self.jumping = False
        if self.change_y == 0:
            self.jumping = False

        self.animate()
        
 
    def animate(self):
        now = pygame.time.get_ticks()
        if self.punching:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.punching_frames)
                bottom = self.rect.bottom
                self.image =self.punching_frames[self.current_frame]
                self.rect.bottom = bottom
        if self.running:
            if now - self.last_update > 70:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_frames_l)
                bottom = self.rect.bottom
                if self.change_x > 0:
                    self.image = self.run_frames_r[self.current_frame]
                else:
                    self.image = self.run_frames_l[self.current_frame]
                self.rect.bottom = bottom
        elif not self.jumping:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect.bottom = bottom
        else:
            if now - self.last_update > 300:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
                bottom = self.rect.bottom
                self.image = self.jump_frames[self.current_frame]
                self.rect.bottom = bottom
 
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.game.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
            self.jumping = True
 
    # Player-controlled movement:
    def go_left(self):
        self.change_x = -5
 
    def go_right(self):
        self.change_x = 5
 
    def stop(self):
        self.change_x = 0
    def go_punch(self):
        self.punching = True
    def stop_punch(self):
        self.punching = False

class Health(pygame.sprite.Sprite):
    #health bar constructor class, made by me
    def __init__(self, game, x, y, hp):
        super().__init__()
        self.image = pygame.image.load("FinalProject/resources/graphics/Hearts/6.png")
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.game = game
        self.hp =hp
    def track_health(self):
        if self.hp < 1:
            self.image = pygame.image.load("FinalProject/resources/graphics/Hearts/0.png")
        elif self.hp < 5:
            self.image = pygame.image.load("FinalProject/resources/graphics/Hearts/1.png")
        elif self.hp < 10:
            self.image = pygame.image.load("FinalProject/resources/graphics/Hearts/2.png")
        elif self.hp < 15:
            self.image = pygame.image.load("FinalProject/resources/graphics/Hearts/3.png")


            

        



class Boss(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.load_images()
        self.current_frame = 0
        self.last_update = 0
        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        if y > SCREEN_HEIGHT - self.rect.height:
            y = SCREEN_HEIGHT - self.rect.height
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
        self.health = 1000
        self.running  = False
        self.jumping = False
        
    #this is a function for storing the positions of a sprite
    #within a spritesheet
    def load_images(self):
        # (x,y,height of sprite, width of sprite)
        self.idle_frames = [self.game.ghostsprites.get_image(  0, 128, 48, 64),
                            self.game.ghostsprites.get_image(  48,128, 48, 64),
                            self.game.ghostsprites.get_image(  96, 128, 48, 64)]
        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
        self.run_frames_r = [self.game.spritesheet.get_image(0, 64, 48, 64),
                             self.game.spritesheet.get_image(48, 64, 48, 643),
                             self.game.spritesheet.get_image(96, 64, 48, 64),]
        self.run_frames_l = []
        for frame in self.run_frames_r:
            frame.set_colorkey(BLACK)
            self.run_frames_l.append(pygame.transform.flip(frame,True,False))
        self.jump_frames = [self.game.spritesheet.get_image(276, 0, 46, 50)]
        for frame in self.jump_frames:
            frame.set_colorkey(BLACK)
        
    def animate(self):
        now = pygame.time.get_ticks()
        if self.running:
            if now - self.last_update > 70:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_frames_l)
                bottom = self.rect.bottom
                if self.change_x > 0:
                    self.image = self.run_frames_r[self.current_frame]
                else:
                    self.image = self.run_frames_l[self.current_frame]
                self.rect.bottom = bottom
        elif not self.jumping:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect.bottom = bottom
        else:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
                bottom = self.rect.bottom
                self.image = self.jump_frames[self.current_frame]
                self.rect.bottom = bottom
    def update(self):
        # Gravity
        #self.calc_grav()

        if self.change_x == 0 or self.jumping == True:
            self.running = False
        else:
            self.running = True

        # Move left/right
        self.rect.x += self.change_x
        
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH
            
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        self.animate()

            

class Platform(pygame.sprite.Sprite):
    #platform constructor class
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
def main():
    #the main loop
  
    game = Game()

    game.show_start_screen()
    while game.running:
        game.new()
        game.show_game_over_screen()
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()