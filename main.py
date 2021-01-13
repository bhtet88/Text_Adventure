from core_mechanics import *
from story import *
import random

### Creating player character ###
name = input("You are an adventurer and just arrived at the airport of a little known European city. What is your name adventurer? ")
player = Player(name)
generic_place = Place([0, 1])
player.place, generic_place.player = generic_place, player

print("\n" + opening.format(player.name))
print("\n" + store_intro.format(player.weight_limit, player.wallet))
input("")

### Purchasing from the store ###

store = Store()
store.add_inventory(store_list) ### Implement list of store items once the specific items are created

store.buying(player)

### Start of journey ###

print("")
print(village_arrive)
input("") #Adds pause to prevent overwhelming text chunks
print(village_depart)
print("")
player.backpack_add(knife)
player.backpack_add(rope)

print("")
print("You take one final look at civilization, wondering if this was the right choice.")
print("")
decision = fixed_input(input("Will you go onward? Is it worth it? "))
while decision != "yes":
    if decision == "no":
        print("")
        print(early_end)
        quit()
    print("")
    print("Invalid input, try again")
    print("")
    decision = fixed_input(input("Will you go onward? Is it worth it? "))

print("")
print(moving_forward)
input("")

print(the_wall)
def wall_decision(player):
    """Function facilitating the choice the player makes when encountering the wall"""
    print("")
    wall_choice = fixed_input(input("What will you do? If you want to look at or use something in your backpack, first type 'Open backpack'. "))
    wall_forward = ["go forward", "press on", "move onwards", "move through", "forward", "go in", "go through wall", "move through wall", "move forward", "step forward", "go through", "walk forward", "walk", "move on", "continue"] #Valid inputs for moving forward
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
            elif item.name.lower() == "rope":
                print("")
                print(wall_rope)
            else:
                print("")
                print("You look at the item you are holding but you can't figure out how this will assist you.")
            return wall_decision(player)
    else:
        print("")
        print("Invalid input, try again")
        return wall_decision(player)

wall_decision(player)
input()

### The Forest ###

print(first_encounter_1)
input("")
print(random.choice(Legionary.battle_lines))
input("")
print(first_encounter_2)
input()

tut_place = Forest_Place([1, 0])
tut_place.enemies = []
tut_place.add_enemy(enemy_constructor("Legionary"))
onward(player, tut_place)

print("")
print(first_encounter_end)
print("")
print("You have just begun your journey in the forest. The forest is very dense, decreasing your range by {0} units but your determination to survive also gives you an extra {1}% points of damage.".format(abs(Forest_Place.range_bonus), int(Forest_Place.damage_bonus * 100)))

times = 1
while times:
    input()
    place = Forest_Place()
    onward(player, place)
    times -= 1

boss_merchant = Forest_Place([0, 1])
boss_merchant.event = Merchant()
input()
onward(player, boss_merchant)

print()
print(boss1_intro1)
input()
print(boss1_intro2)
input()

boss1 = Forest_Place([1, 0])
boss1.size, boss1.enemies = 11, []
boss1.add_enemy(enemy_constructor("Giant_Snake"))
onward(player, boss1)

print(boss1_end)
input()

### The Caves ###

print("You have made it to the tunnels. The tunnels are very dark, decreasing your range by {0} units. However, due to the darkness of the tunnels, you have a {1}% chance to evade encounters entirely.".format(abs(Tunnel_Place.range_bonus), Tunnel_Place.dodge_chance))
input()
print(tunnel_start)
while True:
    print()
    decision = fixed_input(input("Will you reduce the beam of your flashlight? "))
    print()
    if decision == "yes":
        print(light_lower)
        tunnel_1 = Tunnel_Place([0, 1])
        break
    elif decision == "no":
        print(light_same)
        tunnel_1 = Tunnel_Place([1, 0])
        break
    else:
        print("Invalid input, try again")
input()
onward(player, tunnel_1)
times = 6
while times:
    input()
    place = Tunnel_Place()
    onward(player, place)
    times -= 1
boss_merchant = Tunnel_Place([0, 1])
boss_merchant.event = Merchant()
input()
onward(player, boss_merchant)
print(tunnel_end)
input()

### The Cliffs ###

print("""You are now at the perilous cliffs. The cliffs are wide and open, allowing you to clearly see what is up ahead, giving you a range increase of {0} units. Since you are taking every step carefully, you can only take 1 step per turn and 
cannot change this with item effects.""".format(Cliff_Place.range_bonus))
input()
print(cliffs_intro)
times = random.randint(5, 6)
while times:
    input()
    place = Cliff_Place()
    onward(player, place)
    times -= 1
boss_merchant = Cliff_Place([0, 1])
boss_merchant.event = Merchant()
input()
onward(player, boss_merchant)
print(boss2_intro)
input()
print(boss2_intro2)
boss2 = Cliff_Place([1, 0])
boss2.size, boss2.enemies = 11, []
boss2.add_enemy(enemy_constructor("Alpha_Harpy"))
onward(player, boss2)
print(boss2_end)
input()

### The Town ###

print(town_intro)

### The Machine Labs ###

### The Mage Dens ###

### The College ###

### The Hospital ###

### The Senate ### 

### The Imperial Palace ###

### Final Fight ###