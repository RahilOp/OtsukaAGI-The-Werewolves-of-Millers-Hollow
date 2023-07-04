from agent_game import Agent
from place_game import Place
from utils1 import create_new_memory_retriever,LLM
import pandas as pd
import pygame
import warnings
warnings.filterwarnings("ignore")


pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Set the Caption
pygame.display.set_caption("Hayashino")




yamamoto_residence = Place("Yamamoto Residence",
                           "The Yamamoto family's small house is located in Hayashino Town, serving as the residence of Takashi Yamamoto and Yumi Yamamoto.",
                           69,69,
                           377,217)  
well = Place("Well","Villagers use it to get water",437,0,539,173)  
haya1 = Place("Haya Apartment 1","Residence of Kazuki Sato",569,0,716,194)
haya2 = Place("Haya Apartment 2","Residence of Satoshi Takahashi",724,0,873,192)
haya3 = Place("Haya Apartent 3","Residence of Yusuke Mori",886,0,1046,192)
haya4 = Place("Haya Apartent 4","Residence of Ayumi Kimura",1061,0,1220,195)
college = Place("Kogaku Institute of Physics","Kogaku Institute of Physics in Hayashiro conducts groundbreaking physics research with top researchers and advanced facilities",91,398,343,656)
shrine = Place("Mizukami Shrine","Japanese shrines are sacred sanctuaries preserving ancient traditions, offering a profound spiritual glimpse into rich heritage",770,580,957,768)
garden = Place("Hanazawa Park","Hanazawa Park offers exercise, relaxation, and inspiration with nature's beauty",962,559,1230,744)
grocery = Place("Shino Grocery Store","Shino grocery store, owned by Takashi Yamamoto, is a community hub providing diverse essential products and promoting sustainability",1080,350,1235,461)
river1 = Place("River Part 1","River",580,388,677,550)
river2 = Place("River Part 2","River",580,640,674,752)
garden_fence = Place("Fence","Fence of Garden",1050,550,1248,554)

##### array of locations and restricted_area ###########
locations = [yamamoto_residence, well, haya1, haya2, haya3, haya4, college, shrine, garden, grocery]
restricted_areas = [yamamoto_residence,well,haya1,haya2,haya3,haya4,college,shrine,garden_fence,grocery,river1,river2]


# roles = ["Engineer", "Student", "Carpenter", "Professor", ""]
#Creating objects and defining their name, age, traits, status, etc.
left_images_agent1 = [pygame.image.load("assets/agent1_L1.gif").convert_alpha(),pygame.image.load("assets/agent1_L2.gif").convert_alpha(),pygame.image.load("assets/agent1_L3.gif").convert_alpha()]
right_images_agent1 = [pygame.image.load("assets/agent1_R1.gif").convert_alpha(),pygame.image.load("assets/agent1_R2.gif").convert_alpha(),pygame.image.load("assets/agent1_R3.gif").convert_alpha()]
up_images_agent1 = [pygame.image.load("assets/agent1_U1.gif").convert_alpha(),pygame.image.load("assets/agent1_U2.gif").convert_alpha(),pygame.image.load("assets/agent1_U3.gif").convert_alpha()]
down_images_agent1 = [pygame.image.load("assets/agent1_D1.gif").convert_alpha(),pygame.image.load("assets/agent1_D2.gif").convert_alpha(),pygame.image.load("assets/agent1_D3.gif").convert_alpha()]

takashi_status = "living with his wife Yumi Yamamoto, and discusses happenings at stores, neighborhood, and his political ambitions"
takashi=Agent(name = "Takashi Yamamoto", 
              age = 46, agent_type = "TownFolk", 
              traits="rude, aggressive, energetic" , 
              status = takashi_status, 
              location = yamamoto_residence,
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=492, 
              y=334, 
              width = 60,
              height = 60, 
              image_path='assets/char.gif',
              left_images=left_images_agent1,
              right_images=right_images_agent1,
              up_images=up_images_agent1,
              down_images=down_images_agent1)

