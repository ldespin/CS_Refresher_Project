class Trajectory:
    def __init__(self,i):
        self.traj = []
        self.pairs=[]
        self.crossingPoints={}
        self.impactPoints = []
        self.num=i
    def addPoint(self, Point):
        self.traj.append(Point)

class Point:
    def __init__(self,a,b,ind):
        self.x = a
        self.y = b
        self.ind = ind
        
class PointImpact:
    def __init__(self,a,b,ind,indBox,border):
        self.x = a
        self.y = b
        self.ind = ind
        self.box = indBox
        self.border = border

class Trajectories:
    def __init__(self):
        self.trajectories = []

    def addTraj(self, Trajectory):
        self.trajectories.append(Trajectory)


class Box:
    def __init__(self,xmin,xmax,ymin,ymax,ind):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.ind=ind
        self.impactPoints = {"u": [], "b": [], "l": [], "r": []}

class AVGPoints:
    def __init__(self):
        self.AVGPoints=[]
