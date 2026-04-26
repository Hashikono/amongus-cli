#Imports: ANSI and terminal helper to allow for continual inputs
import sys
import time
import msvcrt
import ctypes
import random
import threading

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

class Player:
    def __init__(self, name, y_coor, x_coor):
        self.y = y_coor
        self.x = x_coor
        self.name = name
        self.role = "imposter" #BY DEFAULT WE ARE THE IMPOSTER

    def move(self, direction, game_map):
        #Move the player in the given direction
        new_y, new_x = self.y, self.x
        
        if direction == "up":
            new_y -= 1
        elif direction == "down":
            new_y += 1
        elif direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1
        
        # Check boundaries and collision
        if (new_y >= 0 and new_y < len(game_map) and 
            new_x >= 0 and new_x < len(game_map[0]) and 
            (game_map[new_y][new_x] == " " or 
            (game_map[new_y][new_x] in characters and self.role == "imposter"))):
            
            if (game_map[new_y][new_x] in characters and self.role == "imposter"): 
                self.can_kill(game_map, game_map[new_y][new_x])

            # Clear old position
            game_map[self.y][self.x] = " "
            # Move to new position
            self.y, self.x = new_y, new_x
            # Place name at new position
            game_map[self.y][self.x] = self.name
            return True
        return False
    
    def can_kill(self, game_map, npcs):
        #checking every direction
        print(npcs)
            
        

class NPC:
    def __init__(self, name, y_coor, x_coor, move_interval):
        self.y = y_coor
        self.x = x_coor
        self.name = name
        self.move_interval = move_interval
        self.thread = None
        self.role = "crewmate"
        self.alive = True
        
    
    def move_randomly(self, game_map):
        directions = ["up", "down", "left", "right"]
        random.shuffle(directions)
        
        for direction in directions:
            new_y, new_x = self.y, self.x
            
            if direction == "up":
                new_y -= 1
            elif direction == "down":
                new_y += 1
            elif direction == "left":
                new_x -= 1
            elif direction == "right":
                new_x += 1
            
            # Check boundaries and collision
            if (new_y >= 0 and new_y < len(game_map) and 
                new_x >= 0 and new_x < len(game_map[0]) and 
                game_map[new_y][new_x] == " "):
                
                # Clear old position
                game_map[self.y][self.x] = " "
                # Move to new position
                self.y, self.x = new_y, new_x
                # Place name at new position
                game_map[self.y][self.x] = self.name
                return True
        return False
    
    def run(self, game_map, stop_event):
        while not stop_event.is_set():
            # Random chance to move (approximately 30% chance each cycle)
            if random.random() < 0.3:
                self.move_randomly(game_map)
            time.sleep(self.move_interval)
    
    def start_thread(self, game_map, stop_event):
        # yyyyStart the NPC in a separate thread
        self.thread = threading.Thread(target=self.run, args=(game_map, stop_event))
        self.thread.daemon = True
        self.thread.start()
        return self.thread

def viewpoint(player, view_x, view_y, game_map):
    #vertical camera movement
    if player.y < view_y + 3:
        view_y = max(0, player.y - 3)
    elif player.y > view_y + 4:
        view_y = min(len(game_map) - 8, player.y - 4)

    #horizontal camera movement
    if player.x < view_x + 3:
        view_x = max(0, player.x - 3)
    elif player.x > view_x + 4:
        view_x = min(len(game_map[0]) - 8, player.x - 4)
    
    return view_x, view_y

def draw_view(view_x, view_y, game_map):
    ansi_move_cursor(1, 1)
    #initialize 8x8 viewpoint
    for ya in range(view_y, min(view_y + 8, len(game_map))):
        row = []
        for xa in range(view_x, min(view_x + 8, len(game_map[0]))):
            row.append(game_map[ya][xa])
        # .ljust(60) makes sure old longer lines get overwritten
        print(" ".join(row).ljust(60))
    flush()


characters = ["P", "A", "B", "C", "D"]
def initialize_game():
    # Create player and NPCs
    player = Player("P", 1, 1)
    npc1 = NPC("A", 1, 68, 0.15)
    npc2 = NPC("B", 1, 67, 0.12)
    npc3 = NPC("C", 1, 66, 0.09)
    npc4 = NPC("D", 1, 65, 1)
    
    # Clear the map of any old names (just in case)
    for y in range(len(mainMap)):
        for x in range(len(mainMap[0])):
            if mainMap[y][x] in characters:
                mainMap[y][x] = " "
    
    # Place characters on map
    mainMap[player.y][player.x] = player.name
    mainMap[npc1.y][npc1.x] = npc1.name
    mainMap[npc2.y][npc2.x] = npc2.name
    mainMap[npc3.y][npc3.x] = npc3.name
    mainMap[npc4.y][npc4.x] = npc4.name
    
    return player, [npc1, npc2, npc3, npc4]

def main():
    # Enable ANSI and setup terminal
    enable_windows_ansi()
    ansi_clear_screen()
    ansi_hide_cursor()
    
    # Initialize game
    player, npcs = initialize_game()
    
    # Camera position
    view_x = 0
    view_y = 0
    
    # Stop event for NPC threads
    stop_event = threading.Event()
    
    # Start NPC threads
    npc_threads = []
    for npc in npcs:
        thread = npc.start_thread(mainMap, stop_event)
        npc_threads.append(thread)
    
    cont = True
    
    try:
        while cont:
            # Update camera position
            view_x, view_y = viewpoint(player, view_x, view_y, mainMap)
            
            # Draw the view
            draw_view(view_x, view_y, mainMap)
            
            # Check for player input
            movement = poll_key()
            
            # Handle player movement
            if movement == "q":
                cont = False
            elif movement == "w":
                player.move("up", mainMap)
            elif movement == "s":
                player.move("down", mainMap)
            elif movement == "a":
                player.move("left", mainMap)
            elif movement == "d":
                player.move("right", mainMap)
            
            # Small delay to control frame rate
            time.sleep(0.03)
    
    finally:
        # Clean up
        stop_event.set()  # Signal all NPC threads to stop
        
        # Wait for threads to finish (with timeout)
        for thread in npc_threads:
            thread.join(timeout=0.5)
        
        ansi_show_cursor()
        ansi_move_cursor(25, 1)

if __name__ == "__main__":
    main()