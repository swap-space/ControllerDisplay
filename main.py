import pygame
import serial
import json
from pygame.locals import *

def loadJson():
    buttons = []
    with open('config.json') as jsonFile:
        j = json.load(jsonFile)

        serialPort = str(j['port'])
        buttonDefs = j['buttons']
        for d in buttonDefs:
            buttons.append((str(d['name']), int(d['x']), int(d['y'])))

        controllerImage = pygame.image.load(str(j['controllerImage']))
        selectedImage = pygame.image.load(str(j['selectedImage']))
        borderSize = int(j['border'])

    return buttons, controllerImage, selectedImage, borderSize, serialPort

pygame.init()

buttons, controllerImage, selectedImage, borderSize, serialPort = loadJson()

windowSize = (controllerImage.get_width() + 2*borderSize, controllerImage.get_height() + 2*borderSize)
windowSurface = pygame.display.set_mode(windowSize, pygame.NOFRAME, 32)

def buttonPosition(key):
    pos = buttons[key]
    return pos[1] + borderSize, pos[2] + borderSize

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG = (255, 0, 255) 

with serial.Serial(serialPort, 250000, timeout=0.05) as ser:
    while True:
        fCount = 0
        char = ser.read()
        while fCount < 2:
            if char == b'F':
                fCount = fCount + 1
                
            if fCount >= 2:
                break

            char = ser.read()

        b = ser.read(2)
        intVal = (b[1]<<8) + b[0]

        # Uncomment the line below to make setup easier.
        # It will cause the settings to be reloaded every loop.
        # It's computationally expensive but makes adjustment far easier

        # buttons, _, _, _, _ = loadJson()

        windowSurface.fill(BG)
        windowSurface.blit(controllerImage, (borderSize, borderSize))

        buttonStates = {}
        for i in range(12):
            buttonDef = buttons[i]
            buttonStates[buttonDef[0]] = intVal & (1 << i) is not 0
            if buttonStates[buttonDef[0]]:
                windowSurface.blit(selectedImage, buttonPosition(i))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
