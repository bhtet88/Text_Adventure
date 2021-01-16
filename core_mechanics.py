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
        place.player.backpack_remove(self)

    def __str__(self):
        return "{0}, Armor: {1} Weight: {2} lbs, Price: {3} coins".format(self.name, self.armor, self.weight, self.price)

class Shield(Equipment):
    """Shields are a piece of equipment that the player can choose to use during battle, reducing damage by a certain amount for a certain number of turns. It does this by directly lowering the enemy's damage as long as the effect lasts. Damage reduction is written as the percentage of damage
    remaining after the shield's effect in decimal form. A specific shield cannot be used multiple times in a row, which would create consecutive damage reductions."""

    combat_item = True

    def __init__(self, damage_multiplier, buff_length, weight, price, name="Shield"):
        Equipment.__init__(self, weight, price, name)
        self.damage_multiplier = damage_multiplier
        self.buff_length = buff_length
        self.buff_counter = 0
        self.used = False

    def action(self, place):
        """Multiplies the damage of all enemies on the current place by the damage multiplier, which should never be equal to or greater than 1. Sets the buff counter to the turn when the shield buff will wear off. Since the buff can last across battles, use the global turn count. Set the
        used attribute to True and keep it like that until the shield's buff is over. Make sure to add this item to the Place time items list only once. If the shield is already in use, show a message and let the player do something else."""
        if self.used:
            print("{0} is already in use, pick another item to use.".format(self.name))
            print()
            return place.player.take_turn(place)
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
        return "{0}, Damage Reduction: {1}%, Block Duration: {2} turns, Weight: {3} lbs, Price: {4} coins".format(self.name, round((1 - self.damage_multiplier) * 100), self.buff_length, self.weight, self.price)

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
    ranged = False
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
        if self.ranged:
            self.eff_range = int(max(self.range + self.range_bonus + place.player.range_bonus + place.range_bonus, 1)) #Range must be at least 1 and only ranged weapons get a range bonus

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

class AP_Weapon(Weapon):
    """Exact same as the Weapon class but armor piercing is turned on."""
    armor_piercing = True

class Polearm(Weapon):
    """Polearms are melee weapons that have a special sweep attack, allowing them to hit all enemies in directly in front of the player for reduced damage."""

    def __init__(self, damage, sweep_multiplier, range, weight, price, name="Polearm"):
        Weapon.__init__(self, damage, range, weight, price, name)
        self.sweep_multiplier = sweep_multiplier

    def sweep(self, place):
        """Damages all enemies directly in front of the player for reduced damage governed by the sweep multiplier."""
        for enemy in place.enemies:
            if enemy.position == place.player.position + 1:
                enemy.injure(place, int(self.eff_damage * self.sweep_multiplier), self.armor_piercing)

    def action(self, place):
        """Allow the player to choose between the normal attack or the sweep attack."""
        attack = fixed_input(input("What attack will you use? Type 'Normal' or 'Sweep' to attack or 'Back' to choose a different action. "))
        print()
        if attack == "back":
            return place.player.take_turn(place)
        elif attack == "normal":
            Weapon.action(self, place)
        elif attack == "sweep":
            self.sweep(place)
        else:
            print("Invalid input, try again")
            return self.action(place)

class Bow(Weapon):
    """Bows are long ranged weapons that are armor piercing and can hit enemies that are more than 1 unit away. Damage is weaker than melee weapons. The bow itself is light but the bundle of arrows makes them heavier than expected. Have a special volley attack that allows them to deal half
    damage to all enemies within range"""
    armor_piercing = True
    ranged = True
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
            print()
            if attack == "back":
                return place.player.take_turn(place)
            elif attack == "normal":
                Weapon.action(self, place)
            elif attack == "volley shot":
                self.volley_shot(place)
            else:
                print("Invalid input, try again")
                print()
                return self.action(place)
        else:
            Weapon.action(self, place)

class Rifle(Weapon):
    """Rifles are a powerful ranged weapon similar to bows but in exchange for their great power, each rifle has an accuracy rating that determines if the weapon hits the target or misses. Accuracy is a value between 0 and 100."""
    armor_piercing = True
    ranged = True
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
    ranged = True

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
                print()
                enemy.injure(place, int(dmg * self.spread_multiplier), self.armor_piercing)

class Flamethrower(Weapon):
    """Harnessing the power of fire, the flamethrower is a devestating weapon the player can get in the late game. It shoots an intense stream of fire, damaging all enemies in the spots between the player and the selected target, including all enemies in the same position as the target. 
    The player still has to pick a target so use the default action method. Enemies hit by the flamethrower also are lit on fire, causing them to have burn damage for a few turns. Burn damage cannot be changed by any bonuses. This weapon is not armor piercing, in order to remain balanced, 
    and has a limited range."""

    def __init__(self, damage, burn_damage, burn_length, range, weight, price, name="Flamethrower"):
        Weapon.__init__(self, damage, range, weight, price, name)
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
        return "{0}, Damage: {1}, Burn Damage: {2}, Burn Length: {3} turns, Range: {4} units, Weight: {5} lbs, Armor Piercing: {6}, Price: {7} coins".format(self.name, self.eff_damage, self.burn_damage, self.burn_length, self.eff_range, self.weight, self.armor_piercing, self.price)

