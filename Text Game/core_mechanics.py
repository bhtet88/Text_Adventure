
### Equipment Classes ###

class Equipment:
    """Parent class for the equipment the player can carry. Each equipment has a specific name and weight
    >>> x = Equipment("Pickaxe", 5, 10)
    >>> x.name
    'Pickaxe'
    >>> x.weight
    5
    >>> x.price
    10
    >>> print(x)
    Name: Pickaxe, Weight: 5, Price: 10 coins
    >>> x
    Equipment: Pickaxe
    """
    class_type = "Equipment"

    def __init__(self, name, weight, price):
        self.name = name
        self.weight = weight
        self.price = price

    def __repr__(self):
        return "{0}: {1}".format(self.class_type, self.name)
    
    def __str__(self):
        return "Name: {0}, Weight: {1}, Price: {2} coins".format(self.name, self.weight, self.price)

class Weapon(Equipment): 
    """Weapons that the player and enemies can use to fight with. Each weapon has a name, damage, range, and weight. Some weapons can have an armor piercing ability
    >>> x = Weapon("Rifle", 100, 50, 10, 250)
    >>> x.name 
    'Rifle'
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
    Name: Rifle, Damage: 100, Range: 50, Weight: 10 lbs, Armor Piercing: False, Price: 250 coins
    >>> x
    Weapon: Rifle
    """
    armor_piercing = False
    class_type = "Weapon"
    
    def __init__(self, name, damage, range, weight, price):
        Equipment.__init__(self, name, weight, price)
        self.damage = damage
        self.range = range
    
    def __str__(self):
        return "Name: {0}, Damage: {1}, Range: {2}, Weight: {3} lbs, Armor Piercing: {4}, Price: {5} coins".format(self.name, self.damage, self.range, self.weight, self.armor_piercing, self.price)

class Healing_Tool(Equipment):
    """Healing equipment for the player to regain health. Each healing equipment has a name, healing amount, number of uses, and weight
    >>> x = Healing_Tool("Syringe", 30, 1, 0.5, 12)
    >>> x.name 
    'Syringe'
    >>> x.weight
    0.5
    >>> x.heal_amount
    30
    >>> x.price
    12
    >>> x.uses
    1
    >>> print(x)
    Name: Syringe, Heal Amount: 30 HP, Uses Left: 1, Weight: 0.5, Price: 12 coins
    >>> x
    Healing Equipment: Syringe
    """
    class_type = "Healing Equipment"

    def __init__(self, name, heal_amount, uses, weight, price):
        Equipment.__init__(self, name, weight, price)
        self.heal_amount = heal_amount
        self.uses = uses
        self.weight = weight

    def __str__(self):
        return "Name: {0}, Heal Amount: {1} HP, Uses Left: {2}, Weight: {3}, Price: {4} coins".format(self.name, self.heal_amount, self.uses, self.weight, self.price)

### Player Classes ###

class Entity:
    """Parent class for all characters in the game, including players and enemies. Other characters inherit from this class"""
    class_type = "Entity"

    def __init__(self, name, health, armor):
        self.name = name.strip()
        self.health = health
        self.armor = armor

    def damaged(self, amount):
        "Reduces the entity's current health and armor, taking into account the special attributes of the weapons and equipment when applicable. Remove the enemy from the game when defeated."
    
    def remove(self, place):
        "Removes the current entity from the current place when their health hits zero"

    def __repr__(self):
        return "{0} ({1}, {2})".format(self.class_type, self.name, self.health)

    def __str__(self):
        return "Name: {0}, Health: {1}, Armor: {2}".format(self.name, self.health, self.armor)

class Player(Entity):
    """Class for the player of the game, which is able to do certain actions that enemies cannot do. 
    Has a backpack with a certain weight capacity"""
    class_type = "Player"
    weight_limit = 70
    wallet = 1000
    
    def __init__(self, name, health=100, armor=0):
        Entity.__init__(self, name, health, armor)
        self.backpack = []
        self.current_weight = sum([x.weight for x in self.backpack])
    
    def __str__(self):
        return "Name: {0}, Health: {1}, Armor: {2}, Current Weight: {3} lbs, Carrying Capacity: {4} lbs".format(self.name, self.health, self.armor, self.current_weight, self.weight_limit)

### Enemy Classes ###

class Enemy(Entity):
    """Class for the enemies and creatures that the player fights against"""

### Event Classes ###

class Event:
    """Parent class for the random events in the game, which can be a puzzle, a hazard, or an enemy"""

### Game Manager ###

def fixed_input(s):
    """Takes an input string s and returns a new string that is reformatted to remove the spaces before and after s and make 
    everything lowercase.
    >>> x = fixed_input("   The cow jumped over the Moon   ")  
    >>> x 
    'the cow jumped over the moon'
    """
    return s.lower().strip()
    
