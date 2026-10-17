## Battle of Memory

# How to connect
**SSH Command:** ssh -p 2222 blah.blah

To connect to the SSH server, you first must open up a terminal. Once opened, you can simply put paste the *SSH Command* mentioned above.

# What to do
Once you've loaded into the server, there is quite a few things you can do. Here are the commands you can currently run:

- **contest [BASE_NAME]** -> Attacks that Base.
- **balance** -> Show how much money you have.
- **buy infantry** [AMOUNT]** -> Buys more infantry.
- **infantry** -> Show how many infantry you have.

As soon as you load you, you should automatically recieve a base (which will be referred to as your home base), $100 and 100 infantry.

# How it works
This SSH server runs on Python through the *asyncssh* library. It allows anyone to connect as it's public key authentication funtion always
returns True. The public key and usernames of past connections are also recorded, allowing the server to remember past clients. However, This
hasn't been used by the game yet. 

More onto the game side, the `game.py` file contains all the class information for the game's different objects. This allows for easy use when
implementing it into `ssh-server.py`, the python file that handles the server side of things.