class Explosive(Weapon):
    """Explosives are weapons that are thrown and do damage to all enemies on the same place as the targeted enemy and all enemies in places within the blast radius. Explosives have a limited amount of uses that cannot be changed by any bonuses nor can be refilled."""

    def __init__(self, damage, blast_radius, range, uses, weight, price, name="Explosive"):
        Weapon.__init__(self, damage, range, weight, price, name)
        self.blast_radius = blast_radius
        self.uses = uses

    def attack(self, place, position):
        """Attack method damages all enemies on the same place as the chosen location and also all enemies on positions within the blast radius. If the player is within the blast radius, injure them as well with the same damage. If the item runs out of uses, remove it from the backpack."""
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
            place.player.backpack_remove(self)

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
        elif not choice.isnumeric() or int(choice) not in range(place.player.position + 1, place.size + 1):
            print()
            print("Invalid input, answer must be a valid numeric input")
            print()
            return self.action(place)
        choice = int(choice)
        print()
        self.attack(place, choice - 1)

    def __str__(self):
        return "{0}, Damage: {1}, Blast Radius: {2} units, Range: {3} units, Uses: {4}, Weight: {5} lbs, Armor Piercing: {6}, Price: {7} coins".format(self.name, self.eff_damage, self.blast_radius, self.eff_range, self.uses, self.weight, self.armor_piercing, self.price)

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

    def effect(self, place, amount):
        """Method that performs the intended effects of a healing item. The default is to heal the player by a specified amount and then remove the item from their backpack if it's out of uses."""
        place.player.health += amount
        self.uses -= 1
        print("Healed for {0} HP, {1} uses remaining".format(amount, self.uses))
        self.recalculate(place)
        if not self.eff_uses:
            print("")
            place.player.backpack_remove(self)

    def action(self, place):
        """The default action method for healing items is to heal the player, with the heal amount determined by their heal amount attribute. Players cannot go over their maximum health. Remove the healing item from backpack if it is out of uses. If the player is already at max health, \
        then display a message and let the player try another action. Almost all healing items will use the same action method."""
        diff = place.player.eff_max_health - place.player.health
        if diff == 0:
            print("Health already maximum, can not use this")
            print("")
            return place.player.take_turn(place)
        elif diff <= self.eff_heal:
            self.effect(place, int(diff))
        else:
            self.effect(place, self.eff_heal)

    def __str__(self):
        return "{0}, Heal Amount: {1} HP, Uses Left: {2}, Weight: {3} lbs, Price: {4} coins".format(self.name, self.eff_heal, self.eff_uses, self.weight, self.price)

class Adrenaline(Healing_Tool):
    """Adrenaline shots heal the player but also give a temporary damage boost for a certain amount of turns."""

    def __init__(self, heal_amount, damage_bonus, bonus_length, uses, weight, price, name="Adrenaline"):
        Healing_Tool.__init__(self, heal_amount, uses, weight, price, name)
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
        return "{0}, Heal Amount: {1} HP, Uses Left: {2}, Damage Bonus: {3}, Bonus Length {4} turns, Weight: {5} lbs, Price: {6} coins".format(self.name, self.eff_heal, self.eff_uses, self.damage_bonus, self.bonus_length, self.weight, self.price)

### In-Game Items ###

armor_plate = Armor_Piece(25, 7, 50, "Armor Plate")
bandages = Healing_Tool(20, 1, 0.5, 75, "Bandages")
bow = Bow(30, 4, 12, 75, "Bow")
spear = Weapon(45, 1, 10, 100, "Spear") 
rifle = Rifle(70, 4, 60, 15, 200, "Rifle")
trench_gun = Shotgun(60, 3, 0.4, 0.2, 10, 250, "Trench Gun")
adrenaline = Adrenaline(20, 0.25, 1, 1, 0.5, 10, "Adrenaline")
adrenaline_2 = Adrenaline(20, 0.25, 4, 1, 0.5, 10, "Adrenaline")
polearm = Polearm(55, 0.4, 1, 10, 175, "Polearm")
dynamite = Explosive(35, 1, 3, 1, 4, 100, "Dynamite")
flamethrower = Flamethrower(200, 10, 2, 6, 15, 500, "Flamethrower")
shield = Shield(0.8, 1, 7, 90, "Shield")

heavy_spear = Weapon(65, 1, 15, 150, "Heavy Spear")
longbow = Bow(45, 6, 18, 250, "Longbow")
padded_jacket = Armor_Piece(45, 10.5, 200, "Padded Jacket")
healing_syringe = Healing_Tool(40, 4, 1, 200, "Healing Syringe")

