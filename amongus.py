#Imports: ANSI and terminal helper to allow for continual inputs
import sys
import time
import msvcrt
import ctypes
import random

def enable_windows_ansi():
    #initializing a workable variable
    kernel32 = ctypes.windll.kernel32
    # -11 for this is the thing that allows us to control terinal outputs
    hStdout = kernel32.GetStdHandle(-11)
    #allows us to keep the updated mode/version
    mode = ctypes.c_uint32()
    #trying to read the current mode (small test)
    if kernel32.GetConsoleMode(hStdout, ctypes.byref(mode)) == 0:
        return False
    
    #establishing mode
    #0x0004 = terminal processes
    new_mode = mode.value | 0x0004
    
    #actual application
    if kernel32.SetConsoleMode(hStdout, new_mode) == 0:
        return False
    return True

def ansi_clear_screen():
    # \x1b = ESC character
    # [2J  = clear the whole screen
    # [H   = move cursor to home position (row 1, col 1)
    sys.stdout.write("\x1b[2J\x1b[H")

def ansi_move_cursor(row, col):
    #chucks the cursor somewhere
    sys.stdout.write(f"\x1b[{row};{col}H")

def ansi_hide_cursor():
    sys.stdout.write("\x1b[?25l")

def ansi_show_cursor():
    sys.stdout.write("\x1b[?25h")

#forces our inputs to appear on screen
def flush():
    sys.stdout.flush()

#if you want to use arrow keys (converting arrow keys to wasd)
def poll_key():
    # If no key is waiting, return None immediately.
    # This is what makes the input NON-BLOCKING.
    if not msvcrt.kbhit():
        return None

    # Read one key press as raw bytes
    ch = msvcrt.getch()

    # Arrow keys are special on Windows:
    # first byte is b'\x00' or b'\xe0'
    # second byte tells which arrow it was
    if ch in (b"\x00", b"\xe0"):
        ch2 = msvcrt.getch()
        code = ch2[0]

        # Convert arrows into the same controls as WASD
        if code == 72:   # up arrow
            return "w"
        elif code == 80: # down arrow
            return "s"
        elif code == 75: # left arrow
            return "a"
        elif code == 77: # right arrow
            return "d"
        return None

    # For normal keys, decode the byte into text
    try:
        k = ch.decode("utf-8", errors="ignore").lower()
    except:
        return None

    # Only allow keys we care about
    if k in ["w", "a", "s", "d", "q"]:
        return k

    return None



#Among us CLI 8x8 grid - autoupdating
mainMap = [
    list("+----------------------+----------------------+----------------------+"),
    list("|                      |                      |                      |"),
    list("|                      |                      |                      |"),
    list("|   O    O    O    O   +-----------+----------+                      |"),
    list("|                               /                                     "),
    list("+--------+-----------+         /                                     |"),
    list("        |                     /        +-----------------------------+"),
    list("        |                                                             "),
    list("+-------+----------+-------+           +-----------+-----------------+"),
    list("|                                                                    |"),
    list("+---   ----+-----   --+-------+                   +------------------+"),
    list("           |          |                                              |"),
    list("+--   -----+----   ---+-------------------   ---------+----   -------+"),
    list("|                             |                       |              |"),
    list("+-----------------------------+-----------+-      ---+---------------+"),
    list("                                          |          |----------------"),
    list("                                          +--     ---+---------------+"),
    list("                                          |                      |----"),
    list("                                          +-----    --+---------------"),
    list("                              +------------+          |--------------+"),
    list("                              |                                      |"),
    list("                              +-------------------+------------------+"),
]

# variables (coordinate) format: [y,x]
player = [1,1]
npc1 = [1,68]
npc2 = [1,67]
npc3 = [1,66]

cont = True

# top-left corner of the 8x8 viewport
view_x = 0
view_y = 0

#variable for player
mainMap[player[0]][player[1]] = "P"
mainMap[npc1[0]][npc1[1]] = "A"
mainMap[npc2[0]][npc2[1]] = "B"
mainMap[npc3[0]][npc3[1]] = "C"


