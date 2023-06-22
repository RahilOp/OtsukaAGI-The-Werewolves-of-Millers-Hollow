from utils import generate_response,print_colored,create_new_memory_retriever,LLM
from initialize import df,takashi,yumi,kazuki,satoshi,yusuke,ayumi,yamamoto_residence,shino_grocery_store,haya_apartments,hanazawa_park,kogaku_physics,mizukami_shrine



# Main function to carry on the simulation
def main():
    agents = [takashi, yumi]
    locations = [yamamoto_residence, shino_grocery_store, haya_apartments, hanazawa_park, kogaku_physics, mizukami_shrine]

    for global_time in df['Time']:
        print_colored(f"Global time is: {global_time}", "magenta")
    # people finding on the location and print them
    people = {}
    for location in locations:
        print_colored(f"Location: {location.name}", "blue")
        people[location.name] = []
        for agent in agents:
          if agent.location == location.name:
            people[location.name].append(agent)
        for (num, p) in enumerate(people[location.name]):
            print_colored(f"{num+1}. {p.person.name}", "black")

    for location in locations:
        print("\n\n")
        print_colored(f"{location.name}", "blue")
        # Doing Tasks
        print_colored("Doing Tasks", "red")
        # each agent first does its task at this location
        agent_list = people[location.name]
        for (num, local_agent) in enumerate(agent_list):
         print_colored(f"{num+1}. {local_agent.person.name}", "sky blue")
        _, reaction = local_agent.person.generate_reaction(local_agent.plans[global_time])
        print_colored(f"Task: {local_agent.plans[global_time]}", "sky blue")
        print_colored(f"Reaction: {reaction}", "green")

        print_colored("Interaction", "red")
        for i in range(0, len(agent_list)):
         for j in range(i+1, len(agent_list)):
            print_colored(f"Dialogue between {agent_list[i].person.name} and {agent_list[j].person.name}:", "cyan")
            agent_list[i].make_interaction(global_time,[agent_list[j]], "")

        location_result = generate_response("The person is {} with the profile: {}. He is currently at {}. His memory is having {}, his plans are {}. Based on these informations, can you predict the most probable location out of the locations: {}, where he would be in the next hour? Answer in following format: 'Location_Name'".format(
                                            takashi.person.name, takashi.profile, takashi.location, takashi.person.get_summary(),takashi.plans,locations))
        print(takashi.person.name, location_result)

        new_location = ""
        for location in locations:
           for i in range(0,len(location_result)):
              if location.name == location_result[i:i+len(location.name)]:
                 new_location = location.name
                 break 

        agent_list[i].update_location(new_location)


if __name__ == "__main__":
    main()

