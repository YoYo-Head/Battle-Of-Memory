import asyncssh
import math
import traceback

class User:
    def __init__(self, proccess: asyncssh.SSHServerProcess, key = None, army_power: int = 100, home_base: Base = None):
        self.proccess = proccess
        self.username = proccess.get_extra_info("username")
        self.key = key
        self.army = Army(army_power, self, 50, home_base)
        self.balance = 250
        self.home_base = home_base

    def claim_homebase(self):
        self.home_base.change_ownership(self)


    def attack(self, base: Base):
        self.army.attack_base(base)

    def remove():
        pass

class Army:
    def __init__(self, infantry: int, owner: User, armour: int, base: Base):
        self.infantry = infantry
        self.owner = owner
        self.armour = armour
        self.base = base

    def attack_base(self, base: Base):
        if base.owner == self.owner:
            self.owner.proccess.stdout.write("You can't attack your own base!\n")
            return

        if base.owner == None:
            base.change_ownership(self.owner)
            return

        enemy_army = base.owner.army

        eInfantry_lost = enemy_army.take_damage(self.infantry, self.owner)

        sInfantry_lost = self.take_damage(enemy_army.infantry, base.owner)

        self.owner.proccess.stdout.write(f"Your army killed {eInfantry_lost} infantry.\nYour lost {sInfantry_lost} infantry.\n")



    def take_damage(self, attack_power: int, attacker: User):
        damage = math.ceil(attack_power * 100 / (100 + self.armour))
    
        self.infantry -= damage
    
        if self.infantry <= 0:
            self.infantry = 0
            self.base.change_ownership(attacker)

            return damage

        return damage

class Base:
    def __init__(self, name: str, owner: User = None):

        self.owner = owner
        self.name = name

    def change_ownership(self, user: User):
        # need to create validation code later for username

        user.proccess.stdout.write("Congrats! You now own " + self.name + ".\n")

        self.owner = user

    
    def destroy(self):
        self = None


        