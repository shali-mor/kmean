
import random
from cluster import *
from point import Point

import json
import os


"""

This is a pure Python implementation of the K-Means Clustering algorithmn. The
original can be found here:
http://pandoricweb.tumblr.com/post/8646701677/python-implementation-of-the-k-means-clustering

"""

def handleKmeanRequest(jsonBody):
    body = jsonBody
    number_of_points  = body["number_of_points"]
    user_pair_points = body["user_pair_points"]
    k = body["k"]
    epsilon = body["epsilon"]
    lower = body["min_boundry"]
    upper = body["max_boundry"]
    # Generate some points to cluster

    num_points = number_of_points


    if (user_pair_points is not None):
        pair_len = len(user_pair_points)
        if (k > pair_len):
            print ("number of cluster " + str(k) + " is bigger than the number of pairs" + str(pair_len))
            return None
        points = []
        for i in xrange(pair_len):
            points.append(Point(user_pair_points[i]))
        print points

    else:
        points = [
            makeRandomPoint( lower, upper) for i in xrange(num_points)
        ]

    print("k  = " + str(k))

    print("lower bound = " + str(lower))
    print("upper bound = " + str(upper))
    print("number of sampels  = " + str(number_of_points))

    print("num of clusters = "+str(k))

    print("epsilon = " + str(epsilon))

    clusters=kmeans(points, k, epsilon)


    printClusters(clusters)

    return clusters


def makeRandomPoint( lower, upper):
    '''
    Returns a Point object with n dimensions and values between lower and
    upper in each of those dimensions
    '''
    p = Point([random.uniform(lower, upper) for _ in range(2)])
    return p



def kmeans(points, k, cutoff  ):

    # Pick out the first k points to use as our initial centroids
    initial = points[0:k]
    # in case same input is recieved , we would like to get the same resuls , thus , we'll use the const initials.
    #initial = random.sample(points, k)
    # Create k clusters using those centroids
    # Note: Cluster takes lists, so we wrap each point in a list here.
    clusters = [Cluster([p]) for p in initial]

    # Loop through the data set until the clusters stabilize
    loopCounter = 0
    while True:
        # Create a list of lists to hold the points in each cluster
        lists = [[] for _ in clusters]
        clusterCount = len(clusters)

        # Start counting loops
        loopCounter += 1
        # For every point in the dataset ...
        for p in points:
            # Get the distance between that point and the centroid of the first
            # cluster.
            smallest_distance = getDistance(p, clusters[0].centroid)

            # Set the cluster this point belongs to
            clusterIndex = 0

            # For the remainder of the clusters ...
            for i in range(clusterCount - 1):
                # calculate the distance of that point to each other cluster's
                # centroid.
                distance = getDistance(p, clusters[i+1].centroid)
                # If it's closer to that cluster's centroid update what we
                # think the smallest distance is
                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex = i+1
            # After finding the cluster the smallest distance away
            # set the point to belong to that cluster
            lists[clusterIndex].append(p)

        # Set our biggest_shift to zero for this iteration
        biggest_shift = 0.0

        # For each cluster ...
        for i in range(clusterCount):
            # Calculate how far the centroid moved in this iteration
            shift = clusters[i].update(lists[i])
            # Keep track of the largest move from all cluster centroid updates
            biggest_shift = max(biggest_shift, shift)

        # If the centroids have stopped moving much, say we're done!
        if biggest_shift < cutoff:
            print "Converged after %s iterations" % loopCounter
            break
    return clusters




def obj_dict(obj):
    return obj.__dict__


# ---------------------------------------------------------------------
#   server launch
# ---------------------------------------------------------------------

postreqdata = json.loads(open(os.environ['req']).read())
print postreqdata

res = handleKmeanRequest(postreqdata)
print res
if res is None:
    status_code = 500
    body = "can't calculate kmean"
else :
    body = json.dumps(res,default=obj_dict)
    status_code = 200

#sendResponse(s, status_code, (json.dumps(body)))


response = open(os.environ['res'], 'w')
response.write(json.dumps(body))
response.close()

