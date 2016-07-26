#bioshockPlasmidsAreThePaint.py
#Shadman Hassan
#This program allows the user to create images using a variety of given tools
#at their disposal. This includes tools such as the pencil, eraser, brush, spray,
#stamps, eyedropper, etc. The user can also save and load images and load
#different backgrounds to draw on. They can play music while drawing.
#The theme of this paint program is Bioshock and the wide array of tools
#inside this program is featured as the wide array of weaponry
#featured throughout the popular game series. Remember,
#
#"ADAM is the canvas, but Plasmids Are The Paint"
#   -Suchong Yi, Bioshock

#INSTALL ANDES FONT PROVIDED FIRST!!!!

from pygame import *
from random import *
from math import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

crossCopy = display.set_mode((1280, 913)) #surface for cursor
screen = Surface((1280, 913)).convert() #surface for drawing/blitting and everything else
root = Tk()
root.withdraw()
message = ''
#font.init()
bioFont = font.Font('Andes.ttf', 27)

display.set_caption('BioShock: Plasmids are the Paint, By: Shadman Hassan')  #title of program window

#-----------------------------SOME IMAGES LOADED AND SCALED-----------------------

bg = image.load('bioshockBG.jpg')  #loads background image

title = transform.scale(image.load('title.png'), (300, 190))  #loads and scales various images to proper sizes
bar = transform.scale(image.load('miscs/bar.png'), (350, 190))  #images include almost everything besides tool icons
cWheel = transform.scale(image.load('miscs/colorwheel.png'), (140, 140))  #(E.g. colour wheel,colourbar, canvas border,
border = transform.scale(image.load('border.png'), (896, 639)) #crosshairs cursor, fill/unfill button)
crosshair = transform.scale(image.load('crosshair.png'), (40, 40))
fillImg = transform.scale(image. load('fill.png'), (90, 90))
unfillImg = transform.scale(image.load('unfill.png'), (90, 90))

screen.blit(bg, (0, 0))  # blits various images onto screen (background, title, health
screen.blit(title, (675, 0))  # (colour) bar, colour palette, canvas border)
screen.blit(bar, (27, -5))
screen.blit(cWheel, (2, 0))
screen.blit(border, (381, 145))
screen.blit(unfillImg, (370, 10))

canvas = Rect(392, 155, 875, 620)  #rectangles covering canvas, fill/unfill button, colour wheel and tool icons
fillRect = Rect(370, 10, 90, 90)
cWheelRect = Rect(0, 0, 140, 140)
toolRect = Rect(20, 190, 300, 610)
colRect = (147, 75, 162, 23)  #rectangle displaying colour of the pixel that the mouse cursor is on
draw.rect(screen, (255, 255, 255), canvas)  #draws canvas
draw.rect(screen, (255, 255, 255), colRect)  #draws EVE bar with default colour of white

canSurface = Surface((875, 620)).convert()  # makes blank Surface for the highlighter tool
canSurface.set_alpha(55)  #highlighter more transparent than opaque (closer to 0 thn 255)
canSurface.set_colorkey((255, 255, 255))  #colour key is white

panelRect = Rect(0, 800, 1280, 113) #rectangle for bottom panel
panelImg = screen.subsurface(panelRect).copy() #picture of default blank bottom panel

ammoRect = (200, 110, 300, 35)
ammoRect = screen.subsurface(ammoRect).copy()

