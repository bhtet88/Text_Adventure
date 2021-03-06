from core_mechanics import *
from story import *
import random
import textwrap

wrapper = textwrap.TextWrapper(width=100)

### Creating player character and escaping the cell ###

def escaping(player):
    """Function that is played only when the player takes any of the non-fighting situations. The player is given a few options but regardless of what they choose, they will eventually have to fight a guard and then escape their cell, where all pathways meet back up again."""
    print(wrapper.fill(planning))
    input()
    inspection = choices(planning_choices, "What will you do?")
    print()
    if inspection == 0: #Inspecting toilet
        print(wrapper.fill(inspect_toilet))
        input()
        toilet_choice = choices(["Do nothing", "Clog the toilet", "Throw water on the guard as they pass by"], "What will you do?")
        print()
        if toilet_choice == 0:
            return escaping(player)
        elif toilet_choice == 1: 
            print(wrapper.fill(toilet_clog))
        elif toilet_choice == 2:
            print(wrapper.fill(throw_water))
        input()
        guard_slip = choices(["Beat the guard up", "Rip off their helmet and slam their head on the stone bench"], "What will you do?")
        print()
        if guard_slip == 0:
            print(wrapper.fill(guard_beat))
            return
        elif guard_slip == 1:
            print(wrapper.fill(guard_smash))
            return
    elif inspection == 1: #Inspecting can of food
        print(wrapper.fill(inspect_food))
        input()
        food_choice = choices(["Do nothing", "Peel off the lid and try to sharpen it with the edge of other lids"], "What will you do?")
        print()
        if food_choice == 0:
            return escaping(player)
        elif food_choice == 1:
            print(wrapper.fill(food_lid))
            input()
            player.inventory_add(eval(shank))
            print()
            food_choice = choices(["Bang on the walls, acting insane", "Lie down on the bench and moan as if you were in pain", "Insult the guard when they walk past"], "Now what will you do?")
            print()
            if food_choice == 0: #Act insane
                print(wrapper.fill(act_insane))
            elif food_choice == 1: #Moan
                print(wrapper.fill(moaning))
            elif food_choice == 2: #Insult guard
                choices(["'You really think I'll be here any longer?'", "'Hey asshole, you enjoy being the Federation's bitch?'", "'Bet you are content with your shitty life'", "'You wear that helmet because you look like shit huh?'", "'Hey, fuck you!'"], "What will you say?")
                print()
                print(wrapper.fill(guard_insult))
    elif inspection == 2: #Make a loud noise 
        print(wrapper.fill(act_insane))
    elif inspection == 3: #Insult the guard
        choices(["'You really think I'll be here any longer?'", "'Hey asshole, you enjoy being the Federation's bitch?'", "'Bet you are content with your shitty life'", "'You wear that helmet because you look like shit huh?'", "'Hey, fuck you!'"], "What will you say?")
        print()
        print(wrapper.fill(guard_insult))
    input()
    print(wrapper.fill(first_fight))
    input()
    cell = Cell()
    onward(player, cell)

### Game Start ###
name = input("You are thrown into a cold dark cell. You awake, dazed and confused. What is your name? ") #Player creation
player = Player(name)
generic_place = Place([0, 1])
player.place, generic_place.player = generic_place, player
print()
print(wrapper.fill(opening.format(player.name)))
input()
print(wrapper.fill(footsteps))
input()
first_choice = choices(first_options, "What will you do?")
print() 
if first_choice == 0: #Player stops looking
    print(wrapper.fill(stop_looking.format(random.choice(["male", "female"]))))
    input()
    escaping(player)
elif first_choice == 1: #Player continues to look at the hallway
    print(wrapper.fill(guard_description))
    input()
    print(wrapper.fill(caught_looking.format(random.randint(10000, 99999))))
    input()
    first_guard = choices(caught_looking_options, "What will you do?")
    print()
    if first_guard in [0, 1, 2, 3]: #Submitting to the guard
        print(wrapper.fill(guard_submit))
        input()
        escaping(player)
    elif first_guard == 4: #Offending the guard
        print(wrapper.fill(guard_offend))
        input()
        offend_decision = choices(punish_choices, "What will you do?")
        print()
        if offend_decision == 2: #Chance for the player to escape their cell early, although it will be very difficult
            cell = Cell()
            onward(player, cell)
        elif offend_decision in [0, 1]:
            print(wrapper.fill(guard_punish)) 
            input()
            escaping(player)

