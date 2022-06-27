# WindowCreator is in a very early state, everything is subject to change.

Requires PIL

WindowCreator is a python utility made to eliminate the need for a virtual machine to get an image of a error box. 
It will also be able to work as a python library for making crazy error videos.

Example errors:

![](https://i.imgur.com/3rkfdP8.png)

![](https://i.imgur.com/WyQQpy2.png)

![](https://i.imgur.com/K9qMwwP.png)

![](https://i.imgur.com/ByOzA4c.png)

![](https://i.imgur.com/CrJ1FBg.png)

[And more!](examples.md)

The main file is generate.py, open it in an editor because in its current state, it's just a function dump where you have to go to the end of the file and put what window generating function you want. 
There are examples in the comments at the bottom, just uncomment any line and see the result.

## Currently supported operating systems:
* Windows XP
* Mac OS 9
* Windows 7
* Windows 3.1

# Todo:
## Windows XP
* Implement 7's list button system
* Fix window borders so they match the original
* Add title icons
* Implement inactive window
* Button pressing and interactions
## Mac OS 9
* Implement 7's list button system
* Add the rest of window types
* Implement inactive window
* Button pressing and interactions
## Windows 7
* Look into how dwm animates the window and implement that instead of the placeholder method
* A whole compositing function with
   * Aero blur
   * Aero afterglow
   * and more...
* Add TaskDialog implementation
* Inactive windows
* Button pressing and interactions
## Windows 3.1
* Make the titlebar-less error (the one that is really big and appears in the center of the screen) 

## Future OS's
* Ubuntu (10.04 and a couple others)
* Windows 95,98,2000
* Windows Vista
* Windows 8

Windows 10 and 11 are not planned to be supported
