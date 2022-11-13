def getBeamType():
    ans = ['1','2','3']
    while True:
        res = input('''
Select a Beam Configuration
1) Simply Supported Beam
2) Over-hanging Beam
3) Cantilever Beam
''')
        return res
    
def isLoadFile():
    t = '''
Selection Option:
1)Load a New Beam from scratch
2)Load a file in the same directory
'''
    ans = ['1','2']
    while True:
        res = input(t)
        if res in ans:
            return res == '2'

def loadGraph():
    p_list = []
    f_list = []
    beamType = None
    filename = 'UserInput.txt'
    with open(filename,'r') as f:
        res = f.readline()
        if res == 'User Configs':
            print('No Valid file to load!')
            return None
        beamType = int(f.readline().strip())
        line = f.readline().strip()
        count = int(line)
        for i in range(count):
            line = f.readline().strip()
            p_list.append(int(line))
        line = f.readline().strip()
        count = int(line)
        for i in range(count):
            t = f.readline().strip()
            force = float(f.readline().strip())
            pos_str = list(f.readline().strip().split())
            pos = []
            for i in pos_str:
                pos.append(int(i))
            if t == 'BendingMoment':
                res = f.readline().strip()
                clock = True
                if res == '1':
                    clock = True
                else:
                    clock = False
                f_list.append((t,force,pos,clock))
                continue
            f_list.append((t,force,pos))
    return beamType,p_list,f_list
        



        



def saveGraph(beamType:int,p_list:list,f_list:list):
    filename = 'UserInput.txt'
    with open(filename,'w') as f:
        f.write('User Configs\n')
        f.write(str(beamType)+'\n')
        f.write(str(len(p_list))+'\n')
        for i in p_list:
            f.write(str(i)+'\n')
        f.write(str(len(f_list))+'\n')# num of force
        for i in f_list:
            f.write(str(i[0])+'\n') #type
            f.write(str(i[1])+'\n') #magnitude
            for pos in i[2]:
                f.write(str(pos)+' ')
            f.write('\n')
            if i[0] == 'BendingMoment':
                if i[3]:
                    f.write('1\n')
                else:
                    f.write('0\n')