infoList = ['Pistol (Pencil) - Most basic weapon doing low damage. Shoots (draws) in any line you trace!',
          'RPG (Eraser) - This weapon can obliterate enemies, as if they never existed. Erase mistakes with this weapon!',
          'Machine Gun (Brush) - Reliable weapon dealing higher damage than Pistol. Draw a trail of opaque circles with this!',
          'Shotgun (Spray Can) - A powerful, yet messy, weapon leaving a sign of its use. Use it to spray with a graffiti effect!',
          'Shotgun Lv.2 (Spray Gun) - More accurate than Shotgun. An opaque circle is gradually drawn as left click is held down!',
          'Chemical Thrower (Highlighter) - More ammo is more damage. Draw on top of layers to darken colour!',
          'Bloodlust Tonic (Eyedropper) - Copies health (colour) from an enemy (canvas) and adds it as your own health (colour)!',
          'Skyhook (Line) - Melee weapon that can cut (draw) in any straight line you trace!',
          'Skyhook (Rectangle) - Melee weapon that can cut (draw) in any rectangle formation you choose!',
          'Skyhook (Oval) - Melee weapon that can cut (draw) in any oval formation you choose!',
          'Stamps and Backgrounds - Use your favourite stamps and backgrounds from the critically acclaimed game series, BioShock!',
          'Iron Sights Gear (Vision) - Use this mod to enhance your vision and see things in a different perspective!',
          'Electro Plasmid (Polygon) - This plasmid will create connecting lightning strikes (lines) wherever you choose!',
          'Incinerate (Fill Bucket) - With a snap (click) of your fingers (mouse), set any region aflame (with your chosen colour)!',
          'Telekinesis (Select Move) - Using the power of mind (mouse), select a part of your canvas to move wherever you desire!',
          'Powers of Elizabeth (Vertical Flip) - Using her magic powers, Elizabeth can flip an entire dimension vertically!',
          'Powers of Elizabeth (Horizontal Flip) - Using her magic powers, Elizabeth can flip an entire dimension horizontally!',
          'New Game (Clear) - Wish to start a new game (canvas)? Well with this tool, now you can!']
          #tool descriptions in order of tool icons arrangement, top row to bottom row, left column to right column

#-------------------------------TOOL/MISC BUTTONS---------------------------------

points = []  #list of coordinates where tool icons are to be blitted
rects = []  #list of rectangles placed on the same coordinates as the tool icons
#(but invisible because they aren't drawn)
for x in range(3):
    for y in range(6):
        point = (25 + 100 * x, 200 + 100 * y)  #creates coordinates for the points list
        rect = Rect(25 + 100 * x, 200 + 100 * y, 90, 90)  #creates rectangles for the rects list
        rects.append(rect)
        points.append(point)

miscPoints = []  #list of coordinates where misc icons are to be blitted
miscRects = []  #list of rectangles placed on the same coordinates as misc icon images
for x in range(4):
    miscPoint = (1000 + 70 * x, 10)  #creates coordinates for the miscPoints list
    miscRect = Rect(1000 + 70 * x, 10, 60, 60)  #creates rectangles for the miscRects list
    miscRects.append(miscRect)
    miscPoints.append(miscPoint)

#----------------------------STAMP/BACKGROUND BUTTONS---------------------------

stampPoints = []  #list of coordinates where stamp icons are to be blitted
stampRects = []  #list of rectangles placed on the same coordinates as stamp icon images
bgPoints = []  #list of coordinates where background icons are to be blitted
bgRects = []  #list of rectangles placed on the same coordinates as background icon images
for x in range(12):
    stampPoint = (50 + 100 * x, 810)  #creates coordinates for the stampPoints list
    stampRect = Rect(50 + 100 * x, 810, 90, 90)  #creates rectangles for the stampRects list
    stampRects.append(stampRect)
    stampPoints.append(stampPoint)

for x in range(6):
    bgPoint = (100 + 180 * x, 810)  #creates coordinates for the bgPoints list
    bgRect = Rect(100 + 180 * x, 810, 150, 90)  #creates rectangles for the bgRects list
    bgRects.append(bgRect)
    bgPoints.append(bgPoint)

#-------------------TOOL ICON IMAGES LOADED, SCALED AND BLITTED------------------

tools = ['pencil', 'eraser', 'brush', 'sprayCan', 'sprayGun', 'highlighter', 'eyedropper', 'line', 'rectangle', 'oval',
         'stamp', 'vision', 'multiLine', 'fillBucket', 'select', 'vertical', 'horizontal', 'clear']
#list of tools, the icons in the order of being placed on the screen, top row to
#bottom row, left column first, then right column
toolImgs = []  #list of tool images

for i in range(18):
    toolImg = transform.scale(image.load('tools/' + tools[i] + '.png'), (90, 90))
    toolImgs.append(toolImg)  #loads and scales tool icons to the appropriate size
    draw.circle(screen, (0, 0, 255), (((points[i])[0]) + 45, ((points[i])[1]) + 45), 50)
    screen.blit(toolImg, (points[i]))  #blits tool icons to appropriate places