left_images_agent2 = [pygame.image.load("assets/agent2_L1.png").convert_alpha(),pygame.image.load("assets/agent2_L2.png").convert_alpha(),pygame.image.load("assets/agent2_L3.png").convert_alpha()]
right_images_agent2 = [pygame.image.load("assets/agent2_R1.png").convert_alpha(),pygame.image.load("assets/agent2_R2.png").convert_alpha(),pygame.image.load("assets/agent2_R3.png").convert_alpha()]
up_images_agent2 = [pygame.image.load("assets/agent2_U1.png").convert_alpha(),pygame.image.load("assets/agent2_U2.png").convert_alpha(),pygame.image.load("assets/agent2_U3.png").convert_alpha()]
down_images_agent2 = [pygame.image.load("assets/agent2_D1.png").convert_alpha(),pygame.image.load("assets/agent2_D2.png").convert_alpha(),pygame.image.load("assets/agent2_D3.png").convert_alpha()]

yumi_status = "loves to take care of her family and enjoys spending time with them"
yumi=Agent(name = "Yumi Yamamoto", 
              age = 42, agent_type = "TownFolk", 
              traits="friendly, helpful, organized" , 
              status = yumi_status, 
              location = yamamoto_residence,
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=118,
              y=330, 
              width = 30,
              height = 30, 
              image_path='assets/char.gif',
              left_images=left_images_agent2,
              right_images=right_images_agent2,
              up_images=up_images_agent2,
              down_images=down_images_agent2)


###################### making agent3 ########################
left_images_agent3 = [pygame.image.load("assets/agent3_L1.png").convert_alpha(),pygame.image.load("assets/agent3_L2.png").convert_alpha(),pygame.image.load("assets/agent3_L3.png").convert_alpha()]
right_images_agent3 = [pygame.image.load("assets/agent3_R1.png").convert_alpha(),pygame.image.load("assets/agent3_R2.png").convert_alpha(),pygame.image.load("assets/agent3_R3.png").convert_alpha()]
up_images_agent3 = [pygame.image.load("assets/agent3_U1.png").convert_alpha(),pygame.image.load("assets/agent3_U2.png").convert_alpha(),pygame.image.load("assets/agent3_U3.png").convert_alpha()]
down_images_agent3 = [pygame.image.load("assets/agent3_D1.png").convert_alpha(),pygame.image.load("assets/agent3_D2.png").convert_alpha(),pygame.image.load("assets/agent3_D3.png").convert_alpha()]

kazuki_status = "intelligent student who is focussed on her career and health"
kazuki=Agent(name = "Kazuki Sato", 
              age = 21, agent_type = "TownFolk", 
              traits="energetic, enthusiastic, inquisitive", 
              status = kazuki_status, 
              location = haya1,
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=118,
              y=330, 
              width = 30,
              height = 30, 
              image_path='assets/char.gif',
              left_images=left_images_agent3,
              right_images=right_images_agent3,
              up_images=up_images_agent3,
              down_images=down_images_agent3)

###################### making agent4 ########################
left_images_agent4 = [pygame.image.load("assets/agent4_L1.gif").convert_alpha(),pygame.image.load("assets/agent4_L2.gif").convert_alpha(),pygame.image.load("assets/agent4_L3.gif").convert_alpha()]
right_images_agent4 = [pygame.image.load("assets/agent4_R1.gif").convert_alpha(),pygame.image.load("assets/agent4_R2.gif").convert_alpha(),pygame.image.load("assets/agent4_R3.gif").convert_alpha()]
up_images_agent4 = [pygame.image.load("assets/agent4_U1.gif").convert_alpha(),pygame.image.load("assets/agent4_U2.gif").convert_alpha(),pygame.image.load("assets/agent4_U3.gif").convert_alpha()]
down_images_agent4 = [pygame.image.load("assets/agent4_D1.gif").convert_alpha(),pygame.image.load("assets/agent4_D2.gif").convert_alpha(),pygame.image.load("assets/agent4_D3.gif").convert_alpha()]

