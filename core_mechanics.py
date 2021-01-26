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
    
    def __init__(self, weight, name="Equipment"):
        self.weight = weight
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
        return "{0}, Weight: {1} lbs".format(self.name, self.weight)

class Armor_Piece(Equipment):
    """Armor pieces are equipment that the player can get to add to their armor value, protecting their health from non armor piercing attacks. Armor pieces have to be used first, so their action method is what adds to the player's armor, not just the act
    of acquiring it. All armor pieces are a single use only. 
    """
    combat_item = True

    def __init__(self, armor, weight, name="Armor Piece"):
        Equipment.__init__(self, weight, name)
        self.armor = armor

    def action(self, place):
        """The action method simply adds armor to the player's armor stat and then are removed from their inventory."""
        place.player.armor += self.armor
        print("Added {0} points of armor".format(self.armor))
        print("")
        place.player.inventory_remove(self)

    def __str__(self):
        return "{0}, Armor: {1} Weight: {2} lbs".format(self.name, self.armor, self.weight)

class Shield(Equipment):
    """Shields are a piece of equipment that the player can choose to use during battle, reducing damage by a certain amount for a certain number of turns. It does this by directly lowering the enemy's damage as long as the effect lasts. Damage reduction is written as the percentage of damage
    remaining after the shield's effect in decimal form. A specific shield cannot be used multiple times in a row, which would create consecutive damage reductions."""

    combat_item = True

    def __init__(self, damage_multiplier, buff_length, weight, name="Shield"):
        Equipment.__init__(self, weight, name)
        self.damage_multiplier = damage_multiplier
        self.buff_length = buff_length
        self.buff_counter = 0
        self.used = False

    def action(self, place):
        """Multiplies the damage of all enemies on the current place by the damage multiplier, which should never be equal to or greater than 1. Sets the buff counter to the turn when the shield buff will wear off. Since the buff can last across battles, use the global turn count. Set the
        used attribute to True and keep it like that until the shield's buff is over. Make sure to add this item to the Place time items list only once. If the shield is already in use, show a message and let the player do something else."""
        if self.used:
            print("{0} is already in use, pick another item to use.".format(self.name))
            return 
        for enemy in place.enemies:
            enemy.damage = round(enemy.damage * self.damage_multiplier)
        print("{0} reduced the enemy's attacks by {1}% for {2} turns!".format(self.name, round((1 - self.damage_multiplier) * 100), self.buff_length))
        self.used, self.buff_counter = True, Place.global_turns + self.buff_length
        if self not in Place.current_time_items:
            Place.current_time_items.append(self)

    def check(self, place):
        """If the buff is up, then divide all the damage of all enemies by the damage multiplier to undo the shield's damage reduction. Then, remove this item from the Place time item list. Set the used attribute back to False so the player can use the shield again."""
        if Place.global_turns == self.buff_counter:
            for enemy in place.enemies:
                enemy.damage = int(enemy.damage / self.damage_multiplier)
            Place.current_time_items.remove(self)
            self.used = False

    def __str__(self):
        return "{0}, Damage Reduction: {1}%, Block Duration: {2} turns, Weight: {3} lbs".format(self.name, round((1 - self.damage_multiplier) * 100), self.buff_length, self.weight)

class Booster(Equipment):
    """Booster equipment are items that provide limited time boosts to the player in one stat, which is specified when the instance is created. Booster equipment purely give positive changes to the player, not negative ones. They are also universal bonuses so they cannot be for a specific class of weapon for example. Boosters are always single use items."""
    class_name = "Booster"
    combat_item = True
    time_check = True

    def __init__(self, bonus, kind, bonus_length, weight, name="Booster"):
        Equipment.__init__(self, weight, name)
        self.bonus = bonus
        self.kind = kind
        self.bonus_length = bonus_length
        self.bonus_counter = 0

    def action(self, place):
        """There are six stats the player can have a bonus in: damage, range, healing, move speed, accuracy, or max health. For each one except max health, apply the bonus to the player's respective bonus attribute, calculate the bonus counter using the global turn count, add this item to the time items list in the Place class, and remove the booster from the player's inventory."""
        if self.kind == "max health":
            place.player.max_health += self.bonus
            print("{0} increased {1} by {2} points for {3} turns".format(self.name, self.kind, self.bonus, self.bonus_length))
        elif self.kind == "damage":
            place.player.damage_bonus += self.bonus
            print("{0} increased {1} by {2}% for {3} turns".format(self.name, self.kind, round(self.bonus * 100), self.bonus_length))
        elif self.kind == "range":
            place.player.range_bonus += self.bonus
            print("{0} increased {1} by {2} units for {3} turns".format(self.name, self.kind, self.bonus, self.bonus_length))
        elif self.kind == "healing":
            place.player.heal_bonus += self.bonus
            print("{0} increased {1} by {2} points for {3} turns".format(self.name, self.kind, self.bonus, self.bonus_length))
        elif self.kind == "movement":
            place.player.move_bonus += self.bonus
            print("{0} increased {1} by {2} points for {3} turns".format(self.name, self.kind, self.bonus, self.bonus_length))
        elif self.kind == "accuracy":
            place.player.accuracy_bonus += self.bonus
            print("{0} increased {1} by {2}% for {3} turns".format(self.name, self.kind, self.bonus, self.bonus_length))
        self.bonus_counter = place.global_turns + self.bonus_length
        Place.current_time_items.append(self)
        print()
        place.player.inventory_remove(self)

    def check(self, place):
        """Essentially does what happens in action but backwards, removing the bonus. Also, remove the item from the current time items list in the Place class."""
        if place.global_turns == self.bonus_counter:
            if self.kind == "max health":
                place.player.max_health -= self.bonus
            elif self.kind == "damage":
                place.player.damage_bonus -= self.bonus
            elif self.kind == "range":
                place.player.range_bonus -= self.bonus
            elif self.kind == "healing":
                place.player.heal_bonus -= self.bonus
            elif self.kind == "movement":
                place.player.move_bonus -= self.bonus
            elif self.kind == "accuracy":
                place.player.accuracy_bonus -= self.bonus
            Place.current_time_items.remove(self)

    def __str__(self):
        return "{0}, {1} Bonus: {2}, Bonus Length: {3}, Weight: {4} lbs".format(self.name, self.kind.capitalize(), ((str(round(self.bonus * 100)) + "%") if self.kind == "damage" else self.bonus) , self.bonus_length, self.weight)

