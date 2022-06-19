from PIL import Image, ImageFont, ImageDraw, ImageMath,ImageChops, ImageOps
from math import ceil,floor



#_IMAGE = Image.new("RGBA", (200,100), (255,255,255,255))

#  the put() command pastes an image onto a canvas where the given x,y coordinates dictate where the (0,0) point of the image should go.
#  alignment is a 2 character string that holds two numbers ranging from 0 to 2 (inclusive)
#  it dictates what point on the image should be (0,0) and put exactly where the coordinates given say
#
#     "00"--------"10"--------"20"
#      |           |            |
#      |           |            |
#      |           |            |
#     "01"--------"11"--------"21"
#      |           |            |
#      |           |            |
#      |           |            |
#     "02"--------"12"--------"22"
#
#   here is a diagram showing a rectangular image and its alignment points
#   if we chose "11" as the alignment point, it would become the (0,0) of the image. and if the x,y coordinates were width/2,height/2 of the canvas, the image would be put exactly in the center of the canvas
#   this would not work if the alignment point would be "00"
#
#
#     +-----------------------------------CANVAS-----------------------------------+
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                    "00"---IMAGE----+                       |       using "00"(default) as the alignment point
#     |                                     |              |                       |
#     |                                     |              |                       |
#     |                                     |              |                       |
#     |                                     |              |                       |
#     |                                     |              |                       |
#     |                                     +--------------+                       |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     +----------------------------------------------------------------------------+
#
#
#
#
#
#
#     +-----------------------------------CANVAS-----------------------------------+
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                              +----IMAGE-----+                              |
#     |                              |              |                              |
#     |                              |              |                              |
#     |                              |     "11"     |                              |       using "11" as the alignment point
#     |                              |              |                              |
#     |                              |              |                              |
#     |                              +--------------+                              |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     |                                                                            |
#     +----------------------------------------------------------------------------+
#
#     notice how the alignment point stays in the same place on the canvas, but the whole image doesnt.
#
#
def put(canvas, image,a,b,alignment="00"):
    canvas.alpha_composite(image,(int(a)-( image.size[0] * int(alignment[0]) // 2 ),int(b)-( image.size[1] * int(alignment[1]) // 2) ) )
    return canvas
def put7(canvas, image, a, b, alignment = "00"):  #this is the same as put(), but using windows's weird transparency algorithm. ImageRGB+(BackgroundRGB*ImageAlpha).   this assumes that background alpha is 1(fully opaque), i haven't figured out what it does on a transparent background
    x = int(a)-( image.size[0] * int(alignment[0]) // 2 )
    y = int(b)-( image.size[1] * int(alignment[1]) // 2 )
    cr, cg, cb, ca = canvas.crop((x,y,x+w(image),y+h(image))).split()
    ir, ig, ib, ia = image.split()
    r = ImageMath.eval("convert(  c+(b*(255-a)/255) ,'L')",c=ir,b=cr,a=ia)
    g = ImageMath.eval("convert(  c+(b*(255-a)/255) ,'L')",c=ig,b=cg,a=ia)
    b = ImageMath.eval("convert(  c+(b*(255-a)/255) ,'L')",c=ib,b=cb,a=ia)
    canvas.paste(Image.merge("RGBA",(r,g,b,ca)),(x,y))
    return canvas
#def ApplyRules(rules,width,height,
def h(img):  #get the height
    return img.size[1]
def w(img):  #get the width
    return img.size[0]
def cropx(img,a,b):  #crop but only x
    return img.crop((a,0,b,h(img)))
def cropy(img,a,b):  #crop but only y
    return img.crop((0,a,x(img),b))

def createtext(text,fontdirectory,color=(255,255,255,255), buffersize=(1000,1000)):
    drawntext = Image.new("RGBA",buffersize,(255,127,127,0))
    width = 0
    height = 0
    line = 0
    cursorpos = 0
    newlinesizefile = open(fontdirectory+"newlinesize.txt")
    newlinesize = int(newlinesizefile.read())
    newlinesizefile.close()
    for i in text:
        if(i=="\n"):
            height += newlinesize
            line += newlinesize
            cursorpos = 0
            continue
        char = Image.open(fontdirectory+str(ord(i))+".png").convert("RGBA")
        whitechar = Image.open(fontdirectory+"white"+str(ord(i))+".png").convert("RGBA")
        cred, cgreen, wcblue, calpha = char.split()
        wcred, wcgreen, cblue, wcalpha = whitechar.split()
        alpha2 = ImageMath.eval("convert( int( (r1-r2+255+g1-g2+255+b1-b2+255)/3*alp/255 ), 'L')",r1 = cred,r2 = wcred,b1 = cblue,b2 = wcblue,g1 = cgreen,g2 = wcgreen, alp = (color[3]))
        r = Image.new("L",(w(char),h(char)),color[0])
        g = Image.new("L",(w(char),h(char)),color[1])
        b = Image.new("L",(w(char),h(char)),color[2])
        char = Image.merge("RGBA",(r,g,b,alpha2))
        drawntext.paste(char,(cursorpos,line))
        cursorpos +=w(char)
        width = max(width,cursorpos)
        height = max(height,h(char))
    return drawntext.crop((0,0,width,height))
def createtextmac(text,fontdirectory,color=(0,0,0,255), buffersize=(1000,1000)):
    drawntext = Image.new("RGBA",buffersize,(255,127,127,0))
    width = 0
    height = 0
    line = 0
    cursorpos = 0
    newlinesizefile = open(fontdirectory+"newlinesize.txt")
    newlinesize = int(newlinesizefile.read())
    newlinesizefile.close()
    for i in text:
        if(i=="\n"):
            height += newlinesize
            line += newlinesize
            cursorpos = 0
            continue
        char = Image.open(fontdirectory+str(ord(i))+".png").convert("RGBA")
        colorimg = Image.new("RGBA",(w(char),h(char)),(color[0],color[1],color[2],255))
        char = ImageChops.multiply(char,colorimg)
        drawntext.paste(char,(cursorpos,line))
        cursorpos +=w(char)
        width = max(width,cursorpos)
        height = max(height,h(char))
    return drawntext.crop((0,0,width,height))
def createtext7(im,x,y,text,fontdirectory,color=(0,0,0,255), buffersize=(1000,1000),align="00", kerningadjust=0):
    drawntext = Image.new("RGBA",buffersize,(255,255,0,0))
    whitedrawntext = Image.new("RGBA",buffersize,(0,0,255,0))
    width = 0
    height = 0
    line = 0
    cursorpos = 0
    newlinesizefile = open(fontdirectory+"newlinesize.txt")
    newlinesize = int(newlinesizefile.read())
    newlinesizefile.close()
    for i in text:
        if(i=="\n"):
            height += newlinesize
            line += newlinesize
            cursorpos = 0
            continue
        char = Image.open(fontdirectory+str(ord(i))+".png").convert("RGBA")
        whitechar = Image.open(fontdirectory+"white"+str(ord(i))+".png").convert("RGBA")
        #colorimg = Image.new("RGBA",(w(char),h(char)),(color[0],color[1],color[2],255))
        #char = ImageChops.multiply(char,colorimg)
        drawntext.paste(char,(cursorpos,line))
        whitedrawntext.paste(whitechar,(cursorpos,line))
        cursorpos +=w(char)+kerningadjust
        width = max(width,cursorpos)
        height = max(height,h(char))
    drawntext = drawntext.crop((0,0,width,height))
    drawntext = put(Image.new("RGBA",(w(im),h(im)),(0,0,0,0)),drawntext,x,y,align)
    whitedrawntext = whitedrawntext.crop((0,0,width,height))
    whitedrawntext = put(Image.new("RGBA",(w(im),h(im)),(0,0,0,0)),whitedrawntext,x,y,align)
    imgcolor = Image.new("RGBA",(w(im),h(im)),color)
    c = imgcolor.split()
    ir,ig,ib,ia = im.split()
    r,g,b,a = drawntext.split()
    wr,wg,wb,wa = whitedrawntext.split()
    r = ImageMath.eval("convert( b*c/255+(255-w)*(255-c)/255 ,'L')",w=r,b=wr,c=c[0])
    g = ImageMath.eval("convert( b*c/255+(255-w)*(255-c)/255 ,'L')",w=g,b=wg,c=c[1])
    b = ImageMath.eval("convert( b*c/255+(255-w)*(255-c)/255 ,'L')",w=wb,b=b,c=c[2])
    #imgcolor.show()
    #drawntext.show()
    red = ImageMath.eval("convert( int(((i*(255-t)/255+(c*t)/255)*a/255+i*(255-a)/255)*o/255+(i*(255-o))/255) , 'L')",i=ir,t=r,c=c[0],a=a,o=c[3])   #i is the image RGB,  t is the text RGB,  c is the RGB color variable,  a is the text alpha,  o is the alpha color variable
    #ImageMath.eval("convert( int((255-t)*255/255),'L')",i=ir,t=r,c=c[0]).show()
    green = ImageMath.eval("convert( int(((i*(255-t)/255+(c*t)/255)*a/255+i*(255-a)/255)*o/255+(i*(255-o))/255) , 'L')",i=ig,t=g,c=c[1],a=a,o=c[3])
    blue = ImageMath.eval("convert( int(((i*(255-t)/255+(c*t)/255)*a/255+i*(255-a)/255)*o/255+(i*(255-o))/255) , 'L')",i=ib,t=b,c=c[2],a=a,o=c[3])
    alpha = ImageMath.eval("convert( int(((((r+g+b)/3+(255-(r+g+b)/3)*i/255))*t/255+(i*(255-t))/255)*o/255+(i*(255-o))/255) , 'L')",i=ia,r=r,g=g,b=b,t=a,o=c[3]) #i is the image alpha,  r,g,b are RGB values of the text,  t is text alpha,  o is color alpha
    result = Image.merge("RGBA",(red,green,blue,alpha))
    return result

def measuretext7(text,fontdirectory, buffersize=(1000,1000), kerningadjust=0): #this gives width and height of text using windows 7 rendering
    drawntext = Image.new("RGBA",buffersize,(255,127,127,0))
    width = 0
    height = 0
    line = 0
    cursorpos = 0
    newlinesizefile = open(fontdirectory+"newlinesize.txt")
    newlinesize = int(newlinesizefile.read())
    newlinesizefile.close()
    for i in text:
        if(i=="\n"):
            height += newlinesize
            line += newlinesize
            cursorpos = 0
            continue
        char = Image.open(fontdirectory+str(ord(i))+".png").convert("RGBA")
        #colorimg = Image.new("RGBA",(w(char),h(char)),(color[0],color[1],color[2],255))
        #char = ImageChops.multiply(char,colorimg)
        drawntext.paste(char,(cursorpos,line))
        cursorpos +=w(char)+kerningadjust
        width = max(width,cursorpos)
        height = max(height,h(char))
    return [width,height]

def resize(im,width,height,left,right,up,down,scalingmethod=Image.NEAREST):  #this resizes image but keeps margins intact. think of Unity GUI elements
    if width < w(im):
        im = im.resize((width,h(im)),scalingmethod)
        left = 1
        right = 1
    if height < h(im):
        im = im.resize((w(im),height),scalingmethod)
        up = 1
        down = 1
    result = Image.new("RGBA",(width,height),(0,0,0,0))
    tl = im.crop((0,0,left,up))
    tm = im.crop((left,0,w(im)-right,up))
    tr = im.crop((w(im)-right,0,w(im),up))
    ml = im.crop((0,up,left,h(im)-down))
    mm = im.crop((left,up,w(im)-right,h(im)-down))
    mr = im.crop((w(im)-right,up,w(im),h(im)-down))
    dl = im.crop((0,h(im)-down,left,h(im)))
    dm = im.crop((left,h(im)-down,w(im)-right,h(im)))
    dr = im.crop((w(im)-right,h(im)-down,w(im),h(im)))
    result = put(result,tl,0,0)
    result = put(result,tm.resize((width-left-right,h(tm)),scalingmethod),left,0)
    result = put(result,tr,width,0,"20")
    result = put(result,ml.resize((w(ml),height-up-down),scalingmethod),0,up)
    result = put(result,mm.resize((width-left-right,height-up-down),scalingmethod),left,up)
    result = put(result,mr.resize((w(mr),height-up-down),scalingmethod),width,up,"20")
    result = put(result,dl,0,height,"02")
    result = put(result,dm.resize((width-left-right,h(dm)),Image.NEAREST),left,height,"02")
    result = put(result,dr,width,height,"22")
    return result

def resizeanchor(im,x1,y1,x2,y2,left,right,up,down,scalingmethod=Image.NEAREST):  #this is resize, but you give it desired coordinates and it calculates the size the image should be
    return resize(im,x2-x1,y2-y1,left,right,up,down,scalingmethod)

def tile(im,width,height):    #this tiles an image
    result = Image.new("RGBA",(width,height),(0,0,0,0))
    for x in range(ceil(width/w(im))):
        for y in range(ceil(height/h(im))):
            result = put(result,im,x*w(im),y*h(im))
    return result

#the button functions return an image of a button for the OS.

def CreateXPButton(text,style=0):
    styles = ["xp/Button.png","xp/Button Hovered.png","xp/Button Clicked.png","xp/Button Disabled.png","xp/Button Default.png"]
    Button = Image.open(styles[style]).convert("RGBA")
    col = (0,0,0,255)
    if(style==3):
        col = (161,161,146,255)
    textgraphic = createtext(text,".\\xp\\fonts\\text\\",col)
    Button = resize(Button,max(w(textgraphic)+16,75),max(23,h(textgraphic)+10),8,8,9,9,Image.NEAREST)
    Button = put(Button,textgraphic,w(Button)//2-w(textgraphic)//2,5)
    return Button

def CreateMacButton(text,style=0):
    styles = ["mac/Button.png","mac/Button Disabled.png"]
    Button = Image.open(styles[style]).convert("RGBA")
    col = (0,0,0,255)
    if(style==1):
        col = (161,161,146,255)
        textgraphic = createtextmac(text,".\\mac\\fonts\\caption\\",col)
        Button = resize(Button,max(w(textgraphic)+10,60),max(20,h(textgraphic)+4),2,2,2,2,Image.NEAREST)
    else:
        textgraphic = createtextmac(text,".\\mac\\fonts\\caption\\",col)
        Button = resize(Button,max(w(textgraphic)+10,60),max(20,h(textgraphic)+4),4,4,4,4,Image.NEAREST)
    Button = put(Button,textgraphic,floor(w(Button)/2-w(textgraphic)/2),2)
    return Button

def Create7Button(text,style=0):
    styles = ["7/Button.png","","","7/Button Disabled.png","7/Button Defaulted.png","7/Button Defaulted Animation.png"]
    Button = Image.open(styles[style]).convert("RGBA")
    col = (0,0,0,255)
    #if(style==3):
    #    col = (161,161,146,255)
    #textgraphic = createtext(text,".\\7\\fonts\\text\\",col)
    textsize = measuretext7(text,"7\\fonts\\text\\",kerningadjust=-1)
    Button = resize(Button,max(textsize[0]+16,86),max(24,textsize[1]+9),3,3,3,3,Image.NEAREST)
    Button = createtext7(Button,w(Button)//2-textsize[0]//2,4,text,"7\\fonts\\text\\",kerningadjust=-1)
    return Button

def CreateXPWindow(width,height,captiontext,insideimagepath = "",erroriconpath="",errortext="",button1="",button2="",button3="",button1style=0,button2style=0,button3style=0):
    TopFrame = Image.open("xp/Frame Up Active.png").convert("RGBA")
    LeftFrame = Image.open("xp/Frame Left Active.png").convert("RGBA")
    RightFrame = Image.open("xp/Frame Right Active.png").convert("RGBA")
    BottomFrame = Image.open("xp/Frame Bottom Active.png").convert("RGBA")
    CloseButton = Image.open("xp/Close button.png").convert("RGBA")
    textposx = 15+3
    textposy = 11+h(TopFrame)
    
    captiontextwidth = w(createtext(captiontext,".\\xp\\fonts\\caption\\"))
    width = max(width,captiontextwidth+43)
    createdtext = createtext(errortext,".\\xp\\fonts\\text\\",(0,0,0,255))
    #textposy -= min(15,h(createdtext)//2)
    width = max(width,w(createdtext)+textposx+8+3)
    height = max(height,h(createdtext)+h(TopFrame)+3+25)
    print(textposy)
    if(insideimagepath != ""):
        insideimage = Image.open(insideimagepath).convert("RGBA")
        height = max(h(insideimage)+h(TopFrame)+3,height)
        width = max(width,w(insideimage)+6)
    if(erroriconpath != ""):
        erroricon = Image.open(erroriconpath).convert("RGBA")
        textposx += 15+w(erroricon)
        textposy = max(textposy,11+floor(h(erroricon)/2-h(createdtext)/2)+h(TopFrame))
        height = max(height,h(erroricon)+h(TopFrame)+3+11+11+3)
        width += 14+w(erroricon)
        
    buttonsimage = Image.new("RGBA",(0,0),(0,0,0,0))
    buttonswidth = 0
    buttonsheight = 0
    if button1 != "":
        buttonswidth += 11
        
        button1img = CreateXPButton(button1,button1style)
        #IMAGE = put(IMAGE,button1img,3+12,height-3-12,"02")
        buttonsheight = max(buttonsheight,h(button1img)+14)
        temp = Image.new("RGBA",(buttonswidth+w(button1img),buttonsheight),(0,0,0,0))
        temp = put(temp,buttonsimage,0,0)
        temp = put(temp,button1img,buttonswidth,3)
        buttonsimage = temp.copy()
        buttonswidth += w(button1img)
        if button2 != "":
            buttonswidth += 6
            button2img = CreateXPButton(button2,button2style)
            #IMAGE = put(IMAGE,button2img,3+12,height-3-12,"02")
            buttonsheight = max(buttonsheight,h(button2img)+14)
            temp = Image.new("RGBA",(buttonswidth+w(button2img),buttonsheight),(0,0,0,0))
            temp = put(temp,buttonsimage,0,0)
            temp = put(temp,button2img,buttonswidth,3)
            buttonsimage = temp.copy()
            buttonswidth += w(button2img)
            if button3 != "":
                buttonswidth += 6
                button3img = CreateXPButton(button3,button3style)
                #IMAGE = put(IMAGE,button2img,3+12,height-3-12,"02")
                buttonsheight = max(buttonsheight,h(button3img)+14)
                temp = Image.new("RGBA",(buttonswidth+w(button3img),buttonsheight),(0,0,0,0))
                temp = put(temp,buttonsimage,0,0)
                temp = put(temp,button3img,buttonswidth,3)
                buttonsimage = temp.copy()
                buttonswidth += w(button3img)
        width = max(width,buttonswidth+12)
        height += buttonsheight
    #buttonswidth.show()
    
    width = max(66,width)
    IMAGE = Image.new("RGBA", (width,height), (236,233,216,0))
    #IMAGE = put(IMAGE,cropx(TopFrame,0,27),0,0,"00")
    #IMAGE = put(IMAGE,cropx(TopFrame,28,31).resize((width-w(TopFrame)+4,h(TopFrame)),Image.NEAREST),27,0,"00")
    #IMAGE = put(IMAGE,cropx(TopFrame,31,w(TopFrame)),width,0,"20")
    IMAGE = put(IMAGE,resize(TopFrame,width,h(TopFrame),28,35,9,17,Image.NEAREST),0,0)
    IMAGE = put(IMAGE,LeftFrame.resize((3,height-h(TopFrame)-3),Image.NEAREST),0,h(TopFrame),"00")
    IMAGE = put(IMAGE,RightFrame.resize((3,height-h(TopFrame)-3),Image.NEAREST),width,h(TopFrame),"20")
    IMAGE = put(IMAGE,cropx(BottomFrame,0,5).resize((5,3),Image.NEAREST),0,height,"02")
    IMAGE = put(IMAGE,cropx(BottomFrame,4,w(BottomFrame)-5).resize((width-10,3),Image.NEAREST),5,height,"02")
    IMAGE = put(IMAGE,cropx(BottomFrame,w(BottomFrame)-5,w(BottomFrame)).resize((5,3),Image.NEAREST),width,height,"22")
    IMAGE = put(IMAGE,Image.new("RGBA", (width-6,height-3-h(TopFrame)), (236,233,216,255)),3,h(TopFrame),"00")
    IMAGE = put(IMAGE,CloseButton,width-5,5,"20")
    IMAGE = put(IMAGE,createtext(captiontext,".\\xp\\fonts\\captionshadow\\",(10,24,131,255)),8,8,"00")
    IMAGE = put(IMAGE,createtext(captiontext,".\\xp\\fonts\\caption\\"),7,7,"00")
    if(insideimagepath != ""):
        IMAGE = put(IMAGE,insideimage,3,h(TopFrame))
    if(erroriconpath != ""):
        IMAGE = put(IMAGE,erroricon,3+11,h(TopFrame)+11)
    IMAGE = put(IMAGE,createtext(errortext,".\\xp\\fonts\\text\\",(0,0,0,255)),textposx,textposy)
    IMAGE = put(IMAGE,buttonsimage,width//2-5,height-3,"12")
    return IMAGE

def CreateMacAlertDialog(width,height,title="",bar=True,icon="",errortext="",subtext="",button1="",button2="",button3="",button1default=False,button2default=False,button3default=False,button1style=0,button2style=0,button3style=0):
    WindowBar = Image.open("mac/Error Window With bar.png").convert("RGBA")
    WindowNoBar = Image.open("mac/Error Window No bar.png").convert("RGBA")
    Ridges = Image.open("mac/Red Ridges.png").convert("RGBA")
    ButtonBorder = Image.open("mac//Button Outline.png").convert("RGBA")
    TextHeight = 0
    IconPadding = 0
    Paddingwidth = 7
    if(bar):
        Paddingheight = 29+4
        Barheight = 29
    else:
        Paddingheight = 3+4
        Barheight = 0
    if(errortext != ""):
        ErrorTextImg = createtextmac(errortext,"mac//fonts//caption//")
        width = max(width,w(ErrorTextImg)+79+90)
        #height = max(height,h(ErrorTextImg)+Paddingheight+20)
        TextHeight += h(ErrorTextImg)
    if(subtext != ""):
        SubTextImg = createtextmac(subtext,"mac//fonts//text//")
        SubTextPos = TextHeight
        width = max(width,w(SubTextImg)+79+90)
        TextHeight += h(SubTextImg)
    height += TextHeight + Paddingheight
    if(icon != ""):
        IconImg = Image.open(icon).convert("RGBA")
        height = max(height,h(IconImg)+Paddingheight)
        width += w(IconImg)
        IconPadding = w(IconImg)
    buttonswidth = 0
    if(button1 != ""):
        height += 60
        button1img = CreateMacButton(button1,button1style)
        buttonswidth += w(button1img)
        if(button2 != ""):
            button2img = CreateMacButton(button2,button2style)
            buttonswidth += w(button2img)
            if(button3 != ""):
                button3img = CreateMacButton(button3,button3style)
                buttonswidth += w(button3img)
    width = max(width,buttonswidth+79+90)
    IMAGE = Image.new("RGBA", (width,height), (236,233,216,0))
    if(bar):
        IMAGE = put(IMAGE,resize(WindowBar,width,height,3,4,24,4),0,0)
    else:
        IMAGE = put(IMAGE,resize(WindowNoBar,width,height,3,4,3,4),0,0)
    if bar:
        if(title == ""):
            IMAGE = put(IMAGE,resizeanchor(Ridges,5,4,width-6,16,1,1,1,1),5,4)
        else:
            TitleImage = createtextmac(title,"mac//fonts//caption//")
            IMAGE = put(IMAGE,TitleImage,width//2-w(TitleImage)//2,3)
            IMAGE = put(IMAGE,resizeanchor(Ridges,5,4,width//2-w(TitleImage)//2-3,16,1,1,1,1),5,4)
            IMAGE = put(IMAGE,resizeanchor(Ridges,width//2+w(TitleImage)//2+5,4,width-6,16,1,1,1,1),width//2+w(TitleImage)//2+5,4)
    if(icon != ""):
        IMAGE = put(IMAGE,IconImg,26,Barheight+15)
    if(errortext != ""):
        IMAGE = put(IMAGE,ErrorTextImg,47+IconPadding,Barheight+14)
    if(subtext != ""):
        IMAGE = put(IMAGE,SubTextImg,47+IconPadding,Barheight+SubTextPos+16)
    if(button1 != ""):
        button1img = CreateMacButton(button1,button1style)
        IMAGE = put(IMAGE,button1img,width-17,height-17,"22")
        if(button1default):
            button1border = resize(ButtonBorder,w(button1img)+6,h(button1img)+6,5,5,5,5)
            IMAGE = put(IMAGE,button1border,width-17+3,height-17+3,"22")
        if(button2 != ""):
            button2img = CreateMacButton(button2,button2style)
            IMAGE = put(IMAGE,button2img,width-17-w(button1img)-22,height-17,"22")
            if(button2default):
                button2border = resize(ButtonBorder,w(button2img)+6,h(button2img)+6,5,5,5,5)
                IMAGE = put(IMAGE,button2border,width-17+3-w(button1img)-22,height-17+3,"22")
            if(button3 != ""):
                button3img = CreateMacButton(button3,button3style)
                IMAGE = put(IMAGE,button3img,width-17-w(button2img)-22-w(button1img)-22,height-17,"22")
                if(button3default):
                    button3border = resize(ButtonBorder,w(button3img)+6,h(button3img)+6,5,5,5,5)
                    IMAGE = put(IMAGE,button3border,width-17+3-w(button2img)-22-w(button1img)-22,height-17+3,"22")
    return IMAGE

def CreateMacWindow(width,height,title="",icon="",errortext="",subtext="",button1="",button2="",button3="",button1default=False,button2default=False,button3default=False,button1style=0,button2style=0,button3style=0):
    WindowBar = Image.open("mac/Window With bar.png").convert("RGBA")
    Ridges = Image.open("mac/Ridges.png").convert("RGBA")
    ButtonBorder = Image.open("mac//Button Outline.png").convert("RGBA")
    Paddingheight = 29+4
    TextHeight = 0
    if(errortext != ""):
        ErrorTextImg = createtextmac(errortext,"mac//fonts//caption//")
        width = max(width,w(ErrorTextImg)+79+90)
        #height = max(height,h(ErrorTextImg)+Paddingheight+20)
        TextHeight += h(ErrorTextImg)
    if(subtext != ""):
        SubTextImg = createtextmac(subtext,"mac//fonts//text//")
        width = max(width,w(SubTextImg)+79+90)
        TextHeight += h(SubTextImg)
    height += TextHeight
    if(button1 != ""):
        height += 80
    IMAGE = Image.new("RGBA", (width,height), (236,233,216,0))
    IMAGE = put(IMAGE,resize(WindowBar,width,height,3,4,24,4),0,0)
    if(title == ""):
        IMAGE = put(IMAGE,resizeanchor(Ridges,5,4,width-6,16,1,1,1,1),5,4)
    else:
        TitleImage = createtextmac(title,"mac//fonts//caption//")
        IMAGE = put(IMAGE,TitleImage,width//2-w(TitleImage)//2,3)
        IMAGE = put(IMAGE,resizeanchor(Ridges,5,4,width//2-w(TitleImage)//2-3,16,1,1,1,1),5,4)
        IMAGE = put(IMAGE,resizeanchor(Ridges,width//2+w(TitleImage)//2+5,4,width-6,16,1,1,1,1),width//2+w(TitleImage)//2+5,4)
    if(icon != ""):
        IconImg = Image.open(icon).convert("RGBA")
        IMAGE = put(IMAGE,IconImg,26,37)
    if(errortext != ""):
        IMAGE = put(IMAGE,ErrorTextImg,79,36)
    if(button1 != ""):
        button1img = CreateMacButton(button1,button1style)
        IMAGE = put(IMAGE,button1img,width-17,height-17,"22")
        if(button1default):
            button1border = resize(ButtonBorder,w(button1img)+6,h(button1img)+6,5,5,5,5)
            IMAGE = put(IMAGE,button1border,width-17+3,height-17+3,"22")
        if(button2 != ""):
            button2img = CreateMacButton(button2,button2style)
            IMAGE = put(IMAGE,button2img,width-17-w(button1img)-22,height-17,"22")
            if(button2default):
                button2border = resize(ButtonBorder,w(button2img)+6,h(button2img)+6,5,5,5,5)
                IMAGE = put(IMAGE,button2border,width-17+3-w(button1img)-22,height-17+3,"22")
            if(button3 != ""):
                button3img = CreateMacButton(button3,button3style)
                IMAGE = put(IMAGE,button3img,width-17-w(button2img)-22-w(button1img)-22,height-17,"22")
                if(button3default):
                    button3border = resize(ButtonBorder,w(button3img)+6,h(button3img)+6,5,5,5,5)
                    IMAGE = put(IMAGE,button3border,width-17+3-w(button2img)-22-w(button1img)-22,height-17+3,"22")
    return IMAGE

def CreateMacWindoid(icon="",text="",collapsed=False):
    contentwidth = 0
    contentheight = 0
    textpos = 6
    if(text != ""):
        TextImg = createtextmac(text,"mac//fonts//text//")
        contentwidth += w(TextImg)+7
        contentheight += h(TextImg)+3
    if(icon != ""):
        IconImg = Image.open(icon).convert("RGBA")
        contentwidth += w(IconImg) + 7
        contentheight = max(contentheight,h(IconImg))
        textpos += w(IconImg) + 7
    contentwidth += 12
    contentheight += 8
    CONTENT = Image.new("RGBA",(contentwidth,contentheight),(255,255,198))
    if(text != ""):
        CONTENT = put(CONTENT,TextImg,textpos,5)
    if(icon != ""):
        CONTENT = put(CONTENT,IconImg,6,4)
    Border = Image.open("mac//Windoid.png").convert("RGBA")
    CollapsedBorder = Image.open("mac//Windoid Hidden.png").convert("RGBA")
    Studs = Image.open("mac//Studs.png").convert("RGBA")
    CloseButton = Image.open("mac//Windoid Close Button.png").convert("RGBA")
    HideButton = Image.open("mac//Windoid Hide Button.png").convert("RGBA")
    width = contentwidth + 19
    height = contentheight + 9
    IMAGE = Image.new("RGBA",(width,height),(0,0,0,0))
    if not collapsed:
        IMAGE = put(IMAGE,resize(Border,width,height,14,5,4,5),0,0)
        IMAGE = put(IMAGE,CONTENT,14,4)
        IMAGE = put(IMAGE,CloseButton,2,2)
        IMAGE = put(IMAGE,HideButton,2,height-3,"02")
        IMAGE = put(IMAGE,tile(Studs,8,height-14-15),3,14)
    else:
        IMAGE = put(IMAGE,resize(CollapsedBorder,15,height,2,3,2,3),0,0)
        IMAGE = put(IMAGE,CloseButton,2,2)
        IMAGE = put(IMAGE,HideButton,2,height-3,"02")
        IMAGE = put(IMAGE,tile(Studs,8,height-14-15),3,14)
    return IMAGE

def mix(a,b,c):     #smoothly mixes between two values.
    c = min(1,max(0,c))
    c = c**0.5
    return a*(1-c)+b*c


#this function just takes a corner and squishes it based on width and the height of the image by some amount.
#amount of 3 will put it in the width/3,height/3 position
#amount of 7 will put it in the width/7,height/7 position and so on.
#c is there to animate the translation, from 0 - fully translated, to 1 - no translation
def stretch(size,amount,c):   
    result = size-size*(size/(size-size/amount)) #this is needed because deform() does the opposite of what you would think it will do, it takes 4 points, and then squishes them into a rectangle.
    return mix(result,0,c)

class Windows7Anim:
    def __init__(self,second):
        self.second = second
    
    def getmesh(self, img):
        return [((0,0,w(img),h(img)),(stretch(w(img),30,self.second*4),stretch(h(img),56,self.second*4),
                                      stretch(w(img),18,self.second*4),h(img)-stretch(h(img),16,self.second*4),
                                      w(img)-stretch(w(img),18,self.second*4),h(img)-stretch(h(img),16,self.second*4),
                                      w(img)-stretch(w(img),30,self.second*4),stretch(h(img),56,self.second*4)))]  #values arbitrary, somebody needs to look into dwm and find how it animates the window

def Create7Window(icon="",text="",title="",pos=(0,0),screenres=(1920,1080),wallpaper="",buttons=[]):
    #pos and screenres dictate the glass texture position and size on the window border
    #if wallpaper is not empty, it will composite the error onto an image at pos's coordinates, screenres should be the same size as the wallpaper
    contentwidth = 106
    contentheight = 53
    textpos = 0
    textposy = 25+13
    if(text != ""):
        TextDim = measuretext7(text,"7//fonts//text//",kerningadjust=-1)
        contentwidth = max(contentwidth,TextDim[0]+38+12)
        contentheight += TextDim[1]
        textposy = textposy-min(TextDim[1],21)
    if(icon != ""):
        IconImg = Image.open(icon).convert("RGBA")
        contentwidth = max(contentwidth,w(IconImg)+25+25)
        contentheight = max(contentheight,h(IconImg)+26+26)
        textpos += w(IconImg)-4+25
        textposy += h(IconImg)//2-7
        if(text != ""):
            contentwidth = max(contentwidth,w(IconImg)+25+TextDim[0]+38+9)
    if(title != ""):
        TitleDim = measuretext7(text,"7//fonts//text//",kerningadjust=-1)
        contentwidth = max(contentwidth,TitleDim[0]+49)
    buttonswidth = 0
    #len(buttons)*95
    for i in buttons:
        tempbuttontextsize = measuretext7(i[0],"7\\fonts\\text\\",kerningadjust=-1)
        buttonswidth += max(tempbuttontextsize[0]+16,86) + 10
    if(buttons):
        contentheight += 49
        contentwidth = max(contentwidth,buttonswidth+43)
    CONTENT = Image.new("RGBA",(contentwidth,contentheight),(255,255,255))
    if(icon != ""):
        CONTENT = put(CONTENT,IconImg,25,26)
    if(text != ""):
        CONTENT = createtext7(CONTENT,textpos+12,textposy,text,"7//fonts//text//",kerningadjust=-1)
    if(buttons):
        CONTENT = put(CONTENT, Image.new("RGBA",(contentwidth,49),(240,240,240)),0,contentheight,"02")
    buttonpos = 0
    for i in buttons:
        buttonpos += 10
        Button = Create7Button(i[0],i[1])
        CONTENT = put7(CONTENT, Button, contentwidth-buttonpos,contentheight-12,"22")
        buttonpos += w(Button)
    Window = Image.open("7//Window.png").convert("RGBA")
    CloseButton = Image.open("7//Close Button Single.png").convert("RGBA")
    CloseSymbol = Image.open("7//Close Symbol.png").convert("RGBA")
    GlassImg = Image.open("7//Glass.png").convert("RGBA")
    GlassMask = Image.open("7//Glass Mask.png").convert("RGBA")
    TextGlow = Image.open("7//Text Glow.png").convert("RGBA")
    SideGlowLeft = Image.open("7//Sideglow 1 Left.png").convert("RGBA")
    SideGlowRight = Image.open("7//Sideglow 1 Right.png").convert("RGBA")
    SideShine = Image.open("7//Side Shine.png").convert("RGBA")
    width = contentwidth+8+8
    height = contentheight+8+30
    GlassMask = resize(GlassMask,width,height,8,8,30,8)
    #Glass = put(Image.new("RGBA",(800,602),(0,0,0,0)),GlassImg.resize(screenres),int((width/screenres[0])*50-50-pos[0]+pos[0]*0.12173472694),0)
    Glass = put(Image.new("RGBA",(800,602),(0,0,0,0)),GlassImg.resize(screenres),int(-pos[0]+width/16-screenres[0]/16+pos[0]/8),-pos[1])
    WithBorder = ImageChops.multiply(GlassMask,Glass)
    WithBorder = put(WithBorder, SideGlowLeft, 0, 0)
    WithBorder = put(WithBorder, SideGlowRight, width, 0, "20")
    WithBorder = put(WithBorder, SideShine.resize((w(SideShine),(height-29-8)//4)), 0, 29)
    WithBorder = put(WithBorder, SideShine.resize((w(SideShine),(height-29-8)//4)), width, 29, "20")
    #WithBorder.show()
    if(title != ""):
        WithBorder = put(WithBorder,resize(TextGlow,TitleDim[0]+7+14,h(TextGlow),23,23,1,1),-7,0)
        WithBorder = createtext7(WithBorder,8,7,title,"7//fonts//text//",kerningadjust=-1)
    
    WithBorder = put(WithBorder,resize(Window,width,height,8,8,30,8),0,0)
    WithBorder = put(WithBorder,CONTENT,8,30)
    WithBorder = put(WithBorder,CloseButton,width-6,1,"20")
    WithBorder = put(WithBorder,CloseSymbol,width-6-18,5,"20")
    ShadowTop = Image.open("7//Shadow Top.png")
    ShadowRight = Image.open("7//Shadow Right.png")
    ShadowBottom = Image.open("7//Shadow Bottom.png")
    ShadowLeft = Image.open("7//Shadow Left.png")
    IMAGE = Image.new("RGBA",(width+19+13,height+18+12),(0,0,0,0))
    IMAGE = put(IMAGE, resize(ShadowTop,width+13+16,12,26,26,1,1),0,0)
    IMAGE = put(IMAGE, resize(ShadowLeft,13,height,1,1,20,14),0,12)
    IMAGE = put(IMAGE, resize(ShadowRight,19,height,1,1,20,14),width+13,12)
    IMAGE = put(IMAGE, resize(ShadowBottom,width+13+17,18,28,27,1,1),0,height+12)
    IMAGE = put(IMAGE,WithBorder,13,12)
    if(wallpaper != ""):
        WallpaperImg = Image.open(wallpaper).convert("RGBA")
        IMAGE = put(WallpaperImg, IMAGE, pos[0]-13, pos[1]-12)
    return IMAGE
def Export7Animation(img,savepath):  #just put the generated window into img and set savepath to the folder you want it to save  "7//animoutput//" is recommended
    for i in range(16):
        ImageChops.multiply(ImageOps.deform(img, Windows7Anim(i/60)),Image.new("RGBA",(w(img),h(img)),(255,255,255,int(max(0,min(1,(i+0.1)/15))**0.5*255)))).save(savepath+str(i)+".png")
def Create3_1Window(icon="",text="",title="",buttons=[]):
    contentwidth = 0
    contentheight = 0
    textpos = 18
    textposy = 16
    if(text != ""):
        TextImg = createtextmac(text,"3.1//fonts//text//")
        contentwidth += w(TextImg)+18+18
        contentheight += h(TextImg)+16
    if(icon != ""):
        IconImg = Image.open(icon).convert("RGBA")
        textpos += w(IconImg)+19
        contentwidth += w(IconImg)+19
        contentwidth = max(contentwidth,w(IconImg)+19+19)
        contentheight = max(contentheight,17+h(IconImg)+17)
        if(text != ""):
            textposy = max(16,h(IconImg)//2-h(TextImg)//2+17)
    Window = Image.open("3.1//Window.png").convert("RGBA")
    CloseButton = Image.open("3.1//Close Button.png").convert("RGBA")
    CONTENT = Image.new("RGBA",(contentwidth,contentheight),(255,255,255,255))
    if(text != ""):
        CONTENT = put(CONTENT,TextImg,textpos,textposy)
    if(icon != ""):
        CONTENT = put(CONTENT,IconImg,19,17)
    width = contentwidth+5+5
    height = contentheight+24+5
    IMAGE = resize(Window,width,height,6,6,24,5)
    IMAGE = put(IMAGE,CONTENT,5,24)
    IMAGE = put(IMAGE, CloseButton,6,5)
    return IMAGE
    #
        
# Example XP windows:
#o = CreateXPWindow(0,0,"Notepad",errortext="The text in the Untitled file has changed.\n\nDo you want to save the changes?",button1="Yes",button2="No",button3="Cancel",button1style=4)

#o = CreateXPWindow(0,0,"Notepad",erroriconpath="xp\\Exclamation.png",errortext="The text in the Untitled file has changed.\n\nDo you want to save the changes?",button1="Yes",button1style=4)

#o = CreateXPWindow(0,0,"Notepad",erroriconpath="xp\\Exclamation.png",errortext="The text in the Untitled file has changed.\n\nDo you want to save the changes?")

#o = CreateXPWindow(0,0,"Notepad",errortext="The text in the Untitled file has changed.\n\nDo you want to save the changes?")

#o = CreateXPWindow(0,0,"LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONG",errortext="short",button1="OK",button1style=4)

#o = CreateXPWindow(0,0,"Notepad",erroriconpath="xp\\Exclamation.png",errortext="The text in the Untitled file has changed.\n\nDo you want to save the changes?",button1="Yes",button2="No",button3="Cancel",button1style=4)

# Example 7 windows:
#o = Create7Window(icon="7\\Question Mark.png",text="text",title="title",buttons=[["Cancel",0],["No",0],["Yes",4]])
#o = Create7Window(icon="7\\Question Mark.png",text="text",title="title",buttons=[["Cancel",0],["No",0],["Yes",4]],wallpaper="7\\wallpaper.png",pos=(400,400))

o = Create3_1Window(icon="3.1//Stop.png",text="hfgkdfjgdhfgkjdfg")

o.show()

o.save("output.png")


