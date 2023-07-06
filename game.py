import pygame
import datetime
import pygame.mixer
from agent_game import Agent , paths
from place_game import Place
from pygame_utils import create_popup,check_collision, show_popup
from pipeline import pipeline
# from debug_pipeline import pipeline
from initialize import df,agents,locations,profiles,restricted_areas, win, WINDOW_HEIGHT, WINDOW_WIDTH, well , haya1 , takashi, garden, yamamoto_residence
import threading
from threading import Thread
import time
import warnings
from pygame import *
from moviepy.editor import VideoFileClip
# import os
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

## Killing Action ####
killing_action = pygame.image.load("assets/killing_action.gif").convert_alpha()
# killing_action = pygame.transform.scale(killing_action, (1300, 800))

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)

# Create a font object
font = pygame.font.Font(None, 22)

# # Set up the GIF
# gif_path = "assets/killing_action.gif"
# clip = VideoFileClip(gif_path)

# # Variables for the GIF animation
# gif_timer = 0
# gif_duration = 2000  # 2 seconds



#### END GAME Background #####
background_image = pygame.image.load("assets/bg_end.png")  # Replace with the actual path to your background image

# Resize the background image to fit the screen
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


# char = pygame.image.load('assets/char.gif')

# Font #
# font_path = os.path.join("assets/japanese.otf")
font_japanese = pygame.font.Font("assets/japanese.otf", 80)


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
char_townfolk = pygame.image.load("assets/char.gif").convert_alpha()

def change_background():
    global current_background, current_background_timer

    if current_background == env:
        current_background = env_night
    else:
        current_background = env

    current_background_timer = pygame.time.get_ticks()

timing = [global_time for global_time in df['Time']]


counter = 0
data_modified = threading.Event()
i_location = {}
target_location = {}
buffer_location = {}
current_actions = {}
for agent in agents:
    i_location[agent.person.name] = agent.location
    buffer_location[agent.person.name] = agent.location
    target_location[agent.person.name] = agent.location
    current_actions[agent.person.name] = "Resting"




#################### Showing Story Screen ##################



# Set up fonts
title_font = pygame.font.Font("assets/japanese.otf", 50)
text_font = pygame.font.Font("assets/japanese.otf", 24)

# Set up the storyline text
title_text = "林野村"
story_text = "ミラーホロウの狼人たちは、戦略と推理が交差する、高度な心理戦と対立が織り成す、壮大なサスペンスゲームです。"