store_list = [spear, bandages, bow, rifle, armor_plate, dynamite, polearm, trench_gun, shield, flamethrower]

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
    Has a backpack with a certain weight capacity
    >>> x = Player("Dave")
    >>> x.backpack
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
    uses_bonus = 0

    def __init__(self, name, health=100, armor=0, move_speed=1):
        Entity.__init__(self, health, armor)
        self.name = name
        self.move_speed = move_speed
        self.eff_move = move_speed 
        self.backpack = []
        self.current_weight = 0
        self.weight_limit = 50
        self.max_health = 100
        self.eff_max_health = self.max_health
        self.wallet = 1000
        self.place = None
    
    def recalculate(self, place):
        """The player recalculate method recalculates their move speed stat and all the items in their inventory."""
        if isinstance(place, Cliff_Place):
            self.eff_move = 1
        else:
            self.eff_move = int(max(self.move_speed + self.move_bonus + place.move_bonus, 1)) #Player will always move at least one unit
        self.eff_max_health = int(max(50, self.max_health + place.max_health_bonus)) #Player max health will always be at least 50 points
        if self.health > self.eff_max_health:
            self.health = self.eff_max_health
        for item in self.backpack:
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
            self.backpack.append(item)
            self.current_weight = sum([x.weight for x in self.backpack])
            print("Added {0} to backpack".format(item.name))
        else:
            print("Weight limit exceeded. Remove items to add this")

    def backpack_remove(self, item):
        """Allows for the removal of an item from the player's backpack.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> player = Player("Dan")
        >>> player.backpack_add(spear)
        Added Spear to backpack
        >>> player.backpack
        [Spear]
        >>> player.backpack_remove(spear)
        Spear removed from backpack
        >>> player.backpack 
        []
        """
        permanent = ["knife", "rope"]
        if item.name.lower() in permanent:
            print("Cannot remove this item from your backpack")
        elif item in self.backpack:
            self.backpack.remove(item)
            self.current_weight = sum([x.weight for x in self.backpack])
            print("{0} removed from backpack".format(item.name))
        else:
           print("Equipment not in backpack")

    def show_backpack(self):
        """Displays all the items in the player's backpack, with one item on each line."""
        self.recalculate(self.place)
        print("*** Backpack (Weight: {0} / {1}) ***".format(self.current_weight, self.weight_limit))
        i = 0
        for x in self.backpack:
            print("[{0}] ".format(i) + str(x))
            i += 1

    def show_weapons(self):
        """Displays all the weapons that the player is carrying."""
        self.recalculate(self.place)
        print("*** Weapons ***")
        weapons, i = [x for x in self.backpack if isinstance(x, Weapon)], 0
        for item in sorted(weapons, key=lambda x: x.range, reverse=True): 
            print("[{0}] ".format(i) + str(item))
            i += 1

    def use_weapon(self):
        """Allows the player to select a weapon from their inventory and return the weapon object for them to use. Returns None if the weapon isn't in the backpack"""
        self.show_weapons()
        print("")
        index = fixed_input(input("What weapon will you use? Type the name of the number of it or 'None' to select nothing and perform a different action. ")) #There will be no weapon with a name of 'None'
        if index == 'none':
            return None
        elif not index.isnumeric():
            print("")
            print("Not a valid numerical input")
            return None
        index, weapons = int(index), sorted([x for x in self.backpack if isinstance(x, Weapon)], key=lambda x: x.range, reverse=True)
        if index in range(len(weapons)):
            return weapons[index]
        print("")
        print("Weapon not in backpack")

    def use_backpack(self):
        """Allows the player to access their backpack and select an item to use. This method returns the item object so the game can see what item the player wants to use. If the player closes the backpack, return None. If the player gives an invalid input,
        raise an error and also return None. If the player removes an item, remove the item from the backpack and return None."""
        self.show_backpack()
        print("")
        choice = fixed_input(input("What would you like to do? Type 'Use' or 'Remove' followed by the number of the item or 'Close' to go back. "))
        if choice == "close":
            return None
        try:
            action, index = choice.split(" ", 1)[0], choice.split(" ", 1)[1]
        except:
            print("")
            print("Invalid input, try again")
            return None
        if not index.isnumeric():
            print("")
            print("Invalid input, ensure you are typing in a valid number.")
            return None
        index = int(index)
        if action == "use":
            if index in range(len(self.backpack)):
                return self.backpack[index]
            print("")
            print("Equipment not in backpack")
            return None
        elif action == "remove":
            if index in range(len(self.backpack)):
                print("")
                return self.backpack_remove(self.backpack[index])
            print("")
            print("Equipment not in backpack")
            return None
        else:
            print("")
            print("Invalid command")

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
    death_lines = ["'Whimpers'"]

    def __init__(self, health=50, armor=0, damage=15, range=1, move_speed=2):
        Enemy.__init__(self, health, armor, damage, range, move_speed)

class Feral_Monkey(Enemy):
    """Feral monkeys are rabid beasts that the result of failed experiments with Roman sorcery. Despite losing their minds and being unable to think for themselves for anything other than survival, they fight alongside the Roman defenses. They have the ability to hurl fecal matter at the
    player if the player is 2 units away. This attack can damage the player but only deals 40% of the base attack."""

    name = "Feral Monkey"
    battle_lines = ["'OOOO OOOO AAHH AAHH'"]
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
    death_lines = ["'SSSS...SSSS...SS...S'"]
    time_check = True

    def __init__(self, health=400, armor=0, damage=35, range=1, move_speed=4):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.crit_health= 40
        self.gap = 3
        self.rattle_buff = 10
        self.rattle_length = 2
        self.rattle_counter = 1
        self.corrosion = 5
        self.lunge_range = 4
        self.lunge_muliplier = 0.70

    def lunge(self, place):
        """The lunge move allows the snake to lunge forwards at the player, performing a long range attack with range determined by the lunge range attribute. This attack applies no corrosive damage but only does a portion of the normal damage, determined by the lunge multiplier attribute."""
        print("{0} aggressively lunges at you!".format(self.name))
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
        print("{0} attacks you with its large fangs!".format(self.name))
        print()
        Enemy.attack(self, place)
        print()
        print("{0} does an additional {1} points of corrosive damage directly to your health!".format(self.name, self.corrosion))
        print()
        place.player.injure(place, self.corrosion, True)

    def take_turn(self, place):
        """The snake's first priority is performing its rattle move. While it is unable to rattle, it will analyze if it can make it directly in front of the player with its move speed. If it can, it will move in front of the player if it can. If it cannot but the player is within lunge
        range, the snake will perform a lunge. If the snake is in front of the player, it will rattle if it can or normally attack the player. When its health reaches a certain level determined by the crit health attribute, it will try to stay away from the player and perform lunges.
        Priorities are 1) Rattle 2) Move 3) Attack 4) Lunge."""
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

    def check(self, place):
        """Checks the global turn count to see when to take off the rattle damage buff."""
        if place.turn_count == self.rattle_counter:
            self.damage -= self.rattle_buff

