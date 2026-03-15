#Among us CLI 8x8 grid - autoupdating
mainMap = [
    list("+----------------------+----------------------+----------------------+"),
    list("|C                     |                      |                      |"),
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

# variables
y = 1
x = 1
cont = True

# top-left corner of the 8x8 viewport
view_x = 0
view_y = 0


def viewpoint(direction):
    #refers global variables and ensures changes made to them
    global view_x, view_y, x, y

    #vertical camera movement (if the y is not within the view bounds, we shift the bounds)
    if y < view_y + 3:
        view_y = max(0, y - 3)
    elif y > view_y + 4:
        view_y = min(len(mainMap) - 8, y - 4)

    #horizontal camera movement
    if x < view_x + 3:
        view_x = max(0, x - 3)
    elif x > view_x + 4:
        view_x = min(len(mainMap[0]) - 8, x - 4)


while cont:
    #initialize 8x8 viewpoint
    print("&&&&&&&&&&&&&&&&&&&&")
    for ya in range(view_y, view_y + 8):
        for xa in range(view_x, view_x + 8):
            print(mainMap[ya][xa], end=" ")
        print()

    movement = input()

    #check: movement type | we can move | empty space
    if movement == "w" and y > 0 and mainMap[y - 1][x] == " ":
        mainMap[y - 1][x] = mainMap[y][x]
        mainMap[y][x] = " "
        y -= 1
        viewpoint("up")

    elif movement == "a" and x > 0 and mainMap[y][x - 1] == " ":
        mainMap[y][x - 1] = mainMap[y][x]
        mainMap[y][x] = " "
        x -= 1
        viewpoint("left")

    elif movement == "s" and y < len(mainMap) - 1 and mainMap[y + 1][x] == " ":
        mainMap[y + 1][x] = mainMap[y][x]
        mainMap[y][x] = " "
        y += 1
        viewpoint("down")

    elif movement == "d" and x < len(mainMap[0]) - 1 and mainMap[y][x + 1] == " ":
        mainMap[y][x + 1] = mainMap[y][x]
        mainMap[y][x] = " "
        x += 1
        viewpoint("right")

    elif movement == "q":
        cont = False