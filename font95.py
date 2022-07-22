from PIL import ImageGrab, Image, ImageDraw, ImageChops
from time import *
import pyperclip
#keyboard = PyKeyboard()
from pynput.keyboard import Key, Controller, KeyCode
#import keyboard
#import keyboard._winkeyboard as _os_keyboard

#Coordinates of the top left corner of the selected text.
_X = 655
_Y = 396
keys = """ 1'3457'908=,-./0123456789;;,=./2abcdefghijklmnopqrstuvwxyz[\]6-`abcdefghijklmnopqrstuvwxyz[\]`"""
shif = """ @@@@@@ @@@@              @ @ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@                           @@@@"""
keyboard = Controller()
chars = ""
for i in range(32,127):
    chars += chr(i)
print(chars)
index = 0
#entries = _os_keyboard.map_name(normalize_name(":"))
#print(entries)
#scan_code, modifiers = next(iter(entries))
#print(scan_code)
#print(modifiers)
#print(KeyCode.from_char("$"))
sleep(1.5)
for i in keys:
    #pyperclip.copy(i)
    if shif[index] == "@":
        keyboard.press(Key.shift)
    keyboard.tap(i)
    if shif[index] == "@":
        keyboard.release(Key.shift)
    #keyboard.press(Key.ctrl)
    #keyboard.press('v')
    #keyboard.release('v')
    #keyboard.release(Key.ctrl)
    #sleep(0.02)
    #keyboard.press(Key.left)
    #keyboard.release(Key.left)
    sleep(0.01)
    keyboard.press(Key.shift)
    keyboard.press(Key.left)
    sleep(0.04)
    keyboard.release(Key.left)
    keyboard.release(Key.shift)
    #keyboard.write(i)
    #keyboard.press_and_release('ctrl+a')
    #sleep(0.01)
    screenshot = ImageGrab.grab()
    screenshotcrop = screenshot.crop((_X,_Y,1920,1080))
    keyboard.press(Key.backspace)
    keyboard.release(Key.backspace)
    #keyboard.press_and_release('backspace')
    #sleep(0.1)
    pixels = screenshotcrop.load()
    width = 0
    height = 0
    for y in range(25):
        for x in range(20):
            if (pixels[x,y] != (255,255,255)) and (x)>width:
                width = x
    for x in range(20):
        for y in range(25):
            if (pixels[x,y] != (255,255,255)) and (y)>height:
                height = y
    width += 1
    height += 1
    screenshotfinal = screenshotcrop.crop((0,0,width,height)).convert("RGBA")
    #screenshotfinal.show()
    #screenshotfinalwhite = Image.new("RGBA",(width,height),(0,0,0,255))
    pixels = screenshotfinal.load()
    #pixelswhite = screenshotfinalwhite.load()
    """for x in range(width):
        if(x == 0):
            for y in range(height):
                #pixelswhite[x,y] = (255,255,255,255-pixels[x,y][1])
                pixels[x,y] = (255,255,255,pixels[x,y][0])
        else:
            for y in range(height):
                #pixelswhite[x,y] = (255,255,255,pixels[x,y][1])
                pixels[x,y] = (255,255,255,255-pixels[x,y][0])"""
    #for x in range(width):
    #    for y in range(height):
    #        pixels[x,y] = (255,255,255-pixels[x,y][2],255)
    w = Image.new("L",(width,height),255)
    invert = Image.new("RGBA",(width,height),(255,255,0,0))
    drawline = ImageDraw.Draw(invert)
    drawline.rectangle((0,0,1,height),fill=(0,0,255,0))
    screenshotfinal = ImageChops.difference(invert,screenshotfinal)
    r,g,b,a = screenshotfinal.split()
    screenshotfinal = Image.merge("RGBA",(w,w,w,r))

    screenshotfinal.save(".\\95\\fonts\\caption\\"+str(index+32)+".png","PNG")  #above but vice versa
    index += 1
    #print(invert.size)
    #print(screenshotfinal.size)
    #invert.show()
    #screenshotfinal.show()"""
    #break
        
