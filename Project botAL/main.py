from pyautogui import *
import pyautogui,time,sys,keyboard,random,win32api,win32con,numpy,math,cv2
from win32gui import FindWindow, GetWindowRect



def click_point(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def move_click(x,y,duration=0.3):
    tween = (pyautogui.easeInQuad,pyautogui.easeInOutQuad,pyautogui.easeInBounce,pyautogui.easeInElastic)
    pyautogui.moveTo(x, y, random.uniform(0.1,duration),random.choice(tween))
    pyautogui.click()

def move_click_center(pos,duration=0.5):
    tween = (pyautogui.easeInQuad,pyautogui.easeInOutQuad,pyautogui.easeInBounce,pyautogui.easeInElastic)
    pyautogui.moveTo(pos, random.uniform(0.1,duration),random.choice(tween))
    pyautogui.click()

def rand_click_inrectangle(x,y,w,h,duration=0.5):
    tween = (pyautogui.easeInQuad,pyautogui.easeInOutQuad,pyautogui.easeInBounce,pyautogui.easeInElastic)
    pyautogui.moveTo(random.randint(x,w), random.randint(y,h), random.uniform(0.1,duration),random.choice(tween))
    pyautogui.click()

def detec_ship(name1,name2=None,name3=None):
    global distance_to_boss,distance_to_ship,find,min_delta,unreach
    g_ship = []
    ship = []
    ship1 = list(pyautogui.locateAllOnScreen(f'{path}{name1}',grayscale=True,confidence=0.8,region=region))
    ship = ship1
    if name2 != None :
        ship2 = list(pyautogui.locateAllOnScreen(f'{path}{name2}',grayscale=True,confidence=0.8,region=region))
        ship = ship1 + ship2
        if name3 != None :
            ship3 = list(pyautogui.locateAllOnScreen(f'{path}{name3}',grayscale=True,confidence=0.8,region=region))
            ship = ship1 + ship2 + ship3

    
    if len(ship) > 1 :
        rectList, _ = cv2.groupRectangles(numpy.array(ship).tolist(), 1, 0.2)
        g_ship = rectList
    else:
        g_ship = ship

    for n in range (0,len(g_ship)):
        x, y, w, h = g_ship[n]
        distance_to_boss = math.sqrt(((x-x_b)**2)+((y-y_b)**2))

        if distance_to_boss <= min_delta:
            min_delta = distance_to_boss
            find = n
    
    try:
        x = g_ship[find] 
    except:
        print('',end='')
    else:
        x, y, w, h = g_ship[find]
        rand_click_inrectangle(x,y,x+w,y+h)
        if pyautogui.locateAllOnScreen(f'{path}unreachable.png',grayscale=True,confidence=0.8,region=region) != None :
            g_ship = numpy.delete(g_ship, find)
            detec_ship(name1,name2=None,name3=None)
        else:
            time.sleep(2)


def detec_ship_event(name1,name2,name3):
    global distance_to_boss,find,min_delta
    g_ship = []
    ship = []
    ship1 = list(pyautogui.locateAllOnScreen(f'{path}{name1}',grayscale=True,confidence=0.8,region=region))
    if name2 != None :
        ship2 = list(pyautogui.locateAllOnScreen(f'{path}{name2}',grayscale=True,confidence=0.8,region=region))
    if name3 != None :
        ship3 = list(pyautogui.locateAllOnScreen(f'{path}{name3}',grayscale=True,confidence=0.8,region=region))

    ship = ship1 + ship2 + ship3
    print(ship)

    if len(ship) > 1 :
        rectList, _ = cv2.groupRectangles(numpy.array(ship).tolist(), 1, 0.2)
        g_ship = rectList
    else:
        g_ship = ship
    
    print(g_ship)
    for n in range (0,len(g_ship)):
        x, y, w, h = g_ship[n]
        distance_to_boss = math.sqrt(((x-x_b)**2)+((y-y_b)**2))
        distance_to_ship = math.sqrt(((x-x_c)**2)+((y-y_c)**2))
        deltaship = abs(distance_to_ship - distance_to_boss)

        if deltaship <= min_delta:
            min_delta = deltaship
            find = n
    
    
    x, y, w, h = g_ship[find]
    distance_to_ship = math.sqrt(((x-x_c)**2)-((y-y_c)**2))

    if distance_to_ship // 105 > 5 :
        tile = distance_to_ship // 105
        n = tile - 5 
        limit_x = (5*x+n*x_c)/tile
        limit_y = (5*y+n*y_c)/tile
        rand_click_inrectangle(limit_x,limit_y,limit_x+w,limit_y+h)
        time.sleep(3)
    else :
        rand_click_inrectangle(x,y,x+w,y+h)
        time.sleep(2)
    
def find_rand_click(name,duration=0.5):
    if pyautogui.locateOnScreen(f'{path}{name}',grayscale=True,confidence=0.8,region=region) != None:
            x,y,w,h = pyautogui.locateOnScreen(f'{path}{name}',grayscale=True,confidence=0.8,region=region)
            rand_click_inrectangle(x,y,x+w,y+h,duration)
            time.sleep(0.3)

def find_center(name):
    locate = pyautogui.locateCenterOnScreen(f'{path}{name}',grayscale=True,confidence=0.8,region=region)
    return locate

def find_rec(name):
    locate = pyautogui.locateOnScreen(f'{path}{name}',grayscale=True,confidence=0.8,region=region)
    return locate
path = 'C:\\Users\\Admin\\Desktop\\cd\\Project botAL\\'

#boss_coor
boss_coordinate = (900,430)
x_b,y_b = boss_coordinate


#start
print('start',end='')
for n in range(0,5):
    print('.',end='')
    time.sleep(0.3)
print('go')




while keyboard.is_pressed('q') == False:
    
    #boss_coor
    boss_coordinate = (900,430)
    x_b,y_b = boss_coordinate
    distance_to_boss = 0
    distance_to_ship = 0
    current_locate =[]
    min_delta = 0
    find = int()
    unreach = []

    # FindWindow takes the Window Class name (can be None if unknown), and the window's display text. 
    while True:
        if FindWindow(None, 'NoxPlayer') != None :
            window_handle = FindWindow(None, 'NoxPlayer')
            window_rect   = GetWindowRect(window_handle)
            x_r,y_r,w_r,h_r = window_rect 
            if x_r >= 0:
                region = (x_r+4,y_r+33,w_r-4,h_r-4)
                break
            else :
                time.sleep(0.5)


    # start if see logo
    '''
    if pyautogui.locateOnScreen("C:\\Users\\Admin\\Desktop\\cd\\Project botAL\\Al logo.png",grayscale=True,confidence=0.8) != None:
        move_click(836,304,2)
    #login
        if pyautogui.locateOnScreen('logo.png',grayscale=True,confidence=0.8) != None:
            move_click(880,435,1)
            if pyautogui.locateOnScreen('Exit.png',grayscale=True,confidence=0.8) != None:
                move_click(897,88,1)
            if pyautogui.locateOnScreen('next.png',grayscale=True,confidence=0.8) != None:
                move_click(407,387,2)
                #home
                if pyautogui.locateOnScreen('home.png',grayscale=True,confidence=0.8) != None:
                    move_click(942,50,2)

    #mainscreen
    #check resouce
    if pyautogui.pixel(32,143)[0] == 183: #red 183
        rand_click_inrectangle(8,137,24,170)
        time.sleep(1)
        if pyautogui.pixel(327,232)[0] == 35: #red 35   #check oil
            rand_click_inrectangle(152,159,185,190)
            time.sleep(1)
        if pyautogui.pixel(293,164)[0] == 255: #red 255 #check coin 
            rand_click_inrectangle(280,159,313,190)
            time.sleep(1)

        #check comission
        if  pyautogui.pixel(183,267)[0] == 249:
            rand_click_inrectangle(294,233,376,256)
            time.sleep(1)
        elif :
        #check classroom
        if  pyautogui.pixel(287,346)[0] == 209:
            rand_click_inrectangle(294,340,376,363)
            time.sleep(1)
        #check Lab
        if  pyautogui.pixel(287,418)[0] == 205:
            rand_click_inrectangle(294,447,334,470)
            time.sleep(1)
    '''
    #auto do
    
    find_rand_click('tap_continue.png')
    find_rand_click('confirm.png')
    find_rand_click('GO.png')
    find_rand_click('GO!.png')
    find_rand_click('touch_continue.png')
    find_rand_click('win.png')
    find_rand_click('elite.png')

    

    # current to locate is y = 180
    if pyautogui.locateCenterOnScreen(f'{path}current locate.png',grayscale=True,confidence=0.8,region=region) != None :
        try:
            current = pyautogui.locateCenterOnScreen(f'{path}current locate.png',grayscale=True,confidence=0.8,region=region)
            x,y = current
        except:
            print('',end='')
        else:
            current_locate = (x,y-180)
            x_c,y_c = current_locate

    else:
        find_rand_click('switch.png')

    #loop battle stage
    stage = 'stage 3-4.png'

    if pyautogui.locateOnScreen(f'{path}{stage}',grayscale=True,confidence=0.8,region=region) != None:
        x,y,w,h = pyautogui.locateOnScreen(f'{path}{stage}',grayscale=True,confidence=0.8,region=region)
        rand_click_inrectangle(x,y,x+w,y+h)
    
    # retire full inventory if find sort pop up
    if pyautogui.locateCenterOnScreen(f'{path}sort.png',grayscale=True,confidence=0.8,region=region) != None:
        x,y,w,h = pyautogui.locateOnScreen(f'{path}sort.png',grayscale=True,confidence=0.8,region=region)
        rand_click_inrectangle(x,y,x+w,y+h)
        time.sleep(1)
        loop_start = True
        #loop to find quick retire
        while loop_start:
            print('in loop')
            if find_center('quick retire.png') != None:
                x,y,w,h = find_rec('quick retire.png')
                rand_click_inrectangle(x,y,x+w,y+h)
                time.sleep(2)
                if find_center('confirm_b.png') != None:
                    x,y,w,h = find_rec('confirm_b.png')
                    rand_click_inrectangle(x,y,x+w,y+h)
                    time.sleep(2)

                    #confirm and back to battle
                    if find_center('confirm_r.png') != None:
                        x,y,w,h = find_rec('confirm_r.png')
                        rand_click_inrectangle(x,y,x+w,y+h)

                    get_back = True

                    while get_back:
                        find_rand_click('tap_continue.png')
                        find_rand_click('disassemble.png')
                        if find_center('confirm_b.png') != None :
                            x, y, w, h = find_rec('confirm_b.png')
                            rand_click_inrectangle(x,y,x+w,y+h)
                            time.sleep(1)
                            back = True
                            while back:
                                if find_center('back.png') != None:
                                    x,y,w,h = find_rec('back.png')
                                    rand_click_inrectangle(x,y,x+w,y+h)
                                    time.sleep(1)
                                    get_back = False
                                    back = False

                    loop_start = False
    

    #if see battle botton
    if pyautogui.locateOnScreen(f'{path}battle.png',grayscale=True,confidence=0.8,region=region) == None :

        if pyautogui.locateCenterOnScreen(f'{path}boss.png',grayscale=True,confidence=0.8,region=region) != None:
            x,y,w,h = pyautogui.locateOnScreen(f'{path}boss.png',grayscale=True,confidence=0.8,region=region)
            rand_click_inrectangle(x,y,x+w,y+h)
            time.sleep(2)
            if pyautogui.locateAllOnScreen(f'{path}unreachable.png',grayscale=True,confidence=0.8,region=region) != None:
                detec_ship('ship_bs.png','ship_cv.png','ship_cl.png')
        else:
            detec_ship('ship_bs.png','ship_cv.png','ship_cl.png')

    elif pyautogui.locateOnScreen(f'{path}battle.png',grayscale=True,confidence=0.8,region=region) != None :
        if pyautogui.locateOnScreen(f'{path}battle.png',grayscale=True,confidence=0.8,region=region) != None :
            x,y,w,h = pyautogui.locateOnScreen(f'{path}battle.png',grayscale=True,confidence=0.8,region=region)
            rand_click_inrectangle(x,y,x+w,y+h)
    
     
print('Exit')