class Weapon(Equipment): 
    """Weapons that the player and enemies can use to fight with. Each weapon has damage, range, weight, and price. Some weapons can have an armor piercing ability.
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
    ranged = False
    
    def __init__(self, damage, range, weight, name="Weapon"):
        Equipment.__init__(self, weight, name)
        self.damage = damage
        self.range = range
        self.eff_damage = damage
        self.eff_range = range
    
    def recalculate(self, place):
        """Recalculates the effective damage and range of the weapon, taking into account the bonuses of the weapon class, the player, and the current place."""
        self.eff_damage = int(max(self.damage * (1 + place.player.damage_bonus), 5)) #Prevents the weapons from becoming useless 
        if self.ranged:
            self.eff_range = int(max(self.range + place.player.range_bonus, 1)) #Range must be at least 1 and only ranged weapons get a range bonus

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
        choice = fixed_input(input("Who will you attack? Type the number of the enemy you will attack or type 'Back' to perform a different action. "))
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
        return "{0}, Damage: {1}, Range: {2} units, Weight: {3} lbs, Armor Piercing: {4}".format(self.name, self.eff_damage, self.eff_range, self.weight, self.armor_piercing)

class Firearm(Weapon):
    """Firearms are powerful ranged weapons similar to bows but in exchange for their great power, each firearm has an accuracy rating that determines if the weapon hits the target or misses. Accuracy is a value between 0 and 100."""
    ranged = True

    def __init__(self, damage, range, accuracy, weight, armor_piercing=True, name="Firearm"):
        Weapon.__init__(self, damage, range, weight, name)
        self.armor_piercing = armor_piercing
        self.accuracy = accuracy
        self.eff_accuracy = accuracy

    def recalculate(self, place):
        """Uses the normal weapon class recalculation plus recalculates the effective accuracy attribute."""
        Weapon.recalculate(self, place)
        self.eff_accuracy = int(max(min(self.accuracy + place.player.accuracy_bonus, 100), 40)) #Ensures that accuracy will never surpass 100 but will also always be at least 40

    def attack(self, place, target):
        """Rifles have to perform a random roll to see if they hit their target or not."""
        hit = random.choices([1, 0], weights=(self.eff_accuracy, 100 - self.eff_accuracy))
        if hit[0]:
            target.injure(place, self.eff_damage, self.armor_piercing)
        else:
            print("You missed!")
        
    def __str__(self):
        return "{0}, Damage: {1}, Range: {2} units, Accuracy: {3}, Weight: {4} lbs, Armor Piercing: {5}".format(self.name, self.eff_damage, self.eff_range, self.eff_accuracy, self.weight, self.armor_piercing)

class Shotgun(Weapon):
    """Shotguns are a powerful short ranged weapon that have no accuracy stat but have extremely limited range. In exchange, shotguns are damage machines. For every space closer to the player that the enemy is past the maximum range, the gun gains a damage bonus. Furthermore, a player is able
    to deal full damage to the selected enemy but then all other enemies on the same spot as that enemy are also hit by the spread of the pellets, causing reduced damage."""
    ranged = True

    def __init__(self, damage, range, spread_multiplier, cqc_bonus, weight, name="Shotgun"):
        Weapon.__init__(self, damage, range, weight, name)
        self.spread_multiplier = spread_multiplier
        self.cqc_bonus = cqc_bonus

    def attack(self, place, target):
        """For every 1 unit the enemy is closer to the player after the max range of the shotgun, the player gets a damage addition determined by the CQC bonus attribte. When the player picks a target to attack, the other enemies on that same place as get hit with reduced damage, which is
        determined by the spread multiplier attribute."""
        dmg = round(self.eff_damage + (self.cqc_bonus * (self.eff_range - (target.position - place.player.position))))
        target.injure(place, dmg, self.armor_piercing)
        for enemy in place.enemies:
            if enemy.position == target.position and enemy is not target:
                print()
                enemy.injure(place, round(dmg * self.spread_multiplier), self.armor_piercing)

class Flamethrower(Weapon):
    """Harnessing the power of fire, the flamethrower is a devestating weapon the player can get in the late game. It shoots an intense stream of fire, damaging all enemies in the spots between the player and the selected target, including all enemies in the same position as the target. 
    The player still has to pick a target so use the default action method. Enemies hit by the flamethrower also are lit on fire, causing them to have burn damage for a few turns. Burn damage cannot be changed by any bonuses. This weapon is not armor piercing, in order to remain balanced, 
    and has a limited range."""

    def __init__(self, damage, burn_damage, burn_length, range, weight, name="Flamethrower"):
        Weapon.__init__(self, damage, range, weight, name)
        self.burn_damage = burn_damage
        self.burn_length = burn_length

    def attack(self, place, target):
        """Damage all enemies in all spots between the player and the place of the target, including all enemies on the target spot as well. All enemies hit will be on fire, changing their on fire attribute to True. Set the burn counter attribute here. Since enemies must be slain to progress
        forward, can use the place's turn counter instead of the global turn count. This weapon is also placed in the Place time item list. The check method will handle inflicting burn damage, so don't worry about that here. Enemies are given an on fire attribute so that 
        burn damage does not stack continually."""
        hostiles = [x for x in place.enemies if place.player.position < x.position <= target.position] #Using a new list allows the program to check if it should print an extra line or not
        for enemy in hostiles:
            enemy.injure(place, self.eff_damage, self.armor_piercing)
            enemy.on_fire, enemy.burn_counter = True, place.turn_count + self.burn_length
            if enemy is not hostiles[len(hostiles) - 1]: #Prevents addition of an extra line if the enemy is the last one in the list
                print()
        if self not in Place.current_time_items: #Prevents the same flamethrower from being added multiple times
            Place.current_time_items.append(self)

    def check(self, place):
        """Checks if the burn effect has worn off, either because there are no more enemies left, signalling the end of battle, or if the burn counter is equal to the place's turn count. If the effect wears off, set each enemy's on fire attribute back to False and remove the weapon from
        the Place time items list. If the effect is still ongoing, apply the burn damage to each enemy on fire. Burn damage pierces through armor so set AP to be True for the injure argument."""
        if all(enemy.on_fire == False for enemy in place.enemies):
            Place.current_time_items.remove(self)
        else:
            for enemy in list(place.enemies):
                if enemy.burn_counter == place.turn_count:
                    enemy.on_fire = False
                if enemy.on_fire:
                    print()
                    enemy.injure(place, self.burn_damage, True)
            if not place.enemies:
                Place.current_time_items.remove(self)

    def __str__(self):
        return "{0}, Damage: {1}, Burn Damage: {2}, Burn Length: {3} turns, Range: {4} units, Weight: {5} lbs, Armor Piercing: {6}".format(self.name, self.eff_damage, self.burn_damage, self.burn_length, self.eff_range, self.weight, self.armor_piercing)

class Explosive(Weapon):
    """Explosives are weapons that are thrown and do damage to all enemies on the same place as the targeted enemy and all enemies in places within the blast radius. Explosives have a limited amount of uses that cannot be changed by any bonuses nor can be refilled."""

    def __init__(self, damage, blast_radius, range, uses, weight, name="Explosive"):
        Weapon.__init__(self, damage, range, weight, name)
        self.blast_radius = blast_radius
        self.uses = uses

    def attack(self, place, position):
        """Attack method damages all enemies on the same place as the chosen location and also all enemies on positions within the blast radius. If the player is within the blast radius, injure them as well with the same damage. If the item runs out of uses, remove it from the inventory."""
        for enemy in place.enemies:
            if enemy.position >= position - self.blast_radius and enemy.position <= position + self.blast_radius:
                enemy.injure(place, self.damage, self.armor_piercing)
                print()
        if position - self.blast_radius <= place.player.position <= position + self.blast_radius:
            print("You were caught in the blast radius, damaging youself!")
            print()
            place.player.injure(place, self.damage, self.armor_piercing)
        self.uses -= 1
        if not self.uses:
            place.player.inventory_remove(self)

    def action(self, place):
        """Instead of picking an enemy to attack, the player picks a certain position to attack in front of them, meaning this action method has to show valid positions instead of valid targets."""
        pos = []
        place.visualize()
        print()
        print("*** Positions ****")
        for x in range(place.player.position + 1, place.size + 1):
            pos.append(x + 1)
        print(pos)
        print()
        choice = fixed_input(input("Which position will you aim your explosive? Type in the number of the position to attack or 'Back' to do something else. "))
        if choice == "back":
            print()
            return place.player.take_turn(place)
        elif not choice.isnumeric() or int(choice) not in range(place.player.position + 1, place.size + 2):
            print()
            print("Invalid input, answer must be a valid numeric input")
            print()
            return self.action(place)
        choice = int(choice)
        print()
        self.attack(place, choice - 1)

    def __str__(self):
        return "{0}, Damage: {1}, Blast Radius: {2} units, Range: {3} units, Uses: {4}, Weight: {5} lbs, Armor Piercing: {6}".format(self.name, self.eff_damage, self.blast_radius, self.eff_range, self.uses, self.weight, self.armor_piercing)

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

    def __init__(self, heal_amount, uses, weight, name = "Healing Equipment"):
        Equipment.__init__(self, weight, name)
        self.heal_amount = heal_amount
        self.eff_heal = heal_amount
        self.uses = uses
        self.eff_uses = uses

    def recalculate(self, place):
        """Recalculates the effective healing of a healing item by taking into account the base heal amount, heal bonus of the class, heal bonus of the player, and heal bonus of the place."""
        self.eff_heal = int(max(self.heal_amount + place.player.heal_bonus, 5)) #Prevents item from being completely useless

    def effect(self, place, amount):
        """Method that performs the intended effects of a healing item. The default is to heal the player by a specified amount and then remove the item from their inventory if it's out of uses."""
        place.player.health += amount
        self.uses -= 1
        print("Healed for {0} HP, {1} uses remaining".format(amount, self.uses))
        self.recalculate(place)
        if not self.eff_uses:
            print("")
            place.player.inventory_remove(self)

    def action(self, place):
        """The default action method for healing items is to heal the player, with the heal amount determined by their heal amount attribute. Players cannot go over their maximum health. Remove the healing item from inventory if it is out of uses. If the player is already at max health, \
        then display a message and let the player try another action. Almost all healing items will use the same action method."""
        diff = place.player.eff_max_health - place.player.health
        if diff == 0:
            print("Health already maximum, can not use this")
            return None
        elif diff <= self.eff_heal:
            self.effect(place, int(diff))
        else:
            self.effect(place, self.eff_heal)

    def __str__(self):
        return "{0}, Heal Amount: {1} HP, Uses Left: {2}, Weight: {3} lbs".format(self.name, self.eff_heal, self.eff_uses, self.weight)

