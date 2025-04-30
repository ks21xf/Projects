#CREDIT to ClearCode and this youtube video to help learn PyGame - https://www.youtube.com/watch?v=8OMghdHP-zs&t=926s
import pygame
from os.path import join
import random
from time import sleep
class Player(pygame.sprite.Sprite):
    def __init__(self,groups):                                                              #pass in group you want sprite to be attached to
        super().__init__(groups)
        #keep the original surface for the rotation, self.image will be the rotated image
        self.original_surf = pygame.image.load(join('images','player.png')).convert_alpha() #use the join function from os to make a path. convert_alpha converts the png into something easier to render. the convert_alpha includes the transparent pixels 
        self.image = self.original_surf
        self.rect =  self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))        # this is a rectangle that wraps around player_surf. Its easier to interact with rectangles (you have things like topleft, center, etc) and they are used for collision detection and positioning while surfaces are usually used to store pixel information of images
                                                                                            #player_rect = player_surf.get_rect(center = (0,0)) - this places the center of the player_rect at 0,0
        self.direction = pygame.math.Vector2(0,0)                                           #2d vector. vectors useful for scalar mult and vector addition that lists dont provide. the first entry is x, the second is y
        self.speed = 300

        #cooldown for shooting
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400 #ms

        # transform
        self.rotation = 0

        #masks are used to get pixel perfect collisons by turning overlayed/invisible pixels black and visible pixels white - masks figure out which portion of an image is visible
        #we can use masks  to get better collisions by checking if the visible portions of the masks of objects collide (see the collisions list in collisions fuction)
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self): #checks if we can fire the laser again by getting the current time and checking the if the difference between that and the laser fire time (which is the time that we fired the last lazer) is, and if it is long enough we can fire the laser again
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() #amount of time elasped in ms since beginning of game (pygame.init())
            if current_time - self.laser_shoot_time >=self.cooldown_duration: 
                self.can_shoot =True

    def update(self,dt):                                                                       #when you call update from all_sprites, this method runs. so this method has the updates for the player
        keys = pygame.key.get_pressed()                                                     #pygame.key different than event.key since pygame.py checks if a button is being pressed or not while event.key checks if the action of pressing a key has happened
                                                                                            #player_direction.x = int(keys[pygame.K_RIGHT]) #pygame.K_RIGHT is true (1) when it is being pressed and false (0) otherwise. so setting the direction equal to that will give us the desired movement
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])             #logic is that if moving right, left isn't pressed, so that is 1-0, if w moving left and not right, thats 0-1, moving -1 in x direction
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        #any vector in an if statement in pygame will be false if the vector is [0,0], so any other value will return true. that means the else statement
        self.direction = self.direction.normalize() if self.direction else self.direction   #this is done because moving diagonally makes us move faster because we have the vector (1,1) when moving diagonally and the hypotenuse is going to be >1. to fix this, we normalize the vector so the hypotenuse, or the direction the player will actually travel, will be =1
        self.rect.center += self.direction * self.speed * dt 

        recent_keys = pygame.key.get_just_pressed()                                         # a slower version of get_pressed needed so the player doesn't fire a million lasers
        if (recent_keys[pygame.K_SPACE]) and self.can_shoot:                                                   #this fires only once
            #fire laster
            Laser(laser_surf,self.rect.midtop,(all_sprites,laser_sprites)) #pass laser_surf so we dont create it every tiem a player fires a laser, place it at the midtop of the palyer, and pass in the all sprites and laser sprites groups 
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play() 

        self.laser_timer() 

        #continuous rotation
        #self.rotation += 1 *dt
        #self.image = pygame.transform.rotozoom(self.original_surf,self.rotation,1) #rotozoom is replacing .rotate in order to get a less choppy rotate. if it looks worse, switch to .rotate

class Star(pygame.sprite.Sprite):
    def __init__(self,groups,star_surf):                                                              #pass in group you want sprite to be attached to
        super().__init__(groups) 
        self.image = star_surf
        self.rect = self.image.get_frect(center = (random.randint(0,WINDOW_WIDTH),random.randint(0,WINDOW_HEIGHT)))
    
class Laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

        #mask 
        self.mask = pygame.mask.from_surface(self.image)


    def update(self,dt): #move laser
        self.rect.centery -= 400 *dt
        if self.rect.bottom < 0: #delete any lasers that go out of bounds. if laser is above the window and not visible
            self.kill() #remove laser sprite

