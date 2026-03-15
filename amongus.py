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

#variables
y = 1
x = 1
cont = True
xrange = range(8)
yrange = range(8)

#functions 
def viewpoint(direction):
    # check direction | check we could move the range | check if centered
    if direction == "up" and yrange[0] != 0 and (yrange[0]+3 == y or yrange[0]+4 == y):
        for index in range(8):
            yrange[index] = yrange[index] - 1
    elif direction == "down" and yrange[7] != len(mainMap)-1 and (yrange[0]+3 == y or yrange[0]+4 == y):
        for index in range(8):
            yrange[index] = yrange[index] + 1
    elif direction == "left" and xrange[0] != 0 and (xrange[0]+3 == y or xrange[0]+4 == y):
        for index in range(8):
            xrange[index] = xrange[index] - 1
    elif direction == "right" and xrange[7] != len(mainMap[0])-1 and (xrange[0]+3 == y or xrange[0]+4 == y):
        for index in range(8):
            xrange[index] = xrange[index] + 1


while cont:
    #initializing the map
    for ya in yrange:
        for xa in xrange:
            print(mainMap[ya][xa], end=" ")
        print("")
    #waiting for input
    movement = input()
    #basic movement
    if movement == "w" and y > 0 and mainMap[y-1][x] == " ":
        mainMap[y-1][x] = mainMap[y][x]
        mainMap[y][x] = " "
        y -= 1
        viewpoint("up")
    elif movement == "a" and x > 0 and mainMap[y][x-1] == " ":
        mainMap[y][x-1] = mainMap[y][x]
        mainMap[y][x] = " "
        x -= 1
        viewpoint("left")
    elif movement == "s" and y < 7 and mainMap[y+1][x] == " ":
        mainMap[y+1][x] = mainMap[y][x]
        mainMap[y][x] = " "
        y += 1
        viewpoint("down")
    elif movement == "d" and x < 7 and mainMap[y][x+1] == " ":
        mainMap[y][x+1] = mainMap[y][x]
        mainMap[y][x] = " "
        x += 1
        viewpoint("right")
    elif movement == "q":
        cont = False