class Adrenaline(Healing_Tool):
    """Adrenaline shots heal the player but also give a temporary damage boost for a certain amount of turns."""

    def __init__(self, heal_amount, damage_bonus, bonus_length, uses, weight, name="Adrenaline"):
        Healing_Tool.__init__(self, heal_amount, uses, weight, name)
        self.damage_bonus = damage_bonus
        self.in_effect = False
        self.bonus_counter = 0
        self.bonus_length = bonus_length
    
    def effect(self, place, amount):
        """Adrenaline shots heal the player and then apply a damage bonus for a certain amount of time set by the bonus length attribute. After the time is up, remove the damage bonus using the check method. Player can use the adrenaline to heal even if they can't benefit from the 
        damage buff.
        """
        Healing_Tool.effect(self, place, amount)
        if not self.in_effect: 
            place.player.damage_bonus += self.damage_bonus
            self.bonus_counter, self.in_effect = Place.global_turns + self.bonus_length, True #Bonus counter holds info on when to stop the effect
            Place.current_time_items.append(self)
            print()
            print("{0} gained a {1}% damage boost for {2} turns".format(place.player.name, int(self.damage_bonus * 100), self.bonus_length))
        else:
            print()
            print("Adrenaline damage bonus already in effect, cannot perform bonus again")

    def check(self, place):
        """The check method is run at the end of every turn to see if the bonus of the adrenaline has worn off. If it has worn off, set the in effect method back to False and reduce the player's damage bonus attribute by the adrenaline's damage bonus."""
        if Place.global_turns == self.bonus_counter:
            place.player.damage_bonus -= self.damage_bonus
            self.in_effect = False
            Place.current_time_items.remove(self)
            print()
            print("Adrenaline damage bonus has worn off")

    def __str__(self):
        return "{0}, Heal Amount: {1} HP, Uses Left: {2}, Damage Bonus: {3}, Bonus Length {4} turns, Weight: {5} lbs".format(self.name, self.eff_heal, self.eff_uses, self.damage_bonus, self.bonus_length, self.weight)

### In-Game Items ###

wrench = "Weapon(30, 1, 5, 'Wrench')"
shank = "Weapon(35, 1, 0.5, 'Shank')"
stun_baton = "Weapon(50, 1, 2, 'Stun Baton')"
pistol = "Firearm(40, 3, 95, 5, False, 'LP-2043 Laser Pistol')"
rifle = "Firearm(50, 4, 70, 8, False, 'LR2047-7 Laser Rifle')"
sniper_rifle = "Firearm(50, 5, 80, 15, True, 'LR 2050-SR Precision Laser Rifle')"
shotgun = "Shotgun(60, 2, 0.7, 50, 20, 'CQC-2049L Laser Shotgun')"
flamethrower = "Flamethrower(70, 20, 4, 5, 10, 'F-2048 Flamethrower')"

grenade = "Explosive(75, 1, 5, 1, 2, 'PG-2039 Plasma Grenade')"

guard_vest = "Armor_Piece(30, 1, 'Guard Vest')"
salvaged_armor = "Armor_Piece(40, 4, 'Salvaged Armor Pieces')"
engineer_armor = "Armor_Piece(50, 2, 'Engineer Armor')"
wd_armor = "Armor_Piece(50, 1, 'War Dog Armor')"
marksman_vest = "Armor_Piece(50, 2, 'Marskman Vest')"
ballistic_vest = "Armor_Piece(80, 5, 'Ballistic Vest')"
heavy_armor = "Armor_Piece(100, 7, 'Heavy Armor')"
riot_armor = "Armor_Piece(150, 12, 'Riot Armor')"

stim = "Healing_Tool(50, 1, 0.5, 'Stim Shot')"
adrenaline = "Adrenaline(70, 0.4, 2, 1, 1)"
nano_stim = "Adrenaline(70, 0.7, 4, 3, 3, 'Nano Stim')"

riot_shield = "Shield(0.50, 3, 14, 'Riot Shield')"

gum = Booster(15, "accuracy", 2, 0.5, "Chewing Gum")

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
    time_check = False

    def __init__(self, health, armor):
        self.health = health
        self.armor = armor
        self.on_fire = False
        self.burn_counter = 0
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
        print("{0} took {1} {2}!".format(self.name, damage, ("armor piercing damage" if AP else "damage")))
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
    Has an inventory with a certain weight capacity
    >>> x = Player("Dave")
    >>> x.inventory
    []
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
    accuracy_bonus = 0

    def __init__(self, name, health=100, armor=0, move_speed=1):
        Entity.__init__(self, health, armor)
        self.name = name
        self.move_speed = move_speed
        self.eff_move = move_speed 
        self.inventory = [Weapon(25, 1, 0, "Fists")]
        self.current_weight = 0
        self.weight_limit = 30
        self.max_health = 100
        self.eff_max_health = self.max_health
        self.place = None
    
    def recalculate(self, place):
        """The player recalculate method recalculates their move speed stat and all the items in their inventory."""
        self.eff_move = int(max(self.move_speed + self.move_bonus, 1)) #Player will always move at least one unit
        self.eff_max_health = int(max(50, self.max_health)) #Player max health will always be at least 50 points
        if self.health > self.eff_max_health:
            self.health = self.eff_max_health
        for item in self.inventory:
            item.recalculate(place)

    def inventory_add(self, item):
        """Adds item to the player's inventory as long as adding the weight of the item does not cause the current weight to exceed the weight_limit.
        >>> player = Player("Dan")
        >>> x = Weapon(20, 1, 5, 50)
        >>> player.inventory_add(x)
        Added Weapon to inventory
        >>> z = Weapon(20, 1, 75, 50)
        >>> player.inventory_add(z)
        Weight limit exceeded. Remove items to add this
        """
        if self.weight_limit - self.current_weight >= item.weight:
            self.inventory.append(item)
            self.current_weight = sum([x.weight for x in self.inventory])
            print("Added {0} to inventory".format(item.name))
        else:
            print("Weight limit exceeded. Remove items to add this")

    def inventory_remove(self, item):
        """Allows for the removal of an item from the player's inventory.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> player = Player("Dan")
        >>> player.inventory_add(spear)
        Added Spear to inventory
        >>> player.inventory
        [Spear]
        >>> player.inventory_remove(spear)
        Spear removed from inventory
        >>> player.inventory 
        []
        """
        permanent = ["fists"]
        if item.name.lower() in permanent:
            print("Cannot remove this item from your inventory")
        elif item in self.inventory:
            self.inventory.remove(item)
            self.current_weight = sum([x.weight for x in self.inventory])
            print("{0} removed from inventory".format(item.name))
        else:
           print("Equipment not in inventory")

    def show_inventory(self):
        """Displays all the items in the player's inventory, with one item on each line."""
        self.recalculate(self.place)
        print("*** Inventory (Weight: {0} / {1}) ***".format(self.current_weight, self.weight_limit))
        i = 0
        for x in self.inventory:
            print("[{0}] ".format(i) + str(x))
            i += 1

    def show_weapons(self):
        """Displays all the weapons that the player is carrying."""
        self.recalculate(self.place)
        print("*** Weapons ***")
        weapons, i = [x for x in self.inventory if isinstance(x, Weapon)], 0
        for item in sorted(weapons, key=lambda x: x.range, reverse=True): 
            print("[{0}] ".format(i) + str(item))
            i += 1

    def use_weapon(self):
        """Allows the player to select a weapon from their inventory and return the weapon object for them to use. Returns None if the weapon isn't in the inventory"""
        self.show_weapons()
        print("")
        index = fixed_input(input("What weapon will you use? Type the name of the number of it or 'Back' to perform a different action. ")) #There will be no weapon with a name of 'None'
        if index == 'back':
            return None
        elif not index.isnumeric() or int(index) not in range(len([x for x in self.inventory if isinstance(x, Weapon)])):
            print("")
            print("Not a valid numerical input")
            return None
        index, weapons = int(index), sorted([x for x in self.inventory if isinstance(x, Weapon)], key=lambda x: x.range, reverse=True)
        if index in range(len(weapons)):
            return weapons[index]
        print("")
        print("Weapon not in inventory")

    def use_inventory(self):
        """Allows the player to access their inventory and select an item to use. This method returns the item object so the game can see what item the player wants to use. If the player closes the inventory, return None. If the player gives an invalid input,
        raise an error and also return None. If the player removes an item, remove the item from the inventory and return None."""
        self.show_inventory()
        print("")
        choice = fixed_input(input("What would you like to do? Type 'Use' or 'Drop' followed by the number of the item or 'Back' to go back. "))
        if choice == "back":
            return None
        try:
            action, index = choice.split(" ", 1)[0], choice.split(" ", 1)[1]
        except:
            print()
            print("Invalid input, try again")
            return None
        if not index.isnumeric():
            print()
            print("Invalid input, ensure you are typing in a valid number.")
            return None
        index = int(index)
        if action == "use":
            if index in range(len(self.inventory)):
                return self.inventory[index]
            print()
            print("Equipment not in inventory")
            return None
        elif action == "drop":
            if index in range(len(self.inventory)):
                print()
                return self.inventory_remove(self.inventory[index])
            print()
            print("Equipment not in inventory")
            return None
        else:
            print()
            print("Invalid command")

    def sorting(self):
        """Allows the player to sort their items when OUT OF COMBAT. Used at the end of a battle or event. Essentially a modified version of the use_inventory method that prevents the player from using a healing item at max health or a weapon, as that can cause a game breaking infinite turn."""
        item = self.use_inventory()
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
        """Method that allows the player to take their turn during combat. Players can either attack, move, or use an item in their inventory. If the player puts in an invalid input, allow them to try again. If the enemy is out of a weapon's range, 
        display a message saying so and let the player try again. If the player chooses an piece of equipment that isn't combat oriented, display a message and try again.
        """
        place.player.recalculate(place)
        place.visualize()
        print()
        print("*** Player ***")
        print("{0}, Health: {1}, Armor: {2}, Move Speed: {3} units per turn".format(self.name, self.health, self.armor, self.eff_move))
        print()
        place.show_enemies()
        print()
        action = fixed_input(input("What will you do? Type 'Attack' to attack the enemy, 'Move' to move, or 'Inventory' to look at and use something in your inventory. "))
        print()
        if action == "attack": #Attack decision
            weapon = self.use_weapon()
            if not weapon:
                print()
                self.take_turn(place)
            else: 
                print()
                weapon.action(place)
        elif action == "move": #Movement decision
            self.move(place)
        elif action == "inventory": #Item usage decision
            item = self.use_inventory()
            print()
            if item and item.combat_item:
                item.action(place)
                if not isinstance(item, Weapon):
                    print()
                    self.take_turn(place)
            elif item and not item.combat_item:
                print("Not an item for combat, try again")
                print()
                self.take_turn(place)
            else:
                self.take_turn(place)
        else:
            print("Invalid input, try again")
            print()
            self.take_turn(place)

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
    possible_loot = []
    can_drop = True
    armor_piercing = False
    machine = False
    charmable = True

    def __init__(self, health, armor, damage, range, move_speed):
        Entity.__init__(self, health, armor)
        self.default_health = health
        self.damage = damage
        self.range = range
        self.move_speed = move_speed
    
    def move(self, place, back=False):
        """Default move method that advances the enemy towards the player as much as possible unless the player is within range or they reach the end of the place. If the back argument is True, this function will move the enemy as far away as possible."""
        if not back:
            dist = self.position - (place.player.position + self.range)
            self.position = self.position - min(dist, self.move_speed)
        elif back:
            dist = place.size - self.position
            self.position = self.position + min(dist, self.move_speed)
        print("{0} moved {1} steps {2}!".format(self.name, min(dist, self.move_speed), ("towards you" if not back else "away from you")))

    def attack(self, place):
        """Method that calls the player's injure method to apply the normal damage"""
        print("{0} attacks!".format(self.name))
        print()
        place.player.injure(place, self.damage, self.armor_piercing)

    def take_turn(self, place):
        """The default take turn method for enemies. The enemy will either advance towards the player if the player is not in range or they will attack if the player is in range."""
        print()
        if self.position - place.player.position <= self.range:
            self.attack(place)
        else:
            self.move(place)

    def remove(self, place):
        """Enemies will spout a random death line when they are eliminated. This is a guarenteed event before they are removed from the place. Uses the remove method in the Entity parent class."""
        print(random.choice(self.death_lines))
        print("{0} eliminated!".format(self.name))
        Entity.remove(self, place)
        if random.choice([1, 2]) == 1:
            place.loot.append(eval(stim))
        if self.possible_loot and self.can_drop:
            place.loot.append(eval(random.choice(self.possible_loot)))

    def __str__(self):
        return "{0}, Health: {1}, Armor: {2}, Damage: {3}, Range: {4} units, Move Speed: {5} units per turn".format(self.name, self.health, self.armor, self.damage, self.range, self.move_speed)

