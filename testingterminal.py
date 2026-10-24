from colorist import Color

print(f"{Color.RED}!!! YOUR BASE ({Color.CYAN + "yahya" + Color.RED}) IS UNDER ATTACK !!!\n!!! YAHYA'S ARMY HAS KILLED 12 INFANTRY OF YOUR ARMY !!!{Color.OFF}\n\n")
code_f = f"{Color.RED}!!! YOUR BASE ({Color.CYAN + "yahya".upper() + Color.OFF}){Color.RED} IS UNDER ATTACK !!!\n!!! {"yahya".upper()}'S ARMY HAS KILLED {12} INFANTRY OF YOUR ARMY !!!{Color.OFF}\n\n"

print(code_f)
