import pygame
import datetime
import pygame.mixer
from agent_game import Agent 
from place_game import Place
from initialize import locations, restricted_areas, agents, win, WINDOW_HEIGHT, WINDOW_WIDTH
from pygame_utils import create_popup,check_collision, show_popup
from pipeline import pipeline
from initialize import df,agents,locations,profiles
import threading
from threading import Thread
import time
import warnings
warnings.filterwarnings("ignore")


pygame.init()
pygame.display.init()

pygame.mixer.music.load("assets/background_song.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Set up clock
clock = pygame.time.Clock()
time = datetime.datetime(2023, 6, 26, 7, 0)  # Starting time is 7:00 AM

env = pygame.image.load("assets/env.png").convert_alpha()
env = pygame.transform.scale(env, (1300, 800))
env_night = pygame.image.load("assets/env_night.jpeg").convert_alpha()
env_night = pygame.transform.scale(env_night, (1300, 800))

# char = pygame.image.load('assets/char.gif')



# Define the duration for each background
sec = 10
background_duration = sec * 1000  # in milliseconds

current_background = env
current_background_timer = pygame.time.get_ticks()

##### Werewolf images

left_images_werewolf = [pygame.image.load("assets/werewolf_L1.png").convert_alpha(),pygame.image.load("assets/werewolf_L2.png").convert_alpha(),pygame.image.load("assets/werewolf_L3.png").convert_alpha()]
right_images_werewolf = [pygame.image.load("assets/werewolf_R1.png").convert_alpha(),pygame.image.load("assets/werewolf_R2.png").convert_alpha(),pygame.image.load("assets/werewolf_R3.png").convert_alpha()]
up_images_werewolf = [pygame.image.load("assets/werewolf_U1.png").convert_alpha(),pygame.image.load("assets/werewolf_U2.png").convert_alpha(),pygame.image.load("assets/werewolf_U3.png").convert_alpha()]
down_images_werewolf = [pygame.image.load("assets/werewolf_D1.png").convert_alpha(),pygame.image.load("assets/werewolf_D2.png").convert_alpha(),pygame.image.load("assets/werewolf_D3.png").convert_alpha()]

char_werewolf = pygame.image.load("assets/char_werewolf.png").convert_alpha()

def change_background():
    global current_background, current_background_timer

    if current_background == env:
        current_background = env_night
    else:
        current_background = env

    current_background_timer = pygame.time.get_ticks()


def redrawGameWindow():
    # win.blit(env, (0,0))
   
    win.blit(current_background, (0, 0))

    for agent in agents:
        agent.draw(win,left_images_werewolf,right_images_werewolf,up_images_werewolf,down_images_werewolf,char_werewolf,env,env_night,current_background)
    
   
    if show_popup:
        create_popup(popup_title , popup_text,mouse_pos[0]-80, mouse_pos[1]-20, win, WINDOW_HEIGHT, WINDOW_WIDTH)
    pygame.display.update()


timing = [global_time for global_time in df['Time']]


counter = 0
data_modified = threading.Event()
i_location = {}
for agent in agents:
    i_location[agent.person.name] = agent.location

day = 0

def fetch_data():
    global i_location, counter, day
    while True:
        print("Day: ", day)
        
        if counter == 0:
           day+=1

        response = pipeline(counter + 7)
        
        cnt = 0
        for agent in response:
            if agent.agent_type == "WereWolf":
                cnt+=1

        if len(response) == 0 or len(response-cnt)<=cnt:
            print("The Game has been finished.")
            break
    
        counter += 1
        counter %= 14 
        
        print("Counter" , counter)
        ok = False
        for agent in response:
            if agent.location != i_location[agent.person.name]:
                ok = True
                break
        
        if ok:
            for agent in response:
                i_location[agent.person.name]=agent.location
            data_modified.set()

        data_modified.wait()
        data_modified.clear()
    
    
thread1 = Thread(target = fetch_data, args = ())
thread1.start()
# main loop

run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False    
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for object in locations:
                if object.rect.collidepoint(mouse_pos):
                    # print("Colliding")
                    popup_title = object.name
                    popup_text = object.description
                    popup_width = 600
                    popup_height = 200
                    show_popup = True
                    break
                else:
                    show_popup = False
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
        #         agents[0].x = 492
        #         agents[0].y = 334

    # move_manual(agent1)
    # move_manual(agent2)
    # agent2.update_location()
    # move_agent2(agent2,path_agent2)
    # move_agent3(agent3,path_agent3)
    # move_agent4(agent4,path_agent4)
    # move_agent5(agent5,path_agent5)
    # move_agent6(agent6,path_agent6)
     # Time handling
    time += datetime.timedelta(minutes=1)  # Increment time by 1 minute
    

    if pygame.time.get_ticks() - current_background_timer >= background_duration:
        change_background()
    
    
    # redrawGameWindow()
    redrawGameWindow()
    
thread1.join() 
    
pygame.mixer.music.stop()
pygame.quit()