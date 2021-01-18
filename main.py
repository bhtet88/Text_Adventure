from core_mechanics import *
from story import *
import random

### Creating player character and escaping the cell###

def escaping(player):
    """Function that is played only when the player takes any of the non-fighting situations. The player is given a few options but regardless of what they choose, they will eventually have to fight a guard and then escape their cell, where all pathways meet back up again."""
    print(planning)
    input()
    inspection = choices(planning_choices, "What will you do?")
    print()
    if inspection == 0: #Inspecting toilet
        print(inspect_toilet)
        input()
        toilet_choice = choices(["Do nothing", "Clog the toilet", "Throw water on the guard as they pass by"], "What will you do?")
        print()
        if toilet_choice == 0:
            return escaping(player)
        elif toilet_choice == 1: 
            print(toilet_clog)
        elif toilet_choice == 2:
            print(throw_water)
        input()
        guard_slip = choices(["Beat the guard up", "Rip off their helmet and slam their head on the stone bench"], "What will you do?")
        print()
        if guard_slip == 0:
            print(guard_beat)
            return
        elif guard_slip == 1:
            print(guard_smash)
            return
    elif inspection == 1: #Inspecting can of food
        print(inspect_food)
        input()
        food_choice = choices(["Do nothing", "Peel off the lid and try to sharpen it with the edge of other lids"], "What will you do?")
        print()
        if food_choice == 0:
            return escaping(player)
        elif food_choice == 1:
            print(food_lid)
            input()
            player.inventory_add(shank)
            print()
            food_choice = choices(["Bang on the walls, acting insane", "Lie down on the bench and moan as if you were in pain", "Insult the guard when they walk past"], "Now what will you do?")
            print()
            if food_choice == 0: #Act insane
                print(act_insane)
            elif food_choice == 1: #Moan
                print(moaning)
            elif food_choice == 2: #Insult guard
                choices(["'You really think I'll be here any longer?'", "'Hey asshole, you enjoy being the Federation's bitch?'", "'Bet you are content with your shitty life'", "'You wear that helmet because you look like shit huh?'", "'Hey, fuck you!'"], "What will you say?")
                print()
                print(guard_insult)
    elif inspection == 2: #Make a loud noise 
        print(act_insane)
    elif inspection == 3: #Insult the guard
        choices(["'You really think I'll be here any longer?'", "'Hey asshole, you enjoy being the Federation's bitch?'", "'Bet you are content with your shitty life'", "'You wear that helmet because you look like shit huh?'", "'Hey, fuck you!'"], "What will you say?")
        print()
        print(guard_insult)
    input()
    print(first_fight)
    input()
    cell = Cell()
    onward(player, cell)

name = input("You are thrown into a cold dark cell. You awake, dazed and confused. What is your name? ") #Player creation
player = Player(name)
generic_place = Place([0, 1])
player.place, generic_place.player = generic_place, player
print()
print(opening.format(player.name))
input()
print(footsteps)
input()
first_choice = choices(first_options, "What will you do?")
print() 
if first_choice == 0: #Player stops looking
    print(stop_looking.format(random.choice(["male", "female"])))
    input()
    escaping(player)
elif first_choice == 1: #Player continues to look at the hallway
    print(guard_description)
    input()
    print(caught_looking.format(random.randint(10000, 99999)))
    input()
    first_guard = choices(caught_looking_options, "What will you do?")
    print()
    if first_guard in [0, 1, 2, 3]: #Submitting to the guard
        print(guard_submit)
        input()
        escaping(player)
    elif first_guard == 4: #Offending the guard
        print(guard_offend)
        input()
        offend_decision = choices(punish_choices, "What will you do?")
        print()
        if offend_decision == 2: #Chance for the player to escape their cell early, although it will be very difficult
            cell = Cell()
            onward(player, cell)
        elif offend_decision in [0, 1]:
            print(guard_punish) 
            input()
            escaping(player)

input()
print(escape)