import asyncssh
import asyncio
import sys
from typing import Optional

port = 2222

accounts = {
    "normal_user": b"",
}

async def handle_client(proccess: asyncssh.SSHServerProcess):
    username = proccess.get_extra_info("username")
    proccess.stdout.write(f"Hello {username}! Welcome to \n BATTLE OF MEMORY \n By Yahya :) \n")
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
        return False

    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
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