class Harpy(Enemy):
    """Harpies are warrior bird-like creatures that swoop in quickly to attack and then move back to the safety of the skies. They have a unique attack where they can attack the player if they are in range and then end their attack further away from the player. They also have armor to add 
    additional protection. However, they are intrinsically frail and have low health. Harpies can also screech to give a damage bonus to all allies and themselves in exchange for lowering their range."""

    name = "Harpy"
    battle_lines = ["'SCREEECH!'", "'CAAAAA CAAAAAW!'", "'CAW CAW CAW!'"]
    death_lines = ["'AAAAAAAA'"]
    time_check = True

    def __init__(self, health=50, armor=60, damage=15, range=2, move_speed=2):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.default_range = range
        self.retreat = 2
        self.can_screech = True
        self.screech_damage = 1.50
        self.screech_length = 3
        self.screech_counter = 0
        self.range_debuff = 1 #Debuff is a positive number

    def screech(self, place):
        """Screeches, causing all allies and itself to gain damage governed by the screech damage attribute, which is a multiplier for their damage. Non Harpy Archer instances have their ranges also lowered by the range debuff attribute. Sets the can screech attribute to False to prevent 
        the same Harpy from screeching many times. The screech counter should then be calculated using the place turn count as these Harpy instances only show up in the specific battle."""
        print(random.choice(self.battle_lines))
        print()
        print("{0} screeches, increasing the damage of all allies and itself by {1}% but lowering their range by {2} units!".format(self.name, round(self.screech_damage * 100 - 100), self.range_debuff))
        for enemy in place.enemies:
            enemy.damage = round(enemy.damage * self.screech_damage) #Range will always be at least 1
            if isinstance(enemy, Harpy):
                enemy.range = max(enemy.range - self.range_debuff, 1)
        self.screech_counter = place.turn_count + self.screech_length
        self.can_screech = False

    def attack(self, place):
        """The attack method for Harpies injures the player and then moves the Harpy back by the amount determined by the retreat attribute. This reflects the enemy swooping in and then retreating."""
        i = place.size - self.position
        print("{0} swoops in for an attack and then retreats {1} steps back!".format(self.name, min(i, self.retreat)))
        print()
        place.player.injure(place, self.damage, self.armor_piercing)
        if i <= self.retreat:
            self.position = place.size
        else:
            self.position += self.retreat

    def take_turn(self, place):
        """Harpies screech if no other ally has screeched, otherwise they will move towards the player if not in range. Once in range, they attack, causing them to retreat and have to move back towards the player."""
        print()
        dist = self.position - place.player.position
        if sum([(1 if x.can_screech == False else 0) for x in place.enemies if isinstance(x, Harpy)]) < 2 and self.can_screech:
            self.screech(place)
        elif dist > self.range:
            self.move(place)
        elif dist <= self.range:
            self.attack(place)

    def check(self, place):
        """If the screech effect is over, divide the enemy damage by the screech damage multiplier and increase their range. Range cannot become higher than their original range, stored in the default range attribute. Set the can screech attribute back to True."""
        if place.turn_count == self.screech_counter:
            for enemy in place.enemies:
                enemy.damage = round(enemy.damage / self.screech_damage)
                if isinstance(enemy, Harpy):
                    enemy.range = min(enemy.range + self.range_debuff, enemy.default_range)
            self.can_screech = True

class Harpy_Archer(Enemy):
    """Harpy archers have no screech ability but attack from a distance with their bows. They have a high move speed and range so they can attack the player from range and in safety. They will try to maintain a gap distance if they can and attack while the gap is maintained. It has a special 
    move method that allows it to advance until the player is within range instead of merely the full move speed."""
    name = "Harpy Archer"
    battle_lines = Harpy.battle_lines
    death_lines = Harpy.death_lines
    armor_piercing = True

    def __init__(self, health=50, armor=30, damage=10, range=4, move_speed=4):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.gap = 2

    def take_turn(self, place):
        """If the player is within range and the gap is maintained, then the Harpy archer attacks. If the player is not in range, then the Harpy archer moves until within range. If the desired gap between the player and the archer is not maintained, the archer moves back as much as it can to 
        maintain a safe distance, assuming it is not already at the end of the place."""
        print()
        dist = self.position - place.player.position
        if dist <= self.gap and self.position < place.size:
            self.move(place, True)
        elif dist <= self.range:
            self.attack(place)
        elif dist > self.range:
            self.move(place)