satoshi_status = "Retired Navy Officer and a wise man who loves helping others and takes care of his health"
satoshi=Agent(name = "Satoshi Takahashi", 
              age = 56, agent_type = "WereWolf", 
              traits="wise, resourceful, humorous", 
              status = satoshi_status, 
              location = haya2,
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=118,
              y=330, 
              width = 30,
              height = 30, 
              image_path='assets/char.gif',
              left_images=left_images_agent4,
              right_images=right_images_agent4,
              up_images=up_images_agent4,
              down_images=down_images_agent4)


###################### making agent5 ########################
left_images_agent5 = [pygame.image.load("assets/agent5_L1.png").convert_alpha(),pygame.image.load("assets/agent5_L2.png").convert_alpha(),pygame.image.load("assets/agent5_L3.png").convert_alpha()]
right_images_agent5 = [pygame.image.load("assets/agent5_R1.png").convert_alpha(),pygame.image.load("assets/agent5_R2.png").convert_alpha(),pygame.image.load("assets/agent5_R3.png").convert_alpha()]
up_images_agent5 = [pygame.image.load("assets/agent5_U1.png").convert_alpha(),pygame.image.load("assets/agent5_U2.png").convert_alpha(),pygame.image.load("assets/agent5_U3.png").convert_alpha()]
down_images_agent5 = [pygame.image.load("assets/agent5_D1.png").convert_alpha(),pygame.image.load("assets/agent5_D2.png").convert_alpha(),pygame.image.load("assets/agent5_D3.png").convert_alpha()]

yusuke_status = "Yusuke Mori is a skilled carpenter and a religious person"
yusuke=Agent(name = "Yusuke Mori", 
              age = 45, agent_type = "WereWolf", 
              traits="friendly, outgoing, generous", 
              status = yusuke_status, 
              location = haya3,
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=118,
              y=330, 
              width = 30,
              height = 30, 
              image_path='assets/char.gif',
              left_images=left_images_agent5,
              right_images=right_images_agent5,
              up_images=up_images_agent5,
              down_images=down_images_agent5)


###################### making agent6 ########################
left_images_agent6 = [pygame.image.load("assets/agent6_L1.png").convert_alpha(),pygame.image.load("assets/agent6_L2.png").convert_alpha(),pygame.image.load("assets/agent6_L3.png").convert_alpha()]
right_images_agent6 = [pygame.image.load("assets/agent6_R1.png").convert_alpha(),pygame.image.load("assets/agent6_R2.png").convert_alpha(),pygame.image.load("assets/agent6_R3.png").convert_alpha()]
up_images_agent6 = [pygame.image.load("assets/agent6_U1.png").convert_alpha(),pygame.image.load("assets/agent6_U2.png").convert_alpha(),pygame.image.load("assets/agent6_U3.png").convert_alpha()]
down_images_agent6 = [pygame.image.load("assets/agent6_D1.png").convert_alpha(),pygame.image.load("assets/agent6_D2.png").convert_alpha(),pygame.image.load("assets/agent6_D3.png").convert_alpha()]

ayumi_status = "religious lady who is always looking for ways to support her students"
ayumi=Agent(name = "Ayumi Kimura", 
              age = 44, agent_type = "TownFolk", 
              traits="nurturing, kind, patient", 
              status = ayumi_status, 
              location = haya4,
              memory_retriever=create_new_memory_retriever(), 
              llm=LLM, 
              reflection_threshold=8, 
              verbose=False, 
              x=118,
              y=330, 
              width = 30,
              height = 30, 
              image_path='assets/char.gif',
              left_images=left_images_agent6,
              right_images=right_images_agent6,
              up_images=up_images_agent6,
              down_images=down_images_agent6)

agents = [takashi,yumi,kazuki,satoshi,yusuke,ayumi]
# Profiles of agents
# Takashi Yamamoto's Profile
takashi_profile = [
    "Takashi Yamamoto is a shopkeeper who owns Shino Grocery Store and loves interacting with customers.",
    "Takashi manages day to day operations at the store and helps out customers with their orders.",
    "Takashi is always willing to help out and make sure everyone is taken care of. ",
    "Takashi is also really interested in the local mayor election that is coming up next month.",
]

