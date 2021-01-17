from core_mechanics import *
from story import *
import random

### Creating player character and escaping the cell###
name = input("You are thrown into a cold dark cell by unknown forces. You awake, dazed and confused. What is your name? ") #Player creation
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
elif first_choice == 1: #Player continues to look at the hallway
    print(guard_description)
    input()
    print(caught_looking)
    input()
    first_guard = choices(caught_looking_options, "What will you do?")
    print()
    if first_guard in [0, 1, 2, 3]: #Submitting to the guard
        print(guard_submit)
    elif first_guard == 4: #Offending the guard
        print(guard_offend)
        input()
        offend_decision = choices(punish_choices, "What will you do?")
        print()
        if offend_decision == 0: #Chance for the player to escape their cell early, although it will be very difficult
            cell = Cell()
            onward(player, cell)
        elif offend_decision in [1, 2]:
            print(guard_punish)