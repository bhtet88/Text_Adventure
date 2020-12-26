import random

### Equipment Classes ###

class Equipment:
    """Parent class for the equipment the player can carry. Each equipment has a specific weight and price
    >>> x = Equipment(5, 10)
    >>> x.weight
    5
    >>> x.price
    10
    >>> print(x)
    Weight: 5 lbs, Price: 10 coins
    >>> x
    Equipment
    """
    class_type = "Equipment"
    
    def __init__(self, weight, price, name=None):
        self.weight = weight
        self.price = price
        self.name = name

    def __repr__(self):
        if not self.name:
            return self.class_type
        return self.name
    
    def __str__(self):
        return "Weight: {0} lbs, Price: {1} coins".format(self.weight, self.price)

class Weapon(Equipment): 
    """Weapons that the player and enemies can use to fight with. Each weapon has damage, range, weight, and price. Some weapons can have an armor piercing ability
    >>> x = Weapon(100, 50, 10, 250)
    >>> x.damage 
    100
    >>> x.range
    50
    >>> x.weight 
    10
    >>> x.price
    250
    >>> x.armor_piercing
    False
    >>> print(x)
    Damage: 100, Range: 50 units, Weight: 10 lbs, Armor Piercing: False, Price: 250 coins
    >>> x
    Weapon
    """
    armor_piercing = False
    class_type = "Weapon"
    
    def __init__(self, damage, range, weight, price, name=None):
        Equipment.__init__(self, weight, price, name)
        self.damage = damage
        self.range = range
    
    def __str__(self):
        return "Damage: {0}, Range: {1} units, Weight: {2} lbs, Armor Piercing: {3}, Price: {4} coins".format(self.damage, self.range, self.weight, self.armor_piercing, self.price)

class Healing_Tool(Equipment):
    """Healing equipment for the player to regain health. Each healing equipment has healing amount, number of uses, weight, and price
    >>> x = Healing_Tool(30, 1, 0.5, 12)
    >>> x.weight
    0.5
    >>> x.heal_amount
    30
    >>> x.price
    12
    >>> x.uses
    1
    >>> print(x)
    Heal Amount: 30 HP, Uses Left: 1, Weight: 0.5 lbs, Price: 12 coins
    >>> x
    Healing Equipment
    """
    class_type = "Healing Equipment"

    def __init__(self, heal_amount, uses, weight, price, name=None):
        Equipment.__init__(self, weight, price, name)
        self.heal_amount = heal_amount
        self.uses = uses

    def __str__(self):
        return "Heal Amount: {0} HP, Uses Left: {1}, Weight: {2} lbs, Price: {3} coins".format(self.heal_amount, self.uses, self.weight, self.price)

### Store Class ###

class Store:
    """Class for the store at the beginning of the game, which gives players the only chance to buy equipment before going on their journey. A store has an inventory of items, which are in the form of a dictionary where 
    the keys are the name of the item and the values are the object instances themselves.
    >>> x = Store()
    >>> x.items
    {}
    >>> x
    Store instance
    >>> print(x)
    Store selling []
    """

    def __init__(self, items = {}):
        self.inventory = items

    def add_inventory(self, lst):
        """Takes in a list of equipment instances and adds them to the store's inventory, which is a dictionary. Keys are the name of the weapon (all lowercase) and the values are equipment instances themselves. If multiple
        of the same equipment is being added, create a new key for each of them. This will make deletion easier in the future.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> store = Store()
        >>> store.add_inventory([spear])
        >>> store.inventory
        {"spear": Spear}
        """
        for x in lst:
            self.inventory[x.name.lower()] = [x]
    
    def remove_inventory(self, item_name):
        """Removes an instance of an object from the store inventory. If there are no more object instances for a key, remove that key. item_name is a lowercase string version of the name of the item being removed.
        >>> weapon = Weapon(20, 1, 1, 100, "Spear")
        >>> store = Store({"spear": weapon})
        >>> store.inventory
        {"spear": weapon}
        >>> store.remove_inventory(self, "spear")
        >>> store.inventory
        {}
        """
        if item_name in self.inventory:
            del self.inventory[item_name]

    def purchase(self, player, item):
        """Allows for the player to purchase an item from the store. Must check to see if the player can carry an item and if the player has enough money to buy it.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> expensive_weapon = Weapon(20, 1, 1, 2000, "Expensive")
        >>> heavy_weapon = Weapon(20, 1, 100, 100, "Heavy")
        >>> player = Player("Dan")
        >>> store = Store()
        >>> store.purchase(player, spear)
        Item not in store
        >>> store.inventory = [spear, expensive_weapon, heavy_weapon]
        >>> store.purchase(player, spear)
        Purchased Spear for 100 coins
        Wallet: 900
        >>> store.purchase(player, expensive_weapon)
        Not enough money
        >>> store.purchase(player, heavy_weapon)
        Adding item would go over the weight limit
        """
        if item not in self.inventory:
            print("Item not in store")
        elif player.wallet < item.price:
            print("Not enough money")
        elif player.weight_limit - player.current_weight < item.weight:
            print("Adding item would go over the weight limit")
        else:
            player.backpack_add(item)
            player.wallet -= item.price

        
        

    def refund(self, player, item): 
        """Allows for the player to refund an item to the store, placing that item back into the store's inventory and adding the price of the item back to the player's wallet.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> store = Store()
        >>> player = Player("Dan")
        >>> player.backpack_add(spear)
        Added Spear
        >>> store.refund(player, spear)
        Spear refunded for 100 coins
        >>> player.wallet
        1100
        """
        if item in player.backpack:
            self.inventory.append(item)
            player.backpack_remove(item)
            player.wallet += item.price
            print("{0} refunded for {1} coins".format(item.name, item.price))
        else:
            print("Item does not exist in your backpack")
    
    def __repr__(self):
        return "Store instance"

    def __str__(self):
        goods = []
        for item in self.inventory.values():
            goods.append(item.name)
        return "Store selling {0}".format(str(goods))