class Prison_Guard(Enemy):
    """Prison Guards are the first enemy the player encounters in the game, being the weakest prison guards. Poorly trained and poorly armored, these guards serve as the prison's cheap way to enforce peace. They are armed with a stun baton, which acts as a normal melee weapon and deals low 
    damage with each hit. They also have a low movement, low health, and low armor."""
    name = "Prison Guard"
    battle_lines = ["'Come on prisoner, I'll make you regret this!'", "'Don't let the prisoner escape!'", "'I can't wait to kill you!'", "'It was a mistake leaving you alive!'", "'We should have killed you when we first found you!'"]
    death_lines = ["'How could I die to filth?'", "'Comrades...kill this...bitch!'", "'You will never get past the rest!'", "'AAAHHHHH!'"]
    possible_loot = [stun_baton, guard_vest, gum]
    can_drop = False

    def __init__(self, health=40, armor=30, damage=20, range=1, move_speed=1):
        Enemy.__init__(self, health, armor, damage, range, move_speed)

class Dog(Enemy):
    """Loyal prison guard dogs, they fight alongside their human masters. They have lower health and no armor but move faster than prison guards. Deal low damage and serve as a means to quickly lower the player's health to assist the guards. 
    >>> x = Dog(75, 0, 10, 1, 2)
    >>> print(x)
    Dog, Health: 75, Armor: 0, Damage: 10, Range: 1 units, Move Speed: 2 units per turn
    >>> x
    Dog
    """
    name = "Dog"
    battle_lines = ["'GRRRRRRRR!'"]
    death_lines = ["'Whimpers'"]

    def __init__(self, health=20, armor=0, damage=15, range=1, move_speed=2):
        Enemy.__init__(self, health, armor, damage, range, move_speed)

class War_Dog(Dog):
    """War dogs are dogs bred for killing, augmented by technology and genetic modification. They have been given more armor and health their their ordinary counterparts and move slightly faster. Aside from that, they have no other special moves and are functionally similar to normal dogs."""
    name = "War Dog"
    possible_loot =  [wd_armor]

    def __init__(self, health=50, armor=50, damage=25, range=1, move_speed=3):
        Dog.__init__(self, health, armor, damage, range, move_speed)

class Federation_Rifleman(Enemy):
    """Federation rifleman are the main bulk of the Federation's military, given moderate armor, kept in good health, and equipped with a laser rifle and grenades. They have a special grenade throw that allows them to lob a medium damage explosive at the player. They have a limited amount of grenades and there is a cooldown period in between throws. Their normal attack is a laser rifle, which fires non armor piercing ammunition and deals moderate damage. Their rifles also have medium range, requiring them to advance towards the player before firing."""
    name = "Rifleman"
    battle_lines = ["'Federation's best about to kick your ass!'", "'Ok, the fun's over!'", "'You'll wish you were never born!'", "'Moving in for the kill!'", "'OOO RAA!'"]
    death_lines = ["'I may be gone but so will you very soon!", "'Help! I need assi...'", "'Fuck, they got me!'", "'Finish them off comrades!'", "'Nooooo...how could...this...happen?'"]
    possible_loot = [rifle, grenade, ballistic_vest]
    time_check = True

    def __init__(self, health=70, armor=80, damage=30, range=4, move_speed=1):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.grenades = 2
        self.grenade_damage = 35
        self.grenade_range = 5
        self.can_throw = True
        self.cooldown = 2
        self.grenade_counter = 0

    def throw_grenade(self, place):
        """The soldier throws a grenade at the player if the player is within grenade range, dealing damage to the player. Then, the can throw attribute is set to False and the counter is recalculated."""
        print("Federation {0} throws a plasma grenade at you!".format(self.name))
        print()
        place.player.injure(place, self.grenade_damage, Explosive.armor_piercing)
        self.grenades -= 1
        self.can_throw, self.grenade_counter = False, place.turn_count + self.cooldown

    def take_turn(self, place):
        """The soldier will throw a grenade at the player if they are within range, has grenades, and is allowed to throw a grenade. Otherwise, the soldier will follow the standard take turn method, moving towards the player until they are in range and then attacking."""
        if self.position - place.player.position <= self.grenade_range and self.can_throw and self.grenades:
            print()
            self.throw_grenade(place)
        else:
            Enemy.take_turn(self, place)

    def check(self, place):
        """Checks if the grenade cooldown is over and if so, sets the can throw attribute back to True."""
        if self.grenade_counter == place.turn_count:
            self.can_throw = True

