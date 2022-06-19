# XP

```CreateXPWindow(0,0,captiontext="",errortext="This is an example error")```

![](https://i.imgur.com/td2lf00.png)
---

```CreateXPWindow(0,0,captiontext="",erroriconpath="xp//Critical Error.png",errortext="This is an example error")```

![](https://i.imgur.com/p8iI7uy.png)
-

```CreateXPWindow(0,0,captiontext="Caption",erroriconpath="xp\\Information.png",errortext="This is an example error",button1="OK",button1style=4)```

![](https://i.imgur.com/NPkhwlX.png)
-

```CreateXPWindow(0,0,captiontext="Question",erroriconpath="xp\\Question.png",errortext="Multiple buttons with different styles\nAnd showing off the multiline capabilities\n.\n.\n.\n.",button1="OK",button1style=4,button2="Cancel",button3="This button is disabled and long\nand has a double line!",button3style=3)```

![](https://i.imgur.com/gv0waEX.png)
-
# 7

```Create7Window(icon="7\\Question Mark.png",text="Error with no buttons",title="Title text"```

![](https://i.imgur.com/mIx628a.png)
-

```Create7Window(icon="7\\Question Mark.png",text="Error text",title="Window title",buttons=[["Cancel",0],["No",0],["Yes",4]])```

![](https://i.imgur.com/ZFEkhGj.png)
-

```Create7Window(text="Error with no icon",title="Window title",buttons=[["Cancel",0],["No",0],["Yes",4]])```

![](https://i.imgur.com/FZt2rQN.png)
-

```Create7Window(text="Error with no icon and buttons",title="Window title")```

![](https://i.imgur.com/azalG8L.png)
