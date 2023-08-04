import pygame
import numpy as np
import time
import argparse

def makeArgs():
    parser = argparse.ArgumentParser(prog="Conway's Game of Life",
                                     description="Running without file input produces blank grid, clicking on a cell will activate it.\n"
                                                 "Hotkeys: Space = start/pause, r = reset, s = save (will ask for filename in terminal)",
                                     epilog="Some combinations of arguments will cause it to not work, understand what you are doing before specifying")

    parser.add_argument("-p", "--preset", type=str, help="Chose premade configurations from conway's chiren file")
    parser.add_argument("-d", "--dimensionality", type=int, help="Sets dimensionality of grid, usually unneccessary to change unless making new designs")
    parser.add_argument("-c", "--cell-size", type=int, help="Sets cell size in pixels")
    parser.add_argument("-s", "--speed", type=int, help="Sets tick speed in Hz")

    arguments = parser.parse_args()

    if arguments.cell_size is not None:
        global cellSize
        cellSize = arguments.cell_size
    if arguments.dimensionality is not None:
        global dimmo
        dimmo = arguments.dimensionality
    if arguments.preset is not None:
        global file
        global setto
        file = savePath + arguments.preset + ".txt"
        setto = True
        print(file, setto)
    if arguments.speed is not None:
        global tickSpeed
        tickSpeed = arguments.speed

tickSpeed = 15
setto = False
file = ""
dimmo = 50
cellSize = 10
savePath = r"conways chiren/"

makeArgs()

print(cellSize)

gridL, gridH = dimmo, dimmo

backColor = (102, 51, 153)
activeColor = (255, 128, 0)

screenHeight = gridL * cellSize
screenLength = gridH * cellSize

gridState = np.zeros((gridL, gridH), dtype=bool)
colors = np.zeros((gridL, gridH, 3), dtype=np.uint8)
prevStates = np.zeros((gridL, gridH), dtype=bool)

playingGame = False

pygame.init()
screen = pygame.display.set_mode((screenHeight, screenLength))
clock = pygame.time.Clock()
pygame.display.set_caption("It's The Food Hoe")

mousePressed = False
prevXCell = None
prevYCell = None

running = True

def toggleColor(x, y):
    gridState[y, x] = not gridState[y, x]
    if gridState[y, x]:
        colors[y, x] = activeColor
    else:
        colors[y, x] = backColor

def drawCells():
    for y in range(gridH):
        for x in range(gridL):
            if gridState[y, x]:
                color = colors[y, x]
                pygame.draw.rect(screen, color, (x * cellSize, y * cellSize, cellSize, cellSize))

def drawLines():
    for x in range(0, screenLength, cellSize): #start, stop, stepsize
        pygame.draw.line(screen, (0,0,0), (x, 0), (x, screenLength)) # surface, color, startPos, endPos
    for y in range(0, screenHeight, cellSize):
        pygame.draw.line(screen, (0,0,0), (0, y), (screenHeight, y))

def setConfig(file, xoffset=0, yOffset=0):
    pattern = np.loadtxt(file, delimiter=',')

    initialConfig = np.zeros((gridL, gridH), dtype=bool)

    for y in range(len(pattern)):
        for x in range((len(pattern))):
            initialConfig[y+yOffset, x+xoffset] = pattern[y][x]
    return initialConfig

def setInitial(file):
    initConfig = setConfig(file)
    gridState[:initConfig.shape[0], :initConfig.shape[1]] = initConfig # grid state for index up to length/width of loaded array

#setInitial((savePath+"gosper.txt"))
if setto:
    setInitial(file)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            xCell = mouseX // cellSize
            yCell = mouseY // cellSize
            mousePressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mousePressed = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playingGame = not playingGame
            elif event.key ==pygame.K_s:
                filename = input("Enter File To Save As ===> ")
                np.savetxt((savePath+filename+".txt"), gridState, fmt="%d", delimiter=',')
            elif event.key ==pygame.K_r:
                gridState = np.zeros((gridL, gridH), dtype=bool)


    screen.fill(backColor)

    drawCells()
    drawLines()

    if mousePressed and not playingGame:
        mouseX, mouseY = pygame.mouse.get_pos()
        xCell = mouseX // cellSize
        yCell = mouseY // cellSize

        if (xCell < 0 or xCell >= gridL) or (yCell < 0 or yCell >= gridH):
            continue

        if (xCell, yCell) != (prevXCell, prevYCell):
            # Update the cell state and color only if the mouse cell position has changed
            newState = not prevStates[yCell, xCell]
            if newState != prevStates[yCell, xCell]:
                toggleColor(xCell, yCell)
                prevStates[yCell, xCell] = newState

            # Update the previous mouse cell position
            prevXCell, prevYCell = xCell, yCell

    if playingGame:
        nextState = np.zeros((gridL, gridH), dtype=bool)
        for x in range(gridL):
            for y in range(gridH):
               # print(x, y)
                lifeScore = gridState[max(0,y-1):min(y+2, gridH), max(0, x-1):min(x+2, gridL)].sum() - gridState[y, x]
                #print(f"Score for {y}, {x} is {live}")
                if (int(lifeScore) == 2 and gridState[y, x]) or int(lifeScore) == 3:
                    #print(f"{live} Stays Alive S")
                    nextState[y, x] = True
                    colors[y, x] = activeColor
                else:
                   # print("Dead")
                    nextState[y, x] = False
                    colors[y, x] = backColor

       # print(nextState)
        gridState = nextState



    pygame.display.update()
    pygame.display.flip()
    clock.tick(tickSpeed)


screen.fill(backColor)
pygame.quit()