class Alpha_Harpy(Harpy):
    """The Alpha Harpy is a Harpy that also has a wing beat move that uses its powerful wings to push the player backwards a certain amount of spaces if the player is too close to the enemy. This move has a cooldown period as well. On top of this, the Alpha still retains all the moves of a 
    regular Harpy except it has more move speed and range."""
    name = "Alpha Harpy"

    def __init__(self, health=200, armor=250, damage=25, range=3, move_speed=6):
        Harpy.__init__(self, health, armor, damage, range, move_speed)
        self.can_beat = False
        self.beat_counter = 0
        self.cooldown = 3
        self.knockback = 1
        self.gap = 1

    def wing_beat(self, place):
        """The Alpha beats her wings furiously, moving the player back a certain number of steps governed by the knockback attribute. Display a message for this move and then push the player back. Ensure to recalculate the counter for this move and also set the can beat attribute to False."""
        print("{0} beats its wings furiously, knocking you backwards {1} steps!".format(self.name, min(self.knockback, place.player.position)))
        place.player.position = max(place.player.position - self.knockback, 0)
        self.can_beat, self.beat_counter = False, place.turn_count + self.cooldown

    def take_turn(self, place):
        """The Alpha will use her wing beat if the player is within a certain distance from her, determined by the gap attribute, and if the player is not at the end of the place. Otherwise, she will use the regular Harpy take turn method."""
        if self.can_beat and self.position - place.player.position <= self.gap and place.player.position:
            print()
            self.wing_beat(place)
        else:
            Harpy.take_turn(self, place)

    def check(self, place):
        """The Alpha's check method checks if the wing beat cooldown is over and if so, sets the can beat attribute to True. It also uses the Harpy check method for its other time limited effects."""
        if place.turn_count == self.beat_counter:
            self.can_beat = True
        Harpy.check(self, place)

class City_Guard(Legionary):
    """The City Guard are essentially Legionaries with more armor, more health, and a range of 2 units due to their pole arms. Other than that, they function the exact same in combat as their Legion counterparts."""
    name = "City Guard"
    
    def __init__(self, health=150, armor=200, damage=30, range=2, move_speed=1):
        Legionary.__init__(self, health, armor, damage, range, move_speed)

class Armored_Dog(Immortal_Dog):
    """Armored Dogs operate the same as normal Immortal Dogs except that they have been granted additional armor, providing significant protection."""
    name = "Armored Dog"

    def __init__(self, health=50, armor=100, damage=15, range=1, move_speed=2):
        Immortal_Dog.__init__(self, health, armor, damage, range, move_speed)

class Roman_Archer(Enemy):
    """Roman archers are braver than expected for people with bows. Instead of running away from the player to keep peppering with their arrows, they will engage in melee combat if the player is in front of them, holding their ground until death. Their melee attacks deal more 
    damage than their bow's damage but they only have a range of 1 unit with them and unlike their bows, will not penetrate armor. They also have light armor and a medium move speed in exchange for low health. They move at the start of battle to get into range but afterwards will hold their 
    position until death."""
    name = "Roman Archer"
    battle_lines = ["'Target spotted, let's get him!'", "'Show him the might of Roman archery!'", "'If you're in range, it's too late!'"]
    death_lines = ["'AAAAAHHHHHH!'", "'Show...no...mercy...comrades!'", "'For the...Emperor!'"]
    armor_piercing = True

    def __init__(self, health=70, armor=50, damage=15, range=4, move_speed=3):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.melee_damage = 40
        self.melee_range = 1

    def melee(self, place):
        """The archer goes into melee combat once the player is directly in front of them, which injures the player by the damage from the melee damage attribute. This attack is also not armor piercing as a trade off for the higher damage."""
        place.player.injure(place, self.melee_damage, False)

    def take_turn(self, place):
        """If the player is not in range, the archer will move towards the player to close the gap and get in range. Afterwards, it will continue to attack the player with their normal bow attack, using the default attack method, until the player is within melee range. Once in melee range, 
        the archer will switch to using their melee attack. If the player moves out of melee range, the archer will return to using their bow. If the player moves out of bow range, the archer will move to get back into range."""
        if self.position - place.player.position <= self.melee_range:
            print()
            self.melee(place)
        else:
            Enemy.take_turn(self, place)

class Engineer(Enemy):
    """Engineers are enemies that the player encounters in the Machine Labs, which are humans who were in charge of designing and manufacturing the prototype technology there. They are armed with a wrench and have low health but high armor. They also fight with a wrench, a low damage and low 
    range melee weapon. Their power comes from the Tune Up move, with gives machine type allies damage and movement bonuses, with a short cooldown. Furthermore, any machine on the same spot as an engineer gains a health bonus and this bonus can stack with multiple engineers. Finally, 
    engineers have a repair ability, where they pick the lowest health machine ally and increase their health by a certain amount. Repairing has no cooldown and can be used repeatedly."""
    name = "Engineer"
    battle_lines = ["'Roman engineering is revolutionary!'", "'Fear the genius of Rome!'", "'I may be weak but my inventions are strong!'", "'With my technology, failure is impossible!'", "'Rome's greatest mind ready to kill you!'"]
    death_lines = ["'Impossible...success was...inevitable!'", "'Were my calculations...wrong?'", "'Man dies, machines live...forever!'", "'My inventions will avenge me!'"]

    def __init__(self, health=80, armor=200, damage=15, range=1, move_speed=5):
        Enemy.__init__(self, health, armor, damage, range, move_speed)
        self.damage_boost = 1.2
        self.repair_threshold = 0.30
        self.repair_amount = 50
        self.move_boost = 1
        self.can_tune = True
        self.cooldown = 2
        self.tune_counter = 0
        self.gap = 2

    def tune_up(self, place):
        """The tune up move boosts all machine type allies by multiplying their damage by the damage multiplier and by increasing their move speed by the move boost. Then, the can tune attribute is set to False and the tune counter is set to the next turn when the move's cooldown is over. """
        print("{0} does a tune up on all machine type allies, granting them a {1}% damage boost and an additional {2} units of move speed!".format(self.name, round((self.damage_boost * 100) - 100), self.move_boost))
        for enemy in place.enemies:
            if enemy.machine:
                enemy.damage, enemy.move_speed = enemy.damage * self.damage_boost, enemy.move_speed + self.move_boost
        self.can_tune, self.tune_counter = False, place.turn_count + self.cooldown

    def repair(self, place, target):
        """The engineer directly adds health to the target, which is a specific machine ally. This is only done when the machine is at a certain percentage of their base health and this move has no cooldown."""
        print("{0} repairs {1} for {2} health".format(self.name, target.name, self.repair_amount))
        target.health = min(target.health + self.repair_amount, target.default_health)

    def take_turn(self, place):
        """The engineer's first priority is staying away from combat as much as possible, meaning that it will retreat if the player is within the gap and the engineer is not at the end of the place. If there are machine allies, the engineer will prioritize repairing any below a certain 
        health percentage, otherwise it tune up its machine allies if they are on the field. If the player is directly in front of the engineer, they will attempt to retreat if they can or else they will attempt to fight. If none of these conditions are met, then the engineer will skip a turn. 
        If there are no machine allies left, the engineer will advance towards the player and attempt to attack them."""
        dist, place_machines = self.position - place.player.position, [x for x in place.enemies if x.machine]
        if place_machines:
            print()
            if dist <= self.gap and self.position < place.size:
                self.move(place, True)
            elif dist <= self.range:
                self.attack(place)
            elif min(place_machines, key=lambda x: x.health / x.default_health) <= self.repair_threshold:
                self.repair(place, min(place_machines, key=lambda x: x.health / x.default_health))
            elif self.can_tune:
                self.tune_up(place)
            else:
                print("{0} does nothing this turn.".format(self.name))
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