def viewpoint(direction):
    #refers global variables and ensures changes made to them
    global view_x, view_y, player

    #vertical camera movement (if the y is not within the view bounds, we shift the bounds)
    if player[0] < view_y + 3:
        view_y = max(0, player[0] - 3)
    elif player[0] > view_y + 4:
        view_y = min(len(mainMap) - 8, player[0] - 4)

    #horizontal camera movement
    if player[1] < view_x + 3:
        view_x = max(0, player[1] - 3)
    elif player[1] > view_x + 4:
        view_x = min(len(mainMap[0]) - 8, player[1] - 4)

#applies terminal update to the game
def draw_view():
    ansi_move_cursor(1,1)
    #initialize 8x8 viewpoint
    for ya in range(view_y, view_y + 8):
        row = []
        for xa in range(view_x, view_x + 8):
            row.append(mainMap[ya][xa])
        # .ljust(60) makes sure old longer lines get overwritten (erasing old print statements)
        print(" ".join(row).ljust(60))
    flush()

#NPC random movement
def npc_movement(npc):
    #random variables
    direction = random.randint(1, 4)
    spaces = random.randint(1,1)
    #deciding movements
    for _ in range(spaces):
        if direction == 1 and npc[0] > 0 and mainMap[npc[0] - 1][npc[1]] == " ":
            mainMap[npc[0] - 1][npc[1]] = mainMap[npc[0]][npc[1]]
            mainMap[npc[0]][npc[1]] = " "
            npc[0] -= 1

        elif direction == 2 and npc[1] > 0 and mainMap[npc[0]][npc[1] - 1] == " ":
            mainMap[npc[0]][npc[1] - 1] = mainMap[npc[0]][npc[1]]
            mainMap[npc[0]][npc[1]] = " "
            npc[1] -= 1

        elif direction == 3 and npc[0] < len(mainMap) - 1 and mainMap[npc[0] + 1][npc[1]] == " ":
            mainMap[npc[0] + 1][npc[1]] = mainMap[npc[0]][npc[1]]
            mainMap[npc[0]][npc[1]] = " "
            npc[0] += 1

        elif direction == 4 and npc[1] < len(mainMap[0]) - 1 and mainMap[npc[0]][npc[1] + 1] == " ":
            mainMap[npc[0]][npc[1] + 1] = mainMap[npc[0]][npc[1]]
            mainMap[npc[0]][npc[1]] = " "
            npc[1] += 1

    
enable_windows_ansi()
ansi_clear_screen()
ansi_hide_cursor()

try:
    while cont:
        #updates the view
        draw_view()
        #check for arrow keys
        movement = poll_key()


        #check: movement type | we can move | empty space
        if movement == "w" and player[0] > 0 and mainMap[player[0] - 1][player[1]] == " ":
            mainMap[player[0] - 1][player[1]] = mainMap[player[0]][player[1]]
            mainMap[player[0]][player[1]] = " "
            player[0] -= 1
            viewpoint("up")

        elif movement == "a" and player[1] > 0 and mainMap[player[0]][player[1] - 1] == " ":
            mainMap[player[0]][player[1] - 1] = mainMap[player[0]][player[1]]
            mainMap[player[0]][player[1]] = " "
            player[1] -= 1
            viewpoint("left")

        elif movement == "s" and player[0] < len(mainMap) - 1 and mainMap[player[0] + 1][player[1]] == " ":
            mainMap[player[0] + 1][player[1]] = mainMap[player[0]][player[1]]
            mainMap[player[0]][player[1]] = " "
            player[0] += 1
            viewpoint("down")

        elif movement == "d" and player[1] < len(mainMap[0]) - 1 and mainMap[player[0]][player[1] + 1] == " ":
            mainMap[player[0]][player[1] + 1] = mainMap[player[0]][player[1]]
            mainMap[player[0]][player[1]] = " "
            player[1] += 1
            viewpoint("right")

        elif movement == "q":
            cont = False
        
        #npc movement
        chanc = random.randint(1,8)
        if (chanc == 1):
            npcs = [npc1, npc2, npc3]
            for npc in npcs:
                npc_movement(npc)
        time.sleep(0.03)
finally:
    ansi_show_cursor()
    ansi_move_cursor(15, 1)
    print(npc1)