class Federation_Marksman(Enemy):
    """Federation marksmen are long range units that are fragile but armed with a sniper rifle that fires armor piercing laser rounds. They do their best to stay away from the player as much as they can, sitting at the outer range of their rifles and dealing damage from a distance. As a precision shooter, the marksman can only fire every other turn in order to give time for proper aim. If the player gets too close, the marksman retreats unless they are at the end of the place."""
    name = "Marksman"
    battle_lines = ["'Marksman in position'", "'Ready to hunt'", "'This will be just like at the 2041 Riots'", "'Enemy in my sites'", "'In position, engaging targets'", "'Targets spotted, engaging from a distance'"]
    death_lines = ["'Marksman down, I repeat, marksman down!'", "'All units, you lost your marksman!'", "'Shit, I'm out of the fight!'", "'Good luck guys, I'm not going to make it!'"]
    possible_loot = [sniper_rifle, marksman_vest, gum]
    armor_piercing = True
    time_check = True

    def __init__(self, health=50, armor=50, damage=30, range=5, move_speed=3):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.accuracy = 60
        self.can_attack = True
        self.attack_counter = 0
        self.gap = 2

    def attack(self, place):
        """Attacks the player like normal but then sets the can attack attribute to False and calculates the attack counter."""
        if random.choices([0, 1], weights=(1 - self.accuracy, self.accuracy))[0] == 1:
            Enemy.attack(self, place)
            self.can_attack, self.attack_counter = False, place.turn_count + 1
        else:
            print("Federation {0} missed!".format(self.name))

    def take_turn(self, place):
        """First priority is to maintain the gap so if the player is too close and the marksman can retreat, the marksman retreats. If the player is not in range, the marksman advances until they are in range. If the marksman is in range and can attack, they attack. Otherwise, the marksman 
        skips their turn. At the start of their turn, they get a range boost if they have allies in front of them."""
        print()
        dist = self.position - place.player.position
        if dist <= self.gap and self.position < place.size:
            self.move(place, True)
        elif dist > self.range:
            self.move(place)
        elif dist <= self.range and self.can_attack:
            self.attack(place)
        else:
            print("Federation {0} prepares their aim and skips a turn".format(self.name))

    def check(self, place):
        if self.attack_counter == place.turn_count:
            self.can_attack = True

class Federation_Enforcer(Enemy):
    """Federation enforcers are close quarters battle specialists, equipped with higher tier armor and powerful shotguns. Enforcers deal high damage at close range but have a very short range. They follow the default take turn and attack methods, with the only thing special about them 
    being their stats. They can drop adrenaline as well but don't use in battle because they don't view prisoners worthy enough to use it on."""
    name = "Enforcer"
    battle_lines = ["'Enforcer, closing the distance!'", "'I'll fill you full of laser beams!'", "'This shotty will melt your insides!'", "'I'm going to love seeing you squirm!'", "'Die! That's all your kind is good for!'", "'Moving in for the kill!'"]
    death_lines = ["'No way...they got me!'", "'AAAA AAAAA HELP ME!'", "'NOOOO, IT'S NOT OVER!'", "'DEATH WAS ON MY SIDE!'", "'HELP ME DAMN IT!'"]
    possible_loot = [shotgun, heavy_armor, adrenaline]

    def __init__(self, health=100, armor=100, damage=40, range=2, move_speed=1):
        Enemy.__init__(self, health, armor, damage, range, move_speed)

class Federation_Shielder(Enemy):
    """Federation shielders are the government's main riot control units, deployed to any situations that require crowds to be dispersed or eliminated, there is no difference to the Federation. While not having more health than a typical Federation rifleman, shielders are dressed in heavy duty 
    riot control armor. They also have a large riot shield as their main staple. Because of this, they have a special injure method that reduces incoming damage by a certain percentage. Furthermore, if two or more shielders stand together on the same place, this damage reduction is increased. 
    Shielders carry a laser pistol and fire it at the player when in range. They will move towards the player at the start of battle and hold their ground till death."""
    name = "Riot Shielder"
    battle_lines = ["'Shield incoming, I have your backs!'", "'Shielder coming through!'", "'Stay behind me boys, I'll cover you!'", "'I'll draw their attention, you kill them!'", "'Stick together y'all, we can do this!'", "'Stay strong, use me for cover!'"]
    death_lines = ["'I'm sorry guys...they were too much...'", "'Impressive...they got...me...'", "'Don't worry about me guys, it's too late'", "'Honor fight with you all, go kick their ass'", "'You can win...without...me...'"]
    possible_loot = [pistol, riot_shield, riot_armor]

    def __init__(self, health=100, armor=150, damage=20, range=1, move_speed=1):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.damage_reduction = 0.20
        self.team_damage_reduction = 0.30

    def injure(self, place, damage, AP):
        """Unique injure method that first reduces the incoming damage by the correct damage reduction percentage and then uses the default Entity injure method."""
        if any([x.position == self.position for x in place.enemies if isinstance(x, Federation_Shielder) and x is not self]):
            print("Damage reduced by {0}%".format(round(self.team_damage_reduction * 100)))
            damage = damage * (1 - self.team_damage_reduction)
        else:
            print("Damage reduced by {0}%".format(round(self.damage_reduction * 100)))
            damage = damage * (1 - self.damage_reduction)
        print()
        Entity.injure(self, place, round(damage), AP)

class Volk(Federation_Rifleman):
    """Code wise, Volk behaves like a rifleman, able to throw grenades at the player or attack them with his flamethrower. Since he has a flamethrower, his stats should be adjusted to be different from a base rifleman. Volk also has the ability to heal with a limited amount of experimental healing syringes. There is a cooldown in between heals. After a certain amount of attacks, Volk has to reload his flamethrower, taking him out of the fight for a turn. Upon death, he drops all of the possible loot he has, meaning he needs a modified remove method."""
    name = "Volk"
    battle_lines = ["'It's a shame you have to die'", "'You could have joined me, the Federation'", "'You can't hide from me or my flame'", "'This is for all my fallen men!'", "'I will enjoy burning you alive!'"]
    death_lines = ["'I guess it is all over...You really are...a force...to be...reckoned...with...'"]
    possible_loot = [flamethrower, riot_armor, nano_stim, nano_stim]
    
    def __init__(self, health=200, armor=250, damage=40, range=5, move_speed=2):
        Federation_Rifleman.__init__(self, health, armor, damage, range, move_speed)
        self.can_heal = True
        self.syringes = 5
        self.heal_threshold = 50
        self.heal_amount = 70
        self.heal_cooldown = 4
        self.heal_counter = 0
        self.mag_size = 5
        self.ammo = self.mag_size

    def reloading(self, place):
        """Reloads the flamethrower, setting the ammo back to full capacity and setting the reload attribute to False."""
        print("'Just wait till I finish reloading!'")
        self.ammo = self.machine
    
    def attack(self, place):
        """Attacks like normal but then deducts 1 from the ammo count."""
        print("'Burn!!!'")
        print()
        Federation_Rifleman.attack(self, place)
        self.ammo -= 1
        if not self.ammo:
            print()
            print("'You're lucky I'm out of fuel buddy!'")

    def healing(self, place):
        """Heals Volk when his health is below a certain threshold but the heal amount. Then sets the can heal attribute to False and recalculates the heal counter for the cooldown of the ability."""
        self.health += self.heal_amount
        self.syringes -= 1
        self.can_heal, self.heal_counter = False, place.turn_count + self.heal_cooldown
        print("'Ah, now that's better! I'm almost invincible!'")

    def take_turn(self, place):
        """If the flamethrower is out of ammo, reload the weapon. Otherwise, if Volk's health is below the threshold, have him heal. Otherwise, use the standard Rifleman take turn method."""
        if not self.ammo:
            print()
            self.reloading(place)
        elif self.health <= self.heal_threshold and self.syringes:
            print()
            self.healing(place)
        else:
            Federation_Rifleman.take_turn(self, place)

    def remove(self, place):
        print(random.choice(self.death_lines))
        print("{0} eliminated!".format(self.name))
        Entity.remove(self, place)
        for loot in self.possible_loot:
            place.loot.append(eval(loot))
    
    def check(self, place):
        if place.turn_count == self.heal_counter:
            self.can_heal = True
        Federation_Rifleman.check(self, place)

