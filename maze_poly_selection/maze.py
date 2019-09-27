import c4d
from c4d import gui
import random
from c4d import utils

def main():

    ppos = []
    col = 0
    obj = doc.GetActiveObject()
    if not obj:
        return
    if obj.GetType() == 5168:
        c4d.CallCommand(16768, 16768)
        obj = doc.GetActiveObject()

    cnt = obj.GetPolygonCount()
    sel = obj.GetPolygonS()
    sel.DeselectAll()
    poly = obj.GetAllPolygons()

    for p in poly:
        ppos.append([obj.GetPoint(p.a),
                    obj.GetPoint(p.b),
                    obj.GetPoint(p.c),
                    obj.GetPoint(p.d)])

    xcur = 0
    xmax = 0

    for i in range(len(ppos)):
        xcur = ppos[i][0].x
        xmax = ppos[i+1][0].x
        #print xcur, xmax

        if xcur > xmax:
            col = i+1
            break

    row = cnt/col

    selM = [range(cnt)[i:i+row] for i in range(0, len(range(cnt)), row)]
    maze = [[0 for x in range(row)] for y in range(col)]

    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0] # 4 directions to move in the maze

    # start the maze from a random cell
    cx = random.randint(0, row - 1)
    cy = random.randint(0, col - 1)
    maze[cy][cx] = 1
    stack = [(cx, cy, 0)] # stack element: (x, y, direction)

    while len(stack) > 0:
        (cx, cy, cd) = stack[-1]
        # to prevent zigzags:
        # if changed direction in the last move then cannot change again
        if len(stack) > 2:
            if cd != stack[-2][2]: dirRange = [cd]
            else: dirRange = range(4)
        else: dirRange = range(4)

        # find a new cell to add
        nlst = [] # list of available neighbors
        for i in dirRange:
            nx = cx + dx[i]; ny = cy + dy[i]
            if nx >= 0 and nx < row and ny >= 0 and ny < col:
                if maze[ny][nx] == 0:
                    ctr = 0 # of occupied neighbors must be 1
                    for j in range(4):
                        ex = nx + dx[j]; ey = ny + dy[j]
                        if ex >= 0 and ex < row and ey >= 0 and ey < col:
                            if maze[ey][ex] == 1: ctr += 1
                    if ctr == 1: nlst.append(i)

        # if 1 or more neighbors available then randomly select one and move
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]; cy += dy[ir]; maze[cy][cx] = 1
            stack.append((cx, cy, ir))
        else: stack.pop()

    print len(selM)
    print len(selM[0])
    print len(maze)
    print len(maze[0])
    for x in range(len(selM)):


        for z in range(len(selM[x])):
            if maze[x][z] == 1:
                sel.Select(selM[x][z])

    c4d.EventAdd()

    #print col







if __name__=='__main__':
    main()
