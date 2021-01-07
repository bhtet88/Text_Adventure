import random
import time
from story import *

### Equipment Classes ###

class Equipment:
    """Parent class for the equipment the player can carry. Each equipment has a specific weight and price
    >>> x = Equipment(5, 10)
    >>> x.weight
    5
    >>> x.price
    10
    >>> print(x)
    Equipment, Weight: 5 lbs, Price: 10 coins
    >>> x
    Equipment
    """
    class_name = "Equipment"
    combat_item = False
    
    def __init__(self, weight, price, name="Equipment"):
        self.weight = weight
        self.price = price
        self.name = name

    def recalculate(self, place):
        """The default recalculate method does nothing but for Weapons and Healing Tools, it recalculates their effective statistics so that the shown statistics are accurate."""
        pass

    def action(self, place):
        """All items have an action method that allows them to perform their intended function. The action takes in a player instance and a place instance in to ensure the item can have access to everything it needs to perform any action. The default action is that an item does nothing."""
        print("This item does nothing right now") 

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return "{0}, Weight: {1} lbs, Price: {2} coins".format(self.name, self.weight, self.price)

class Lyre(Equipment):
    """The lyre is a unique piece of equipment, only obtainable in a playthrough if the player gets the gift of Apollo. It is a supportive, combat usable item that allows the player to serenade all enemies except those that can't be charmed. Serenaded enemies have their damage reduced for the
    remainder of battle.
    """
    attack_debuff = 0.80
    min_attack = 10
    combat_item = True

    def __init__(self, weight=3, price=0, name="Lyre"):
        Equipment.__init__(self, weight, price, name)

    def action(self, place):
        """The Lyre lowers the attack of all enemies on the field by the attack debuff attribute. Enemies cannot go less than the min attack attribute."""
        for enemy in place.enemies:
            if enemy.charmable:
                if self.min_attack >= int(self.attack_debuff * enemy.attack):
                    enemy.damage = self.min_attack
                else:
                    enemy.damage = int(enemy.damage * self.attack_debuff)

class Armor_Piece(Equipment):
    """Armor pieces are equipment that the player can get to add to their armor value, protecting their health from non armor piercing attacks. Armor pieces have to be used first, so their action method is what adds to the player's armor, not just the act
    of acquiring it. All armor pieces are a single use only. 
    """
    combat_item = True

    def __init__(self, armor, weight, price, name="Armor Piece"):
        Equipment.__init__(self, weight, price, name)
        self.armor = armor

    def action(self, place):
        """The action method simply adds armor to the player's armor stat and then are removed from their backpack."""
        place.player.armor += self.armor
        print("Added {0} points of armor".format(self.armor))
        print("")
        place.player.backpack_remove(self.name.lower())

    def __str__(self):
        return "{0}, Armor: {1} Weight: {2} lbs, Price: {3} coins".format(self.name, self.armor, self.weight, self.price)

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
    Weapon, Damage: 100, Range: 50 units, Weight: 10 lbs, Armor Piercing: False, Price: 250 coins
    >>> x
    Weapon
    """
    class_name = "Weapon"
    combat_item = True
    armor_piercing = False
    damage_bonus = 0
    range_bonus = 0
    
    def __init__(self, damage, range, weight, price, name="Weapon"):
        Equipment.__init__(self, weight, price, name)
        self.damage = damage
        self.range = range
        self.eff_damage = damage
        self.eff_range = range
    
    def recalculate(self, place):
        """Recalculates the effective damage and range of the weapon, taking into account the bonuses of the weapon class, the player, and the current place."""
        self.eff_damage = int(max(self.damage * (1 + (self.damage_bonus + place.player.damage_bonus + place.damage_bonus)), 5)) #Prevents the weapons from becoming useless 
        self.eff_range = int(max(self.range + self.range_bonus + place.player.range_bonus + place.range_bonus, 1)) #Range must be at least 1

    def combat_table(self, place):
        """Helper method for the action method for Weapons, showing the enemies sorted by distance and the current weapon's effective range."""
        sorted_list, i = sorted(place.enemies, key = lambda x: x.position - place.player.position), 0
        print("*** Targets ***")
        for enemy in sorted_list:
            dist = enemy.position - place.player.position
            print("[{0}] {1}, Health: {2}, Armor: {3}, Damage: {4}, Distance: {5}".format(i, enemy.name, enemy.health, enemy.armor, enemy.damage, dist))
            i += 1
        print("")
        print("{0} Range: {1}".format(self.name, self.eff_range))
        return sorted_list, i

    def attack(self, place, target):
        """Helper method for the action method that actually calculates how to damage the enemies. Call this after the player is done making a valid decision on who to attack. The default just injures the single target."""
        target.injure(place, self.eff_damage, self.armor_piercing)

    def action(self, place):
        """The default action method for weapons allows the player to target a certain enemy in the place and attack them with the weapon by calling their injure method. When showing all the enemies, only show their health, armor, damage, and distance from the player.
        If the enemy is out of range, have the player pick another target. Calls self.attack at the end to perform the actual damaging"""
        sorted_list, i = self.combat_table(place)
        print("")
        choice = fixed_input(input("Who will you attack? Type the number of the enemy you will attack or type 'Back' to go back and perform a different action. "))
        if choice == "back":
            print("")
            return place.player.take_turn(place)
        elif not choice.isnumeric() or int(choice) > i:
            print("")
            print("Invalid input, answer must be a valid numeric input")
            print("")
            return self.action(place)
        choice = int(choice)
        target = sorted_list[choice]
        if target.position - place.player.position > self.eff_range:
            print("")
            print("Target out of range, choose another enemy")
            print("")
            return self.action(place)
        print("")
        self.attack(place, target)

    def __str__(self):
        return "{0}, Damage: {1}, Range: {2} units, Weight: {3} lbs, Armor Piercing: {4}, Price: {5} coins".format(self.name, self.eff_damage, self.eff_range, self.weight, self.armor_piercing, self.price)