# Set up buttons
button_width, button_height = 120, 40
button_pos = (WINDOW_WIDTH // 2 - button_width // 2, WINDOW_HEIGHT - 100)

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def show_story_screen():
    alpha = 0
    fade_speed = 1
    fade_out = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                fade_out = True
            if event.type == KEYDOWN and event.key == K_RETURN:
                return
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    return

        if fade_out:
            if alpha >= 255:
                pygame.quit()
                return
            alpha += fade_speed

        win.blit(background_image, (0, 0))
        pygame.time.delay(10)  # Delay after blitting the background

        # Draw the title text with transparency
        title_surface = title_font.render(title_text, True, (255, 255, 255, alpha))
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 150))
        win.blit(title_surface, title_rect)
        pygame.time.delay(10)  # Delay after blitting the title text

        # Draw a dividing line with transparency
        line_rect = pygame.Rect(200, 200, WINDOW_WIDTH - 400, 2)
        pygame.draw.rect(win, (255, 255, 255, alpha), line_rect)
        pygame.time.delay(10)  # Delay after blitting the dividing line

        # Draw the story text with transparency
        story_surface = text_font.render(story_text, True, (255, 255, 255, alpha))
        story_rect = story_surface.get_rect(center=(WINDOW_WIDTH // 2, 300))
        win.blit(story_surface, story_rect)
        pygame.time.delay(10)  # Delay after blitting the story text

        # Draw the OK button with transparency
        button_rect = pygame.Rect(button_pos, (button_width, button_height))
        pygame.draw.rect(win, (0, 0, 0, alpha), button_rect)
        pygame.draw.rect(win, (255, 255, 255, alpha), button_rect.inflate(-4, -4))
        button_text = text_font.render("OK", True, (0, 0, 0, alpha))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        win.blit(button_text, button_text_rect)
        pygame.time.delay(10)  # Delay after blitting the OK button

        pygame.display.flip()
        pygame.time.delay(100)  # Delay before rendering the next frame




############################ Story Screen END ##################

show_story_screen()


=======

winning_status = "Playing"
day = 0

response = []

def fetch_data():
    global i_location, counter, day, response, winning_status
    while True:
        print("Day: ", day)
        
        if counter == 0:
           day+=1

        response = pipeline(counter + 7, day)
        
        for agent in response[0]:
            buffer_location[agent.person.name] = agent.location
            current_actions[agent.person.name] = response[1][agent.person.name]
        
        cnt = 0
        for agent in response[0]:
            if agent.agent_type == "WereWolf":
                cnt+=1
        
        print(len(response[0]), cnt)
        status = True 
        if cnt==0:
            print("The Game has been finished. TownFolks Won.")
            winning_status = "TownFolks Won"
            status = False
        elif (len(response)-cnt<=cnt):
            print("The Game has been finished. WereWolfs Won.")
            winning_status = "Werewolf Won"
            status = False

        if not status:
            break
    
        counter += 1
        counter %= 14 
        cnt +=1
        data_modified.set()

        data_modified.wait()
        data_modified.clear()

thread1 = Thread(target = fetch_data, args = ())
thread1.start()
# main loop

########### Blitting image for 5 seconds ##############

def blit_image(image, duration):
    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        current_time = pygame.time.get_ticks()

        # Clear the screen
        win.fill(WHITE)

        # Check if the image should be displayed
        if current_time - start_time < duration:
            # Blit the image onto the screen
            image_rect = image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            win.blit(image, image_rect)
        else:
            return

        pygame.display.flip()

######## Generating pop up for 5 seconds ##########

def generate_popup(text):
    popup_start_time = pygame.time.get_ticks()
    popup_duration = 5000  # 5 seconds in milliseconds

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        current_time = pygame.time.get_ticks()

        # Clear the screen
        # win.fill(WHITE)

        # Check if the pop-up duration has passed
        if current_time - popup_start_time >= popup_duration:
            return

        # Create the pop-up window
        popup_surface = pygame.Surface((200, 100))
        popup_surface.fill((255, 0, 0))  # Red background color
        popup_text_surface = text_font.render(text, True, (255, 255, 255))
        popup_text_rect = popup_text_surface.get_rect(center=(100, 50))
        popup_surface.blit(popup_text_surface, popup_text_rect)

        # Blit the pop-up window onto the screen
        popup_rect = popup_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        win.blit(popup_surface, popup_rect)

        pygame.display.flip()


##################### Voting starts #######################
run = True
ctr_killing_time  = 0
ctr_voting_time  = 0
def redrawGameWindow():
    
    # win.blit(env, (0,0))
   if(run == True):
    win.blit(current_background, (0, 0))

    for agent in agents:
        if agent.state == 'alive':
            if agent.show_popup == True:
                win.blit(font.render(current_actions[agent.person.name], True, BLACK, LIGHT_BLUE), (agent.x+10, agent.y))
            agent.draw(win,left_images_werewolf,right_images_werewolf,up_images_werewolf,down_images_werewolf,char_werewolf,env,env_night,current_background)


    if show_popup:
        create_popup(popup_title , popup_text,mouse_pos[0]-80, mouse_pos[1]-20, win, WINDOW_HEIGHT, WINDOW_WIDTH)
    pygame.display.update()


def redrawGameWindow():
    # win.blit(env, (0,0))
   
    win.blit(current_background, (0, 0))

    for agent in agents:
        if agent.state == 'alive':
            agent.draw(win,left_images_werewolf,right_images_werewolf,up_images_werewolf,down_images_werewolf,char_werewolf,env,env_night,current_background)
    
   
    if show_popup:
        create_popup(popup_title , popup_text,mouse_pos[0]-80, mouse_pos[1]-20, win, WINDOW_HEIGHT, WINDOW_WIDTH)
    pygame.display.update()


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

    ######### Checking if the game ends ########################

    if (winning_status != "Playing"):
        # Clear the screen
        win.fill((0, 0, 0))

        win.blit(background_image, (0, 0))
        
        # Render the "Game End" message
        ans = "人狼の勝利"
        if(winning_status == "TownFolks Won"):
            ans = "タウンフォークスが勝ちました"
        else:
            ans = "人狼が勝ちました"

        text = font_japanese.render(ans, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        win.blit(text, text_rect)

        ########### Imges ###############
        image1_rect = char_werewolf.get_rect()
        image2_rect = char_townfolk.get_rect()
        image1_rect.bottomleft = (50, WINDOW_HEIGHT - 20)
        image2_rect.bottomright = (WINDOW_WIDTH - 50, WINDOW_HEIGHT - 20)
        win.blit(char_werewolf, image1_rect)
        win.blit(char_townfolk, image2_rect)



        pygame.display.flip()
        
        # Delay for a few seconds before closing the screen
        pygame.time.delay(10000)  # Adjust the delay duration as needed
        
        win.fill((0, 0, 0))
        win.blit(background_image, (0, 0))
        text = font_japanese.render("ゲームエンド", True, (255, 255, 255))
        # text = font.render("Game END", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        # Draw the "Game End" message on the screen
        win.blit(text, text_rect)
        
        # Update the display
        pygame.display.flip()
        
        # Delay for a few seconds before closing the screen
        pygame.time.delay(10000)  # Adjust the delay duration as needed
        
        # Exit the game loop
        # run = False
        pygame.mixer.music.stop()
        pygame.quit()
        break

    
    ### Killing Action ####
    # if (counter%14)+7 == 7:
    #     if gif_timer <= gif_duration:
    #         # Blit the GIF onto the window surface
    #         gif_surface = pygame.image.fromstring(clip.get_frame(gif_timer / 1000), clip.size, "RGB")
    #         gif_rect = gif_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    #         win.blit(gif_surface, gif_rect)

    #         gif_timer += clock.tick(30)  # Update the GIF timer
    #     else:
    #         # Reset the counter and GIF timer
    #         gif_timer = 0
    #     pygame.display.flip()
    #     clock.tick(30)
    # ###


    ####### Generating Pop Out ##########
    if (counter% 15)+7 == 19:
        if(ctr_killing_time == 0):
            generate_popup("Killing Time!")
            # blit_image(killing_action, 5000)
            ctr_killing_time += 1
    else:
        ctr_killing_time = 0
    if (counter% 15)+7 == 8:
        if(ctr_voting_time == 0):
            generate_popup("Voting Starts!")
            # blit_image(killing_action, 5000)
            ctr_voting_time += 1
    else:
        ctr_voting_time = 0
        




    # move_manual(agent1)
    # move_manual(agent2)
    # agent2.update_location()
    # for agent in agents:
    #     agent.move_agent(agent.location,agent.location)
    # if(cnt>0):
    # if len(response) == 0:    
    # print("######### Creating Screen 1  ##############")
    
    for agent in agents:
        # print("############### Name : " , agent.person.name)
        if(buffer_location[agent.person.name] != target_location[agent.person.name]):
            i_location[agent.person.name] = target_location[agent.person.name]
            target_location[agent.person.name] = buffer_location[agent.person.name]
            agent.current_point = 1
            agent.move_agent(paths[i_location[agent.person.name].name][target_location[agent.person.name].name])
        else:
            agent.move_agent(paths[i_location[agent.person.name].name][target_location[agent.person.name].name]) 
   
    # move_agent4(agent4,path_agent4)
    # move_agent5(agent5,path_agent5)
    # move_agent6(agent6,path_agent6)
     # Time handling
    time += datetime.timedelta(minutes=1)  # Increment time by 1 minute
    

    if pygame.time.get_ticks() - current_background_timer >= background_duration:
        change_background()
    
    # print("##############  Creating Screen 2 ###############")
    # redrawGameWindow()
    redrawGameWindow()
    
thread1.join() 
    
pygame.mixer.music.stop()
pygame.quit()