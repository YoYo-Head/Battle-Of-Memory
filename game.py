import asyncssh
import math
import traceback
import threading
import gc
import time
from colorist import Color, Effect

Effect.BOLD_OFF = Effect.BOLD_OFF + Effect.UNDERLINE_OFF


def get_all_instances(class_object):
    instances = []

    for object in gc.get_objects():
        if isinstance(object, class_object):
            instances.append(object)
    return instances

def base_minutely_money(user: User):
    while True:
        bases = 0
        rate = 50

        for base in get_all_instances(Base):
            if base.owner == user:
                bases += 1

        income = bases * rate

        user.balance += income

        time.sleep(60)

class User:
    def __init__(self, proccess: asyncssh.SSHServerProcess, key = None, army_power: int = 100, balance: int = 100):
        self.proccess = proccess
        self.username = proccess.get_extra_info("username")
        self.key = key

        found_name = True
        counter = 0

        while found_name:
            format = f"{self.username}#{counter}'s Base"

            if counter == 0:
                format = f"{self.username}'s Base"

            found_name = Base.base_with_name(format)
            counter += 1

        self.home_base = Base(format)
        self.army = Army(army_power, self, 50, self.home_base)
        self.balance = balance
        self.thread_for_base_money = threading.Thread(target=base_minutely_money, args=(self,))

    def begin_minutely_money(self):
        self.thread_for_base_money.start()

    def claim_homebase(self):
        self.home_base.change_ownership(self)


    def check_balance(self):
        print(Effect.BOLD_OFF.upper())

        self.proccess.stdout.write(f"{Color.GREEN}You have {Effect.BOLD}${self.balance}{Effect.BOLD_OFF}.{Color.OFF}\n\n")

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
            self.owner.proccess.stdout.write("You can't attack your own base!\n\n")
            return

        if base.owner == None:
            base.change_ownership(self.owner)
            return

        

        enemy_army = base.owner.army

        eInfantry_lost = enemy_army.take_damage(self.infantry, self.owner)

        sInfantry_lost = self.take_damage(enemy_army.infantry, base.owner)
        base.owner.proccess.stdout.write(f"!!! YOUR BASE ({base.name.upper()}) IS UNDER ATTACK !!!\n!!! {self.owner.username.upper()}'S ARMY HAS KILLED {eInfantry_lost} INFANTRY OF YOUR ARMY !!!\n\n")
        self.owner.proccess.stdout.write(f"Your army killed {eInfantry_lost} infantry.\nYou lost {sInfantry_lost} infantry.\n\n")

    def buy_infantry(self, amount: int):
        cost_per_person = 20

        price = amount * cost_per_person

        if self.owner.balance < price:
            self.owner.proccess.stdout.write("You don't have enough money to buy " + str(amount) + " infantry!\n\n")
            return

        self.owner.balance -= price
        self.infantry += amount

        self.owner.proccess.stdout.write(f"You have now bought an extra {amount} infantry!\nThis action costed ${price}.\nYou now have ${self.owner.balance}.\n\n")

    def upgrade_armour(self, amount: int):
        cost_per_level = 5

        price = amount * cost_per_level

        if self.owner.balance < price:
            self.owner.proccess.stdout.write("You don't have enough money to buy " + str(amount) + " levels of armour!\n\n")
            return
        
        self.owner.balance -= price
        self.armour += amount
        
        self.owner.proccess.stdout.write(f"You have now bought an extra {amount} levels of armour!\nThis action costed ${price}.\nYou now have ${self.owner.balance}.\n\n")

    def check_infantry(self):
        self.owner.proccess.stdout.write(f"You have {self.infantry} infantry.\n\n")


    def take_damage(self, attack_power: int, attacker: User):
        damage = math.ceil(attack_power * 100 / (100 + self.armour))
    
        self.infantry -= damage
    
        if self.infantry <= 0:
            damage += self.infantry

            self.infantry = 0
            self.base.change_ownership(attacker)

            return damage

        return damage

    def check_armour_level(self):
        self.owner.proccess.stdout.write(f"You have level {self.armour} armour.\n\n")

class Base:
    def __init__(self, name: str, owner: User = None):

        self.owner = owner
        self.name = self.get_formatted_name(name)

    def change_ownership(self, user: User):
        try:
            if self.owner.home_base == self:
                self.owner.proccess.stdout.write(f"{Color.RED}You have lost the game since you've lost your homebase!{Color.OFF}\n")
                self.owner.proccess.exit(0)
            else:
                self.owner.proccess.stdout(f"You have just lost {self.name}!\n\n")
        except Exception:
            traceback.print_exc()


        user.proccess.stdout.write("Congrats! You now own " + self.name + ".\n\n")

        self.owner = user

    @classmethod
    def fetch_bases(cls) -> list[Base]:
        return get_all_instances(cls)

    @classmethod
    def fetch_user_bases(cls, user: User) -> list[Base]:
        bases = get_all_instances(cls)

        bases = cls.fetch_bases()

        user_bases = []

        for base in bases:
            if base.owner == user:
                user_bases.append(base)

        return user_bases

    @classmethod
    def base_with_name(cls, name: str) -> bool:
        bases = cls.fetch_bases()

        for base in bases:
            if base.name == cls.get_formatted_name(name):
                return True

        return False

    @classmethod
    def fetch_base(cls, name: str) -> Base:
        bases = cls.fetch_bases()

        for base in bases:

            if base.name.lower() == cls.get_formatted_name(name):
                return base

        return None        

    @classmethod
    def get_formatted_name(cls, name) -> str:
        return Color.CYAN + name + Color.OFF   
    
    def destroy(self):
        self = None


        