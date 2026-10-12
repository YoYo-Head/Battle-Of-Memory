import asyncssh
import math

class User:
    def __init__(self, proccess: asyncssh.SSHServerProcess, key = None, army_power: int = 100):
        self.proccess = proccess
        self.username = proccess.get_extra_info("username")
        self.key = key
        self.army = Army(army_power, self)

    def attack(self, base: Base):
        self.army.attack_base(base)

class Army:
    def __init__(self, infantry: int, owner: User, armour: int, base: Base):
        self.infantry = infantry
        self.owner = owner
        self.armour = armour
        self.base = base

    def attack_base(self, base: Base):
        base.take_damage(self.infantry / 10)

    def take_damage(self, attack_power: int, attacker: User):
        damage = math.ceil(attack_power * 100 / (100 + self.armour))
    
        self.infantry -= damage
    
        if self.infantry <= 0:
            self.infantry = 0
            self.base.change_ownership(attacker)

class Base:
    def __init__(self, owner: User):

        self.owner = owner

    def change_ownership(self, user):
        # need to create validation code later for username

        self.owner = user

    
    def destroy(self):
        self = None


        