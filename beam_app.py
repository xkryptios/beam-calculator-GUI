import turtle



def drawRectangle(t,start,width,height):
    t.up()
    t.setpos(start)
    t.setheading(0)
    t.down()

    t.fd(width)
    t.lt(90)
    t.fd(height)
    t.lt(90)
    t.fd(width)
    t.lt(90)
    t.fd(height)
    t.up()

def drawTriangle(t,start,color='white'):
    x,y = start
    length = 35
    t.up()
    t.setpos(x,y)
    t.down()
    t.setheading(240)
    t.fillcolor(color)
    t.begin_fill()
    t.fd(length)
    t.lt(120)
    t.fd(length)
    t.lt(120)
    t.fd(length)
    t.up()
    t.end_fill()

# def drawSupport(x,y):
#     t = turtle.Turtle() if reuse is None else reuse
#     t.hideturtle()
#     t.penup()
#     t.goto(x,y)
#     t.setheading(240)
#     t.pendown()
#     t.fillcolor('yellow')
#     t.begin_fill()
#     length = 35
#     t.fd(length)
#     t.lt(120)
#     t.fd(length)
#     t.lt(120)
#     t.fd(length)
#     t.up()
#     return t

def drawForce(t,force_list):
    t.clear()
    for force in force_list:
        if force[0] == 'PointWeight':
            drawPointWeight(t,force[1],force[2])
        elif force[0] == 'DistributedWeight':
            drawDistributedWeight(t,force[1],force[2])
        else:
            clockwise = force[3]
            if clockwise:
                drawBendingMoment(t,force[1],force[2],force[3])
            else:
                drawBendingMoment(t,force[1],force[2],force[3])

            

def drawPointWeight(t,weight,points):
    t.up()
    t.pencolor('black')
    x = -400 + 40* points[0] # points only has 1 element
    y = 200
    t.goto(x,y)
    t.setheading(270)
    t.down()
    t.stamp()
    t.bk(30)
    t.write(weight,font=('Aerial',12,'normal'),align='center')
    t.up()

def drawDistributedWeight(t,weight,points):
    # points is a list
    start_pos = min(points)
    end_pos = max(points)
    t.color('#0284c7')
    for i in range(start_pos,end_pos):
        if i == (start_pos+end_pos)//2:
            t.up()
            t.goto(-400+40*i,240)
            t.write(weight,font=('Aerial',12,'normal'),align='center')
        drawDistributedWeightBlock(t,i)

    t.up()

    pass

def drawBendingMoment(t:turtle.Turtle,weight,points,clockwise=True):
    t.up()
    point = points[0]
    x = -400+point*40
    y = 180
    t.goto(x,y)
    t.down()
    t.fillcolor('#22c55e')
    t.begin_fill()
    t.circle(2)
    t.end_fill()
    t.up()
    t.goto(x+6,y-10)
    t.color('#22c55e')
    if not clockwise:
        t.setheading(0)
        t.down()
        t.circle(12,180)
        t.stamp()
        t.up()
    else:
        t.setheading(230)
        t.goto(x+6,y-14)
        t.stamp()
        t.goto(x+6,y-10)
        t.setheading(0)
        t.down()
        t.circle(12,180)
        t.up()
    t.goto(x,y+25)
    txt = str(weight)+' Nm'
    t.write(txt,font=('Aerial',12,'normal'),align='center')
    t.color('black')



    

def drawSelectionIndicator(t,selectedPoint,color='red',text=''):
    x = -400 + selectedPoint*40
    y = 200

    t.up()
    t.goto(x,y)
    t.pencolor(color)
    t.down()
    t.setheading(270)
    t.stamp()
    t.bk(100)
    t.write(text,font=('Aerial',12,'normal'),align='center')
    t.up()

def addNewForce(new_force,force_list):
    # check if coinciding force
    templ = []
    for force in force_list:
        if hasIntersection(new_force[2],force[2]):
            templ.append(force)

    for force in templ:
        force_list.remove(force)

    force_list.append(new_force)


def drawBeam(t,window):
    # beam corners = (-400,200),(400,200)
    #                (-400,160),(400,160)
        
    width = 800
    height = 40
    startx = -400
    starty = 160
    drawRectangle(t,(-400,160),800,40)
    for i in range(startx,(startx+width),40):
        t.up()
        t.goto(i,starty)
        t.down()
        t.setheading(90)
        t.fd(height)
    window.update()

def drawDistributedWeightBlock(t,cell_num):
    i = min(cell_num,19)
    t.up()
    x = -400 + i*40
    y = 200
    t.goto(x,y)
    t.down()
    t.setheading(0)
    t.fillcolor('#0284c7')
    t.begin_fill()
    for i in range(4):
        t.fd(40)
        t.lt(90)
    t.end_fill()
    t.up()
    t.fillcolor('black')



def getBeamType():
    while True:
        type = input("""
        Choose type of beam:
        1. Simply Supported
        2. Overhanging supported
        3. Cantilever
        """)
        types = ['1','2','3']
        if type not in types:
            continue
        return int(type)

def writeInstruction(t:turtle.Turtle,supportReady:bool,saveReady:bool,selecting:bool,savedState:bool=False):
    t.clear()
    t.up()
    instruction = {
        'choosing_support':'Arrow Keys: Move the cursor     ENTER Key: Confirm second support location      Q:Quit',
        'selecting':'Arrow Keys: Move the cursor     Enter: Confirm range of Distributed Weight',
        'norm': 'Arrow Keys: Move the cursor     A: Add Point Weight     S: Add Distributed Weight     D: Add a Clockwise Moment\nF: Add a Anti-Clockwise Moment     P: Generate Graph',
        'saveReady' : 'O: Save current configuration     Q: Quit',
        'savedState': "File Saved Successfully! Enter 'Q' to QUIT",
        'base': "Enter Q to QUIT"
    }
    t.goto(-400,300)
    if savedState:
        t.write(instruction['savedState'],font=('Aerial',15,'normal'))
    elif saveReady:
        t.write(instruction['saveReady'],font=('Aerial',15,'normal'))
    elif not supportReady:
        t.write(instruction['choosing_support'],font=('Aerial',15,'normal'))
    elif selecting:
        t.write(instruction['selecting'],font=('Aerial',15,'normal'))
    else:
        t.write(instruction['norm'],font=('Aerial',15,'normal'))



    t = turtle.Turtle()
    t.hideturtle()
    t.up()
    t.goto(-400,0)
    instruction = ''
    t.write(instruction,font=('Aerial',30,'normal'))
    
def drawCantileverEdge(t:turtle.Turtle):
    t.up()
    t.goto(400,200)
    t.down()
    t.fillcolor('grey')
    t.begin_fill()
    t.goto(400,220)
    t.goto(420,220)
    t.goto(420,140)
    t.goto(400,140)
    t.goto(400,200)
    t.end_fill()
    t.up()
    t.color('black')

def hasIntersection(l1,l2):
    for element in l1:
        if element in l2:
            return True
    return False
