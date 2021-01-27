from pyautogui import *
import pyautogui,time,sys,keyboard,random,win32api,win32con,numpy

def check_position_screen():
    print('press ctrl+c to stop')
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')

#check_position_screen() 165 250 165 430 1 block = 105
pyautogui.displayMousePosition()