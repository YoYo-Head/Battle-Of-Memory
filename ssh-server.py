import asyncssh
import asyncio
import sys
from typing import Optional

port = 2222

async def handle_client(proccess: asyncssh.SSHServerProcess):
    username = proccess.get_extra_info("username")
    proccess.stdout.write(f"Hello {username}! Welcome to \n BATTLE OF MEMORY \n By Yahya :)")
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

async def start_server():
    await asyncssh.create_server(Server, "", port, server_host_keys=["ssh_host_key"], process_factory=handle_client)

loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(start_server())

except (OSError, asyncssh.Error) as exc:
    sys.exit("Error starting server: " + str(exc))

print("Server has started!")

loop.run_forever()