from core_mechanics import *
from story import *
import random

### Creating player character ###

name = input("You are an adventurer and just arrived at the airport of a little known European city. What is your name adventurer? ")
player = Player(name)
generic_place = Place("Tutorial")
player.place, generic_place.player = generic_place, player

print("\n" + opening.format(player.name))
print("\n" + store_intro.format(player.weight_limit, player.wallet))
input("")

### Purchasing from the store ###

store = Store()
store.add_inventory(store_list) ### Implement list of store items once the specific items are created

buying(player, store)

### Start of journey ###

print("")
print(village_arrive)
input("") #Adds pause to prevent overwhelming text chunks
print(village_depart)
print("")
player.backpack_add(knife)

print("")
print("You take one final look at civilization, wondering if this was the right choice.")
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
    print("")
    wall_choice = fixed_input(input("What will you do? If you want to look at or use something in your backpack, first type 'Open backpack'. "))
    wall_forward = ["go forward", "press on", "move onwards", "move through", "forward", "go in", "go through wall", "move through wall", "move forward", "step forward", "go through", "walk forward", "walk", "move on"] #Valid inputs for moving forward
    wall_retreat = ["run away", "run", "leave", "go back", "return to village", "go home", "walk away", "step back"] #Valid inputs for leaving the situation, causing an early ending
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
            return wall_decision(player)
        else:
            if item.name.lower() == "boomerang": #Player uses the boomerang to see if it can return through the cloud, giving more info and some illusion of player choice.
                print("")
                print(wall_boomerang)
            else:
                print("")
                print("You look at the item you are holding but you can't figure out how this will assist you.")
            return wall_decision(player)
    else:
        print("")
        print("Invalid input, try again")
        return wall_decision(player)

wall_decision(player)
input("")

### First encounter ###

print(first_encounter_1)
input("")
print(random.choice(Legionary.battle_lines))
input("")
print(first_encounter_2)
input()

tut_place = Jungle_Place("Tutorial", 4)
onward(player, tut_place)

print("")
print(first_encounter_end)

times = random.randint(5, 7)
while times:
    input()
    place = Jungle_Place()
    onward(player, place)
    times -= 1