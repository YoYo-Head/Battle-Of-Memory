import asyncssh
import math
import traceback

class User:
    def __init__(self, proccess: asyncssh.SSHServerProcess, key = None, army_power: int = 100, home_base: Base = None, balance: int = 100):
        self.proccess = proccess
        self.username = proccess.get_extra_info("username")
        self.key = key
        self.army = Army(army_power, self, 50, home_base)
        self.balance = 250
        self.home_base = home_base
        self.balance = balance

    def claim_homebase(self):
        self.home_base.change_ownership(self)


    def check_balance(self):
        self.proccess.stdout.write(f"You have ${self.balance}.\n")

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

    def buy_infantry(self, amount: int):
        cost_per_person = 20

        price = amount * cost_per_person

        if self.owner.balance < price:
            self.owner.proccess.stdout.write("You don't have enough money to buy " + str(amount) + " infantry!\n")
            return

        self.owner.balance -= price
        self.infantry += amount

        self.owner.proccess.stdout.write(f"You have now bought an extra {amount} infantry!\nThis action costed ${price}.\nYou now have ${self.owner.balance}.\n")

    def check_infantry(self):
        self.owner.proccess.stdout.write(f"You have {self.infantry} infantry.\n")


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


        