class Bow(Weapon):
    """Bows are long ranged weapons that are armor piercing and can hit enemies that are more than 1 unit away. Damage is weaker than melee weapons. The bow itself is light but the bundle of arrows makes them heavier than expected. Have a special volley attack that allows them to deal half
    damage to all enemies within range"""
    armor_piercing = True
    diana_bonus = False

    def __init__(self, damage, range, weight, price, name="Bow"):
        Weapon.__init__(self, damage, range, weight, price, name)

    def volley_shot(self, place):
        """The volley shot deals half of the bow's effective damage (damage after all buffs and debuffs are applied) to all enemies within range by summoning the might of Diana."""
        targets = [enemy for enemy in place.enemies if enemy.position - place.player.position <= self.eff_range]
        for target in targets:
            target.injure(place, self.eff_damage // 2, self.armor_piercing)

    def action(self, place):
        """The action method for bows allows the player to decide if they want to use the normal attack or use the volley shot method if they have the gift of Diana. Each decision will call the proper method."""
        if self.diana_bonus:
            attack = fixed_input(input("What attack will you use? Type 'Normal' or 'Volley Shot' to attack or 'Back' to choose a different action. "))
            if attack == "back":
                print("")
                return place.player.take_turn(place)
            elif attack == "normal":
                Weapon.action(self, place)
            elif attack == "volley shot":
                self.volley_shot(place)
            else:
                print("Invalid input, try again")
                print("")
                return self.action(place)
        else:
            Weapon.action(self, place)

class Rifle(Weapon):
    """Rifles are a powerful ranged weapon similar to bows but in exchange for their great power, each rifle has an accuracy rating that determines if the weapon hits the target or misses. Accuracy is a value between 0 and 100."""
    armor_piercing = True
    accuracy_bonus = 0

    def __init__(self, damage, range, accuracy, weight, price, name="Rifle"):
        Weapon.__init__(self, damage, range, weight, price, name)
        self.accuracy = accuracy
        self.eff_accuracy = accuracy

    def recalculate(self, place):
        """Uses the normal weapon class recalculation plus recalculates the effective accuracy attribute."""
        Weapon.recalculate(self, place)
        self.eff_accuracy = int(max(min(self.accuracy + self.accuracy_bonus + place.accuracy_bonus, 100), 30)) #Ensures that accuracy will never surpass 100 but will also always be at least 40

    def attack(self, place, target):
        """Rifles have to perform a random roll to see if they hit their target or not."""
        hit = random.choices([1, 0], weights=(self.eff_accuracy, 100 - self.eff_accuracy))
        if hit[0]:
            target.injure(place, self.eff_damage, self.armor_piercing)
        else:
            print("You missed!")
        
    def __str__(self):
        return "{0}, Damage: {1}, Range: {2} units, Accuracy: {3}, Weight: {4} lbs, Armor Piercing: {5}, Price: {6} coins".format(self.name, self.eff_damage, self.eff_range, self.eff_accuracy, self.weight, self.armor_piercing, self.price)

class Shotgun(Weapon):
    """Shotguns are a powerful short ranged weapon that have no accuracy stat but have extremely limited range. In exchange, shotguns are damage machines. For every space closer to the player that the enemy is past the maximum range, the gun gains a damage bonus. Furthermore, a player is able
    to deal full damage to the selected enemy but then all other enemies on the same spot as that enemy are also hit by the spread of the pellets, causing reduced damage."""
    
    def __init__(self, damage, range, spread_multiplier, cqc_bonus, weight, price, name="Shotgun"):
        Weapon.__init__(self, damage, range, weight, price, name)
        self.spread_multiplier = spread_multiplier
        self.cqc_bonus = cqc_bonus

    def attack(self, place, target):
        """For every 1 unit the enemy is closer to the player after the max range of the shotgun, the player gets a damage addition determined by the CQC bonus attribte. When the player picks a target to attack, the other enemies on that same place as get hit with reduced damage, which is
        determined by the spread multiplier attribute."""
        dmg = int(self.eff_damage * (1 + (self.cqc_bonus * (self.eff_range - (target.position - place.player.position)))))
        target.injure(place, dmg, self.armor_piercing)
        for enemy in place.enemies:
            if enemy.position == target.position and enemy is not target:
                print("")
                enemy.injure(place, int(dmg * self.spread_multiplier), self.armor_piercing)

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
    Healing Equipment, Heal Amount: 30 HP, Uses Left: 1, Weight: 0.5 lbs, Price: 12 coins
    >>> x
    Healing Equipment
    """
    class_name = "Healing"
    combat_item = True
    heal_bonus = 0
    uses_bonus = 0

    def __init__(self, heal_amount, uses, weight, price, name = "Healing Equipment"):
        Equipment.__init__(self, weight, price, name)
        self.heal_amount = heal_amount
        self.eff_heal = heal_amount
        self.uses = uses
        self.eff_uses = uses

    def recalculate(self, place):
        """Recalculates the effective healing of a healing item by taking into account the base heal amount, heal bonus of the class, heal bonus of the player, and heal bonus of the place."""
        self.eff_heal = int(max(self.heal_amount + self.heal_bonus + place.player.heal_bonus + place.heal_bonus, 5)) #Prevents item from being completely useless
        self.eff_uses = int(max(self.uses + self.uses_bonus + place.player.uses_bonus + place.uses_bonus, 0))

    def action(self, place):
        """The default action method for healing items is to heal the player, with the heal amount determined by their heal amount attribute. Players cannot go over their maximum health. Remove the healing item from backpack if it is out of uses. If the player is already at max health, \
        then display a message and let the player try another action."""
        diff = place.player.eff_max_health - place.player.health
        if diff == 0:
            print("Health already maximum, can not use this")
            print("")
            return place.player.take_turn(place)
        elif diff <= self.eff_heal:
            place.player.health = place.player.eff_max_health
        else:
            place.player.health += self.eff_heal
        self.uses -= 1
        print("Healed for {0} HP, {1} uses remaining".format(min(diff, self.eff_heal), self.uses))
        self.recalculate(place)
        if not self.eff_uses:
            print("")
            place.player.backpack_remove(self.name.lower())

    def __str__(self):
        return "{0}, Heal Amount: {1} HP, Uses Left: {2}, Weight: {3} lbs, Price: {4} coins".format(self.name, self.eff_heal, self.eff_uses, self.weight, self.price)

### In-Game Items ###

armor_plate = Armor_Piece(25, 7, 50, "Armor Plate")
bandages = Healing_Tool(20, 1, 0.5, 75, "Bandages")
bow = Bow(30, 4, 12, 75, "Bow")
spear = Weapon(45, 1, 10, 100, "Spear") 
rifle = Rifle(70, 4, 60, 15, 200, "Rifle")
trench_gun = Shotgun(60, 3, 0.4, 0.2, 10, 250, "Trench Gun")

heavy_spear = Weapon(65, 1, 15, 150, "Heavy Spear")
longbow = Bow(45, 6, 18, 250, "Longbow")
padded_jacket = Armor_Piece(45, 10.5, 200, "Padded Jacket")
healing_syringe = Healing_Tool(40, 4, 1, 200, "Healing Syringe")

store_list = [spear, bandages, bow, rifle, armor_plate, trench_gun]

knife = Weapon(40, 1, 0, 0, "Knife")
rope = Equipment(0, 0, "Rope")

### Creature Class ###

class Entity:
    """Parent class for all characters in the game, including players and enemies. Other characters inherit from this class
    >>> x = Entity(150, 100)
    >>> x.health
    150
    >>> x.armor 
    100
    >>> print(x)
    Entity, Health: 150, Armor: 100
    >>> x
    Entity
    """
    name = "Entity"

    def __init__(self, health, armor):
        self.health = health
        self.armor = armor
        self.position = None

    def injure(self, place, damage, AP):
        """Method to apply damage to the entity. Takes in a damage value and a boolean about whether the attack was armor piercing or not. AP damage is applied to the armor first and only lowers the entity's health when the armor is depleted."""
        if AP:
            self.health -= damage
        else:
            diff = damage - self.armor
            if diff >= 0:
                self.armor = 0
                self.health -= diff
            else:
                self.armor -= damage
        print("{0} took {1} damage!".format(self.name, damage))
        if self.health <= 0:
            print("")
            self.remove(place)

    def remove(self, place):
        """Removes the current entity from the current place when their health hits zero."""
        place.enemies.remove(self)

    def __repr__(self):
        return self.name

    def __str__(self):
        return "{0}, Health: {1}, Armor: {2}".format(self.name, self.health, self.armor)

class Player(Entity):
    """Class for the player of the game, which is able to do certain actions that enemies cannot do. Unlike the enemies, the player is able to pick a weapon to attack with.
    Has a backpack with a certain weight capacity
    >>> x = Player("Dave")
    >>> x.backpack
    {}
    >>> x.current_weight 
    0
    >>> x
    Player: (100, 0)
    >>> print(x)
    Dave, Health: 100, Armor: 0, Current Weight: 0 lbs, Move Speed: 1 units per turn
    """
    damage_bonus = 0
    range_bonus = 0
    move_bonus = 0
    heal_bonus = 0
    uses_bonus = 0

    def __init__(self, name, health=100, armor=0, move_speed=1):
        Entity.__init__(self, health, armor)
        self.name = name
        self.move_speed = move_speed
        self.eff_move = move_speed 
        self.backpack = {}
        self.current_weight = 0
        self.weight_limit = 50
        self.max_health = 100
        self.eff_max_health = self.max_health
        self.wallet = 1000
        self.place = None
    
    def recalculate(self, place):
        """The player recalculate method recalculates their move speed stat and all the items in their inventory."""
        self.eff_move = int(max(self.move_speed + self.move_bonus + place.move_bonus, 1)) #Player will always move at least one unit
        self.eff_max_health = int(max(50, self.max_health + place.max_health_bonus)) #Player max health will always be at least 50 points
        if self.health > self.eff_max_health:
            self.health = self.eff_max_health
        for item in self.backpack.values():
            item.recalculate(place)

    def backpack_add(self, item):
        """Adds item to the player's backpack as long as adding the weight of the item does not cause the current weight to exceed the weight_limit.
        >>> player = Player("Dan")
        >>> x = Weapon(20, 1, 5, 50)
        >>> player.backpack_add(x)
        Added Weapon to backpack
        >>> z = Weapon(20, 1, 75, 50)
        >>> player.backpack_add(z)
        Weight limit exceeded. Remove items to add this
        """
        if self.weight_limit - self.current_weight >= item.weight:
            self.backpack[item.name.lower()] = item
            self.current_weight = sum([x.weight for x in self.backpack.values()])
            print("Added {0} to backpack".format(item.name))
        else:
            print("Weight limit exceeded. Remove items to add this")

    def backpack_remove(self, item_name):
        """Allows for the removal of an item from the player's backpack. Takes in the name of a piece of equipment as an argument
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> player = Player("Dan")
        >>> player.backpack_add(spear)
        Added Spear to backpack
        >>> player.backpack
        {'spear': Spear}
        >>> player.backpack_remove("spear")
        Spear removed from backpack
        >>> player.backpack 
        {}
        """
        permanent = ["knife", "rope"]
        if item_name in permanent:
            print("Cannot remove this item from your backpack")
        elif item_name in self.backpack:
            item = self.backpack.get(item_name)
            del self.backpack[item_name]
            self.current_weight = sum([x.weight for x in self.backpack.values()])
            print("{0} removed from backpack".format(item.name))
        else:
           print("Equipment not in backpack")

    def show_backpack(self):
        """Displays all the items in the player's backpack, with one item on each line."""
        self.recalculate(self.place)
        print("*** Backpack (Weight: {0} / {1}) ***".format(self.current_weight, self.weight_limit))
        weapons = [print(x) for x in self.backpack.values() if x.class_name == Weapon.class_name]
        healing = [print(x) for x in self.backpack.values() if x.class_name == Healing_Tool.class_name]
        equip = [print(x) for x in self.backpack.values() if x.class_name == Equipment.class_name]

    def show_weapons(self):
        """Displays all the weapons that the player is carrying."""
        self.recalculate(self.place)
        print("*** Weapons ***")
        weapons = [x for x in self.backpack.values() if isinstance(x, Weapon)]
        for item in sorted(weapons, key=lambda x: x.range, reverse=True): 
            print(item)

    def use_weapon(self):
        """Allows the player to select a weapon from their inventory and return the weapon object for them to use. Returns None if the weapon isn't in the backpack"""
        self.show_weapons()
        print("")
        weapon = fixed_input(input("What weapon will you use? Type the name of the weapon or 'None' to select nothing and perform a different action. ")) #There will be no weapon with a name of 'None'
        if weapon in self.backpack:
            return self.backpack[weapon]
        elif weapon != "none":
            print("")
            print("Weapon not in backpack")
        return None

    def use_backpack(self):
        """Allows the player to access their backpack and select an item to use. This method returns the item object so the game can see what item the player wants to use. If the player closes the backpack, return None. If the player gives an invalid input,
        raise an error and also return None. If the player removes an item, remove the item from the backpack and return None."""
        self.show_backpack()
        print("")
        choice = fixed_input(input("What would you like to do? Type 'Use' or 'Remove' followed by the name of the item to either use or remove it or 'Close backpack' to go back. "))
        if choice == "close backpack":
            return None
        try:
            action, item_name = choice.split(" ", 1)[0], choice.split(" ", 1)[1]
        except:
            print("")
            print("Invalid input, try again")
            return None
        if action == "use":
            if item_name in self.backpack:
                return self.backpack[item_name]
            print("")
            print("Item not in backpack")
            return None
        elif action == "remove":
            print("")
            self.backpack_remove(item_name)
            return None

    def sorting(self):
        """Allows the player to sort their items when OUT OF COMBAT. Used at the end of a battle or event. Essentially a modified version of the use_backpack method that prevents the player from using a healing item at max health or a weapon, as that can cause a game breaking infinite turn."""
        item = self.use_backpack()
        if isinstance(item, Weapon):
            print("")
            print("There's no point using a weapon when not in combat")
        elif isinstance(item, Healing_Tool) and self.health == self.eff_max_health:
            print("")
            print("Health already maximum, can not use this")
        elif item:
            print("")
            item.action(self.place)

    def move(self, place):
        """Helper method to allow the player to move either forward or backwards during combat. Since this is only used during battle, this function can call the take_turn method if the player wants to backout of moving and try another action. Must perform checks if the player can move in the
        selected direction, whether they are blocked by an enemy, or if they have reached the end of the place. If the player is immediately blocked, display a message and let them try again. If the player can move at least one unit, let them move and use that as their turn regardless of if 
        they can move all the steps they wanted or not.
        """
        steps= fixed_input(input("How many steps will you move? Type a negative value to move backwards (Max steps: {0}) or 'Back' to perform another action. ".format(self.eff_move)))
        print("")
        if steps == "back":
            return self.take_turn(place)
        if not steps.replace("-", "").isnumeric():
            print("Input not a valid integer, try again")
            print("")
            return self.take_turn(place)
        steps, count = int(steps), 0
        abs_steps, direction = abs(steps), (steps // abs(steps) if steps else 0)
        if abs(steps) > self.eff_move:
            print("Cannot take that many steps, try again")
            print("")
            return self.take_turn(place)
        elif (steps > 0 and self.position >= place.size) or (steps < 0 and self.position == 0):
            print("At the end of place, cannot move any further, try again")
            print("")
            return self.take_turn(place)
        elif (steps > 0 and any([self.position + 1 == enemy.position for enemy in place.enemies])) or (steps < 0 and any([self.position - 1 == enemy.position for enemy in place.enemies])):
                print("Enemy in front of you, eliminate them to proceed, try again")
                print("")
                return self.take_turn(place)
        while abs_steps:
            if (steps > 0 and any([self.position + 1 == enemy.position for enemy in place.enemies])) or (steps < 0 and any([self.position - 1 == enemy.position for enemy in place.enemies])):
                print("Enemy in front of you, eliminate them to proceed")
                break
            elif (steps > 0 and self.position >= place.size) or (steps < 0 and self.position == 0):
                print("Cannot move any further, at end of place")
                break
            if steps > 0:
                self.position += 1
            else: 
                self.position -= 1
            abs_steps -= 1
            count += 1
        print("{0} moved {1} steps {2}".format(self.name, count, "forward" if direction >= 0 else "backwards"))

    def take_turn(self, place):
        """Method that allows the player to take their turn during combat. Players can either attack, move, or use an item in their backpack. If the player puts in an invalid input, allow them to try again. If the enemy is out of a weapon's range, 
        display a message saying so and let the player try again. If the player chooses an piece of equipment that isn't combat oriented, display a message and try again.
        """
        place.player.recalculate(place)
        place.visualize()
        print("")
        print("*** Player ***")
        print("{0}, Health: {1}, Armor: {2}, Move Speed: {3} units per turn".format(self.name, self.health, self.armor, self.eff_move))
        print("")
        place.show_enemies()
        print("")
        action = fixed_input(input("What will you do? Type 'Attack' to attack the enemy, 'Move' to move, or 'Open backpack' to look at and use something in your backpack. "))
        print("")
        if action == "attack": #Attack decision
            weapon = self.use_weapon()
            if not weapon:
                print("")
                return self.take_turn(place)
            print("")
            weapon.action(place)
        elif action == "move": #Movement decision
            self.move(place)
        elif action == "open backpack": #Item usage decision
            item = self.use_backpack()
            print("")
            if not item:
                return self.take_turn(place)
            elif not item.combat_item:
                print("Not an item for combat, try again")
                print("")
                return self.take_turn(place)
            item.action(place)
        else:
            print("Invalid input, try again")
            print("")
            return self.take_turn(place)

    def remove(self, place):
        "The player has a special remove function that ends the game upon their death."
        game_over()

    def __repr__(self):
        return "Player: ({0}, {1})".format(self.health, self.armor)
    
    def __str__(self):
        return "{0}, Health: {1}, Armor: {2}, Current Weight: {3} lbs, Move Speed: {4} units per turn".format(self.name, self.health, self.armor, self.current_weight, self.eff_move)

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
    Enemy, Health: 100, Armor: 100, Damage: 50, Range: 1 units, Move Speed: 1 units per turn
    >>> x 
    Enemy
    """
    name = "Enemy"
    battle_lines = [""]
    death_lines = [""]
    line_chance = 1
    armor_piercing = False
    charmable = True

    def __init__(self, health, armor, damage, range, move_speed):
        Entity.__init__(self, health, armor)
        self.damage = damage
        self.range = range
        self.move_speed = move_speed
    
    def move(self, place, back=False):
        """Default move method that advances the enemy towards the player unless the player is in front of them or they reach the end of the place. If the back argument is True, this function will move the enemy as far away as possible."""
        steps, i = self.move_speed, 0
        while steps:
            if not back:
                if self.position - 1 == place.player.position or self.position <= 0:
                    break
                self.position, steps = self.position - 1, steps - 1
            elif back:
                if self.position + 1 > place.size:
                    break
                self.position, steps = self.position + 1, steps - 1
            i += 1
        print("{0} moved {1} steps {2}!".format(self.name, i, ("towards you" if not back else "away from you")))

    def attack(self, place):
        """Method that calls the player's injure method to apply the normal damage"""
        place.player.injure(place, self.damage, self.armor_piercing)

    def take_turn(self, place):
        """The default take turn method for enemies. The enemy will either advance towards the player if the player is not in range or they will attack if the player is in range."""
        if self.position - place.player.position <= self.range:
            print("")
            print("{0} attacks!".format(self.name))
            print("")
            self.attack(place)
        else:
            print("")
            self.move(place)

    def remove(self, place):
        """Enemies will spout a random death line when they are eliminated. This is a guarenteed event before they are removed from the place. Uses the remove method in the Entity parent class."""
        print(random.choice(self.death_lines))
        print("{0} eliminated!".format(self.name))
        Entity.remove(self, place)

    def __str__(self):
        return "{0}, Health: {1}, Armor: {2}, Damage: {3}, Range: {4} units, Move Speed: {5} units per turn".format(self.name, self.health, self.armor, self.damage, self.range, self.move_speed)

class Legionary(Enemy):
    """First enemies that the player encounters: Undead Legionaries kept alive by a successful experiment with magic, with the side effect of making them accelerate mental degredation. They have no special abilities,
    only a dagger and shield. Follow the default take turn method where they either move towards the player if they aren't in range or they attack if the player is in range.
    >>> x = Legionary(100, 50, 20, 1, 1)
    >>> x.damage 
    20
    >>> x
    Legionary
    >>> print(x)
    Legionary, Health: 100, Armor: 50, Damage: 20, Range: 1 units, Move Speed: 1 units per turn
    """
    name = "Legionary"
    battle_lines = ["'Rome will prevail!'", "'You cannot run from the might of Rome!'", "'Another soul attempting to steal our treasure, you'll die like the rest!'", "'I'll enjoy watching you squirm at the end of my blade!'"]
    line_chance = 3
    death_lines = ["'How could I perish to a mere human?'", "'No...I will...not...fall!'", "'I may be dead, but my comrades will avenge me!'", "'You will never get past the rest!'"]

    def __init__(self, health=100, armor=50, damage=25, range=1, move_speed=1):
        Enemy.__init__(self, health, armor, damage, range, move_speed)

class Immortal_Dog(Enemy):
    """Using the same magic that keeping the Legionaries alive, these dogs are loyal to their undead human allies. Can move up to 2 steps per turn but deal very little damage. 
    >>> x = Immortal_Dog(75, 0, 10, 1, 2)
    >>> print(x)
    Immortal Dog, Health: 75, Armor: 0, Damage: 10, Range: 1 units, Move Speed: 2 units per turn
    >>> x
    Immortal Dog
    """
    name = "Immortal Dog"
    battle_lines = ["'GRRRRRRRR!'"]
    line_chance = 1
    death_lines = ["'Whimpers'"]

    def __init__(self, health=50, armor=0, damage=15, range=1, move_speed=2):
        Enemy.__init__(self, health, armor, damage, range, move_speed)

class Feral_Monkey(Enemy):
    """Feral monkeys are rabid beasts that the result of failed experiments with Roman sorcery. Despite losing their minds and being unable to think for themselves for anything other than survival, they fight alongside the Roman defenses. They have the ability to hurl fecal matter at the
    player if the player is 2 units away. This attack can damage the player but only deals 40% of the base attack."""

    name = "Feral Monkey"
    battle_lines = ["'OOOO OOOO AAHH AAHH'"]
    line_chance = 1
    death_lines = ["'Whimpers'"]

    def __init__(self, health=70, armor=0, damage=30, range=1, move_speed=2):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.dung_multiplier = 0.40
        self.dung_range = 3
        self.throw = True
        self.dung_counter = 0
    
    def dung_hurl(self, place):
        """Feral monkeys can hurl dung at the player if the player is 2 spaces away, which deals 40% of their base damage stat. Once hurling the dung, they must wait a turn before throwing another one so they have time to make their projectile."""
        print("{0} throws a ball of poop at you!".format(self.name))
        print("")
        place.player.injure(place, int(self.damage * self.dung_multiplier), self.armor_piercing)
        self.throw, self.dung_counter = False, 0

    def take_turn(self, place):
        """If the player is within 3 spaces away from the monkey and they aren't in a cooldown period, throw a dung pile. Otherwise, perform the same take turn as the default Enemy class, moving towards the player to attack them."""
        if self.throw and (1 < self.position - place.player.position <= self.dung_range):
            print("")
            self.dung_hurl(place)
        else:
            Enemy.take_turn(self, place)
            self.dung_counter += 1
            if self.dung_counter == 1:
                self.throw = True

class Giant_Snake(Enemy):
    """The final boss of the forest level is a giant snake, a mutant beast that escaped Roman grasps and now lives in a large field in the forest. The snake has a high move stat, allowing it to close the gap quickly. It also has a lunge attack, allowing it to attack the player from a long
    range for reduced damage. It also has the rattle move, which gives it a flat bonus attack buff for a few turns. Normal attacks from the snake result in some health damage even if the player has armor on. If the player has no armor, this corrosive damage is dealt as pure bonus damage.
    Can be charmed."""
    name = "Giant Snake"
    battle_lines = ["'SSSSSSSSSSSS'"]
    line_chance = 1
    death_lines = ["'SSSS...SSSS...SS...S'"]

    def __init__(self, health=250, crit_health=40, gap=3, armor=0, damage=35, rattle_buff=10, rattle_length=2, corrosion=5, range=1, lunge_range=4, lunge_multiplier=0.70, move_speed=3):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.crit_health=crit_health
        self.gap = gap
        self.rattle_buff = rattle_buff
        self.rattle_length = rattle_length
        self.rattle_counter = 1
        self.corrosion = corrosion
        self.lunge_range = lunge_range
        self.lunge_muliplier = lunge_multiplier

    def lunge(self, place):
        """The lunge move allows the snake to lunge forwards at the player, performing a long range attack with range determined by the lunge range attribute. This attack applies no corrosive damage but only does a portion of the normal damage, determined by the lunge multiplier attribute."""
        print("{0} aggressively lunges at you.".format(self.name))
        print()
        place.player.injure(place, int(self.damage * self.lunge_muliplier), self.armor_piercing)

    def rattle(self, place):
        """The rattle ability gives the snake a flat damage bonus determined by the rattle buff attribute. It lasts for a limited amount of turns, governed by the rattle length attribute. The turn it was activated doesn't count. Once a rattle has been performed, apply the bonus and then 
        set the rattle counter to the turn number when the rattle effect will wear off and the snake can do the rattle again."""
        print("{0} rattles its tail, increasing its damage by {1} points for {2} turns".format(self.name, self.rattle_buff, self.rattle_length))
        self.damage += self.rattle_buff
        self.rattle_counter = place.turn_count + self.rattle_length

    def attack(self, place):
        """The attack method applies damage normally, just like the default attack method, but also applies the additional corrosion damage directly to the player's health. If the player has no armor, then corrosion is applied as a pure bonus damage on top of the normal damage."""
        Enemy.attack(self, place)
        print("")
        print("{0} does an additional {1} points of corrosive damage directly to your health!".format(self.name, self.corrosion))
        print("")
        place.player.injure(place, self.corrosion, True)

    def take_turn(self, place):
        """The snake's first priority is performing its rattle move. While it is unable to rattle, it will analyze if it can make it directly in front of the player with its move speed. If it can, it will move in front of the player if it can. If it cannot but the player is within lunge
        range, the snake will perform a lunge. If the snake is in front of the player, it will rattle if it can or normally attack the player. When its health reaches a certain level determined by the crit health attribute, it will try to stay away from the player and perform lunges.
        Priorities are 1) Rattle 2) Move 3) Attack 4) Lunge. This method is also in charge of taking off the rattle buff when the buff's time is up."""
        print()
        if place.turn_count > self.rattle_counter or place.turn_count == 1:
            self.rattle(place)
        elif self.health > self.crit_health:
            if self.position - place.player.position <= self.range:
                self.attack(place)
            elif self.position - place.player.position <= self.move_speed:
                    self.move(place)
            elif self.position - place.player.position <= self.lunge_range:
                self.lunge(place)
            else:
                self.move(place)
        else:
            if self.position - place.player.position < self.gap:
                self.move(place, True)
            elif self.position - place.player.position <= self.lunge_range:
                self.lunge(place)
            else:
                self.move(place)
        if place.turn_count == self.rattle_counter:
            self.damage -= self.rattle_buff

### Event Classes ###

class Event:
    """Parent class for the random events in the game, which can be a puzzle, a hazard, or a treasure. All Event instances have a play method that plays the event and contains all the information on what happens in the event. Therefore, each event instance has a unique play method.
    If an event has any randomized elements, the randomization occurs in the play method so that a single event instance can be used. All events are initialized without any parameters since all the important info is contained in the play method."""

    def __init__(self):
        self.name = "Event"
    
    def play(self, place):
        """The default play method takes in a place instance as a parameter, giving it access to everything it could need to function. Any randomization will occur here so a single instance can suffice for the entire game and no other new ones need to be created. The default play method
        also does nothing."""
        print("You come across an empty space. Take a breath for now and prepare yourself to continue onwards.")
    
    def __repr__(self):
        return self.name

class Three_Perks(Event):
    """This type of event consists of the player finding three statues of three Roman gods with worn away etchings. The player is able to read a 'Place your hand here to...' message, giving the player the choice to stand in front of any of the three statues for a potential permanent bonus.
    The three statues are randomly picked and the player also has the option to skip out on the bonuses entirely. Some statues give a light bonus but others give a strong bonus with a drawback."""

    statues = ["Mercury", "Mars", "Diana", "Vejovis", "Apollo"]

    def __init__(self):
        Event.__init__(self)

    def play(self, place):
        """The player can decide to get a bonus from one of the statues or they can just choose to leave without any bonus."""
        rand_gods = random.sample(self.statues, 3)
        rand_gods_lower = [x.lower() for x in rand_gods]
        print(statues_intro.format(rand_gods[0], rand_gods[1], rand_gods[2]))
        input()
        choice = fixed_input(input("What will you do? If you just want to leave, type 'Leave'. "))
        if choice == "leave":
            print("")
            print("You decide that the risk is not worth it and decide to continue your journey, leaving the room untouched and its guests unamused.")
        elif any([x in choice for x in rand_gods_lower]):
            god = None
            for z in rand_gods_lower:
                if z in choice:
                    god = z
                    break
            print("")
            eval("self." + god + "(self, place)")
            print("")
            print(statues_exit) 
        else:
            print("")
            print("Invalid input, try again")
            print("")
            return self.play(place)

    def mercury(self, place):
        """Mercury's gift gives the player a permanent movement bonus."""
        print(mercury)
        input()
        speed_boost = 1
        place.player.move_speed += speed_boost
        print("The gift of Mercury has been acquired! Your max movement speed has been increased by {0} units permanently.".format(speed_boost))

    def mars(self, place):
        """Mars's gift gives players an overall damage bonus in exchange for a decreased max health."""
        print(mars)
        input()
        damage_boost, health_decrease = 0.25, 15
        place.player.damage_bonus += damage_boost
        place.player.max_health -= health_decrease
        place.player.recalculate()
        print("The gift of Mars has been acquired! You now deal an extra {0}% more damage with each attack but your max health decreases by {1} points.".format(int(damage_boost * 100), health_decrease))

    def diana(self, place):
        """Diana's gift boosts the player's use of bows, giving a range and damage bonus and the ability to use the volley shot attack."""
        print(diana)
        input()
        damage_boost, range_bonus = 0.2, 1
        Bow.damage_bonus, Bow.range_bonus = damage_boost + Weapon.damage_bonus, range_bonus + Weapon.range_bonus
        Bow.diana_bonus = True
        print("The gift of Diana has been acquired! You now deal an extra {0}% more damage with bows and their range has been increased by {1} units. Can now use the volley shot attack that attacks all enemies within range for half damage".format(damage_boost * 100, range_bonus))

    def vejovis(self, place):
        """Vejovis's gift gives the player a healing boost to all healing items and an additional use for each item."""
        print(vejovis)
        input()
        heal_boost, use_boost = 10, 1
        place.player.heal_bonus += heal_boost
        place.player.use_bonus += use_boost
        print("The gift of Vejovis has been acquired! All healing items now heal {0} more health points and have {1} more use.".format(heal_boost, use_boost))
    
    def apollo(self, place):
        """Apollo's gift is the only way for the player to obtain the Lyre, which allows them to seranade most enemies and lower their damage."""
        lyre = Lyre()
        print(apollo)
        input()
        while True:
            answer = fixed_input(input("Will you add the Lyre to your backpack? Type 'Open backpack' to manage your backpack. "))
            if answer == "open backpack":
                print("")
                place.player.sorting()
            elif answer == "yes" and place.player.weight_limit - place.player.current_weight < lyre.weight:
                print("")
                print("Not enough room in your backpack, remove items to make space")
            elif answer == "yes":
                print("")
                place.player.backpack_add(lyre)
                print("The gift of Apollo has been acquired! The Lyre allows you to seranade all enemies on the field with Apollo's help, lowering their attacks by {0} points each".format(Lyre.attack_debuff))
                break
            elif answer == "no":
                print("")
                print("You decide to leave behind the Lyre for your own reasons.")
                break
            else: 
                print("")
                print("Invalid input, try again")
            print("")

class Legendary_Item(Event):
    """The legendary item event is when the player comes across a skeleton of a long dead adventurer like them. This skeleton has a powerful item that can aid the player in their travels. The item can be a supportive item, a weapon, or a healing item."""

    possible_items = {Rifle(50, 5, 85, 10, 500, "Ross Rifle"): ross_rifle_text}

    def __init__(self):
        Event.__init__(self)

    def play(self, place):
        """Player comes across a room, text plays to describe the room and the item found. Player has the choice to either pick up the item or to not, assuming they can carry it."""
        print(legit_intro)
        input()
        loot = random.choice(list(self.possible_items.keys()))
        print(self.possible_items[loot])
        input()
        print(loot)
        while True:
            print("")
            choice = fixed_input(input("Will you take the {0} with you? Type 'Open backpack' to manage your backpack. ".format(loot.name)))
            if choice == "no":
                print("")
                print("You decide to leave this legendary item with its original owner, certain you will find even greater things the more you push onwards. However, you do take the 500 coins that were in a puse in the coat pocket.")
                place.player.wallet += 500
                break
            elif choice == "open backpack":
                print("")
                place.player.sorting()
            elif choice == "yes" and place.player.weight_limit - place.player.current_weight < loot.weight:
                print("")
                print("Not enough room in your backpack, remove items to make space")
            elif choice == "yes":
                print("")
                place.player.backpack_add(loot)
                print("")
                print("You also take the 500 coins that were in a purse in the coat pocket")
                place.player.wallet += 500
                break
            else:
                print("")
                print("Invalid input, try again")

class Ghostly_Vision(Event):
    """Event where the player sees a ghostly vision. The player has the choice to either run away or stay and keep watching. The choice doesn't change anything as the this is a purely dialogue event."""
    possible_scenes = {ghosts_banquet: ghosts_banquet_end, ghosts_battle: ghosts_battle_end}

    def __init__(self):
        Event.__init__(self)

    def play(self, place):
        """This event plays a random vision scene and asks if the player wants to continue watching. Regardless of what they do, it plays the appropriate dialogue and ends without any changes to the player and no new items."""
        scene = random.choice(list(self.possible_scenes.keys()))
        print(scene)
        input()
        while True:
            choice = fixed_input(input("Will you run away or stay and watch what happens next? "))
            print("")
            if "run" in choice:
                print(ghosts_run)
                break
            elif "stay" in choice or "watch" in choice:
                print(self.possible_scenes[scene])
                break
            else:
                print("Invalid input, try again")
                print("")

class Merchant(Event):
    """Event where the player finds an ancient Roman merchant who serves as a shop for the player. Player is allowed to buy things, just like from the store at the beginning of the game. Merchant sells powerful yet expensive weapons and strong healing items. Player has the choice to 
    skip this event."""

    possible_items = [heavy_spear, longbow, padded_jacket, healing_syringe, rifle, armor_plate, bandages]

    def __init__(self):
        Event.__init__(self)

    def play(self, place):
        """The merchant is like any other store, except that they carry much better items than normally expected and the store is randomly generated from a list of possible items. Players also have the option to skip the store."""
        merchant, goods = Store(), random.sample(self.possible_items, 5)
        merchant.add_inventory(goods)
        print(merchant_intro)
        input()
        while True:
            choice = fixed_input(input("Will you buy items from this person or continue onwards? "))
            print("")
            if "yes" in choice or "buy" in choice:
                buying(place.player, merchant)
                break
            elif "no" in choice or "continue" in choice:
                print("For your own reasons, you decide to keep going and not stop here.")
                break
            else:
                print("Invalid input, try again")
                print("")

### Place Class ###

class Place:
    """Place class that is made up of a randomized set of tiles. Places can be visualized as a B x 1 grid, where B is an integer. Since the player begins battles ar position 0, the true length of a place is actually the size attribute + 1. Length is randomly determined by the class 
    attribute for possible sizes. Can randomly contain an enemy or event, depending on the type. A place can have up to 3 enemies at a time. The player starts at the first tile of the place and the enemies start on the opposite side. The enemies attribute is a list of enemies 
    while the event attribute is an single event instance. Different place and place types have a different list of possible enemies and events.
    """
    possible_sizes = [x for x in range(4, 6)]
    possible_enemies = [Entity.name] #Contains the possible types of enemies and events that the place can be populated with. The enemies list is filled with the name of the potential enemies, not classes
    possible_events = [Event()]
    damage_bonus = 0
    range_bonus = 0
    move_bonus = 0
    max_health_bonus = 0
    heal_bonus = 0
    move_bonus = 0
    uses_bonus = 0
    accuracy_bonus = 0

    def __init__(self, type = random.choice(["Enemy", "Event"]), size = random.choice(possible_sizes)):
        self.size = size
        self.type = type
        self.enemies = []
        self.event = Event()
        self.player = None
        self.turn_count = 1
        self.fill()

    def add_enemy(self, enemy):
        """Helper function that adds an enemy instance to the enemies list. Takes in an enemy instance as an argument."""
        self.enemies.append(enemy)
        enemy.position = self.size

    def fill(self):
        """Fills the place with either enemies (up to three) or an event, depending on the type of the room.
        """
        if self.type == "Boss":
            return
        elif self.type == "Tutorial":
            self.add_enemy(enemy_constructor(Legionary.name))
        elif self.type == "Enemy" and self.possible_enemies:
            number = random.randint(1, 3)
            for x in range(number):
                self.add_enemy(enemy_constructor(random.choice(self.possible_enemies)))
        for enemy in self.enemies:
            enemy.position = self.size #Sets each enemy's position to be at the end of the place for when battle begins.
        if self.type == "Event" and self.possible_events:
            self.event = random.choice(self.possible_events)
    
    def show_enemies(self):
        """Prints all the enemies at the current place. 
        """
        print("*** Enemies ***")
        for enemy in self.enemies:
            print(enemy)

    def visualize(self):
        """Visualizes the place by showing it as a series of underscores for empty tiles. Tiles with an entity are replaced with their class symbol. Since multiple enemies can be on the same spot, that is also reflected on the visualization.
        >>> steve = Player("Steve")
        >>> steve.position = 0
        >>> place = Place("Tutorial", 4)
        >>> place.player = steve
        >>> place.visualize()
        [ Steve, ________, ________, ________, Legionary ]
        """
        spots = ["________"] * (self.size + 1)
        spots[self.player.position] = self.player.name
        for enemy in self.enemies:
            if spots[enemy.position] == "________":
                spots[enemy.position] = enemy.name
            else:
                spots[enemy.position] += " / " + enemy.name
        separator = ", "
        print("[ " + separator.join(spots) + " ]")

    def __repr__(self):
        return "Place"

    def __str__(self):
        return "{0} Place, Size: {1}".format(self.type, self.size)

class Forest_Place(Place):
    """Place class for locations in the forest. Small length places that can have Legionaries, Immortal Dogs, and Feral Monkeys. The final fight of the jungle section will be a large snake.
    """
    possible_sizes = [x for x in range(3, 6)]
    possible_enemies = [Legionary.name, Immortal_Dog.name, Feral_Monkey.name]
    possible_events = [Legendary_Item(), Ghostly_Vision(), Merchant()]
    range_bonus = -1
    damage_bonus = 0.20

    def __init__(self, type = random.choice(["Enemy", "Event"]), size = random.choice(possible_sizes)):
        Place.__init__(self, type, size)

### Store Class ###

class Store:
    """Class for the store at the beginning of the game, which gives players the only chance to buy equipment before going on their journey. A store has an inventory of items, which are in the form of a dictionary where 
    the keys are the name of the item and the values are the object instances themselves.
    >>> x = Store()
    >>> x.inventory
    {}
    >>> x
    Store instance
    >>> print(x)
    Store selling []
    """

    def __init__(self):
        self.inventory = {}

    def add_inventory(self, lst):
        """Takes in a list of equipment instances and adds them to the store's inventory, which is a dictionary. Keys are the name of the weapon (all lowercase) and the values are equipment instances themselves. If multiple
        of the same equipment is being added, create a new key for each of them. This will make deletion easier in the future.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> store = Store()
        >>> store.add_inventory([spear])
        >>> store.inventory
        {'spear': Spear}
        """
        for x in lst:
            self.inventory[x.name.lower()] = x
    
    def remove_inventory(self, item_name):
        """Removes an instance of an object from the store inventory. If there are no more object instances for a key, remove that key. item_name is a lowercase string version of the name of the item being removed.
        >>> weapon = Weapon(20, 1, 1, 100, "Spear")
        >>> store = Store({"spear": weapon})
        >>> store.inventory
        {'spear': Spear}
        >>> store.remove_inventory("spear")
        >>> store.inventory
        {}
        """
        if item_name in self.inventory:
            del self.inventory[item_name]
        else:
            print("Item not in inventory")

    def show_inventory(self):
        """Shows the store's inventory by printing out, with each item on a different line"""
        print("*** Store Menu ***")
        [print(x) for x in self.inventory.values() if x.class_name == Weapon.class_name]
        [print(x) for x in self.inventory.values() if x.class_name == Healing_Tool.class_name]
        [print(x) for x in self.inventory.values() if x.class_name == Equipment.class_name]

    def purchase(self, player, item_name):
        """Allows for the player to purchase an item from the store. Must check to see if the player can carry an item and if the player has enough money to buy it.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> expensive_weapon = Weapon(20, 1, 1, 2000, "Expensive")
        >>> heavy_weapon = Weapon(20, 1, 100, 100, "Heavy")
        >>> player = Player("Dan")
        >>> store = Store()
        >>> store.purchase(player, spear)
        Item not in store
        >>> store.add_inventory([spear, expensive_weapon, heavy_weapon])
        >>> store.purchase(player, "spear")
        Purchased Spear for 100 coins
        Added Spear to backpack
        Wallet: 900
        >>> store.purchase(player, "expensive")
        Not enough money
        >>> store.purchase(player, "heavy")
        Adding item would go over the weight limit
        """
        if item_name not in self.inventory:
            print("Item not in store")
            return
        item = self.inventory.get(item_name)
        if player.wallet < item.price:
            print("Not enough money")
            return
        if player.weight_limit - player.current_weight < item.weight:
            print("Adding item would go over the weight limit")
            return
        else:
            print("Purchased {0} for {1} coins".format(item.name, item.price))
            player.backpack_add(self.inventory.pop(item_name))
            player.wallet -= item.price
            print("Wallet: {0}".format(player.wallet))

    def refund(self, player, item_name): 
        """Allows for the player to refund an item to the store, placing that item back into the store's inventory and adding the price of the item back to the player's wallet.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> store = Store()
        >>> player = Player("Dan")
        >>> player.backpack_add(spear)
        Added Spear to backpack
        >>> store.refund(player, "spear")
        Spear refunded for 100 coins
        Spear removed from backpack
        Wallet: 1100
        >>> player.wallet
        1100
        """
        if item_name in player.backpack:
            item = player.backpack.get(item_name)
            print("{0} refunded for {1} coins".format(item.name, item.price))
            self.add_inventory([player.backpack.get(item_name)])
            player.backpack_remove(item_name)
            player.wallet += item.price
            print("Wallet: {0}".format(player.wallet))
        else:
            print("Item does not exist in backpack")
    
    def __repr__(self):
        return "Store instance"

    def __str__(self):
        goods = []
        for item in self.inventory.values():
            goods.append(item.name)
        return "Store selling {0}".format(str(goods))

### Game Manager ###

def fixed_input(s):
    """Takes an input string s and returns a new string that is reformatted to remove the spaces before and after s and make 
    everything lowercase.
    >>> x = fixed_input("   The cow jumped over the Moon   ")  
    >>> x 
    'the cow jumped over the moon'
    """
    return s.lower().strip()

def buying(player, store):
    """Function that allows the player to purchase items from the store. Player can either buy an item, refund an item, or type "Done" to finalize their purchase and start their adventure. Raises an Invalid Input message if the input is one word that is not 'Done' 
    or if it's multiple words that are not a valid command. The except case handles the first issue and the else case handles the second issue.  
    """
    while True:
        store.show_inventory()
        print("")
        player.show_backpack()
        print("")
        command = fixed_input(input("What do you want to do? Type 'Buy' or 'Refund' followed by the name of the item or type 'Done' to leave the store. "))
        try:
            action = command.split(" ", 1)[0]
            if action == "done":
                break
            item_name = command.split(" ", 1)[1]
            if action == "buy":
                print("")
                store.purchase(player, item_name)
                print("")
            elif action == "refund":
                print("")
                store.refund(player, item_name)
                print("")
            else:
                print("")
                print("Invalid input, try again")
                print("")
        except:
            print("")
            print("Invalid input. If buying or refunding, make sure to type in the action followed by the name of the item")
            print("")

def enemy_constructor(name):
    """Takes in a string version of the name of a class and then constructs instances of that class. This allows the game to generate new enemies. Uses a variety of conditional statements to decide which class instance to create. If stats of a class are to be changed, change them here.
    >>> x = enemy_constructor("Legionary")
    >>> isinstance(x, Legionary)
    True
    """
    if name == Legionary.name:
        return Legionary()
    elif name == Immortal_Dog.name:
        return Immortal_Dog()
    elif name == Feral_Monkey.name:
        return Feral_Monkey()
    elif name == Giant_Snake.name:
        return Giant_Snake()

def onward(player, place):
    """Moves the player onto a new place, where if the place is an enemy place, a battle will begin and if the place is an event place, the event will be played"""
    place.player, player.place = player, place
    player.recalculate(place)
    player.position = 0
    if place.enemies:
        battle(place)
    else:
        place.event.play(place)
        if place.event in place.possible_events:
            place.possible_events.remove(place.event)
    while True:
        print("")
        choice = fixed_input(input("Type 'Open backpack' to manage your backpack or 'Continue' to move forwards. "))
        if choice == "continue":
            print("")
            print("You continue forwards")
            break
        elif choice == "open backpack":
            print("")
            player.sorting()
        else:
            print("")
            print("Invalid input, try again")

def battle(place):
    """Facilitates the entire battle if a player is in an enemy place. Battles begin with the player at position 0 and the enemies at the opposite end. The player always makes the first turn, then all the enemies."""
    openings = ["Hostiles in front of you, prepare to fight!", "Enemies ahead, stand your ground!", "Enemies approaching, here we go!", "Aggressive foes ahead, they want you dead!", "Get ready, these creatures live for death!"]
    print(random.choice(openings))
    print("")
    print(">>> Battle begin")
    def fight(): #Using this internal function to avoid writing a battle opening for every call of the function
        print("")
        print("TURN {0}".format(place.turn_count))
        print("")
        print(">>> {0}'s Turn".format(place.player.name))
        print("")
        place.player.take_turn(place)
        for enemy in place.enemies:
            time.sleep(1.5)
            print("")
            print(">>> {0}'s Turn".format(enemy.name))
            if random.randint(1, enemy.line_chance) == 1:
                print("")
                print(random.choice(enemy.battle_lines))
            enemy.take_turn(place)
        if place.enemies:
            place.turn_count += 1
            time.sleep(1.5)
            return fight()
        print("")
        print(">>> End of battle")
    fight()
    
def game_over():
    """Function that prints a game over message when the player dies and quits the program"""
    print("You have died! The lost treasure will remain hidden from the rest of the world. Perhaps this is for the better.")
    quit()