# Adding Profile
yumi_profile = [
    "Yumi Yamamoto is a housewife who loves to take care of her family",
    "Yumi Yamamoto is always looking for new ways to make life easier and more enjoyable for everyone",
    "Yumi Yamamoto goes to bed around 10pm, wakes up around 6am, eats dinner around 6pm."
]

# Adding Profile
kazuki_profile = [
    "Kazuki Sato is a student at  Kogaku Institute of Physics studying physics and lives a healthy life",
    "Kazuki Sato is working on her physics degree and exercises every morning in the nearby Hanazawa Park",
    "Kazuki Sato loves to connect with people and explore new ideas",
]

# Adding Profile
satoshi_profile = [
    "Satoshi Takahashi is a retired navy officer who loves to share stories from his time in the military",
    "Satoshi Takahashi lives a healthy lifestyle",
    "Satoshi Takahashi is always full of interesting stories and advice",
    "Satoshi Takahashi spends his free time tending the park and is an avid reader",
    "Satoshi Takahashi is planning on contesting for local mayor in the upcoming election and he is telling his neighbors about it",
    "Satoshi Takahashi goes to bed around 9pm, wakes up around 5am, eats dinner around 5:00 pm",
]

# Adding Profile
yusuke_profile = [
    "Yusuke Mori is a skilled and experienced carpenter with a passion for woodworking and craftsmanship",
    "Yusuke Mori is the go-to person whenever people need his services for repairing old furniture or creating new pieces",
    "Yusuke Mori holds a contract of supplying furniture for Kogaku Institute of Physics",
    "Yusuke Mori is responsible for maintaining wooden Hanazawa fences",
    "Yusuke Mori is a religious person",
]

# Adding Profile
ayumi_profile = [
    "Ayumi Kimura is a college professor who loves to help people reach their goals. She is always looking for ways to support her students",
    "Ayumi Kimura is teaching a course on physics at Kogaku Institute of Physics and working on her research paper",
    "Ayumi Kimura is a religious lady and loves to interact with people",
    "Ayumi Kimura is nature loving and loves to go for a morning walk",
    "Ayumi Kimura is also really interested in the local mayor election that is coming up next month",
    "Ayumi Kimura goes to bed around 7pm, wakes up around 7am, eats dinner around 5pm"
]

profiles = {
    "Takashi Yamamoto": takashi_profile, 
    "Yumi Yamamoto": yumi_profile, 
    "Kazuki Sato": kazuki_profile, 
    "Satoshi Takahashi": satoshi_profile, 
    "Yusuke Mori": yusuke_profile, 
    "Ayumi Kimura": ayumi_profile
}

for i in range(0,len(agents)):
  for profile_point in profiles[agents[i].person.name]:
    agents[i].profile.append(profile_point)
    agents[i].memory.add_memory(profile_point)


#Adding relations
takashi.relations = {
    "Yumi Yamamoto": "Yumi Yamamoto is the wife of Takashi Yamamoto, Takashi Yamamoto loves her a lot and they both discuss daily happenings at the Shino Grocery Store and neighborhood, and local politics. They have dinner together.",
    "Kazuki Sato": "Kazuki and Takashi know each other and sometimes Kazuki visits Yamamoto Residence for dinner.",
    "Satoshi Takahashi": "Takashi Yamamoto thinks that Satoshi Takahashi is not a good candidate for contesting local mayor elections. Satoshi Takahashi is a regular customer at Shino Grocery store.",
    "Yusuke Mori": "Takashi Yamamoto calls Yusuke Mori only for repairing furniture or for creating new wooden pieces.",
    "Ayumi Kimura": "Takashi Yamamoto lives in the same neighborhood as Ayumi Kimura."
}

