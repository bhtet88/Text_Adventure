from core_mechanics import *
from story import *

### Creating player character ###

name = input("You are an adventurer and just arrived at the airport of a little known European city. What is your name adventurer? ")
player = Player(name)

print("\n" + opening.format(player.name))

print("\n" + store_intro.format(player.weight_limit, player.wallet))
print("")
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
    command = input("What do you want to do? Type 'Buy' or 'Refund' followed by the name of the item or type 'Done' to leave the store and start your journey. ")
    command = fixed_input(command)
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