class Siege_Cannon(Enemy):
    """The Siege Cannon is a powerful machine enemy found in the Machine Labs. It is a four legged machine with a powerful siege cannon on its back, making it a strong ranged enemy. Similar to an archer, it remains as far of the player as it can and retreats if the player gets too close. 
    However, the cannon has limited movement speed due to the cannon's weight, meaning it has difficulty retreating. Also, while it does powerful damage, this enemy has low health for a machine type enemy."""
    name = "Siege Cannon"
    battle_lines = []
    death_lines = []
    machine = True

class Ripper_Bot(Enemy):
    """The Ripper Bot is a melee, humanoid looking machine enemy found in the Machine Labs that has a deadly sword on each of its arms. It is heavily armored and has high health but low mobility. To partially resolve the issue, the Romans added an emergency thruster to it, giving it a quick 
    burst of speed and dash forwards. However, the Ripper is unable to move for a turn after this move is used to allow its movement mechanisms to cool down and function once again. Up close, this enemy does high damage but the motors for the arms overheat after an attack, preventing it from 
    attacking again for a turn. This serves to give the player an opportunity to get the upper hand against them."""

class Charger(Enemy):
    """Chargers are machine enemies that are extremely simple. Designed as cheap and replaceable assets, these enemies move to their target as fast as they can and detonate themselves, effectively acting like suicide bombers. They have no concern for their own safety or that of their nearby 
    allies. Upon death, they explode and deal damage to anyone, including allies, on the same tile as them. They have next to no armor and medium health combined with a high move speed."""

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
                merchant.buying(place.player)
                break
            elif "no" in choice or "continue" in choice:
                print("For your own reasons, you decide to keep going and not stop here.")
                break
            else:
                print("Invalid input, try again")
                print("")

class Encounter(Event):
    """The encounter events are purely dialogue based. A piece of dialogue plays and then the player goes on their way. These serve as a way to describe more about the world and their environment to the player"""
    encounters = [abandoned_village, water]

    def __init__(self):
        Event.__init__(self)
    
    def play(self, place):
        """Randomly show a text message from the encounters list. No player input or any changes to the game itself."""
        print(random.choice(self.encounters))

class Dodge(Event):
    """Dialogue only event where the player, if chance is in their favor, can evade an enemy encounter, essentially giving themselves a free pass through the tunnel. This event only occurs in the tunnel."""

    def __init__(self):
        Event.__init__(self)
    
    def play(self, place):
        print(dodge_text)
        Tunnel_Place.possible_events.append(Dodge())

class City_Navigation(Event):
    """Event that occurs as the player is trying to escape the Romans in the city. The player is given the choice to either go left, right, or forward through an intersection. """

    def __init__(self):
        Event.__init__(self)
    
    def play(self, place):
        """Player is allowed to go left, right, or forward through the intersections in the city"""
        move = fixed_input(input("You are running through the town to escape the Romans! Will you go left, right, or forward at the intersection? "))
        print()
        if move == "left":
            print("You go left at the intersection.")
            Town_Place.possible_events.append(City_Navigation())
        elif move == "right":
            print("You go right at the intersection.")
            Town_Place.possible_events.append(City_Navigation())
        elif move == "forward":
            print("You go forward through the intersection.")
            Town_Place.possible_events.append(City_Navigation())
        else:
            print("Invalid input, try again")
            self.play(place)

### Place Class ###