# adding relations
yumi.relations = {
  'Takashi Yamamoto' : 'Takashi Yamamoto is the husband of Yumi Yamamoto. Yumi Yamamoto loves her husband and they both discuss daily happenings at the Shino Grocery Store and neighborhood, and local politics. They have dinner together.',
  'Kazuki Sato' : 'Kazuki Sato and Yumi Yamamoto know each other very well. They enjoy each others company and also have regular conversations and sometimes Kazuki visits Yamamoto Residence for dinner.',
  'Satoshi Takahashi': 'Yumi Yamamoto thinks that Satoshi Takahashi is not a good candidate for contesting local mayor elections.',
  'Yusuke Mori': 'Takashi Yamamoto calls Yusuke Mori only for repairing furniture or for creating new wooden pieces. Sometimes they meet each other at Mizukami Shrine and have small conversations.',
  'Ayumi Kimura': 'Yumi Yamamoto lives in the same neighborhood as Ayumi Kimura. Yumi Yamamoto thinks that Ayumi Kimura is an ideal candidate for local mayor elections.'
}

# adding relations
kazuki.relations = {
    'Yumi Yamamoto' : 'Kazuki Sato and Yumi Yamamoto know each other very well. They enjoy each others company and also have regular conversations and sometimes Kazuki visits Yamamoto Residence for dinner.',
    'Takeshi Yamamoto' : 'Kazuki and Takashi know each other and sometimes Kazuki visits Yamamoto Residence for dinner.',
    'Satoshi Takahashi': 'Kazuki Sato sees Satoshi Takahashi as a wise person and sometimes talks with him regarding advice on career and life.',
    'Yusuke Mori': 'Kazuki meets Yusuke Mori only when Yusuke comes to Kogaku Institute of Physics or Haya Apartments for some wooden work.',
    'Ayumi Kimura': 'Ayumi Kimura and Kazuki Sato know each other really well. They have talks in Kogaku Institute of Physics and meet each other everyday. Kazuki is Ayumi’s favorite student.'
}

# adding relations
satoshi.relations = {
    'Takashi Yamamoto' : 'Satoshi Takahashi does not like Takashi Yamamoto because of the differences in their political ideologies. Takashi Yamamoto thinks that Satoshi Takahashi is not an ideal candidate for the local mayor elections.',
    'Yumi Yamamoto' : 'Satoshi Takahashi and Yumi Yamamoto do not get along really well because of the differences in their local political thinking.',
    'Kazuki Sato': 'Satoshi Takahashi is kind of a mentor to Kazuki Sato and gives her advice regarding career and life.',
    'Yusuke Mori': 'Yusuke Mori and Satoshi Takahashi are good friends. They both interact at Mizukami Shrine. Yusuke Mori considers Satoshi Takahashi as an ideal candidate for the local mayor elections.',
    'Ayumi Kimura': 'Ayumi Kimura and Satoshi Takahashi know each other really well. They generally meet either in Hanazawa Park or Mizukami Shrine and have long and deep conversations together.',
}

# adding relations
yusuke.relations = {
    'Yumi Yamamoto' : 'Yumi Yamamoto and Yusuke Mori have good relations with each other. But their political thinking does not match. Yumi Yamamoto thinks Satoshi Takahashi is not an ideal candidate for the local mayor elections. Yusuke Mori thinks that Satoshi Takahashi is an ideal candidate for the local mayor elections.',
    'Kazuki Sato' : 'Yusuke Mori meets Kazuki only when Yusuke comes to Kogaku Institute of Physics or Haya Apartments for some wooden work.',
    'Satoshi Takahashi': 'Yusuke Mori and Satoshi Takahashi are good friends. They both interact at Mizukami Shrine. Yasuke respects Satoshi Takahashi and thinks that Satoshi is an ideal candidate for the local mayor elections.',
    'Takashi Yamamoto': 'Yusuke Mori meets Takashi Yamamoto only when Takashi calls him for any carpentry work. Yusuke also visits Yamamoto Residence for work.',
    'Ayumi Kimura': 'Ayumi Kimura and Yusuke Mori have bad relations with each other. Yusuke Mori does not like Ayumi Kimura as she blames that the contract of supplying furniture to Kogaku Institute of Physics should not be given to him as he offers high rates.'
}