#----------------STAMP/BACKGROUND IMAGES LOADED, SCALED AND BLITTED---------------

stamps = ['bigDaddy', 'bigSister', 'booker', 'delta', 'elizabeth', 'handyman', 'patriot',
          'skyhook', 'wrench', 'chain', 'adam', 'eve']
#list of stamps in order of being placed on the panel, left to right
stampImgs = []  #list of scaled stamp images
stampImgs2 = []  #list of stamp images with original resolutions

for i in range(12):
    stampImg = transform.scale(image.load('stamps/' + stamps[i] + '.png'), (90, 90))
    stampImgs.append(stampImg)  #loads and scales stamp icons to the appropriate size
    stampImgs2.append(image.load('stamps/' + stamps[i] + '.png'))
    #loads stamp images, but retains original resolutions
    screen.blit(stampImg, (stampPoints[i]))  #blits stamp icons to appropriate places

newPanelImg = screen.subsurface(panelRect).copy() #picture of bottom panel with stamp icons

bgImgs = []  #list of scaled background images
bgImgs2 = []  #list of background images with original resolutions

for i in range(6):
    bgImg = transform.scale(image.load('backgrounds/bg' + str(i + 1) + '.jpg'), (150, 90))
    bgImgs.append(bgImg)  #loads and scales background icons to the appropriate size
    bgImgs2.append(image.load('backgrounds/bg' + str(i + 1) + '.jpg'))
    #loads background images, but retains original resolutions

#-------------------OTHER ICON IMAGES LOADED, SCALED AND BLITTED------------------

miscs = ['save', 'load', 'undo', 'redo']
miscImgs = []  #list of various icon images

for i in range(4):
    miscImg = transform.scale(image.load('miscs/' + miscs[i] + '.png'), (60, 60))
    miscImgs.append(miscImg)  #loads and scales misc icons to the appropriate size
    screen.blit(miscImg, (miscPoints[i]))  #blits misc icons to appropriate places

#----------------------------STARTUP STEPS OUTSIDE LOOP---------------------------

tool = 'pencil'  #variable for selected tool (default is pencil on first run)

toolHist = ['pencil']

thick = 10  #variable for thickness of tool(default is 10 since it's an average size)

col = (0, 0, 0)  #variable for colour(default is black)

panel = 'stamps'  #variable for current panel being displayed (default is stamps)

oldmx, oldmy = (0, 0)  #makes sure the program doesn't crash the through the first run
#since oldmx,oldmy isn't defined until the end of the first run

pencilImg = transform.scale(toolImgs[0], (60, 60))  #blits image icon of default tool (pencil)
screen.blit(pencilImg, (125, 105))  #on the upper left corner

stamp = image.load('stamps/bigDaddy.png')  #loads default stamp image (Big Daddy)
bg = image.load('backgrounds/bg1.jpg')  #loads default background image

stampNum = 0

lineList = []
undoList = []
redoList = []

copy = screen.subsurface(canvas).copy()

fill = False #flag for whether the shape should be filled/unfilled
drag = False #flag for stating if the mouse is being clicked and dragged or not
save = False #flag for if save dialog box pops up or not
load = False #flag for if load dialog box pops up or not

newSelect = True #flags for select tool, checkpoints for each process within the
ready = False #tool
dragReady = False
finalStep = False