class Place:
    """Place class that is made up of a randomized set of tiles. Places can be visualized as a B x 1 grid, where B is an integer. Since the player begins battles ar position 0, the true length of a place is actually the size attribute + 1. Length is randomly determined by the class 
    attribute for possible sizes. Can randomly contain an enemy or event, depending on the type. A place can have up to a certain number of enemies at a time. The player starts at the first tile of the place and the enemies start on the opposite side. The enemies attribute is a list of enemies 
    while the event attribute is an single event instance. Different place and place types have a different list of possible enemies and events.
    """
    global_turns = 0
    current_time_items = [] #Contains current items with time limited effects used by the player. This is checked at the end of every turn to see if the item is still in use.
    possible_sizes = [x for x in range(4, 6)]
    possible_enemies = ["Entity"] #Contains the possible types of enemies and events that the place can be populated with. The enemies list is filled with the name of the potential enemies, not classes
    possible_events = []
    min_enemies = 1
    max_enemies = 3
    damage_bonus = 0
    range_bonus = 0
    move_bonus = 0
    max_health_bonus = 0
    heal_bonus = 0
    move_bonus = 0
    uses_bonus = 0
    accuracy_bonus = 0

    def __init__(self, type_weight=[1, 1]):
        self.size = random.choice(self.possible_sizes) #Picks random size based off of the possible sizes
        self.type = random.choices(["Enemy", "Event"], weights=type_weight)[0] #Picks a random type based off of the type_weight
        self.enemies = []
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
                self.add_enemy(enemy_constructor(random.choice(self.possible_enemies)))
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

    def __repr__(self):
        return "Place"

    def __str__(self):
        return "{0} Place, Size: {1}".format(self.type, self.size)

class Forest_Place(Place):
    """Place class for locations in the forest. Small length places that can have Legionaries, Immortal Dogs, and Feral Monkeys. The final fight of the jungle section is a large snake.
    """
    possible_sizes = [x for x in range(3, 6)]
    possible_enemies = ["Legionary", "Immortal_Dog", "Feral_Monkey"]
    possible_events = [Encounter(), Encounter(), Encounter(), Encounter()]
    range_bonus = -1
    damage_bonus = 0.20

    def __init__(self, type_weight=[4, 1]):
        Place.__init__(self, type_weight)

class Tunnel_Place(Place):
    """Place class for locations within the tunnel after the forest. Each place is very small, forcing the player to fight almost instantly. Players get a range penalty again due to the darkness but have a chance to completely dodge an enemy encounter. The tunnels only have Legionaries 
    patrolling it There should be at most 3 enemies per encounter, making this an easy place. The only event is the Dodge event, which is what happens when the player dodges a fight."""
    possible_sizes = [x for x in range(3, 5)]
    possible_enemies = ["Legionary"]
    possible_events = [Dodge()]
    max_enemies = 2
    range_bonus = -2
    dodge_chance = 40

    def __init__(self, type_weight=[6, 4]):
        Place.__init__(self, type_weight)

class Cliff_Place(Place):
    """The cliffs are located directly after the tunnel and give the player a range bonus. In exchange, the player's move speed is locked to 1 step per turn. Using an item that boosts movement speed will just waste the item. Each place is of medium length, allowing the player some 
    ranged combat options. There are no events for these places and the enemies are Harpy warriors, which quickly swoop down to attack the player and then retreat. Since Harpies attack in packs, up to 4 can attack the player at once."""
    possible_sizes = [x for x in range(6, 8)]
    possible_enemies = ["Harpy", "Harpy_Archer"]
    possible_events = []
    max_enemies = 4
    range_bonus = 2

    def __init__(self, type_weight=[1, 0]):
        Place.__init__(self, type_weight)

class Town_Place(Place):
    """The town is located after the cliffs and these places contains medium to small sized places and provides no bonuses at all. Enemies encountered here consist of City Guard, which are Legionaries that are more heavily armed and armored, dealing more damage and having more survivability. 
    Their dogs are also given an upgrade in the form of armor, giving them more protection. A new enemy is the Roman auxiliary archer, which has both a melee weapon and a bow. The archer doesn't retreat but instead switches to melee combat, dealing more damage but is not armor piercing."""
    possible_sizes = [x for x in range(4, 7)]
    possible_enemies = ["City_Guard", "Armored_Dog", "Roman_Archer"]
    possible_events = [City_Navigation()]
    min_enemies = 3
    max_enemies = 4

    def __init__(self, type_weight=[1, 1]):
        Place.__init__(self, type_weight)

class Machine_Labs(Place):
    """The Machine Labs are located in the town and the player gets to visit them if they choose the correct pathway in the story. The labs are perhaps the largest section of the game, having the most enemy variety and the most items the player can acquire. Enemies here are both man and 
    machine, with each type having their own unique moves that work together to give the player a tough time. The final boss of the area is an experimental machine called 'Dominion' and will prove to be the player's toughest fight yet. This area gives the player a movement and damage bonus to 
    assist them but due to the heavy air from all the industrial work, the player has reduced max health. Places are medium sized but there can be many enemies at a time, creating challenging situations."""
    possible_sizes = [x for x in range(5, 10)]
    possible_enemies = []
    possible_events = []
    min_enemies = 2
    max_enemies = 5
    move_bonus = 1
    damage_bonus = 0.40
    max_health_bonus = -30

    def __init__(self, type_weight=[1, 1]):
        Place.__init__(self, type_weight)

### Store Class ###

