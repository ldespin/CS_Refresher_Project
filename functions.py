import classes_traj as t
import numpy as np
import matplotlib.pyplot as plt


#We define the coordinates of the first box, considering our set of trajectories
def initBox(listTraj):
    xmin = listTraj.trajectories[0].traj[0].x
    xmax = listTraj.trajectories[0].traj[0].x
    ymin = listTraj.trajectories[0].traj[0].y
    ymax = listTraj.trajectories[0].traj[0].y
    for j in listTraj.trajectories:
        for k in j.traj:
            if (k.x<xmin):
                xmin = k.x
            elif (k.x>xmax):
                xmax = k.x
            if (k.y<ymin):
                ymin = k.y
            elif (k.y>ymax):
                ymax = k.y
    return [xmin, xmax, ymin, ymax]


#We define a function that create our boxes, depending on the subdivision parameter K
def createBoxes(xmin, xmax, ymin, ymax, K):
    boxes = {}
    x_len = (xmax-xmin)/K
    y_len = (ymax-ymin)/K
    xbox_min = xmin
    xbox_max = xmin + x_len
    ybox_min = ymin
    ybox_max = ymin + y_len
    i = 1
    for j in range(K):
        for k in range(K):
            boxes[i] = t.Box(xbox_min+k*x_len,xbox_max+k*x_len,ybox_min+j*y_len,ybox_max+j*y_len,i)
            i+=1
    return boxes


#For a chosen box and a chosen trajectory, we spot the points where the trajectory crosses one of the borders of the box
#We return a List which contains pairs of points (one in the box and one outside), and the value -1 or 1 (1 if the trajectory is entering the box, -1 if not) 

def crossingPoints(boxes,Traj):
    t = Traj.traj
    # We store in L all pairs of points which defines an entry or an out of the box
    #If one point is outside the box and the next one is inside, we have a spot where the trajectory in entering
    #If one point is inside the box and the next one is outside, we have a spot where the trajectory in going out
    for i in range(len(t)-1) : 
        for j in boxes:
            Box=boxes[j]
            if t[i].x <= Box.xmax and t[i].x >= Box.xmin and t[i].y <= Box.ymax and t[i].y >= Box.ymin :
                if t[i+1].x >= Box.xmax or t[i+1].x <= Box.xmin or t[i+1].y >= Box.ymax or t[i+1].y <= Box.ymin :
                    Traj.pairs.append([t[i],t[i+1],j,"out"])

            else : 
                if t[i+1].x >= Box.xmin and t[i+1].x <= Box.xmax and t[i+1].y >= Box.ymin and t[i+1].y <= Box.ymax :
                    Traj.pairs.append([t[i],t[i+1],j,"in"])
    pass

#After we created the list with crossingPoints(), we can determine the point where the trajectory crosses the box, and the border it crosses

def defImpactPoints(boxes,Traj):
    L = Traj.pairs
    for i in range(len(L)-1):
        if L[i][0].ind==L[i+1][0].ind and L[i][-1]=="in":
            L[i],L[i+1]=L[i+1],L[i]


    for pair in L:
        P1 = pair[0]
        P2 = pair[1]
        Box=boxes[pair[2]]

        A=t.Point(Box.xmin, Box.ymin, None)
        B=t.Point(Box.xmax, Box.ymin, None)
        C=t.Point(Box.xmax, Box.ymax, None)
        D=t.Point(Box.xmin, Box.ymax, None)
        
        #if the two points of a pair have the same x coordinates, we won't be able to compute the intersection with the box, so we must define it here
        #the intersection point will have the same x coordinates as P1 and P2, and its y coordinate will be ymin or ymax of the box
        if P1.x==P2.x:
            if min(P1.y,P2.y)<=Box.ymax and max(P1.y,P2.y)>=Box.ymax:
                y_impact = Box.ymax
                border='u'
            else:
                y_impact = Box.ymin
                border='b'
            x_impact = P1.x
        
        #same reasonning with the same y coordinates
        elif P1.y==P2.y:
            if min(P1.x,P2.x)<=Box.xmax and max(P1.x,P2.x)>=Box.xmax:
                x_impact = Box.xmax
                border='r'
            else:
                x_impact = Box.xmin
                border='l'
            y_impact = P1.y
        
        #In the other cases, we compute the intersection point with every border of the box, and we deduce the one that is appropriate
        elif defInter(P1, P2, A, B)[0]<=max(P1.x,P2.x) and defInter(P1, P2, A, B)[0]>=min(P1.x,P2.x) and defInter(P1, P2, A, B)[0]<=Box.xmax and defInter(P1, P2, A, B)[0]>=Box.xmin :
            #Intersection with the bottom border
            x_impact = defInter(P1, P2, A, B)[0]
            y_impact = Box.ymin
            border = 'b'
        elif defInter(P1, P2, D, C)[0]<=max(P1.x,P2.x) and defInter(P1, P2, D, C)[0]>=min(P1.x,P2.x) and defInter(P1, P2, D, C)[0]<=Box.xmax and defInter(P1, P2, D, C)[0]>=Box.xmin :
            #Intersection with the upper border
            x_impact = defInter(P1, P2, D, C)[0]
            y_impact = Box.ymax
            border = 'u'
        elif defInter(P1, P2, B, C)[1]<=max(P1.y,P2.y) and defInter(P1, P2, B, C)[1]>=min(P1.y,P2.y) and defInter(P1, P2, B, C)[1]<=Box.ymax and defInter(P1, P2, B, C)[1]>=Box.ymin :
            #Intersection with the right border
            x_impact = Box.xmax
            y_impact = defInter(P1, P2, B, C)[1]
            border = 'r'
        elif defInter(P1, P2, A, D)[1]<=max(P1.y,P2.y) and defInter(P1, P2, A, D)[1]>=min(P1.y,P2.y) and defInter(P1, P2, A, D)[1]<=Box.ymax and defInter(P1, P2, A, D)[1]>=Box.ymin :
            #Intersection with the left border
            x_impact = Box.xmin
            y_impact = defInter(P1, P2, A, D)[1]
            border = 'l'

        #We define the impact point its index in the trajectory

        P_impact=t.PointImpact(x_impact,y_impact, P1.ind, Box.ind, border)

        #We add it to the list of impact points of the trajectory

        Traj.impactPoints.append(P_impact)

        #We add this point in the list of impact points of the box
        Box.impactPoints[border].append(P_impact)
        pass

