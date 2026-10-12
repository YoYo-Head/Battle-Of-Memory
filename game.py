import asyncssh

class User:
    def __init__(self, proccess: asyncssh.SSHServerProcess, key = None):
        self.proccess = proccess
        self.username = proccess.get_extra_info("username")
        self.key = key

    
        

class Base:
    def __init__(self, owner: User, take_health: int, defence: int = 10, max_health: int = 100):

        if take_health > max_health:
            return ValueError(take_health)

        self.health = max_health - take_health
        self.max_health = max_health
        self.defence = defence
        self.owner = owner

    def change_ownership(self, user):
        # need to create validation code later for username

        self.owner = user

    def attack(self, attack_power: int, attacker):
        damage = attack_power * 100 / (100 + self.defence)

        self.health -= damage

        if self.health <= 0:
            self.change_ownership(attacker)
            self.health = self.max_health

    def change_defence(self, amount: int):
        self.defence += amount

    
    def destroy(self):
        self = None


        