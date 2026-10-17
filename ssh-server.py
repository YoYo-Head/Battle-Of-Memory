import asyncssh
import asyncio
import sys
import game
from typing import Optional
import traceback
import gc

port = 2222

prevConnections = []
known_users = []
game_players = []

eax_base = game.Base("EAX")
ebx_base = game.Base("EBX")
ecx_base = game.Base("ECX")
edx_base = game.Base("EDX")


def get_all_instances(class_object):
    instances = []

    for object in gc.get_objects():
        if isinstance(object, class_object):
            instances.append(object)
    return instances

def assign_base() -> game.Base:
    try:
        for base in get_all_instances(game.Base):
            if base.owner == None:
                return base

    except Exception:
        traceback.print_exc()

    return None

def search_base_object(name: str) -> game.Base:
    for base in get_all_instances(game.Base):
        if base.name.lower() == name.lower().strip():
            return base

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

    player = game.User(proccess, playerInfo["key"], home_base=assign_base())
    player.claim_homebase()

    async for line in proccess.stdin:
        incoming_message = line.lower().strip()

        if "contest" in incoming_message:

            name = incoming_message.replace("contest", "").strip()

            if name == "":
                player.proccess.stdout.write("Please specify the name of the base you wish to attack!\n")
                return

            base = search_base_object(name)

            try:
                player.army.attack_base(base)
            except Exception:
                traceback.print_exc()

        if "buy infantry" in incoming_message:
            data = incoming_message.replace("buy infantry", "").strip()

            if data == "":
                player.proccess.stdout.write("Please specify how many infantry you wish to buy!\n")
                return

            try:
                amount = int(data)

            except Exception:
                player.proccess.stdout.write("Please only use integers!\n")
                print("type failiar")
                return

            print(f"amount: {amount}")

            try:
                player.army.buy_infantry(amount)
            except Exception:
                traceback.print_exc()

        if "balance" in incoming_message:
            player.check_balance()

        if "infantry" in incoming_message:
            player.army.check_infantry()

        
    
    #proccess.exit(0)

    #game.User(proccess)



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