#We define a function that returns the coordinates of the intersection of two lines defined by four points
def defInter(A, B, C, D):
    if C.x==D.x:
        x_inter = C.x
        y_inter = (B.y-A.y)/(B.x-A.x)*(x_inter-A.x)+A.y
    elif C.y==D.y:
        y_inter = C.y
        x_inter = (B.x-A.x)/(B.y-A.y)*(y_inter-A.y)+A.x
    return [x_inter, y_inter]

#for every box, we compute the average coordinates of the intersection points of each border
def AvgPoints(boxes,K):
    lAVGPoints = t.AVGPoints().AVGPoints
    for i in boxes:
        Box=boxes[i]
        for border in Box.impactPoints:
            if border=='u':
                if i<=K*(K-1):
                    x_avg = np.mean([P.x for P in Box.impactPoints[border]]+[P.x for P in boxes[i+K].impactPoints['b']])
                    y_avg = np.mean([P.y for P in Box.impactPoints[border]]+[P.y for P in boxes[i+K].impactPoints['b']])
                else:
                    x_avg = np.mean([P.x for P in Box.impactPoints[border]])
                    y_avg = np.mean([P.y for P in Box.impactPoints[border]])
            elif border=='b':
                if i>K:
                    x_avg = np.mean([P.x for P in Box.impactPoints[border]]+[P.x for P in boxes[i-K].impactPoints['u']])
                    y_avg = np.mean([P.y for P in Box.impactPoints[border]]+[P.y for P in boxes[i-K].impactPoints['u']])
                else:
                    x_avg = np.mean([P.x for P in Box.impactPoints[border]])
                    y_avg = np.mean([P.y for P in Box.impactPoints[border]])
            elif border=='r':
                if i%K!=0:
                    x_avg = np.mean([P.x for P in Box.impactPoints[border]]+[P.x for P in boxes[i+1].impactPoints['l']])
                    y_avg = np.mean([P.y for P in Box.impactPoints[border]]+[P.y for P in boxes[i+1].impactPoints['l']])
                else:
                    x_avg = np.mean([P.x for P in Box.impactPoints[border]])
                    y_avg = np.mean([P.y for P in Box.impactPoints[border]])
            else :
                if i%K!=1:
                    x_avg = np.mean([P.x for P in Box.impactPoints[border]]+[P.x for P in boxes[i-1].impactPoints['r']])
                    y_avg = np.mean([P.y for P in Box.impactPoints[border]]+[P.y for P in boxes[i-1].impactPoints['r']])
                else:
                    x_avg = np.mean([P.x for P in Box.impactPoints[border]])
                    y_avg = np.mean([P.y for P in Box.impactPoints[border]])
            lAVGPoints.append(t.PointImpact(x_avg,y_avg,None,Box.ind,border))
    return lAVGPoints

def consTraj(boxes,Traj,K):
    lAVGPoints = AvgPoints(boxes,K)
    for i in range(len(Traj.impactPoints)):
        for P in lAVGPoints:
            if Traj.impactPoints[i].border==P.border and Traj.impactPoints[i].box==P.box:
                Traj.impactPoints[i]=P
    pass