# adding relations
ayumi.relations = {
    'Yumi Yamamoto' :  'Yumi Yamamoto lives in the same neighborhood as Ayumi Kimura. Yumi Yamamoto thinks that Ayumi Kimura is an ideal candidate for local mayor elections.',
    'Kazuki Sato' : 'Ayumi Kimura and Kazuki Sato know each other really well. They have talks in Kogaku Institute of Physics and meet each other everyday. Kazuki is Ayumi’s favorite student.',
    'Satoshi Takahashi': 'Ayumi Kimura and Satoshi Takahashi know each other really well. They generally meet either in Hanazawa Park or Mizukami Shrine and have long and deep conversations together.',
    'Yusuke Mori': 'Ayumi Kimura and Yusuke Mori have bad relations with each other. Ayumi thinks that the contract of supplying furniture to Kogaku Institute of Physics should not be given to Yusuke Mori, as Yusuke Mori offers high rates as compared to other contractors.',
    'Takashi Yamamoto': 'Ayumi Kimura lives in the same neighborhood as Takashi Yamamoto.'
}

for agent in agents:
 for (key, value) in agent.relations.items():
    agent.person.memory.add_memory(f"{key}:{value}")


#Adding basic plans of the agents in their memories

# Read a CSV file
df = pd.read_csv('villagers_plans.csv')
df['Time'] = pd.to_datetime(df['Time']).dt.time
# df.set_index('Time', inplace=True)
# column1 = df['Time']  # Replace 'Time' with the actual name of the first column

for agent in agents:
    agent.plans = df[['Time', agent.person.name]].copy()
    agent.plans.rename(columns = {agent.person.name: 'Plans'}, inplace=True)
    print("Plans of:", agent.person.name)
    print(agent.plans.head(1))
    print(agent.plans[agent.plans['Time'].apply(lambda x: x.hour) == 10]['Plans'].values[0])














# #Creating locations and adding their descriptions
# yamamoto_residence = Place("Yamamoto Residence", "The Yamamoto family's small house is located in Hayashino Town, serving as the residence of Takashi Yamamoto and Yumi Yamamoto", {})
# shino_grocery_store = Place("Shino Grocery Store", "Shino grocery Store is a vital hub in the community, offering a wide range of essential products for everyday living. From fresh produce and pantry staples to household goods and personal care items, the grocery store caters to diverse needs. People visit the grocery store and buy the daily needed items. With a commitment to sustainability, the grocery store encourages eco-friendly practices such as the use of reusable bags and supporting local farmers. In essence, the grocery store is a community cornerstone, providing a reliable source for everyday necessities. It is owned by Takashi Yamamoto.", {})
# haya_apartments = Place("Haya Apartments", "Haya Apartments, situated in Hayashino Town, is home to a diverse community of independent individuals and families. The apartments within the building are fully furnished and feature tasteful wooden furniture.", {})
# hanazawa_park = Place("Hanazawa Park", "Hanazawa Park is a place where people visit for exercising or walking. They also interact with new people and get new ideas. Hanazawa Park has wooden fencing around it. People get relaxed in Hanazawa Park. It has a large variety of trees and flowers", {})
# kogaku_physics = Place("Kogaku Institute of Physics", "Kogaku Institute of Physics, located in Hayashino, is a leading scientific institution dedicated to the study and exploration of physics. With cutting-edge facilities and a team of renowned researchers, it strives to advance our understanding of the physical world through rigorous experimentation and theoretical investigations", {})
# mizukami_shrine = Place("Mizukami Shrine", "A Japanese shrine is a sacred sanctuary steeped in tradition and spiritual significance. People visit shrines to worship God. Shrines serve as cultural touchstones, preserving Japan's ancient traditions and values. A visit to a Japanese shrine is a profound spiritual experience, offering a glimpse into the country's rich heritage and profound reverence", {})