class Store:
    """Class for the store at the beginning of the game, which gives players the only chance to buy equipment before going on their journey. A store has an inventory of items, which are in the form of a dictionary where 
    the keys are the name of the item and the values are the object instances themselves.
    >>> x = Store()
    >>> x.inventory
    []
    >>> x
    Store instance
    >>> print(x)
    Store selling []
    """

    def __init__(self):
        self.inventory = []

    def add_inventory(self, lst):
        """Takes in a list of equipment instances and adds them to the store's inventory, which is a dictionary. Keys are the name of the weapon (all lowercase) and the values are equipment instances themselves. If multiple
        of the same equipment is being added, create a new key for each of them. This will make deletion easier in the future.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> store = Store()
        >>> store.add_inventory([spear])
        >>> store.inventory
        [Spear]
        """
        for x in lst:
            self.inventory.append(x)
    
    def remove_inventory(self, item):
        """Removes an instance of an object from the store inventory. If there are no more object instances for a key, remove that key. item_name is a lowercase string version of the name of the item being removed.
        >>> weapon = Weapon(20, 1, 1, 100, "Spear")
        >>> store = Store()
        >>> store.add_inventory([weapon])
        >>> store.inventory
        [Spear]
        >>> store.remove_inventory(weapon)
        >>> store.inventory
        []
        """
        if item in self.inventory:
            self.inventory.remove(item)
        else:
            print("Item not in inventory")

    def show_inventory(self):
        """Shows the store's inventory by printing out, with each item on a different line"""
        print("*** Store Menu ***")
        i = 0
        for x in self.inventory:
            print("[{0}] ".format(i) + str(x))
            i += 1

    def purchase(self, player, item):
        """Allows for the player to purchase an item from the store. Must check to see if the player can carry an item and if the player has enough money to buy it.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> expensive_weapon = Weapon(20, 1, 1, 2000, "Expensive")
        >>> heavy_weapon = Weapon(20, 1, 100, 100, "Heavy")
        >>> player = Player("Dan")
        >>> store = Store()
        >>> store.purchase(player, spear)
        Item not in store
        >>> store.add_inventory([spear, expensive_weapon, heavy_weapon])
        >>> store.purchase(player, spear)
        Purchased Spear for 100 coins
        Added Spear to backpack
        Wallet: 900
        >>> store.purchase(player, expensive_weapon)
        Not enough money
        >>> store.purchase(player, heavy_weapon)
        Adding item would go over the weight limit
        """
        if item not in self.inventory:
            print("Item not in store")
            return
        elif player.wallet < item.price:
            print("Not enough money")
            return
        elif player.weight_limit - player.current_weight < item.weight:
            print("Adding item would go over the weight limit")
            return
        else:
            print("Purchased {0} for {1} coins".format(item.name, item.price))
            player.backpack_add(item)
            self.remove_inventory(item)
            player.wallet -= item.price
            print("Wallet: {0}".format(player.wallet))

    def refund(self, player, item): 
        """Allows for the player to refund an item to the store, placing that item back into the store's inventory and adding the price of the item back to the player's wallet.
        >>> spear = Weapon(20, 1, 1, 100, "Spear")
        >>> store = Store()
        >>> player = Player("Dan")
        >>> player.backpack_add(spear)
        Added Spear to backpack
        >>> store.refund(player, spear)
        Spear removed from backpack
        Spear refunded for 100 coins
        Wallet: 1100
        >>> player.wallet
        1100
        """
        if item in player.backpack:
            self.add_inventory([item])
            player.backpack_remove(item)
            print("{0} refunded for {1} coins".format(item.name, item.price))
            player.wallet += item.price
            print("Wallet: {0}".format(player.wallet))
        else:
            print("Item does not exist in backpack")
    
    def buying(self, player):
        """Function that allows the player to purchase items from the store. Player can either buy an item, refund an item, or type "Done" to finalize their purchase and start their adventure. Raises an Invalid Input message if the input is one word that is not 'Done' 
        or if it's multiple words that are not a valid command. The except case handles the first issue and the else case handles the second issue.
        """
        while True:
            self.show_inventory()
            print()
            player.show_backpack()
            print()
            command = fixed_input(input("What do you want to do? Type 'Buy' or 'Refund' followed by the number of the item or type 'Done' to leave the store. "))
            action = command.split(" ", 1)[0]
            if action == "done":
                    break
            try:
                index = command.split(" ", 1)[1]
                if index.isnumeric():
                    index = int(index)
                    if action == "buy" and index in range(len(self.inventory)):
                        print()
                        self.purchase(player, self.inventory[index])
                        print()
                    elif action == "refund" and index in range(len(player.backpack)):
                        print()
                        self.refund(player, player.backpack[index])
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
        return "Store instance"

    def __str__(self):
        return "Store selling {0}".format(str(self.inventory))

### Game Manager ###

def fixed_input(s):
    """Takes an input string s and returns a new string that is reformatted to remove the spaces before and after s and make 
    everything lowercase.
    >>> x = fixed_input("   The cow jumped over the Moon   ")  
    >>> x 
    'the cow jumped over the moon'
    """
    return s.lower().strip()

def enemy_constructor(name):
    """Takes in a string version of the name of a class and then constructs instances of that class. This allows the game to generate new enemies. Uses a variety of conditional statements to decide which class instance to create. If stats of a class are to be changed, change them here.
    >>> x = enemy_constructor("Legionary")
    >>> isinstance(x, Legionary)
    True
    """
    return eval(name + "()")

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
        choice = fixed_input(input("Type 'Inventory' to manage your backpack or 'Continue' to move forwards. "))
        if choice == "continue":
            print("")
            print("You continue forwards")
            break
        elif choice == "inventory":
            print("")
            player.sorting()
        else:
            print("")
            print("Invalid input, try again")

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
    fight()

def game_over():
    """Function that prints a game over message when the player dies and quits the program"""
    print("You have died! The lost treasure will remain hidden from the rest of the world. Perhaps this is for the better.")
    quit()