class Engineer(Enemy):
    """Engineers are enemies that the player encounters in the Machine Labs, which are humans who were in charge of designing and manufacturing the prototype technology there. They are armed with a wrench and have low health and low armor. They also fight with a wrench, a low damage and low range melee weapon. Their power comes from the Tune Up move, with gives machine type allies damage and movement bonuses, with a short cooldown. Finally, engineers have a repair ability, where they pick the lowest health machine ally and increase their health by a certain amount. Repairing has a cooldown."""
    name = "Engineer"
    battle_lines = ["'Federation engineering is revolutionary!'", "'Fear the mind of the Federation!'", "'I may be weak but my inventions are strong!'", "'With my technology, failure is impossible!'", "'Federation's greatest mind ready to kill you!'"]
    death_lines = ["'Impossible...success was...inevitable!'", "'Were my calculations...wrong?'", "'Man dies, machines live...forever!'", "'My machines will avenge me!'"]
    possible_loot = [engineer_armor, wrench]
    time_check = True

    def __init__(self, health=50, armor=50, damage=10, range=1, move_speed=5):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.damage_boost = 1.2
        self.repair_threshold = 0.40
        self.repair_amount = 50
        self.repair_cooldown = 2
        self.can_repair = True
        self.repair_counter = 0
        self.move_boost = 1
        self.can_tune = True
        self.cooldown = 4
        self.tune_counter = 0
        self.gap = 3

    def tune_up(self, place):
        """The tune up move boosts all machine type allies by multiplying their damage by the damage multiplier and by increasing their move speed by the move boost. Then, the can tune attribute is set to False and the tune counter is set to the next turn when the move's cooldown is over. """
        print("{0} does a tune up on all machine type allies, granting them a {1}% damage boost and an additional {2} units of move speed for {3} turns!".format(self.name, round((self.damage_boost * 100) - 100), self.move_boost, self.cooldown))
        for enemy in place.enemies:
            if enemy.machine:
                enemy.damage, enemy.move_speed = round(enemy.damage * self.damage_boost), enemy.move_speed + self.move_boost
        self.can_tune, self.tune_counter = False, place.turn_count + self.cooldown

    def repair(self, place, target):
        """The engineer directly adds health to the target, which is a specific machine ally. This is only done when the machine is at a certain percentage of their base health and this move has no cooldown."""
        print("{0} repairs {1} for {2} health".format(self.name, target.name, self.repair_amount))
        target.health = min(target.health + self.repair_amount, target.default_health)
        self.can_repair, self.repair_counter = False, place.turn_count + self.repair_cooldown

    def take_turn(self, place):
        """The engineer's first priority is staying away from combat as much as possible, meaning that it will retreat if the player is within the gap and the engineer is not at the end of the place. If there are machine allies, the engineer will prioritize repairing any below a certain 
        health percentage, otherwise it tune up its machine allies if they are on the field. If the player is directly in front of the engineer, they will attempt to retreat if they can or else they will attempt to fight. If none of these conditions are met, then the engineer will skip a turn. 
        If there are no machine allies left, the engineer will advance towards the player and attempt to attack them."""
        dist, place_machines = self.position - place.player.position, [x for x in place.enemies if x.machine]
        low_hp = min(place_machines, key=lambda x: x.health / x.default_health)
        if place_machines:
            print()
            if dist <= self.gap and self.position < place.size:
                self.move(place, True)
            elif dist <= self.range:
                self.attack(place)
            elif (low_hp.health / low_hp.default_health) <= self.repair_threshold and self.can_repair:
                self.repair(place, min(place_machines, key=lambda x: x.health / x.default_health))
            elif self.can_tune:
                self.tune_up(place)
            else:
                print("{0} does nothing this turn".format(self.name))
        else:
            Enemy.take_turn(self, place)

    def check(self, place):
        """The check method just haves to check if the cooldown for the tune up move is over. If so, each machine type ally on the field has its damage divided by the damage boost and has its move speed lowered by the move boost. Ensure that the move speed never goes below 1. Also, 
        set the can tune attribute back to True."""
        if place.turn_count == self.tune_counter:
            for enemy in place.enemies:
                if enemy.machine:
                    enemy.damage, enemy.move_speed = round(enemy.damage / self.damage_boost), max(enemy.move_speed - self.move_boost, 1)
            self.can_tune = True
        if place.turn_count == self.repair_cooldown:
            self.can_repair = True

class Arty(Enemy):
    """The Arty is a powerful machine enemy found in the Machine Labs. It is a four legged machine with miniturized motar on its back, making it a strong ranged enemy. Due to the complex machinary behind this enemy's weapon, it can only fire every 2 turns to allow for reloading and aiming. Similar to an archer, it remains as far of the player as it can and retreats if the player gets too close. However, the Arty has limited movement speed due to the mortar's weight, meaning it has difficulty retreating. Also, while it does powerful damage, this enemy has low health for a machine type enemy."""
    name = "Arty"
    battle_lines = ["'Enemies spotted, preparing mortar'", "'Arty ready for battle'", "'Arty entering combat'", "'Mortar ready'", "'Bombardment commencing'"]
    death_lines = ["'Powering down'", "'Maximum damage sustained, powering down'", "'Arty offline'"]
    possible_loot = [salvaged_armor]
    machine = True
    time_check = True

    def __init__(self, health=70, armor=50, damage=25, range=5, move_speed=1):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.can_attack = True
        self.attack_counter = 0
        self.reload = 2
        self.gap = 2

    def attack(self, place):
        """Uses the default attack method but then calculates the attack counter and sets the can attack attribute to False."""
        Enemy.attack(self, place)
        self.can_attack, self.attack_counter = False, place.turn_count + self.reload

    def take_turn(self, place):
        """If the player is not in range, then the Arty will move towards the player until they are in range. Once in range, they will attack if they are able to or if not, will skip a turn. If the player is too close, the Arty attempts to retreat until it can not retreat anymore, 
        where it will attempt to fight the player at close range."""
        dist = self.position - place.player.position
        print()
        if dist <= self.gap and self.position < place.size:
            self.move(place, True)
        elif dist > self.range:
            self.move(place)
        elif self.can_attack:
            self.attack(place)
        else:
            print("'Reloading mortar'")

    def check(self, place):
        """Checks if the reloading process is finished and if so, sets the can attack attribute to True."""
        if place.turn_count == self.attack_counter:
            self.can_attack = True

class Ripper(Enemy):
    """The Ripper is a melee, humanoid looking machine enemy found in the Machine Labs that has a deadly chainsaw on each of its arms. It is heavily armored and has high health but low mobility. To partially resolve the issue, the engineers added an emergency thruster to it, giving it a quick 
    burst of speed and dash forwards. However, the Ripper is unable to move for a turn after this move is used to allow its movement mechanisms to cool down and function once again. Up close, this enemy does high damage but the motors for the arms overheat after an attack, preventing it from 
    attacking again for a turn. This serves to give the player an opportunity to get the upper hand against them."""
    name = "Ripper"
    battle_lines = ["'Rip and tear'", "'Ripper entering combat'", "'Chainsaws functional'", "'Proceeding to eliminate enemies of the Federation'", "'All systems ready for battle'"]
    death_lines = ["'Powering down'", "'Maximum damage sustained, powering down'", "'Ripper offline'", "'Safety protocols engaged, powering down'", "'Heavy damage, shutting down'"]
    possible_loot = [salvaged_armor]
    machine = True
    time_check = True

    def __init__(self, health=150, armor=200, damage=35, range=1, move_speed=1):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.can_move = True
        self.dash_speed = 3
        self.dash_counter = 0
        self.can_attack = True
        self.attack_counter = 0

    def dash(self, place):
        """Dashes the Ripper forward towards the player as far as the dash speed allows or until it reaches the player. Then, the can dash attribute is set to False and the dash counter is recalculated so that the Ripper cannot move for a turn."""
        steps = min(self.dash_speed, self.position - (place.player.position + 1))
        self.position, self.dash_counter = self.position - steps, place.turn_count + 1
        self.can_move = False
        print("{0} uses its thrusters to dash forward {1} units!".format(self.name, steps))

    def attack(self, place):
        """The Ripper uses the default attack method but after attacking, is unable to attack for a turn. Set the can attack to False and calculate the attack counter attribute."""
        Enemy.attack(self, place)
        self.can_attack, self.attack_counter = False, place.turn_count + 1

    def take_turn(self, place):
        """The Ripper will dash into combat if it is able to and the distance between it and the player is greater than its move speed. Otherwise, it will use its normal movement to get into range. If the player is not in range and it can't move, the Ripper will skip a turn. Once in range, 
        the ripper will attack if it is able to or if not, will display a message and skip a turn."""
        dist = self.position - (place.player.position + 1)
        print()
        if dist > self.range:
            if dist > self.move_speed and self.can_move:
                self.dash(place)
            elif dist <= self.move_speed and self.can_move:
                self.move(place)
            else:
                print("'Movement motors on cooldown. standby'")
        else:
            if self.can_attack:
                self.attack(place)
            else:
                print("'Chainsaw motors on cooldown, standby'")

    def check(self, place):
        """Checks if the dash and attack cooldowns are done and if so, sets their respective booleans to True."""
        if place.turn_count == self.attack_counter:
            self.can_attack = True
        if place.turn_count == self.dash_counter:
            self.can_move = True
            
class Charger(Enemy):
    """Chargers are machine enemies that are extremely simple. Designed as cheap and replaceable assets, these enemies move to their target as fast as they can and detonate themselves, effectively acting like suicide bombers. They have no concern for their own safety or that of their nearby 
    allies. Upon death, they explode and deal damage to anyone, including allies, on the same tile as them. They have next to no armor and medium health combined with a high move speed. Uses the default take turn method of the Enemy class, moving towards the player or attacking if they are 
    in range."""
    name = "Charger"
    battle_lines = ["'Enemy sighted, arming detonation device'", "'Explosives primed'", "'Charging opponent'", "'Attention all units, Charger entering combat'", "'Keep your distance, Charger armed'"]
    death_lines = ["'Detonating device'", "'No one can survive this explosion'", "'All allies, Charger explosion imminent'"]
    possible_loot = [salvaged_armor]
    machine = True

    def __init__(self, health=55, armor=20, damage=50, range=1, move_speed=3):
        Enemy.__init__(self, health, armor, damage, range, move_speed)

    def attack(self, place):
        """The Charger explodes, dealing non armor piercing damage to the player. All allies are also damaged by the same amount. Finally, the Charger's own injure method is called, eliminating it from the field."""
        print("{0} explodes, dealing {1} points of damage to everyone near it!".format(self.name, self.damage))
        print()
        place.player.injure(place, self.damage, False)
        allies = [x for x in place.enemies if x.position == self.position]
        for ally in allies:
            print()
            ally.injure(place, self.damage, False)
        print()
        self.injure(place, self.health, True)

