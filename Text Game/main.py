from core_mechanics import *
from story import *

# Creating player character

name = input("You are an adventurer and just arrived at the airport of a little known European city. What is your name adventurer?")
player = Player(name)

print("\n" + opening.format(player.name))

print("\n" + store_intro.format(player.weight_limit, player.wallet))

#Purchasing from the store