### Creature Class ###

class Entity:
    """Parent class for all characters in the game, including players and enemies. Other characters inherit from this class
    >>> x = Entity(150, 100)
    >>> x.health
    150
    >>> x.armor 
    100
    >>> print(x)
    Health: 150, Armor: 100
    >>> x
    Entity
    """
    class_type = "Entity"

    def __init__(self, health, armor, place = None):
        self.health = health
        self.armor = armor
        self.place = place

    def damaged(self, amount):
        """Reduces the entity's current health and armor, taking into account the special attributes of the weapons and equipment when applicable. Remove the enemy from the game when defeated."""
        self.health -= amount
        if self.health <= 0:
            self.remove_place()

    def add_place(self, place):
        """Adds an entity instance to a specific place."""

    def remove_place(self, place):
        """Removes the current entity from the current place when their health hits zero."""

    def __repr__(self):
        return self.class_type

    def __str__(self):
        return "Health: {0}, Armor: {1}".format(self.health, self.armor)

class Player(Entity):
    """Class for the player of the game, which is able to do certain actions that enemies cannot do. 
    Has a backpack with a certain weight capacity
    >>> x = Player("Dave")
    >>> x.backpack
    []
    >>> x.current_weight 
    0
    >>> x
    Player: (Dave, 100)
    >>> print(x)
    Name: Dave, Health: 100, Armor: 0, Current Weight: 0 lbs, Carrying Capacity: 70 lbs
    """
    class_type = "Player"
    
    def __init__(self, name, health=100, armor=0):
        Entity.__init__(self, health, armor)
        self.position = None 
        self.name = name
        self.backpack = []
        self.current_weight = 0
        self.weight_limit = 70
        self.wallet = 1000

    def backpack_add(self, item):
        """Adds item to the player's backpack as long as adding the weight of the item does not cause the current weight to exceed the weight_limit.
        >>> player = Player("Dan")
        >>> x = Weapon(20, 1, 5, 50)
        >>> player.backpack_add(x)
        Added Weapon
        >>> z = Weapon(20, 1, 75, 50)
        >>> player.backpack_add(z)
        Weight limit exceeded. Remove items to add this
        """
        if self.weight_limit - self.current_weight >= item.weight:
            self.backpack.append(item)
            self.current_weight = sum([x.weight for x in self.backpack])
            print("Added {0}".format(item.name))
        else:
            print("Weight limit exceeded. Remove items to add this")

    def backpack_remove(self, item):
        """Allows for the removal of an item from the player's backpack. Takes in a piece of equipment as an argument
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> player = Player("Dan")
        >>> player.backpack_add(spear)
        Added Spear
        >>> player.backpack
        [Spear]
        >>> player.backpack_remove(spear)
        Spear removed
        >>> player.backpack 
        []  
        """
        if item in self.backpack:
            self.backpack.remove(item)
            print("{0} removed").format(item.name)
        else:
           print("Equipment not in backpack")
            


    def __repr__(self):
        return "{0}: ({1}, {2})".format(self.class_type, self.name, self.health)
    
    def __str__(self):
        return "Name: {0}, Health: {1}, Armor: {2}, Current Weight: {3} lbs, Carrying Capacity: {4} lbs".format(self.name, self.health, self.armor, self.current_weight, self.weight_limit)