class GI_Unit(Federation_Rifleman):
    """The final boss of the Machine Labs is a prototype GI Unit, a prototype robot meant to serve as a mechanized replacement for human soldiers. Aside from how it looks, the GI Unit behaves like any regular rifleman, throwing grenades and firing at the player with their powerful experimental railgun that can on be fired every other turn. The GI unit also carries a backpack with a payload of three missiles, which is able to randomly strike locations within a certain distance from the player. Finally, the GI Unit can call upon a pair of repair drone that are each able to give it 10 HP every turn if it is on the same spot as the GI Unit. These drones count as enemies and are very weak, easily destroyed by the player. The GI Unit carries four repair drones on it. The GI Unit has high health and medium armor."""
    name = "GI Unit"
    battle_lines = ["'Enemy spotted, moving in for the Federation'", "'GI Unit moving into battle'", "'I am the pinnacle of machinary'", "'You will be terminated'", "'Surrender for a quick end'", "'GI advancing'", "'GI engaging target'"]
    death_lines = ["'Damage above th...threshold...Must shut off systeeeems, syyyysteeems...G G G G I I I I Uniiiiit offliiiine'"]
    possible_loot = [riot_armor, nano_stim, nano_stim]

    def __init__(self, health=400, armor=150, damage=40, range=4, move_speed=2):
        Federation_Rifleman.__init__(self, health, armor, damage, range, move_speed)
        self.grenades = 5
        self.repairs = 2
        self.can_repair = True
        self.missile_radius = 2
        self.missiles = 3
        self.missile_damage = 30
        self.missile_cooldown = 3
        self.missile_counter = 0
        self.can_missile = True
        self.can_attack = True
        self.attack_counter = 0

    def call_repair(self, place):
        """When the GI Unit is low on health, it can call in two repair drone that, while weak, are each able to repair the unit by 10 HP per turn that the drone is on the same place as the GI Unit. This method only spawns a drone onto the place and the drone all the repairing logic is handled for in the drone's class."""

    def barrage(self, place):
        """Using its missile backpack, the GI Unit is able to randomly pick a certain number of spots within a certain radius of the player's spot and fire missiles at them. If the player is in any of the randomly selected spots, they take damage. Ensure to calculate the counter and turn the can missile attribute to False."""        

    def take_turn(self, place):
        """If the GI Unit is less than 50% health and can call a repair (can repair is True and it has repairs remaining), it will call in a repair. Else, if the Unit is able to perform a missile barrage, then it will do so. However, if the Unit is within the missile radius of the player, it will retreat first and perform the barrage once it is safely in range. If the player is too far away to be in range, the GI Unit will move in to close the gap and if the player is in range and it can attack, then it will attack. If it cannot do any of these things, the GI Unit will skip a turn."""

    def remove(self, place):
        print(random.choice(self.death_lines))
        print("{0} eliminated!".format(self.name))
        Entity.remove(self, place)
        for loot in self.possible_loot:
            place.loot.append(eval(loot))

    def check(self, place):
        """Performs the normal Rifleman check and then does a check for the missile barrage and the attack ability. The can repair attribute can only turns on True when both repair drones from the previous call were destroyed and is handled by the drone's remove method, not the GI Unit's."""

class Repair_Drone(Enemy):
    """The repair drones are supports to the GI Unit, which can call two drones at a time to repair it for 10 HP per turn each. The repair drone is extremely weak but has an extremely high move speed. It has a special move method that tries to keep it on the same spot as the GI Unit so it can repair it. Drones cannot attack nor do they retreat. They only care about repairing or moving to repair the GI Unit. Upon death, they can turn the GI Unit's can repair attribute back to True if both drones of the pair are destroyed."""
    name = "Repair Drone"
    battle_lines = ["'Repairing GI'", "'Must keep GI alive'", "'Keeping GI alive'", "'GI must survive'"]
    death_lines = ["'Repair unit down'"]

    def __init__(self, health=30, armor=0, damage=0, range=1, move_speed=10):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.repair_amount = 10
        self.tether = None
    
    def tether(self, place, target):
        """Assigns the repair drone to a specific GI Unit to take care of."""
        self.tether = target

    def move(self, place):
        """Repair drones have a special move method that serves to move them to the same spot as a GI Unit, whether forward or backwards."""
        dist = self.tether.position - self.position
        steps = min(abs(dist), self.move_speed)
        if dist >= 0:
            self.position += steps
        else:
            self.position -= steps
        print("{0} moved {1} steps {2}".format(self.name, steps, ("forward" if dist < 0 else "backwards")))

    def repair(self, place, target):
        """Increases the health of the target GI Unit by the repair amount."""
    
    def take_turn(self, place):
        """If there is no GI unit on the same place as the repair drone, move them to the same spot as a GI Unit. Otherwise, repair the GI Unit."""

    def remove(self, place):
        """Perform the default remove method but if there are no more repair drones on the field for the target GI Unit, set the tethered GI Unit's can repair attribute to True."""

### Event Classes ###

class Event:
    """Parent class for the random events in the game, which can be an encounter, a hazard, or a treasure. All Event instances have a play method that plays the event and contains all the information on what happens in the event. Therefore, each event instance has a unique play method.
    If an event has any randomized elements, the randomization occurs in the play method so that a single event instance can be used. All events are initialized without any parameters since all the important info is contained in the play method."""

    def __init__(self):
        self.name = "Event"
    
    def play(self, place):
        """The default play method takes in a place instance as a parameter, giving it access to everything it could need to function. Any randomization will occur here so a single instance can suffice for the entire game and no other new ones need to be created. The default play method
        also does nothing."""
        print("You come across an empty space. Take a breath for now and prepare yourself to continue onwards.")
    
    def __repr__(self):
        return self.name

class Lab_Files(Event):
    """Event that occurs in the labs, where the player can choose to read a file that contains information on the enemies they are fighting and weapons they are using."""
    files = [file_laser_rifle, file_laser_pistol, file_laser_shotgun, file_laser_sniper]

    def __init__(self):
        Event.__init__(self)

    def play(self, place):
        """The player is given the option to read a randomly chosen file. If they choose to, then the file's content is shown. Otherwise, they will put the file down and continue on their way."""
        print(files_intro)
        print()
        choice = fixed_input(input("Will you read the file? "))
        print()
        if "yes" in choice:
            print(random.choice(self.files))
            input()
        elif "no" in choice:
            print("You put the file down and continue through the labs.")
            input()
        else:
            print("Invalid input, try again") 
            print()
            return self.play(place) 

### Place Class ###

