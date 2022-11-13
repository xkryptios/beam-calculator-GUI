import turtle
from beam_app import drawBeam,drawRectangle,drawTriangle,getBeamType,drawCantileverEdge,writeInstruction,drawSelectionIndicator,drawForce,addNewForce
from calculations import drawAxis,graphing
from utility import saveGraph,loadGraph,isLoadFile

beamTypeList = ['','Simply Support Beam','Over-hanging Beam','Cantilever']

beamType = 0
selectedPoint = 0


supportReady = False
saveReady = False
distributedWeightSelectionState = False
support_position = []
tempList = []


# a dictionary used to store force on each point on beam
force_list = []
# format of a force = ['forceType',amount,[points],direction]

t = turtle.Turtle()
t.hideturtle()
selection_t = turtle.Turtle()
selection_t.hideturtle()
instruction_t = turtle.Turtle()
instruction_t.hideturtle()
force_t = turtle.Turtle()
force_t.hideturtle()
temp_t = turtle.Turtle()
temp_t.hideturtle()

window = None


def selectLeft():

    if saveReady: # if already displayed graph, no need to have selected Cell
        return

    global selectedPoint

    if not supportReady: # == if placing second supporting pivot
        newSelectedPoint = selectedPoint - 1
        if newSelectedPoint >= 1 and newSelectedPoint <= 20:
            selection_t.clear()
            drawSelectionIndicator(selection_t,newSelectedPoint)
            selectedPoint = newSelectedPoint
    else:
        newSelectedPoint = selectedPoint - 1 
        if newSelectedPoint >= 0 and newSelectedPoint<=19:
            selection_t.clear()
            drawSelectionIndicator(selection_t,newSelectedPoint)
            selectedPoint = newSelectedPoint
    writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)

def selectRight():
    if saveReady: # if already displayed graph, no need to have selected Cell
        return
    
    global selectedPoint

    if not supportReady: # == if placing second supporting pivot
        # need to limit selector reach cell 0
        newSelectedPoint = selectedPoint + 1
        if newSelectedPoint >= 1 and newSelectedPoint <= 20:
            selection_t.clear()
            drawSelectionIndicator(selection_t,newSelectedPoint)
            selectedPoint = newSelectedPoint
    else:
        newSelectedPoint = selectedPoint + 1
        if newSelectedPoint >= 0 and newSelectedPoint<=20:
            selection_t.clear()
            drawSelectionIndicator(selection_t,newSelectedPoint)
            selectedPoint = newSelectedPoint
    writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)

def drawGraph():
    global saveReady
    if not supportReady or distributedWeightSelectionState:
        return
    saveReady = True
    # force_list,sp_list
    selection_t.clear()
    drawAxis(t)
    graphing(t,support_position,force_list,(-400,0))
    writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)
    window.update()

def addPointWeight():
    if not supportReady or saveReady:
        return

    weight = turtle.numinput("Add Point Weight", "Enter Force(F) on Current Point")
    if weight is not None:
        new_force = ('PointWeight',weight,[selectedPoint])
        addNewForce(new_force,force_list)
        drawForce(force_t,force_list)
    window.listen()

    pass

def addDistributedWeight():
    global distributedWeightSelectionState
    if not supportReady or saveReady:
        return
    elif not distributedWeightSelectionState:
        distributedWeightSelectionState = True
        drawSelectionIndicator(temp_t,selectedPoint,text='START')
        tempList.append(selectedPoint)

    writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)


def addClockWiseBendingMoment():
    if not supportReady or saveReady:
        return
    
    weight  = turtle.numinput("Add Bending Moment", "Enter Bending Moment(N*M)")
    if weight is not None:
        new_force = ('BendingMoment',weight,[selectedPoint],True)
        addNewForce(new_force,force_list)
        drawForce(force_t,force_list)
    writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)
    window.listen()

def addAntiClockWiseBendingMoment():
    if not supportReady or saveReady:
        return    
    weight  = turtle.numinput("Add Bending Moment", "Enter Bending Moment(N*M)")
    if weight is not None:
        new_force = ('BendingMoment',weight,[selectedPoint],False)
        addNewForce(new_force,force_list)
        drawForce(force_t,force_list)
    writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)
    window.listen()