### Escape ###

input()
print(wrapper.fill(escape))
input()
if shank in player.inventory:
    player.inventory_remove(shank)
    print()
player.inventory_add(eval(stun_baton))
player.armor += 60
input()
Prison_Guard.can_drop = True
cell = Cell()
onward(player, cell)
input()
print(wrapper.fill(spotted))
input()
print(wrapper.fill(pa_voice))
input()
print(wrapper.fill(alarm_sounded))
input()

### Fighting through Lower Prison ###

revolt = choices(["Gear yourself up and don't free the prisoners", "Free the prisoners in your wing"], "What will you do?")
print()
if revolt == 1:
    print(wrapper.fill(free_wing8))
    Lower_Prison.max_enemies = 2
elif not revolt:
    print(wrapper.fill(forget_wing8))
    player.armor += 100
encounters = 4
while encounters:
    input()
    place = Lower_Prison()
    onward(player, place)
    encounters -= 1
input()
if revolt == 1: #Revolt
    print(wrapper.fill(lower_section_revolt))
    input()
    print(wrapper.fill(lower_section_pa))
    input()
    print(wrapper.fill(lower_section_ascend_revolt))
elif not revolt: #Solo escape
    print(wrapper.fill(lower_section_solo))
    input()
    print(wrapper.fill(lower_section_report))
    input()
    print(wrapper.fill(lower_section_ascend_solo))

### Level C ###

input()
print(wrapper.fill(levelc_intro))
if revolt == 1:
    Main_Prison_Initial.max_enemies = 2
fights = 0
while fights:
    input()
    place = Main_Prison_Initial()
    onward(player, place)
    fights -= 1
input()
print(wrapper.fill(guards_retreat.format(("You prove to be more than a match for these guards all by yourself." if not revolt else "You and the prisoners show how capable you are, overpowering the guards almost instantly."), ("prisoner is" if not revolt else "prisoners are"))))
input()
print(wrapper.fill(levelc_rest_solo if not revolt else levelc_rest_revolt))
print()
stims = 4
while stims:
    player.inventory_add(eval(stim))
    stims -= 1
print()
player.inventory_add(eval(pistol))
player.armor += 100
player.move_speed += 1
input()
print(wrapper.fill(levelc_reinforcements))
input()
print(wrapper.fill(reinforcement_intimidation.format(("prisoner" if not revolt else "prisoners"))))
if revolt == 1:
    Main_Prison.max_enemies = 2
fights = 6
while fights:
    input()
    place = Main_Prison()
    onward(player, place)
    fights -= 1

### Volk ###

input()
if not revolt:
    print(wrapper.fill(volk_intro_solo))
else:
    print(wrapper.fill(volk_intro_revolt))
input()
print(wrapper.fill(volk_option))
input()
volk_choice = choices(volk_dialogue, "What will you say?")
print()
if volk_choice in [0, 1]: #Surrendering to Volk gives an early end
    print("'Very well, follow me. We have plenty of training to do. Command, this is Volkov. Situation has been resolved. Prisoner is now under my authority.'")
    input()
    print(wrapper.fill(volk_surrender))
    input()
    quit()
print(wrapper.fill(volk_fight))
input()
onward(player, Volk_Fight())
input()
print(wrapper.fill(volk_death))

### Labs ###

input()
print(wrapper.fill(labs_intro))
input()
print(wrapper.fill(first_machine))
input()
onward(player, Machine_Labs([1, 0]))
events = 6
while events:
    input()
    onward(player, Machine_Labs())
    events -= 1
input()
print(wrapper.fill(GI_room))
input()
print(wrapper.fill(GI_PA))
input()
print(wrapper.fill(GI_intro))
input()
print(wrapper.fill(GI_start))
input()
onward(player, GI_Boss())
input()
print(wrapper.fill(GI_defeated))
input()
print(wrapper.fill(AMR_discovered))
input()
print(wrapper.fill(AMR_file))
input()
print(wrapper.fill(AMR_take))
input()
x50 = eval(amr)
player.weight_limit += x50.weight
player.inventory_add(x50)

### Final Area ###

input()
print(wrapper.fill(level_a_intro))
input()
saying = choices(final_choice, "What will you say?")
print()
print("Taking a deep breath, you prepare your weapons and smash through the door, ready to earn your freedom!")
for x in range(2):
    input()
    onward(player, Outside())
input()
onward(player, Final_Tanks())
input()
print(wrapper.fill(end))