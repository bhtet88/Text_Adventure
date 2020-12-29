from core_mechanics import *
from story import *

### Creating player character ###

name = input("You are an adventurer and just arrived at the airport of a little known European city. What is your name adventurer? ")
player = Player(name)

print("\n" + opening.format(player.name))
print("\n" + store_intro.format(player.weight_limit, player.wallet))
input("")

### Purchasing from the store ###

store = Store()
store.add_inventory(store_list) ### Implement list of store items once the specific items are created

def buying(player, store):
    """Function that allows the player to purchase items from the store. Player can either buy an item, refund an item, or type "Done" to finalize their purchase and start their adventure. Raises an Invalid Input message if the input is one word that is not 'Done' 
    or if it's multiple words that are not a valid command. The except case handles the first issue and the else case handles the second issue.  
    """
    store.show_inventory()
    print("")
    player.show_backpack()
    print("")
    command = fixed_input(input("What do you want to do? Type 'Buy' or 'Refund' followed by the name of the item or type 'Done' to leave the store and start your journey. "))
    try:
        action = command.split(" ", 1)[0]
        if action == "done":
            return
        item_name = command.split(" ", 1)[1]
        if action == "buy":
            store.purchase(player, item_name)
            print("")
            return buying(player, store)
        elif action == "refund":
            store.refund(player, item_name)
            print("")
            return buying(player, store)
        else:
            print("Invalid input, try again")
            print("")
            return buying(player, store)
    except:
        print("Invalid input. If buying or refunding, make sure to type in the action followed by the name of the item")
        print("")
        return buying(player, store)

buying(player, store)

### Start of journey ###

print("")
print(village_arrive)
input("") #Adds pause to prevent overwhelming text chunks
print(village_depart)

decision = fixed_input(input("Will you go onward? Is it worth it? "))
while decision != "yes":
    if decision == "no":
        print("")
        print(early_end)
        quit()
    print("Invalid input, try again")
    decision = fixed_input(input("Will you go onward? Is it worth it? "))

print("")
print(moving_forward)
input("")

print(the_wall)
def wall_decision(player):
    """Function facilitating the choice the player makes when encountering the wall"""
    wall_choice = fixed_input(input("What will you do? If you want to look at or use something in your backpack, first type 'Open backpack'. "))
    wall_forward = ["go forward", "press on", "move onwards", "move through", "forward", "go in", "go through wall", "move through wall", "move forward", "step forward"] #Valid inputs for moving forward
    wall_retreat = ["run away", "run", "leave", "go back", "return to village", "go home"] #Valid inputs for leaving the situation, causing an early ending
    if wall_choice in wall_forward:
        print("")
        print(wall_onwards)
        return
    elif wall_choice in wall_retreat:
        print("")
        print(wall_end)
        quit()
    elif wall_choice == "open backpack":
        print("")
        item = player.use_backpack() #Function returns an item from the backpack 
        if not item:
            print("")
            return wall_decision(player)
        else:
            if item.name.lower() == "boomerang": #Player uses the boomerang to see if it can return through the cloud, giving more info and some illusion of player choice.
                print("")
                print(wall_boomerang)
            else:
                print("You look at the item you are holding but you can't figure out how this will assist you.")
            print("")
            return wall_decision(player)
    else:
        print("Invalid input, try again")
        print("")
        return wall_decision(player)

wall_decision(player)

### First encounter ###

