import functions as f
import classes_traj as t
import matplotlib.pyplot as plt
import os
import csv
import re

#Paramamters:

K = 5
set="TESTS/Test5/"


#We start by defining our list of trajectories, from the dataset
list_traj = t.Trajectories()

i=1
for file in os.listdir(set):
    with open(set+file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ')
        traj=t.Trajectory(i)
        j=0
        for row in spamreader:
            traj.addPoint(t.Point(float(row[0]),float(row[1]),j))
            j+=1
        list_traj.addTraj(traj)
    i+=1


#Construction of the environment (first box)
(xmin, xmax, ymin, ymax) = f.initBox(list_traj)

#Subdivision with respect to the K parameter
boxes = f.createBoxes(xmin, xmax, ymin, ymax, K)

plt.axvline(xmin,color = 'green')
plt.axvline(xmax,color = 'green')
plt.axhline(ymin,color = 'green')
plt.axhline(ymax,color = 'green')

for i in boxes:
    plt.axvline(boxes[i].xmin, color = 'green', linewidth = 0.7)
    plt.axvline(boxes[i].xmax, color = 'green', linewidth = 0.7)
    plt.axhline(boxes[i].ymin, color = 'green', linewidth = 0.7)
    plt.axhline(boxes[i].ymax, color = 'green', linewidth = 0.7)

    

for traj in list_traj.trajectories:
    f.crossingPoints(boxes,traj)

for traj in list_traj.trajectories:
    f.defImpactPoints(boxes,traj)

for traj in list_traj.trajectories:
    f.consTraj(boxes,traj,K)

    #To plot the starting trajectories:
    #plt.plot([P.x for P in traj.traj],[P.y for P in traj.traj])

    #To plot the new trajectories:
    #
    plt.plot([P.x for P in traj.impactPoints],[P.y for P in traj.impactPoints], color = 'blue')

    #To plot the impact points
    plt.scatter([P.x for P in traj.impactPoints],[P.y for P in traj.impactPoints],color='red')


plt.show()