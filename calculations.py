import math
import turtle

def drawAxis(t):
    t.up()
    t.goto(-400,0)
    t.setheading(90)
    t.down()
    t.fd(80)
    t.bk(160)
    t.fd(80)
    t.setheading(0)
    t.fd(810)
    t.stamp()

    t.up()
    t.goto(-400,-200)
    t.down()
    t.setheading(90)

    t.fd(100)
    t.bk(200)
    t.fd(100)
    t.setheading(0)
    t.fd(810)
    t.stamp()

def getReaction(s_list:list,f_list:list)->list:
    # iterate thru all force to create 2 reaction force(simply/overhanging), cantiliver(1 reaction + 1 bending)
    reactions = []
    f1 = {} 
    f2 = {}
    if len(s_list) != 0: # if is simple or overhang beam
        clockwise_moment = 0
        for f in f_list:
            if f['type'] == 'PointWeight' or f['type'] == 'DistributedWeight': #calculate f1: clockwise moment = anticlockwise ones
                clockwise_moment += abs(f['f']) * f['position']
            else: #if is bending moment
                clockwise_moment += f['f']
        f1['type'] = 'PointWeight'
        f1['position'] = max(s_list)
        f1['f'] = clockwise_moment/max(s_list)

        f2['type'] = 'PointWeight'
        force = 0
        for f in f_list:
            if f['type'] == 'PointWeight' or f['type'] == 'DistributedWeight':
                force += f['f']
        f2['f'] = -1*force
        f2['f'] -= f1['f']
        f2['position'] = 0
    else: # if is a canteliver ( assume attacked right)
        f1['type'] = 'PointWeight'
        f1['f'] = 0
        f1['position'] = 20
        for f in f_list:
            f1['f'] -= f['f']
        
        f2['type'] = 'BendingMoment'
        anticlockwise_moment = 0
        for f in f_list:
            if f['type'] == 'DistributedWeight' or f['type'] == 'PointWeight':
                anticlockwise_moment += abs(f['f'])*(20-f['position'])
            else:
                anticlockwise_moment -= f['f']
        f2['f'] = anticlockwise_moment
        f2['position'] = 20
        
    reactions.append(f1)
    reactions.append(f2)
    return reactions

        

def processForces(f_list):
    # 0: name, 1:amount, 2:pos_list, 3:direction
    l1 = []
    for f in f_list:
        temp = {}
        if f[0] == 'PointWeight':
            temp['type'] = f[0]
            temp['f'] = -1*f[1]
            temp['position'] = f[2][0]
        elif f[0] == 'DistributedWeight':
            temp['type'] = f[0]
            temp['df'] = -1*f[1]
            temp['start'] = min(f[2])
            temp['end'] = max(f[2])
            temp['f'] = temp['df']*(temp['end'] - temp['start'])
            temp['position'] = temp['start']+((temp['end'] - temp['start'])/2)
        else:
            temp['type'] = f[0]
            temp['position'] = f[2][0]
            if f[3]:
                temp['f'] = f[1]
            else:
                temp['f'] = -1*f[1]
        l1.append(temp)
    return l1

def calc_shear_force(x,fList)->tuple:
    v = 0
    for f in fList:
        if f['type'] == 'PointWeight' and x>=f['position']:
            v+=f['f']
        elif f['type'] == 'DistributedWeight' and x>=f['start']:
            proportion = x-f['start']
            maximum = f['end']- f['start']
            v+= min(proportion,maximum)/maximum * f['f']
        elif f['type'] == 'BendingMoment':
            continue
    return x,v
    

def calc_bending_moment(x,v,fList)->tuple:
    m = 0
    for f in fList:
        if f['type'] == 'PointWeight' and x>f['position']:
            diff = x-f['position']
            m += f['f']*diff
        elif f['type'] == 'DistributedWeight' and x>f['start']:
            m += getDistributedWeightMoment(x,f) 
        elif f['type'] == 'BendingMoment' and x>=f['position']:
            m += f['f']
    return x,m

def getDistributedWeightMoment(x:float,f:dict):
    s = f['start']
    e = f['end']
    # since force is downwards-> always clockwise
    if x<e:
        dist = (x-s)/2
        fraction_length = (x-s)/(e-s)
        fraction_weight = fraction_length * f['f']
        return dist*fraction_weight

    dist = x-f['position']
    return dist*f['f']

def scale(l1,scale):
    temp = []
    xlist = []
    ylist = []
    for i in l1:
        xlist.append(i[0])
        ylist.append(i[1])
    xscale,yscale = scale
    for i in range(len(l1)):
        newy = ylist[i]*yscale
        newx = xlist[i]*xscale
        temp.append((newx,newy))
    return temp

def getMinMax(l1):
    # xlist = []
    ylist = []
    for i in l1:
        # xlist.append(i[0])
        ylist.append(i[1])
    maximum = max(ylist)
    minimum = min(ylist)
    return minimum,maximum

def getScale(l1):
    xlist = []
    ylist = []
    for i in l1:
        xlist.append(i[0])
        ylist.append(i[1])
    
    maxY = abs(max(ylist, key=abs))
    height_in_px = 70
    yscale = height_in_px/maxY
    xscale = 800/20

    return xscale,yscale


def drawDottedVisualization(offset:tuple,value:float,scale:tuple,t:turtle.Turtle):
    t.up()
    x,y = offset
    xscale,yscale = scale
    y += yscale*value
    t.goto(x,y)
    t.setheading(0)
    t.bk(40)
    t.write("{:.2f}".format(value),font=('Aerial',12,'normal'))
    t.fd(40)
    for i in range(100):
        if i%2 == 0:
            t.down()
            t.fd(8)
            t.up()
        else:
            t.fd(8)
    


    

def graphing(t:turtle.Turtle,sp,forces,offset:tuple):
    #  process forces 
    processed_force_list = processForces(forces)
    # get reaction forces
    reactions = getReaction(sp,processed_force_list)
    processed_force_list += reactions

    shear_force_points = []
    bending_moment_points = []
    x = 0.0
    end = 20.01
    while (x<end):
        res = calc_shear_force(x,processed_force_list)
        shear_force_points.append(res)
        res = calc_bending_moment(x,res[1],processed_force_list)
        bending_moment_points.append(res)
        x+=0.01
    minShear,maxShear = getMinMax(shear_force_points)
    minMoment,maxMoment = getMinMax(bending_moment_points)
    shearScale = getScale(shear_force_points)
    bendingScale = getScale(bending_moment_points)
    shear_force_points = scale(shear_force_points,shearScale)
    bending_moment_points = scale(bending_moment_points,bendingScale)

    # draw shear graph
    ox,oy = offset
    t.up()
    t.goto(shear_force_points[0][0]+ox,shear_force_points[0][1]+oy)
    t.down()
    for p in shear_force_points:
        t.goto(p[0]+ox,p[1]+oy)
    t.up()
    drawDottedVisualization((ox,oy),maxShear,shearScale,t)
    drawDottedVisualization((ox,oy),minShear,shearScale,t)

    # draw bending moment graph
    ox,oy = offset
    oy -= 200
    t.goto(bending_moment_points[0][0]+ox,bending_moment_points[0][1]+oy)
    t.down()
    for p in bending_moment_points:
        t.goto(p[0]+ox,p[1]+oy)
    t.up()
    drawDottedVisualization((ox,oy),maxMoment,bendingScale,t)
    drawDottedVisualization((ox,oy),minMoment,bendingScale,t)