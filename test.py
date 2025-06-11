import pygame
import time
from PIL import Image
from random import randint
class Menu_game:
    def __init__(self,screen):
        self.screen = screen
        self.bg = pygame.image.load("assets/Background2.jpg")
        self.bg = pygame.transform.scale(self.bg,(self.screen.get_width(), self.screen.get_height()))
        self.clock = pygame.time.Clock()
        self.menu = "self"
        self.Player1 = player(screen)
        self.Player2 = player(screen)
        self.list_coins = [coin(screen,randint(0,self.screen.get_width()),500,30),coin(screen,randint(0,self.screen.get_width()),500,30)]
        pygame.display.set_caption("Jeu python")
        self.gravity = 0.5
        self.ground = 500
        self.running = True
        self.action = None

    def handle_event(self,event):
        if event.type == pygame.QUIT:
            self.running = False
            print("Fin du jeu")
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                self.action = "Retour"
                print(self.action)

    def load(self):
            self.screen.blit(self.bg,(0,0))
            if time.monotonic()-self.Player1.animage_time > self.Player1.animage_duree:
                self.Player1.animage_index = (self.Player1.animage_index+1)%self.Player1.animage_nb_image
                if self.Player1.animage_index == 0:
                    self.Player1.animage_index = 1

                self.Player2.animage_index = (self.Player2.animage_index+1)%self.Player2.animage_nb_image
                if self.Player2.animage_index == 0:
                    self.Player2.animage_index = 1

                self.Player1.animage_time =  time.monotonic()
            for coins in self.list_coins:
                coins.draw()
                coins.collision(self.Player1)
                coins.collision(self.Player2)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z] or keys[pygame.K_SPACE]:
                self.Player1.jump()
            if keys[pygame.K_d]:
                self.Player1.move_right()
            elif keys[pygame.K_q]:
                self.Player1.move_left()
            else:
                self.Player1.stand()
            if keys[pygame.K_UP]:
                self.Player2.jump()
            if keys[pygame.K_RIGHT]:
                self.Player2.move_right()
            elif keys[pygame.K_LEFT]:
                self.Player2.move_left()
            else:
                self.Player2.stand()
            if keys[pygame.K_ESCAPE]:
                self.action = "Retour"
            self.Player1.Gravity(self.ground,self.gravity)
            self.Player2.Gravity(self.ground,self.gravity)
            #if Player1.animage_index >= Player1.animage_nb_image:
            #   Player1.animage_index = 1
            self.Player1.draw()
            self.Player2.draw()
            self.clock.tick(60)  # limits FPS to 60
            pygame.display.update()

class player():
    def __init__(self,screen):
        self.screen = screen
        self.player_frame = extract_frames("assets/Stand.gif")
        self.player_frame = [pygame.transform.scale(frame,(200, 200)) for frame in self.player_frame]
        self.co_x = self.screen.get_width()/2
        self.co_y = 500
        self.rect = pygame.Rect(self.co_x,self.co_y,100,175)
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


        self.rect.center = self.co_x+100,self.co_y+100
        #pygame.draw.rect(self.screen,"White",self.rect)
        self.screen.blit(self.player_frame[self.animage_index],pygame.Rect(self.co_x,self.co_y,100,175))
    def move_left(self):
        if self.co_x > -50:
            self.co_x -= self.speed
        else:
            print(self.co_x,self.co_y)
        if self.current_animation != "runAnimLeft":
            self.player_frame = [pygame.transform.flip(frame, True, False) for frame in extract_frames("assets/runAnim.gif")]
            self.animage_nb_image = len(self.player_frame)
            self.start_standing = True
            self.axis = "left"
            self.current_animation = "runAnimLeft"

    def move_right(self):
        if self.co_x < self.screen.get_width()-self.player_frame[self.animage_index].get_width()+50:
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

    def Gravity(self,ground,gravity):
        if self.on_ground == False:
            self.player_vel_y += gravity
            self.co_y += self.player_vel_y
        if self.co_y >= ground:
            self.co_y = ground
            self.player_vel_y = 0
            self.on_ground = True

class coin:
    def __init__(self,screen,x,y,radius):
        self.screen = screen
        self.x,self.y = x,y
        self.radius = radius

        self.frames = extract_frames("assets/Coins.gif")
        self.nbframes = len(self.frames)
        self.gif_index = 1
    def draw(self):
        self.rect = self.frames[self.gif_index].get_rect()
        self.rect.center = self.x,self.y
        self.screen.blit(self.frames[self.gif_index],self.rect)

        self.gif_index = (self.gif_index+1) % self.nbframes
        if self.gif_index == 0:
            self.gif_index = 1

    def collision(self,player):
        if player.rect.collidepoint(self.x,self.y):
            print("coin touché")
            player.score +=1
            self.x,self.y = randint(0,self.screen.get_width()),500
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