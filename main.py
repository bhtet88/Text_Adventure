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
    """Function that allows the player to purchase items from the store. Player can either buy an item, refund an item, or type "Done" to finalize their purchase and start their adventure.
    """
    store.show_inventory()
    print("")
    action = input("What do you want to do? Type 'Buy' to buy something, 'Refund' to refund something you bought, or 'Done' to leave the store and start your journey. ")
    action = fixed_input(action)
    if action == "buy":
        print("")
        item_name = input("What do you want to buy? ")
        item_name = fixed_input(item_name)
        store.purchase(player, item_name)
        print("")
        return buying(player, store)
    elif action == "refund":
        print("")
        player.show_backpack()
        item_name = input("What do you want to refund? ")
        item_name = fixed_input(item_name)
        store.refund(player, item_name)
        print("")
        return buying(player, store)
    elif action == "done":
        return
    else:
        print("Invalid input, try again")
        print("")
        return buying(player, store)

buying(player, store)