### Enemy Classes ###

class Enemy(Entity):
    """Class for the enemies and creatures that the player fights against. Each enemy subclass also has a move method that has the logic for how to play each turn when in battle. Each enemy
    has a health, armor, damage, range, and movement speed attribute. 
    >>> x = Enemy(100, 100, 50, 1, 1)
    >>> x.damage
    50
    >>> x.move_speed
    1
    >>> print(x)
    Name: Enemy, Health: 100, Armor: 100, Damage: 50, Range: 1 units, Move Speed: 1 units per turn
    >>> x 
    Enemy: (100, 100)
    """
    class_type = "Enemy"

    def __init__(self, health, armor, damage, range, move_speed):
        Entity.__init__(self, health, armor)
        self.position = None
        self.damage = damage
        self.range = range
        self.move_speed = move_speed

    def __repr__(self):
        return "{0}: ({1}, {2})".format(self.class_type, self.health, self.armor)

    def __str__(self):
        return "Name: {0}, Health: {1}, Armor: {2}, Damage: {3}, Range: {4} units, Move Speed: {5} units per turn".format(self.class_type, self.health, self.armor, self.damage, self.range, self.move_speed)

class Legionary(Enemy):
    """First enemies that the player encounters: Undead Legionaries kept alive by a successful experiment with magic, with the side effect of making them accelerate mental degredation. They have no special abilities,
    only a dagger and shield. 
    >>> x = Legionary(100, 50, 20, 1, 1)
    >>> x.damage 
    20
    >>> x
    Legionary: (100, 50)
    >>> print(x)
    Name: Legionary, Health: 100, Armor: 50, Damage: 20, Range: 1 units, Move Speed: 1 units per turn
    """
    class_type = "Legionary"

class Immortal_Dog(Enemy):
    """Using the same magic that keeping the Legionaries alive, these dogs are loyal to their undead human allies. Can move up to 2 steps per turn but deal very little damage. 
    >>> x = Immortal_Dog(75, 0, 10, 1, 2)
    >>> print(x)
    Name: Immortal Dog, Health: 75, Armor: 0, Damage: 10, Range: 1 units, Move Speed: 2 units per turn
    >>> x
    Immortal Dog: (75, 0)
    """
    class_type = "Immortal Dog"

### Place Class ###

class Place:
    """Place class that is made up of a randomized set of tiles. Places can be visualized as a B x 1 grid, where B is an integer. Can randomly contain an enemy or event. 
    A place can have up to 3 enemies at a time. The player starts at the first tile of the place and the enemies start on the opposite side. Each place has at least a size (default length 4) attribute to initialize it.
    """
    
    def __init__(self, size = 4):
        self.size = size

    def __repr__(self):
        return "Place"

    def __str__(self):
        return "Place, Size: {0}".format(self.size)

class Enemy_Room(Place):
    """Room containing up to 3 enemies. If the player enters an enemy room, a battle will automatically begin, with the enemies on the opposite side of the room as the player."""

    def __init__(self, size = 4):
        Place.__init__(self, size)
        self.enemies = []
        opponent_count = random.randint(1, 3)
        for x in range(opponent_count):
            random.choice() #Randomly select from a list of potential enemies, COME BACK ONCE ENEMIES ARE CREATED

class Event_Room(Place):
    """Room with randomly selected treasure that the player can pick up if they choose."""

    def __init__(self, size = 4):
        Place.__init__(self, size)
        self.event = random.choice() #Random selection from a list of potential hazards, COME BACK TO THIS

### Event Classes ###

class Event:
    """Parent class for the random events in the game, which can be a puzzle, a hazard, or an enemy."""

### Game Manager ###

def fixed_input(s):
    """Takes an input string s and returns a new string that is reformatted to remove the spaces before and after s and make 
    everything lowercase.
    >>> x = fixed_input("   The cow jumped over the Moon   ")  
    >>> x 
    'the cow jumped over the moon'
    """
    return s.lower().strip()
    
### In-Game Items ###

