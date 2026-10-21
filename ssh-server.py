import asyncssh
import asyncio
import sys
import game
from typing import Optional
import traceback
import gc
from rich.console import Console

port = 2222

prevConnections = []
known_users = []
game_players = []

at_base = game.Base("Avenger's Tower")
bc_base = game.Base("Batman's Cave")
ab_base = game.Base("Alpha Base")
bb_base = game.Base("Beta Base")
pc_base = game.Base("Pirate's Cove")
tc_base = game.Base("The Citadel")
ts_base = game.Base("The Stronghold")


def get_all_instances(class_object):
    instances = []

    for object in gc.get_objects():
        if isinstance(object, class_object):
            instances.append(object)
    return instances

def search_base_object(name: str) -> game.Base:
    for base in get_all_instances(game.Base):
        if base.name.lower() == name.lower().strip():
            return base

    return None

def input_handler(line, player: game.User):
        incoming_message = line.lower().strip()

        if "contest" in incoming_message:

            name = incoming_message.replace("contest", "").strip()

            if name == "":
                player.proccess.stdout.write("Please specify the name of the base you wish to attack!\n\n")
                return

            base = search_base_object(name)

            if base == None:
                player.proccess.stdout.write("That base doesn't exist!\nPlease double check base names through 'bases'.\n\n")
                return

            try:
                player.army.attack_base(base)
            except Exception:
                traceback.print_exc()

            return

        if "buy infantry" in incoming_message:
            data = incoming_message.replace("buy infantry", "").strip()

            if data == "":
                player.proccess.stdout.write("Please specify how many infantry you wish to buy!\n\n")
                return

            try:
                amount = int(data)

            except Exception:
                player.proccess.stdout.write("Please only use integers!\n\n")
                return

            try:
                player.army.buy_infantry(amount)
            except Exception:
                traceback.print_exc()

            return

        if "balance" in incoming_message:
            player.check_balance()
            return

        if "infantry" in incoming_message:
            player.army.check_infantry()
            return

        if "buy armour levels" in  incoming_message:
            data = incoming_message.replace("buy armour levels", "").strip()

            if data == "":
                player.proccess.stdout.write("Please specify how many levels of armour you wish to buy!\n")
                return

            try:
                amount = int(data)

            except Exception:
                player.proccess.stdout.write("Please only use integers!\n")
                return

            try:
                player.army.upgrade_armour(amount)
            except Exception:
                traceback.print_exc()

            return

        if "armour level" in incoming_message:
            player.army.check_armour_level()
            return


        if "my bases" == incoming_message:
            player.proccess.stdout.write("List of all your bases:\n")

            bases = game.Base.fetch_user_bases(player)

            for base in bases:
                player.proccess.stdout.write(f"    - {base.name}\n")

            player.proccess.stdout.write("\n")

            return
        
        if "bases" in incoming_message:
            player.proccess.stdout.write("List of all bases:\n")
            bases = game.Base.fetch_bases()
            
            for base in bases:
                player.proccess.stdout.write(f"    - {base.name}\n")

            player.proccess.stdout.write("\n")

            return
        
async def handle_client(proccess: asyncssh.SSHServerProcess):
    username = proccess.get_extra_info("username")
    proccess.stdout.write(f"Hello {username}! Welcome to \nBATTLE OF MEMORY \nBy Yahya :) \n")

    oldUser = False

    for con in prevConnections:
        for user in known_users:
            if con["key"] == user["key"]:
                print(f"User {username} has returned!")
                oldUser = True
                break

        if oldUser:
            break
    

    if not oldUser:
        print(f"New user {username}!")
        known_users.append(prevConnections[len(prevConnections) - 1])

    playerInfo = known_users[len(known_users) - 1]
    
    player = game.User(proccess, playerInfo["key"])
    
    player.claim_homebase()
    player.begin_minutely_money()
    

    async for line in proccess.stdin:
        clean_data = line.lower().strip()

        input_handler(clean_data, player)

    proccess.exit(0)

class Server(asyncssh.SSHServer):
    def connection_made(self, conn: asyncssh.SSHServerConnection):
        peername = conn.get_extra_info("peername")[0]
        print(f"Recieved SSH connection from {peername}")
        

    def connection_lost(self, exc: Optional[Exception]):
        if exc:
            print("SSH connection error: " + str(exc), file=sys.stderr)
        else:
            print("SSH connection lost.")

    def begin_auth(self, username):
        return True

    def public_key_auth_supported(self):
        return True

    def validate_public_key(self, username, key):
        client_key = key.export_public_key().decode("utf-8").strip()

        for connection in prevConnections:
            if connection["key"] == client_key:
                return True

        prevConnections.append( { "key": client_key, "username": username} )
        print("added " + username)
        return True

async def start_server():
    await asyncssh.create_server(Server, "", port, server_host_keys=["ssh_host_key"], process_factory=handle_client)

loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(start_server())

except (OSError, asyncssh.Error) as exc:
    sys.exit("Error starting server: " + str(exc))

print("Server has started!")

loop.run_forever()