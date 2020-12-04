
### Equipment Classes

class Equipment:
    """Parent class for the equipment the player can carry. Each equipment has a specific name, type, and weight"""
    weight = 0
    class_type = "Equipment"

    def __init___(self, name):
        self.name = name

    def __repr__(self):
        return "{0}: {1}".format(self.class_type, self.name)
    
    def __str__(self):
        return self.name

class Weapon(Equipment): 
    """Weapons that the player and enemies can use to fight with, including their base stats, name, and type"""
    armor_piercing = False
    class_type = "Weapon"
    
    def __init__(self, name, damage, range):
        Equipment.__init__(self, name)
        self.damage = damage
        self.range = range
    
    def __str__(self):
        return "Name: {0}, Damage: {1}, Range: {2}"


class Healing_Tool(Equipment):
    """Healing equipment for the player to regain health"""

### Player Classes

class Entity:
    """Parent class for all characters in the game, including players and enemies. Other characters inherit from this class"""
    class_type = "Entity"
    weight_limit = 0

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
    weight_limit = 100
    wallet = 1000
    
    def __init__(self, name, health=100, armor=0):
        Entity.__init__(self, name, health, armor)
        self.backpack = []
        self.current_weight = sum([x.weight for x in self.backpack])
    
    def __str__(self):
        return "Name: {0}, Health: {1}, Armor: {2}, Current Weight: {3} lbs, Carrying Capacity: {4} lbs".format(self.name, self.health, self.armor, self.weight, self.weight_limit)

# Enemy Classes

class Enemy(Entity):
    """Class for the enemies and creatures that the player fights against"""

### Event Classes

class Event:
    """Parent class for the random events in the game, which can be a puzzle, a hazard, or an enemy"""

### Game Manager

def fixed_input(s):
    """Takes an input string s and returns a new string that is reformatted to remove the spaces before and after s and make 
    everything lowercase.
    >>> x = fixed_input("   The cow jumped over the Moon   ")  
    >>> x 
    'the cow jumped over the moon'
    """
    return s.lower().strip()
    