class Place:
    """Place class that is made up of a randomized set of tiles. Places can be visualized as a B x 1 grid, where B is an integer. Since the player begins battles ar position 0, the true length of a place is actually the size attribute + 1. Length is randomly determined by the class 
    attribute for possible sizes. Can randomly contain an enemy or event, depending on the type. A place can have up to a certain number of enemies at a time. The player starts at the first tile of the place and the enemies start on the opposite side. The enemies attribute is a list of enemies 
    while the event attribute is an single event instance. Different place and place types have a different list of possible enemies and events.
    """
    global_turns = 0
    current_time_items = [] #Contains current items with time limited effects used by the player. This is checked at the end of every turn to see if the item is still in use.
    possible_sizes = [x for x in range(4, 6)]
    possible_enemies = ["Entity()"] #Contains the possible types of enemies and events that the place can be populated with. The enemies list is filled with the name of the potential enemies, not classes
    possible_events = []
    min_enemies = 1
    max_enemies = 3

    def __init__(self, type_weight=[1, 1]):
        self.size = random.choice(self.possible_sizes) #Picks random size based off of the possible sizes
        self.type = random.choices(["Enemy", "Event"], weights=type_weight)[0] #Picks a random type based off of the type_weight
        self.enemies = []
        self.loot = []
        self.event = Event()
        self.player = None
        self.turn_count = 0
        self.fill()

    def add_enemy(self, enemy):
        """Helper function that adds an enemy instance to the enemies list. Takes in an enemy instance as an argument."""
        self.enemies.append(enemy)
        enemy.position = self.size

    def fill(self):
        """Fills the place with either enemies or an event, depending on the type of the room."""
        if self.type == "Enemy" and self.possible_enemies:
            number = random.randint(self.min_enemies, self.max_enemies)
            for x in range(number):
                self.add_enemy(eval(random.choice(self.possible_enemies)))
        elif self.type == "Event" and self.possible_events:
            self.event = random.choice(self.possible_events)
    
    def show_enemies(self):
        """Prints all the enemies at the current place. """
        print("*** Enemies ***")
        for enemy in self.enemies:
            print(enemy)

    def visualize(self):
        """Visualizes the place by showing it as a series of underscores for empty tiles. Tiles with an entity are replaced with their class symbol. Since multiple enemies can be on the same spot, that is also reflected on the visualization."""
        spots = ["________"] * (self.size + 1)
        spots[self.player.position] = self.player.name
        for enemy in self.enemies:
            if spots[enemy.position] == "________":
                spots[enemy.position] = enemy.name
            else:
                spots[enemy.position] += " / " + enemy.name
        separator = ", "
        print("[ " + separator.join(spots) + " ]")

    def show_loot(self):
        """Shows the place's loot by printing out, with each item on a different line"""
        print("*** Loot ***")
        i = 0
        for x in self.loot:
            print("[{0}] ".format(i) + str(x))
            i += 1

    def add_loot(self, player, item):
        """Allows for the player to pick up a piece of loot. Must check to see if the player can carry an item."""
        if player.weight_limit - player.current_weight < item.weight:
            print("Adding item would go over the weight limit")
            return
        else:
            player.inventory_add(item)
            self.loot.remove(item)

    def drop_loot(self, player, item): 
        """Allows for the player to drop a piece of loot, placing that item back into the place's loot list and adding the price of the item back to the player's wallet."""
        if item.name != "fists":
            self.loot.append(item)
        player.inventory_remove(item)
        
    def looting(self):
        """Function that allows the player to loot items after a battle. Player can either pick up an item, drop an item, or type "Done" to finish looting. Raises an Invalid Input message if the input is one word that is not 'Done' or if it's multiple words that are not a valid command. 
        The except case handles the first issue and the else case handles the second issue."""
        while True:
            self.show_loot()
            print()
            self.player.show_inventory()
            print()
            command = fixed_input(input("Type 'Take' or 'Drop' followed by the number of the item or type 'Done' to finish looting. "))
            action = command.split(" ", 1)[0]
            if action == "done":
                    break
            try:
                index = command.split(" ", 1)[1]
                if index.isnumeric():
                    index = int(index)
                    if action == "take" and index in range(len(self.loot)):
                        print()
                        self.add_loot(self.player, self.loot[index])
                        print()
                    elif action == "drop" and index in range(len(self.player.inventory)):
                        print()
                        self.drop_loot(self.player, self.player.inventory[index])
                        print()
                    else:
                        print()
                        print("Invalid input, ensure you have a valid numerical input")
                        print()
                else:
                    print()
                    print("Invalid input, ensure you have a valid numerical input")
                    print()
            except:
                print()
                print("Invalid input. If buying or refunding, make sure to type in the action followed by the number of the item")
                print()

    def __repr__(self):
        return "Place"

    def __str__(self):
        return "{0} Place, Size: {1}".format(self.type, self.size)

class Cell(Place):
    """Place class for the player's cell at the beginning of the game. The cell is very small and serves as the first place the player can fight in."""
    possible_sizes = [3]
    possible_enemies = ["Prison_Guard()"]
    possible_events = []
    max_enemies = 1

    def __init__(self, type_weight=[1, 0]):
        Place.__init__(self, type_weight)

class Lower_Prison(Place):
    """Place class for the Lower Prison. The Lower Prison is where prisoners from the lowest rungs of society are kept with little regard for their health or safety. Guards do the bare minimum to keep prisoners alive but can kill them at any time they wish. These places are very close quarters 
    as the player will be using mainly melee weapons anyway. Enemies for this area include guards with stun batons and their loyal dogs."""
    possible_sizes = [x for x in range(3, 6)]
    possible_enemies = ["Prison_Guard()", "Dog()"]
    max_enemies = 4

    def __init__(self, type_weight=[1, 0]):
        Place.__init__(self, type_weight)

class Main_Prison_Initial(Place):
    """Place class for Level C, the main section of the prison. Here, prisoners are mainly people from the middle to upper levels of society, enjoying more comfortable living standards than those in Level D. At the beginning, the player and their fellow prisoners (if they were set free) are 
    greeted by more stun baton guards and dogs. In the second half of the prison, reinforcements are called in and soldiers armed with pulse rifles, plasma grenades, and other heavy firearms are sent in. The main prison also has medium sized the entire time."""
    possible_sizes = [x for x in range(4, 7)]
    possible_enemies = ["Prison_Guard()", "Dog()"]
    max_enemies = 4

    def __init__(self, type_weight=[1, 0]):
        Place.__init__(self, type_weight)

class Main_Prison(Place):
    """Place class for Level C, the main section of the prison. Here, prisoners are mainly people from the middle to upper levels of society, enjoying more comfortable living standards than those in Level D. At the beginning, the player and their fellow prisoners (if they were set free) are 
    greeted by more stun baton guards and dogs. In the second half of the prison, reinforcements are called in and soldiers armed with laser rifles, plasma grenades, and other heavy firearms are sent in. The main prison is also medium sized the entire time."""
    possible_sizes = [x for x in range(6, 9)]
    possible_enemies = ["Federation_Rifleman()", "Federation_Marksman()", "Federation_Enforcer()", "Federation_Shielder()", "War_Dog()"]
    min_enemies = 2
    max_enemies = 3

    def __init__(self, type_weight=[1, 0]):
        Place.__init__(self, type_weight)

class Volk_Fight(Place):
    """The place class where the player fights Volk, a heavily armored commander equipped with a flamethrower. This place is large, reflecting how the player has almost the entirety of Level C at their disposal."""
    possible_sizes = [14]
    possible_enemies = ["Volk()"]
    max_enemies = 1

    def __init__(self, type_weight=[1, 0]):
        Place.__init__(self, type_weight)

class Machine_Labs(Place):
    """The Machine Labs are perhaps the largest section of the game, having the most enemy variety and the most items the player can acquire. Enemies here are both man and machine, with each type having their own unique moves that work together to give the player a tough time. The final boss of the area is an experimental machine will prove to be the player's toughest fight yet. Places are medium to medium-large sized but there can be many enemies at a time, creating challenging situations."""
    possible_sizes = [x for x in range(5, 10)]
    possible_enemies = ["Engineer()", "Ripper()", "Charger()", "Arty()"]
    possible_events = [Lab_Files()]
    min_enemies = 2
    max_enemies = 4

    def __init__(self, type_weight=[3, 2]):
        Place.__init__(self, type_weight)

### Game Manager ###

def fixed_input(s):
    """Takes an input string s and returns a new string that is reformatted to remove the spaces before and after s and make 
    everything lowercase.
    >>> x = fixed_input("   The cow jumped over the Moon   ")  
    >>> x 
    'the cow jumped over the moon'
    """
    return s.lower().strip()

def choices(lst, header):
    """Shows a list of choices the player can make at the time, each with a number for the player to type in if so they can select it. The player can then input a value and then the function will return their selection. lst is a list of strings while the header is the prompt the player is 
    being asked as a string."""
    print("*** " + header + " ***") 
    i = 0
    for x in lst:
        print("[{0}] ".format(i) + x)
        i += 1
    print()
    selection = fixed_input(input("Type in the number of the choice you will make. "))
    if not selection.isnumeric() or int(selection) > len(lst) - 1 or int(selection) < 0:
        print()
        print("Invalid input, ensure input is a valid number.")
        print()
        return choices(lst, header)
    return int(selection)

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
        choice = fixed_input(input("Type 'Inventory' to manage your inventory or 'Continue' to move forwards. "))
        if choice == "continue":
            print()
            print("You continue forwards")
            break
        elif choice == "inventory":
            print()
            player.sorting()
            print()
        else:
            print()
            print("Invalid input, try again")
            print()

def battle(place):
    """Facilitates the entire battle if a player is in an enemy place. Battles begin with the player at position 0 and the enemies at the opposite end. The player always makes the first turn, then all the enemies."""
    print(">>> Battle begin")
    def fight(): #Using this internal function to avoid writing a battle opening for every call of the function
        place.turn_count, Place.global_turns = place.turn_count + 1, Place.global_turns + 1
        print()
        print("TURN {0}".format(place.turn_count))
        print()
        print(">>> {0}'s Turn".format(place.player.name))
        print()
        place.player.take_turn(place)
        for enemy in place.enemies:
            time.sleep(1.5)
            print()
            print(">>> {0}'s Turn".format(enemy.name))
            print()
            print(random.choice(enemy.battle_lines))
            enemy.take_turn(place)
        for item in Place.current_time_items: #Checking to see if any time limited effects for items and enemies need to be removed before continuing to the next turn
            item.check(place)
        for enemy in place.enemies:
            if enemy.time_check:
                enemy.check(place)
        if place.enemies:
            time.sleep(1.5)
            return fight()
        print()
        print(">>> End of battle")
        input()
        if place.loot:
            place.looting()
            print()
    fight()

def game_over():
    """Function that prints a game over message when the player dies and quits the program"""
    print("You take one last look at your surroundings as Federation forces close in on your body. Your death proves that the prison is inescapable. You die, having never recieved freedom again.")
    input()
    quit()