## Battle of Memory

# How to connect
**SSH Command:** ssh -6 -p 2222 yoyo-head123@2a01:4f9:3080:3192::2051
**Requirements:**
1. You must have IPv6 connectivity on your device.
2. You must have a public ssh key generated on your device.

If you are unsure whether your device has IPv6 connectivity, head over to `https://test-ipv6.com` and see whether you past their test.

To generate an ssh public key run the following:

> ssh-keygen -t ed25519

Once you run that command, you can simply press *enter* for all other inputs.

To connect to the SSH server, you first must open up a terminal. Once opened, you can simply put paste the *SSH Command* mentioned above.

# What to do
Once you've loaded into the server, there is quite a few things you can do. Here are the commands you can currently run:

- **contest [BASE_NAME]** -> Attacks that Base.
- **balance** -> Show how much money you have.
- **buy infantry [AMOUNT]** -> Buys more infantry.
- **infantry** -> Show how many infantry you have.
- **bases** -> Shows all the bases in the game.
- **armour level** -> Shows you level of armour.
- **buy armour levels [AMOUNT]** -> Buys more armour levels.
- **my bases** -> Shows the bases you own.
- **exit** -> Disconnects you from the server and also removes any ANSI codes.

As soon as you load you, you should automatically recieve a base (which will be referred to as your home base), $100 and 100 infantry. Also,
you should be getting $50 for every base you own per minute.

# How it works
This SSH server runs on Python through the *asyncssh* library. It allows anyone to connect as it's public key authentication funtion always
returns True. The public key and usernames of past connections are also recorded, allowing the server to remember past clients. However, This
hasn't been used by the game yet. 

More onto the game side, the `game.py` file contains all the class information for the game's different objects. This allows for easy use when
implementing it into `ssh-server.py`, the python file that handles the server side of things.