def confirmSelection():
    global supportReady
    global distributedWeightSelectionState
    if saveReady:
        return
    elif not supportReady: # add in a support at given place
        startx = -400 + selectedPoint*40
        starty = 158
        drawTriangle(t,(startx,starty))
        # clear all selection triangles
        supportReady = True
        support_position.append(selectedPoint)
        writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)
        return
    elif distributedWeightSelectionState:
        if selectedPoint not in tempList:
            tempList.append(selectedPoint)
            high = max(tempList)
            low = min(tempList)
            for i in range(low+1,high):
                tempList.append(i)
            distributedWeightSelectionState = False
            weight = turtle.numinput("Add Distributed Weight", "Enter Force(F)")
            newforce = ('DistributedWeight',weight,tempList.copy())
            addNewForce(newforce,force_list)
            tempList.clear()
            temp_t.clear()
            drawForce(force_t,force_list)
            window.listen()
            writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)

            return
    writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)
    return

def saveGraphHandler():
    if not saveReady:
        return
    saveGraph(beamType,support_position,force_list)
    writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState,True)
    print("Graph saved in UserInput.txt successfully!")

def exitHandler():
    window.bye()
    exit()

def drawApp(beamType):
    drawBeam(t,window)
    t.up()
    t.goto(0,380)
    t.write(beamTypeList[beamType],align='center',font=('Aerial',18,'normal'))
    if beamType != 3:
        drawTriangle(t,(-400,158))
        x = -400+ support_position[1]*40
        drawTriangle(t,(x,158))
    else:
        drawCantileverEdge(t)
    drawForce(force_t,force_list)
    drawGraph()

    t.up()
    t.goto(-400,400)
    t.write('Press Q to QUI',font=('Aerial',30,'normal'))
    writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)




def initialiseScreen(beamType):
    drawBeam(t,window)
    t.up()
    t.goto(0,380)
    t.write(beamTypeList[beamType],align='center',font=('Aerial',18,'normal'))


    if beamType == 1:
        drawTriangle(t,(-400,158))
        drawTriangle(t,(400,158))
        drawSelectionIndicator(selection_t,selectedPoint)

    elif beamType == 2:
        drawTriangle(t,(-400,158))
        drawSelectionIndicator(selection_t,selectedPoint)
    else:
        drawSelectionIndicator(selection_t,selectedPoint)
        writeInstruction()

    writeInstruction(instruction_t,supportReady,saveReady,distributedWeightSelectionState)


def main():
    global t
    global selection_t
    global instruction_t
    global force_t
    global temp_t
    global window
    global supportReady
    global selectedPoint
    global support_position
    global force_list
    global saveReady

    load = None
    beamType = None

    while True:
        load = isLoadFile()
        if load:
            files = loadGraph()
            if files is not None:
                beamType,support_position,force_list = files
                saveReady = True
                # straightaway draw everything
                break
        else:
            break

    # create window and turtle objects used
    window = turtle.Screen()
    window.setup(width=900,height=1000,startx=0,starty=0)
    window.tracer(0)
    t = turtle.Turtle()
    t.hideturtle()
    selection_t = turtle.Turtle()
    selection_t.hideturtle()
    instruction_t = turtle.Turtle()
    instruction_t.hideturtle()
    force_t = turtle.Turtle()
    force_t.hideturtle()
    temp_t = turtle.Turtle()
    temp_t.hideturtle()

    
    if load:
        supportReady = True
        drawApp(beamType)

    else:
        beamType = getBeamType()

        if beamType == 1:
            supportReady = True
            support_position.append(0)
            support_position.append(20)
        elif beamType == 2:
            selectedPoint =1
            support_position.append(0)
        else:
            supportReady = True

        initialiseScreen(beamType)
        window.onkey(selectLeft,'Left')
        window.onkey(selectRight,'Right')
        window.onkey(confirmSelection,'Return')
        window.onkey(addPointWeight,'a')
        window.onkey(addDistributedWeight,'s')
        window.onkey(addClockWiseBendingMoment,'d')
        window.onkey(addAntiClockWiseBendingMoment,'f')
        window.onkey(drawGraph,'p')
        window.onkey(saveGraphHandler,'o')
        
    window.onkey(exitHandler,'q')
    window.listen()
    window.mainloop()
        
    
        
    
    # saveGraph([],[])
    # loadGraph()



    





    # drawBeam(t,window)


if __name__ == '__main__':
    main()