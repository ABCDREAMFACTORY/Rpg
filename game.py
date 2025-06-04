import pygame
from PIL import Image
import time
pygame.init()
fenetreHauteur = 1280
fenetreLargeur = 720
screen = pygame.display.set_mode((fenetreHauteur, fenetreLargeur))
clock = pygame.time.Clock()
running = True

class player():
    def __init__(self,screen):
        self.screen = screen
        self.player_frame = extract_frames("assets/Stand.gif")
        self.player_frame = [pygame.transform.scale(frame,(200, 200)) for frame in self.player_frame]
        self.co_x = self.screen.get_width()/2
        self.co_y = 600
        self.score = 0
        self.speed = 5


        self.animage_nb_image = len(self.player_frame) # pour un tileset de 10 images
        self.animage_duree    = 0.17 
        self.animage_time     = time.monotonic()
        self.animage_index    = 1
        self.axis = "right"

        self.run = False
        self.start_standing = False
        self.current_animation = "Stand"

        self.jump_strength = -12
        self.on_ground = True
        self.player_vel_y = 0
    def draw(self):
        self.rect = self.player_frame[self.animage_index].get_rect()
        self.rect.center = self.co_x,self.co_y
        screen.blit(self.player_frame[self.animage_index],self.rect)
    def move_left(self):
        if self.co_x > self.player_frame[self.animage_index].get_width()/4:
            self.co_x -= self.speed
        if self.current_animation != "runAnimLeft":
            self.player_frame = extract_frames("assets/runAnim.gif")
            self.player_frame = [pygame.transform.flip(frame, True, False) for frame in self.player_frame]
            self.animage_nb_image = len(self.player_frame)
            self.start_standing = True
            self.axis = "left"
            self.current_animation = "runAnimLeft"
    def move_right(self):
        if self.co_x < self.screen.get_width()-self.player_frame[self.animage_index].get_width()/4:
            self.co_x += self.speed
        if self.current_animation != "runAnimRight":
            self.player_frame = extract_frames("assets/runAnim.gif")
            self.start_standing = True
            self.animage_nb_image = len(self.player_frame)
            self.axis = "right"
            self.current_animation = "runAnimRight"
    def stand(self):
        if self.current_animation != "Stand":
            self.player_frame = extract_frames("assets/Stand.gif")
            if self.axis == "left":
                self.player_frame = [pygame.transform.flip(frame,True,False) for frame in self.player_frame]
            self.animage_nb_image = len(self.player_frame)
            self.animage_index  = 1
            self.current_animation = "Stand"
    def jump(self):
        if self.on_ground:
            self.player_vel_y = self.jump_strength
            self.on_ground = False
    def gain_score(self,how_much):
        self.score += how_much
    def Gravity(self):
        if self.on_ground == False:
            self.player_vel_y += gravity
            self.co_y += self.player_vel_y
        if self.co_y >= ground:
            self.co_y = ground
            self.player_vel_y = 0
            self.on_ground = True
def extract_frames(path):
    with Image.open(path) as img:
        frames = []
        for frame in range(img.n_frames):
            img.seek(frame)
            frame_img = img.copy()
            frame_img.convert("RGBA")
            frame_surface = pygame.image.fromstring(frame_img.tobytes(), frame_img.size, frame_img.mode)
            frame_surface = pygame.transform.scale(frame_surface,(200, 200))
            frames.append(frame_surface)
    return frames

Player1 = player(screen)
Player2 = player(screen)

bg = pygame.image.load("assets/Background2.jpg")
bg = pygame.transform.scale(bg,(fenetreHauteur, fenetreLargeur))


pygame.display.set_caption("Jeu python")


gravity = 0.5
ground = 600
while running:
    print("pos:",pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if time.monotonic()-Player1.animage_time > Player1.animage_duree:
        Player1.animage_index = (Player1.animage_index+1)%Player1.animage_nb_image
        if Player1.animage_index == 0:
            Player1.animage_index = 1

        Player2.animage_index = (Player2.animage_index+1)%Player2.animage_nb_image
        if Player2.animage_index == 0:
            Player2.animage_index = 1

        Player1.animage_time =  time.monotonic()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_z] or keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        Player1.jump()
        Player2.jump()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        Player1.move_right()
        Player2.move_left()
    elif keys[pygame.K_q] or keys[pygame.K_LEFT]:
        Player1.move_left()
        Player2.move_right()
    else:
        Player1.stand()
        Player2.stand()
    Player1.Gravity()
    Player2.Gravity()
    #if Player1.animage_index >= Player1.animage_nb_image:
     #   Player1.animage_index = 1
    screen.blit(bg,(0,0))
    Player1.draw()
    Player2.draw()
    clock.tick(60)  # limits FPS to 60
    pygame.display.update()