class Meteor(pygame.sprite.Sprite):
        def __init__(self,surf,pos,groups):
            super().__init__(groups)
            self.spawn_time = pygame.time.get_ticks()
            self.original_surf = surf
            self.image = surf
            self.rect = self.image.get_frect(center =pos)
            self.can_destroy_meteor = False
            self.spawn_duration = 2000
            self.direction = pygame.Vector2(random.uniform(-0.5,0.5),1) #always want y to be one so they fall down at same speed. make x a random fp number between -0.5 and 0.5
            self.speed = random.randint(400,500)
            self.rotation_speed = random.randint(50,150)

            #mask 
            self.mask = pygame.mask.from_surface(self.image) 

            # transform
            self.rotation = 0

        def meteor_timer(self):
            if not self.can_destroy_meteor:
                current_time = pygame.time.get_ticks() #amount of time elasped in ms since beginning of game (pygame.init())
                if current_time - self.spawn_time >=self.spawn_duration: 
                    self.can_destroy_meteor =True

        def update(self,dt):
            self.rect.center += dt * self.direction * self.speed
            if self.can_destroy_meteor:
                self.kill()
            self.meteor_timer()

            self.rotation +=  self.rotation_speed*dt
            self.image = pygame.transform.rotozoom(self.original_surf,self.rotation,1) #rotozoom is replacing .rotate in order to get a less choppy rotate. if it looks worse, switch to .rotate. we also need a 1 as argument for rotozoom to keep something constant idk
            self.rect = self.image.get_frect(center =self.rect.center) #helps the meteors move more naturally by replacing the rect in the image to the center of the previous rectangle

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups): #frames is a list of surfaces.
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index] #first image of frames
        self.rect = self.image.get_frect(center = pos)

    def update(self,dt):
        self.frame_index +=20 * dt #reason why we still use dt is to keep frame independence.
        if self.frame_index <len(self.frames):
            self.image = self.frames[int(self.frame_index)] #this basically plays the images one after the other. the modulo is there to be safe
        else:
            self.kill() # dont forget to kill the sprite!
             
def collisions() :
    global running #make running a global varaible
    #check if a meteor hit the player
    collisions = pygame.sprite.spritecollide(player,meteor_sprites,False,pygame.sprite.collide_mask) #3 arguments here is the single sprite, second argument is a group of sprites, third arguments is dokill, basically if any sprite from the group sprite collides with the single sprite, does the group sprite die (boolean value). last argument is what gives us pixel perfect collision between two masks. that function also automatically makes the masks from stratch, so we dont need to define self.mask anywhere!
    if collisions:
        damage_sound.play()
        game_music.stop()
        sleep(0.5)
        running = False

    #check if any lasers collided with meteors
    for laser in laser_sprites: # what this does is check if any of the laser sprites collided with any of the meteor sprites 
        collisions = pygame.sprite.spritecollide(laser,meteor_sprites,True)
        if collisions: #if there was a collision delete laser
            laser.kill()
            AnimatedExplosion(explosion_frames,laser.rect.midtop,all_sprites) #start an explosion class from the top of the laser 
            explosion_sound.play()

def display_score():
    current_time = int(pygame.time.get_ticks()/100)
    text_surf = font.render(str(current_time),True,(240,240,240)) #create a surface. arguments: whatever  you want to render as text, antialias, which means smoothing out edges of a surface (dont do for pixel art), finally color is last
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT-50))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface,(240,240,240),text_rect.inflate(10,15).move(0,-5),4,10) #inflate increases the size of the rectangle, move will move the rectangle

# general setup
pygame.init()
WINDOW_WIDTH,WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

#import
star_surf =pygame.image.load(join('images','star.png')).convert_alpha() 
meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha() 
laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha() 
font = pygame.font.Font(join('images','Oxanium-Bold.ttf'),40)
explosion_frames = [pygame.image.load(join('images','explosion',f'{i}.png')).convert_alpha() for i in range(21)] #this is getting paths to all explosion pics

laser_sound = pygame.mixer.Sound(join('audio','laser.wav'))
laser_sound.set_volume(0.4) #quiet the sound
explosion_sound = pygame.mixer.Sound(join('audio','explosion.wav'))
explosion_sound.set_volume(0.4) #quiet the sound
damage_sound = pygame.mixer.Sound(join('audio','space shooter_audio_damage.ogg'))
damage_sound.set_volume(0.4) #quiet the sound
game_music = pygame.mixer.Sound(join('audio','game_music.wav'))
game_music.set_volume(0.25)
game_music.play(loops = -1) #runs indefinitely

#sprites 
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group() #we want to make a meteor sprite for checking collisions
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites,star_surf)
player = Player(all_sprites)


# custom events -> meteor event
meteor_event = pygame.event.custom_type() #create custom event
pygame.time.set_timer(meteor_event,500) #set a timer for the event to fire. first argument is the event itself, second is the time in miliseconds


while running:
    dt = clock.tick() /1000 #delta time is the amount of time (ms) it takes for a computer to render 1 frame. we can use it to deal with problems from faster computers being able to render more frames. We times dt by the speed in order to make the speed framerate independent.

    # event loop
    for event in pygame.event.get(): #check keyboard/mouse input
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, (random.randint(0,WINDOW_WIDTH),0), (all_sprites,meteor_sprites)) #first argument is the meteor surface, second argument is randomized positions, third argument is putting the meteor into two sprite groups.we use all_sprites for the updates, while meteor_sprites are used for classification of the meteors
            
    #update
    all_sprites.update(dt) #calls an update method in the classes of the sprites
    collisions()

    # draw game
    display_surface.fill('#3a2e3f')
    display_score()
    all_sprites.draw(display_surface) 


    pygame.display.update() #draws on display surface

pygame.quit()

#2:14:34







# stuff to remember

#player.rect.collidepoint((pygame.mouse.get_pos())) #returns true if mouse collides with spaceship
#list_of_collision_sprites = pygame.sprite.spritecollide(player,meteor_sprites,True): #this is useful to get a nonempty list returned if you want to do something after a collision 
# if list_of_collision_sprites: print(list_of_collision_sprites[0]) #from the last line, this is how to get that collided sprite