# Fit the data into the DBSCAN model
import queue
from queue import *
import numpy as np

class DBSCAN:

  def __init__(self,MinPt,Eps):
    self.MinPt=MinPt
    self.Eps=Eps

  def neighbour_points(self,data, pointId, epsilon):
        points = []
        for i in range(len(data)):
        # Euclidian distance
            if np.linalg.norm([a_i - b_i for a_i, b_i in zip(data[i], data[pointId])]) <= epsilon:
                points.append(i)
        return points


  def update_dbscan_fit(self,data, Eps, MinPt):

    # initialize all points as outliers
    point_label = [0] * len(data)
    point_count = []

    # initilize list for core/border points
    core = []
    border = []

    # Find the neighbours of each individual point
    for i in range(len(data)):
        point_count.append(self.neighbour_points(data, i, Eps))

    # Find all the core points, border points and outliers
    for i in range(len(point_count)):
        if (len(point_count[i]) >= MinPt):
            point_label[i] = core
            core.append(i)
        else:
            border.append(i)

    for i in border:
        for j in point_count[i]:
            if j in core:
                point_label[i] = border
                break

    # Assign points to a cluster

    cluster = 1

    # Here we use a queue to find all the neighbourhood points of a core point and find the
    # indirectly reachable points.
    # We are essentially performing Breadth First search of all points which are within
    # epsilon distance from each other
    for i in range(len(point_label)):
        q = queue.Queue()
        if (point_label[i] ==core):
            point_label[i] = cluster
            for x in point_count[i]:
                if(point_label[x] == core):
                    q.put(x)
                    point_label[x] = cluster
                elif(point_label[x] == border):
                    point_label[x] = cluster
            while not q.empty():
                neighbors = point_count[q.get()]
                for y in neighbors:
                    if (point_label[y] == core):
                        point_label[y] = cluster
                        q.put(y)
                    if (point_label[y] == border):
                        point_label[y] = cluster
            cluster += 1  # Move on to the next cluster

    return point_label, cluster