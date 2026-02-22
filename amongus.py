#Among us CLI 8x8 grid - autoupdating
mainMap = [
    ["-","-","-","-","-","-","-","-"],
    ["-","-","-","-","-","-","-","+"],
    [" "," "," "," "," "," "," ","|"],
    [" "," "," "," "," "," "," ","|"],
    [" "," "," "," "," "," "," ","|"],
    [" "," "," "," "," "," "," ","|"],
    [" "," "," "," "," "," "," ","|"],
    ["+","🟥","+","-","-","-","-","+"]
    ]

y = 7
x = 1
cont = True;


while cont:
    #prints out map
    for level in range(len(mainMap)):
        for dash in mainMap[level]:
            print(dash, end=" ")
        print("")
    #waiting for input
    movement = input()
    
    #basic movement
    if movement == "w" and y > 0 and mainMap[y-1][x] == " ":
        mainMap[y-1][x] =  mainMap[y][x]
        mainMap[y][x] = " "
        y -= 1
    elif movement == "a" and x > 0 and mainMap[y][x-1] == " ":
        mainMap[y][x-1] =  mainMap[y][x]
        mainMap[y][x] = " "
        x -= 1
    elif movement == "s" and y < 7 and mainMap[y+1][x] == " ":
        mainMap[y+1][x] =  mainMap[y][x]
        mainMap[y][x] = " "
        y += 1
    elif movement == "d" and x < 7 and mainMap[y][x+1] == " ":
        mainMap[y][x+1] =  mainMap[y][x]
        mainMap[y][x] = " "
        x += 1
    elif movement == "q":
        cont = False
    

