import pygame,sys
import random
pygame.init()
pygame.font.init()
pygame.mixer.init()
clock=pygame.time.Clock()
game_font=pygame.font.Font(None,40)
#Game Variables
gravity=0.25
bird_movement=0
screen=pygame.display.set_mode((576,1024))
bg_surface=pygame.image.load("sprites/background-day.png").convert()
bg_surface=pygame.transform.scale2x(bg_surface)
floor=pygame.image.load("sprites/base.png").convert()
floor=pygame.transform.scale2x(floor)
floor_x_pos=0
bird_up=pygame.transform.scale2x(pygame.image.load("sprites/bluebird-upflap.png").convert())
bird_mid=pygame.transform.scale2x(pygame.image.load("sprites/bluebird-midflap.png").convert())
bird_down=pygame.transform.scale2x(pygame.image.load("sprites/bluebird-downflap.png").convert())
bird_frames=[bird_down,bird_mid,bird_up]
bird_index=0
bird=bird_frames[bird_index]
bird_rect=bird.get_rect(center=(100,512))
SPAWNBIRD=pygame.USEREVENT+1
pygame.time.set_timer(SPAWNBIRD,200)
#bird=pygame.image.load("sprites/bluebird-midflap.png").convert()
#bird=pygame.transform.scale2x(bird)
#bird_rect=bird.get_rect(center=(100,512))
pipe=pygame.image.load("sprites/pipe-green.png").convert()
pipe=pygame.transform.scale2x(pipe)
pipe_list=[]
SPAWNPIPE=pygame.USEREVENT+2
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height=[400,600,800]
game_active=True
score_ct=0
high_score_ct=0
b=[]
game_over_surface=pygame.transform.scale2x(pygame.image.load("sprites/message.png").convert_alpha())
game_over_rect=game_over_surface.get_rect(center=(288,512))

flap_sound=pygame.mixer.Sound("audio/wing.wav")
point_sound=pygame.mixer.Sound("audio/point.wav")
hit_sound=pygame.mixer.Sound("audio/hit.wav")
hitct=0

def draw_floor():
    screen.blit(floor,(floor_x_pos, 900))
    screen.blit(floor,(floor_x_pos+576, 900))
def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe.get_rect(midtop=(700,random_pipe_pos))
    top_pipe=pipe.get_rect(midbottom=(700,random_pipe_pos-300))
    return(bottom_pipe,top_pipe)
def move_pipe(pipe_list):
    for i in pipe_list:
        i.centerx-=5
    return(pipe_list)
def draw_pipes(pipe_list):
    for i in pipe_list:
        if(i.bottom>1024):
            screen.blit(pipe,i)
        else:
            screen.blit(pygame.transform.flip(pipe,False,True), i)
def check_collision(pipe_list):
    for i in pipe_list:
        if(bird_rect.colliderect(i)):
            return(True)
        if(bird_rect.top<=0 or bird_rect.bottom>=900):
            return(True)
    return(False)
def rotate_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,bird_movement*-3,1)
    return(new_bird)
def bird_animate():
    new_bird=bird_frames[bird_index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return(new_bird,new_bird_rect)
def score_display(game_state):
    if(game_state=='main_game'):
        score=game_font.render(f'SCORE:{int(score_ct)}',True,(255,255,255))
        score_rect=score.get_rect(center=(288,100))
        screen.blit(score,score_rect)
    elif(game_state=='game_over'):
        score = game_font.render(f'SCORE:{int(score_ct)}', True, (255, 255, 255))
        score_rect = score.get_rect(center=(288, 100))
        screen.blit(score, score_rect)
        high_score = game_font.render(f'HIGH SCORE:{int(high_score_ct)}', True, (255,0,0))
        high_score_rect = high_score.get_rect(center=(288,150))
        screen.blit(high_score,high_score_rect)
        endgame=game_font.render("TO PLAY AGAIN PRESS SPACE",True, (255,255,0))
        endgame_rect= endgame.get_rect(center=(288, 400))
        screen.blit(endgame,endgame_rect)
        endgame1 = game_font.render("TO QUIT PRESS ESC",True,(255,255,0))
        endgame1_rect = endgame1.get_rect(center=(288, 800))
        screen.blit(endgame1, endgame1_rect)

def score_inc(pipe_list):
    for i in pipe_list:
        if(i.centerx==100):
            point_sound.play()
            return(True)
    return(False)

while True:
    for event in  pygame.event.get():
        if(event.type==pygame.QUIT):
            pygame.quit()
            sys.exit()
        if(event.type==pygame.KEYDOWN):
            if(event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if(event.key==pygame.K_SPACE and game_active==True):
                flap_sound.play()
                bird_movement=0
                bird_movement-=8
            if (event.key == pygame.K_SPACE and game_active==False):
                score_ct = 0
                game_active=True
                pipe_list.clear()
                bird_rect.center=(100,512)
                bird_movement=0
                hitct=0
        if(event.type==SPAWNBIRD):
            if(bird_index<2):
                bird_index+=1
            else:
                bird_index=0
            bird,bird_rect=bird_animate()
        if(event.type==SPAWNPIPE):
            pipe_list.extend(create_pipe())
    screen.blit(bg_surface,(0,0))
    if(check_collision(pipe_list)==True):
        game_active=False
    if(game_active):
        #bird
        bird_movement+=gravity
        rotated_bird=rotate_bird(bird)
        bird_rect.centery+=bird_movement
        screen.blit(rotated_bird,bird_rect)
        #pipes
        pipe_list=move_pipe(pipe_list)
        draw_pipes(pipe_list)
    else:
        if(hitct==0):
            hit_sound.play()
            hitct=1
        screen.blit(game_over_surface,game_over_rect)
        score_display('game_over')
        if(score_ct>high_score_ct):
            high_score_ct=score_ct
    if(score_inc(pipe_list)==True):
        score_ct+=1
    score_display('main_game')
    #floor
    floor_x_pos-= 1
    draw_floor()
    if(floor_x_pos<-576):
        floor_x_pos=0
    pygame.display.update()
    clock.tick(120)