#-------------------------------USAGE OF EVENT LOOP-------------------------------

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            if fillRect.collidepoint(e.pos):
                if fill:
                    screen.blit(unfillImg, (370, 10))
                    fill = False
                else:
                    screen.blit(fillImg, (370, 10))
                    fill = True
            if canvas.collidepoint(e.pos):
                copy = screen.subsurface(canvas).copy()
                undoList.append(copy) #adds screenshot of current canvas to undo list
                redoList = [] #empties redo list since a new edit has been made and now no future state of canvas exists
            posx, posy = e.pos
            canSurface.fill((255, 255, 255))

            if cWheelRect.collidepoint(e.pos):  #the chosen colour becomes the colour of the
                col = screen.get_at(e.pos)  #pixel the mouse clicks on, in the colour palette

            if tool == 'sprayCan':  #Each time the mouse is clicked, a trail of circles is drawn
                screen.set_clip(canvas)  #(outside the event loop) and some residue of paint (made out of rectangles and
                for i in range(randint(5, 6)):  # circles) is drawn underneath the first circle, when the
                    x = mx - thick // 2 - thick // 4  #mouse is first clicked. This resembles a
                    circy = randint(my + thick // 2, (my + thick // 2 + 5 * thick // 2))  #graffiti effect
                    randthick = randint(thick // 8, thick // 3)
                    draw.circle(screen, col, (x + thick // 3 * i, my), randthick // 2)
                    draw.line(screen, col, (x + thick // 3 * i, my), (x + thick // 3 * i, circy), randthick)
                    draw.circle(screen, col, (x + thick // 3 * i, circy), randthick // 2)
                screen.set_clip(None)

            if tool == 'multiLine':
                if canvas.collidepoint(e.pos):
                    if len(lineList) == 0:
                        lineList.append(e.pos)
                    drag = True

            if tool == 'select':
                if ready:
                    screen.blit(copy,(392,155))
                    selectCopy = screen.subsurface(selectRect).copy() #takes a pic of user dragged rect
                    newSelect = False
                    dragReady = True
                    ready = False
                if finalStep:
                    dragReady = False #restarts select tool so that it can be used again
                    newSelect = True
                    finalStep = False

        if e.type == MOUSEBUTTONUP:
            upCopy = screen.subsurface(canvas).copy()
            if drag:
                lineList.append(e.pos)
                drag = False
            if save:
                fileName = asksaveasfilename(parent=root, title='Save the image as...')
                if fileName != '':
                    image.save(screen.subsurface(canvas), '%s.png' % fileName)  #saves file as the name the user inputs
            elif load:
                fileName = askopenfilename(parent=root, title='Load image...')
                if fileName != '':
                    loadImg = image.load('%s' % fileName)  #loads, scales and blits the image the user inputs
                    loadImg = transform.scale(loadImg, (875, 620))
                    screen.blit(loadImg, (392, 155))

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 4:  #increases thickness when mouse wheel is scrolled upward,
                if thick < 100:  #decreases when scrolled downward
                    thick += 1
            if e.button == 5:
                if thick > 0:
                    thick -= 1

#-----------------------------------TOOL SELECTION---------------------------------

            if e.button == 1:
                for i in range(18):
                    if rects[i].collidepoint(e.pos):
                        tool = tools[i]  #selects the tool of the icon the user clicks on
                        toolImg = transform.scale(toolImgs[i], (60, 60))  #blits image icon of current
                        screen.blit(toolImg, (125, 105))  #tool on the upper left corner
                        draw.circle(screen, (255, 0, 0), (((points[i])[0]) + 45, ((points[i])[1]) + 45), 50)
                        screen.blit(toolImg, (points[i]))
                        if toolHist[-1] != tools[i]:
                            toolHist.append(tools[i])
                        if tool == 'stamp':
                            if panel == 'stamps':
                                panel = 'bgs'
                                screen.blit(panelImg, (0, 800))  #blits default panel background so that new icons can
                                #be blitted on
                                for n in range(6):
                                    screen.blit(bgImgs[n], (bgPoints[n]))
                                    #blits background icons to appropriate places in panel
                                newPanelImg = screen.subsurface(panelRect).copy() #changes picture of bottom panel so
                            else:                                     #that it now shows updated version with new icons
                                panel = 'stamps'  #blits default panel background so that new icons can be blitted on
                                screen.blit(panelImg, (0, 800))
                                for x in range(12): #blits stamp icons to appropriate places in stamp panel
                                    screen.blit(stampImgs[x], (stampPoints[x]))
                                newPanelImg = screen.subsurface(panelRect).copy()
                        if tool == 'multiLine':
                            lineList = []
                        if tool == 'vertical' or tool == 'horizontal':
                            copy = screen.subsurface(canvas).copy()
                            if tool == 'vertical': #flips canvas vertically
                                newCopy = transform.flip(copy, True, False)
                                toolHist.remove('vertical')
                            else: #flips canvas horizontally
                                newCopy = transform.flip(copy, False, True)
                                toolHist.remove('horizontal')
                            screen.blit(newCopy, (392, 155))
                            tool = toolHist[-1]
                            toolImg = transform.scale(toolImgs[tools.index(toolHist[-1])], (60, 60))  #blits image icon
                            screen.blit(toolImg, (125, 105))  #of last tool before clear on the upper left corner
                        if tool == 'clear': #clears canvas
                            copy = screen.subsurface(canvas).copy()
                            draw.rect(screen, (255, 255, 255), canvas)
                            toolHist.remove('clear')
                            tool = toolHist[-1]
                            toolImg = transform.scale(toolImgs[tools.index(toolHist[-1])], (60, 60))  #blits image icon
                            screen.blit(toolImg, (125, 105))  #of last tool before clear on the upper left corner
                if panelRect.collidepoint(e.pos):
                    if panel == 'stamps':
                        for i in range(12):
                            if stampRects[i].collidepoint(e.pos):
                                stampNum = i  #selects the appropriate stamp the user selects
                                tool = 'stamp'
                    elif panel == 'bgs':
                        for i in range(6):
                            if bgRects[i].collidepoint(e.pos):
                                bg = transform.scale(bgImgs2[i], (875, 620))
                                screen.blit(bg, (392, 155))#blits the background the user selects
                                copy = screen.subsurface(canvas).copy()

#----------------------------------OTHER BUTTON FUNCTIONS----------------------------------

                if miscRects[0].collidepoint(e.pos):  #opens save dialog box when the user clicks on the save icon
                    save = True
                    load = False
                elif not miscRects[0].collidepoint(e.pos):
                    save = False

                if miscRects[1].collidepoint(e.pos):  #opens load dialog box when the user clicks on the load icon
                    load = True
                    save = False

                elif not miscRects[1].collidepoint(e.pos):
                    load = False

                if miscRects[2].collidepoint(e.pos):
                    if len(undoList) > 0:
                        redo = screen.subsurface(canvas).copy() #takes a screenshot of the canvas and adds it to the
                        undo = undoList.pop() #redo list
                        screen.blit(undo, (392, 155)) #blits previous state of canvas before the new edit
                        redoList.append(redo)

                if miscRects[3].collidepoint(e.pos):
                    if len(redoList) > 0:
                        undo = screen.subsurface(canvas).copy() #takes a screenshot of the canvas and adds it to the
                        redo = redoList.pop() #undo list
                        screen.blit(redo, (392, 155)) #blits future state of canvas before the last undo
                        undoList.append(undo)

#--------------------------------STARTUP STEPS INSIDE LOOP---------------------------------

    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    dist = round(hypot(mx - oldmx, my - oldmy))  #calculates distance between previous mouse coordinates and current
    #mouse coordinates

    curColRect = (169, 35, 176, 25)  #draws (Health) bar displaying current selected colour
    draw.rect(screen, col, curColRect)

    crossCopy.blit(screen, (0, 0)) #keeps blitting this surface so that the cursor doesn't leave a trail

    if canvas.collidepoint(mx, my):
        ammoPic = bioFont.render(('%d , %d cartridges' %(mx,my)), True, (255, 0, 0))
        screen.blit(ammoRect, (200, 110))
        screen.blit(ammoPic, (200, 110))

    else:
        ammoPic = bioFont.render('Reloading...', True, (255, 0, 0))
        screen.blit(ammoRect, (200, 110))
        screen.blit(ammoPic, (200, 110))

    if canvas.collidepoint(mx, my) or cWheelRect.collidepoint(mx, my):  #draws (EVE) bar displaying the colour of
        draw.rect(screen, (screen.get_at((mx, my))), colRect)  #the pixel the mouse is currently touching

#------------------------------------TOOL FUNCTIONS/USAGE-----------------------------------

    if toolRect.collidepoint(mx, my):  #highlights tool icon the user hovers their mouse over in green
        for i in range(18):  #and also the one they click on with red
            if rects[i].collidepoint(mx, my):
                draw.circle(screen, (255, 0, 0), (((points[i])[0]) + 45, ((points[i])[1]) + 45), 50)
                screen.blit(toolImgs[i], (points[i]))
                screen.blit(panelImg, (0, 800)) #blits pic of default panel so that text can be blitted on top
                txtPic = bioFont.render(infoList[i], True, (255, 0, 0)) #blits text description of the tool the mouse is
                screen.blit(txtPic, (640 - txtPic.get_width() / 2, 815)) #hovering over
            elif not rects[i].collidepoint(mx, my):
                draw.circle(screen, (0, 0, 255), (((points[i])[0]) + 45, ((points[i])[1]) + 45), 50)
                screen.blit(toolImgs[i], (points[i]))

    if not toolRect.collidepoint(mx, my):
        screen.blit(newPanelImg, (0,800)) #shows bottom panel with icons when the user is not hovering over the tools

    for i in range(18):  #highlights selected tools icon with red
        if tool == tools[i]:
            draw.circle(screen, (255, 0, 0), (((points[i])[0]) + 45, ((points[i])[1]) + 45), 50)
            screen.blit(toolImgs[i], (points[i]))

    screen.set_clip(canvas)  #makes sure that the user can't draw outside the canvas

    if canvas.collidepoint(mx, my):
        mouse.set_visible(False) #makes cursor vanish
        crossCopy.blit(crosshair, (mx - 20, my - 20)) #blits crosshairs icon as cursor

    if not canvas.collidepoint(mx, my):
        mouse.set_visible(True) #makes cursor reappear

    if mb[0] == 1 and canvas.collidepoint(mx, my):
        def trail(length, surface, colour, width, mouseX, mouseY, oldMouseX, oldMouseY):
            #variables in parameters are general, easy to understand terms
            for i in range(length):  #function that draws a circle at every pixel the mouse
                pixX = i * (mouseX - oldMouseX) // length  #touches, creating a trail of circles
                pixY = i * (mouseY - oldMouseY) // length  #resembling a line
                draw.circle(surface, colour, (oldMouseX + pixX, oldMouseY + pixY), width)
            draw.circle(surface, colour, (mouseX, mouseY), width)
            return

        if tool == 'pencil':  #draws a regular trail of circles, with a thickness of 0
            trail(dist, screen, col, 0, mx, my, oldmx, oldmy)

        elif tool == 'eraser':  #draws a regular trail of white circles
            trail(dist, screen, (255, 255, 255), thick, mx, my, oldmx, oldmy)

        elif tool == 'brush':  #draws a regular trail of circles, any thickness and colour
            trail(dist, screen, col, thick, mx, my, oldmx, oldmy)
            if thick < 2:
                thick == 2

        elif tool == 'sprayCan':
            trail(dist, screen, col, thick, mx, my, oldmx, oldmy)

        elif tool == 'sprayGun':  #draws circles in random coordinates forming a circle with the radius
            for i in range(thick):  #equal to the thickness and its centre at the mouse position
                sprayX = randint(mx - thick, mx + thick)
                sprayY = randint(my - thick, my + thick)
                if hypot(mx - sprayX, my - sprayY) < thick:
                    draw.circle(screen, col, (sprayX, sprayY), 0)

        elif tool == 'highlighter':  #draws transparent trail of circles in what ever colour the user chooses
            trail(dist, canSurface, col, thick, mx - 400, my - 155, oldmx - 400, oldmy - 155)
            screen.blit(copy, (392, 155))  #blits the canvas and canvas surface onto the screen
            screen.blit(canSurface, (392, 155))

        elif tool == 'eyedropper':  #the chosen colour becomes the colour of the pixel the mouse clicks on
            col = screen.get_at((mx, my))

        elif tool == 'line':  #draws a line, from the coordinates of the first position of the mouse to the
            screen.blit(copy, (392, 155))  #current position of the mouse
            draw.line(screen, col, (posx, posy), (mx, my), thick)

        elif tool == 'rectangle' or tool == 'oval':
            screen.blit(copy, (392, 155))
            rectShape = Rect(min(mx, posx), min(my, posy), max(mx, posx) - min(mx, posx),
                             max(my, posy) - min(my, posy))  #dragged
            if thick == 0:  #rectangle that the user selects
                thick = 1
            if tool == 'rectangle':  #draws a rectangle, to any size the user chooses by dragging the mouse with the
                if fill:             #mouse held down
                    draw.rect(screen, col, rectShape)
                else:
                    draw.rect(screen, col, rectShape, thick) #draws lines to even up corners of rectangle to make it
                    draw.line(screen, col, (min(mx, posx) - (thick / 2) + 1, min(my, posy)), #look better
                              (max(mx, posx) + (thick / 2) - 1, min(my, posy)), thick)
                    draw.line(screen, col, (min(mx, posx) - (thick / 2) + 1, max(my, posy)),
                              (max(mx, posx) + (thick / 2) - 1, max(my, posy)), thick)
            elif tool == 'oval':
                if thick * 2 >= max(mx, posx) - min(mx, posx) or thick * 2 >= max(my, posy) - min(my, posy) or fill:
                        draw.ellipse(screen, col, rectShape)  #draws an ellipse instead of a rectangle
                else: #if drawing an unfilled oval, it only draws the oval if 2 times the width of the oval is smaller
                    draw.ellipse(screen, col, rectShape, thick) #than the radius

        elif tool == 'stamp':
            if panel == 'stamps':
                screen.blit(copy, (392, 155))
                stamp = transform.scale(stampImgs2[stampNum], (thick * 6, thick * 6))
                screen.blit(stamp, (mx - thick * 6 / 2, my - thick * 6 / 2))

        elif tool == 'vision':
            for x in range(875):
                for y in range(620):  #checks every pixel on canvas and turns their colour into the exact
                    invcol = screen.get_at((x + 392, y + 155))  #opposite colour, creating an negative coloured canvas
                    screen.set_at((x + 392, y + 155), ((255 - (invcol[0])), (255 - (invcol[1])), (255 - (invcol[2]))))

        elif tool == 'multiLine':  #draws a set of lines, from each point the mouse clicked on to the current
            screen.blit(copy, (392, 155))  #point the mouse has clicked on
            draw.line(screen, col, lineList[-1], (mx, my), thick)

        elif tool == 'fillBucket':
            sideList = []  #fills the area, with the same colour as the pixel the mouse clicked, with the
            col1 = screen.get_at((mx, my))  #with the colour
            sideList.append((mx, my))  #modified version of flood fill (non-recursive)
            if col1 != col:
                while len(sideList) > 0:
                    ptx, pty = sideList.pop()
                    if screen.get_at((ptx, pty)) == col1:
                        screen.set_at((ptx, pty), col)
                        sideList.append((ptx - 1, pty))
                        sideList.append((ptx + 1, pty))
                        sideList.append((ptx, pty - 1))
                        sideList.append((ptx, pty + 1))

        elif tool == 'select':
            if newSelect:
                screen.blit(copy, (392, 155))
                selectRect = Rect(min(mx, posx), min(my, posy), max(mx, posx) - min(mx, posx),
                                 max(my, posy) - min(my, posy))  #dragged rectangle the user selects
                width = max(mx, posx) - min(mx, posx)
                height = max(my, posy) - min(my, posy)
                draw.rect (screen, (0,0,0), selectRect, 1)
                ready = True
            if dragReady:
                screen.blit(copy, (392, 155)) #allows user to place pic of chosen rect in any position
                screen.blit(selectCopy, (mx-width//2, my-width//2)) #they wish
                finalStep = True
                            
    if canvas.collidepoint(mx, my):
        if mb[2] == 1:
            if tool == 'multiLine':
                screen.blit(upCopy, (392, 155))  #point the mouse has clicked on
                if len(lineList) > 2:
                    draw.line(screen, col, lineList[0], lineList[-1], thick)
                    lineList = []
                    upCopy = screen.subsurface(canvas).copy()

    screen.set_clip(None)
#-------------------------------------ENDING LOOP COMMANDS------------------------------------

    oldmx, oldmy = mx, my  #sets the current mouse coordinate as the previous mouse coordinate
    display.flip()
quit()
