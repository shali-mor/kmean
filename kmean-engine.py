import random
import math


"""

This is a pure Python implementation of the K-Means Clustering algorithmn. The
original can be found here:
http://pandoricweb.tumblr.com/post/8646701677/python-implementation-of-the-k-means-clustering

"""

plotly = False
try:
    import plotly
    from plotly.graph_objs import Scatter, Scatter3d, Layout
except ImportError:
    print "INFO: Plotly is not installed, plots will not be generated."


def handleKmeanRequest(jsonBody):
    body = json.loads(jsonBody)
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
            exit(0);
        points = []
        for i in xrange(pair_len):
            points.append(Point(user_pair_points[i]))
        print points

    else:
        points = [
        makeRandomPoint( lower, upper) for i in xrange(num_points)
        ]


    clusters = kmeans(points, k, epsilon)


    # Print our clusters
    for i, c in enumerate(clusters):
        print "\nCluster : " ,i ,"\t Centroid :",clusters[i].centroid
        for p in c.points:
            print "\t  ", p



    # Display clusters using plotly for 2d data
    print "Plotting points, launching browser ..."
    #plotClusters(clusters)


    return clusters


def makeRandomPoint( lower, upper):
    '''
    Returns a Point object with n dimensions and values between lower and
    upper in each of those dimensions
    '''
    p = Point([random.uniform(lower, upper) for _ in range(2)])
    return p


class Point(object):
    '''
    A point in n dimensional space
    '''
    def __init__(self, coords):
        '''
        coords - A list of values, one per dimension
        '''

        self.coords = coords
        self.n = len(coords)

    def __repr__(self):
        return str(self.coords)

class Cluster(object):
    '''
    A set of points and their centroid
    '''

    def __init__(self, points):
        '''
        points - A list of point objects
        '''

        if len(points) == 0:
            raise Exception("ERROR: empty cluster")

        # The points that belong to this cluster
        self.points = points

        # The dimensionality of the points in this cluster
        self.n = points[0].n

        # Assert that all points are of the same dimensionality
        for p in points:
            if p.n != self.n:
                raise Exception("ERROR: inconsistent dimensions")

        # Set up the initial centroid (this is usually based off one point)
        self.centroid = self.calculateCentroid()

    def __repr__(self):
        '''
        String representation of this object
        '''
        return str(self.points)

    def update(self, points):
        '''
        Returns the distance between the previous centroid and the new after
        recalculating and storing the new centroid.

        Note: Initially we expect centroids to shift around a lot and then
        gradually settle down.
        '''
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        shift = getDistance(old_centroid, self.centroid)
        return shift

    def calculateCentroid(self):
        '''
        Finds a virtual center point for a group of n-dimensional points
        '''
        numPoints = len(self.points)
        # Get a list of all coordinates in this cluster
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y'z etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = [math.fsum(dList)/numPoints for dList in unzipped]

        return Point(centroid_coords)

def kmeans(points, k, cutoff  ):

    # Pick out the first k points to use as our initial centroids
    initial = points[0:k]
    #initial = random.sample(points, k)
    print "initial is : "
    print initial
    # Create k clusters using those centroids
    # Note: Cluster takes lists, so we wrap each point in a list here.
    clusters = [Cluster([p]) for p in initial]

    # Loop through the dataset until the clusters stabilize
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

def getDistance(a, b):
    '''
    Euclidean distance between two n-dimensional points.
    https://en.wikipedia.org/wiki/Euclidean_distance#n_dimensions
    Note: This can be very slow and does not scale well
    '''
    if a.n != b.n:
        raise Exception("ERROR: non comparable points")

    accumulatedDifference = 0.0
    for i in range(a.n):
        squareDifference = pow((a.coords[i]-b.coords[i]), 2)
        accumulatedDifference += squareDifference
    distance = math.sqrt(accumulatedDifference)

    return distance



def plotClusters(data):
    '''
    This uses the plotly offline mode to create a local HTML file.
    This should open your default web browser.
    '''

    # Convert data into plotly format.
    traceList = []
    for i, c in enumerate(data):
        # Get a list of x,y coordinates for the points in this cluster.
        cluster_data = []
        for point in c.points:
            cluster_data.append(point.coords)

        trace = {}
        centroid = {}
        if 2 == 2:
            # Convert our list of x,y's into an x list and a y list.
            trace['x'], trace['y'] = zip(*cluster_data)
            trace['mode'] = 'markers'
            trace['marker'] = {}
            trace['marker']['symbol'] = i
            trace['marker']['size'] = 12
            trace['name'] = "Cluster " + str(i)
            traceList.append(Scatter(**trace))
            # Centroid (A trace of length 1)
            centroid['x'] = [c.centroid.coords[0]]
            centroid['y'] = [c.centroid.coords[1]]
            centroid['mode'] = 'markers'
            centroid['marker'] = {}
            centroid['marker']['symbol'] = i
            centroid['marker']['color'] = 'rgb(200,10,10)'
            centroid['name'] = "Centroid " + str(i)
            traceList.append(Scatter(**centroid))


    title = "K-means clustering with %s clusters - Microsoft assignment " % str(len(data))
    plotly.offline.plot({
        "data": traceList,
        "layout": Layout(title=title)
    })


import s_logger

import json
import time

# import threading
import os
import socket
from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
import subprocess




HOST_NAME = ''  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = int(os.getenv("USER_SIM_PORT", 5555))
USER_NAME = str(os.getenv("TEST_USER", "test-user"))
ENABLE_SSL = False


class recived_hedaer:
    name = ""
    value = ""


recived_hedaers = []

# ---------------------- parse command line parameters ------------------------



# --------------------------------
def sendResponse(s, status_code, body):
    s.send_response(status_code)
    content_length = len(body)

    s.send_header("Content-Length", str(content_length))
    s.send_header("Content-Type", "application/json")
    s.end_headers()
    s.wfile.write(body)


def obj_dict(obj):
    return obj.__dict__
class MyHandler(SimpleHTTPRequestHandler):
    def do_HEAD(s):
        s.protocol_version = "HTTP/1.1"
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()



    def do_GET(s):
        body = ""
        status_code = 403
        s_logger.log.info("GOT GET from = " + str(s.client_address))
        s.protocol_version = "HTTP/1.1"
        get_operation = s.path.strip('/')
        s_logger.log.info("required operation: " + get_operation)
        if (get_operation == "test_connection"):  # test connection
            body, status_code = "test" ,200
        elif (get_operation == "test_http"):
            body, status_code = "test" , 200
        # elif(get_operation == "userSim/get_num_new_devices"):
        #     filters = {"discovery_state" : "new"}
        #     body,status_code = GetNumDevices(filters)


        else:
            status_code = 403
            body = "Error in url path"

        sendResponse(s, status_code, body)

    def do_POST(s):
        body = ""
        status_code = 403
        s_logger.log.info("GOT POST from = " + str(s.client_address[0]))
        s.protocol_version = "HTTP/1.1"
        post_operation = s.path.strip('/')
        s_logger.log.info("required operation: " + post_operation)

        length = int(s.headers.getheader('content-length'))
        cluster_list = []
        if length:
            received_body = s.rfile.read(length)
            if ("kmean-calculation" in post_operation):
                res = handleKmeanRequest(received_body)
                print res

                body = json.dumps(res,default=obj_dict)
                status_code = 200
            elif (post_operation == "test"):
                status_code, body = 200, "test accepted"

            else:
                status_code = 403
                body = "Error in url path"
        else:
            status_code = 403
            body = "No length in headers"
        sendResponse(s, status_code, (json.dumps(body)))

    # this override will silent (no prints) the BaseHTTPServer
    def log_message(self, format, *args):
        return

    def do_PUT(s):
        body = ""
        status_code = 403
        s_logger.log.debug("GOT PUT from = " + str(s.client_address[0]))
        s.protocol_version = "HTTP/1.1"
        put_operation = s.path.strip('/')
        s_logger.log.debug("required operation: " + put_operation)

        length = int(s.headers.getheader('content-length'))
        if length:
            received_body = s.rfile.read(length)
            if (put_operation == "userSim/clear_ips_notifications"):
                global num_ips_completed_rules
                global num_recived_ips_alerts

                num_ips_completed_rules = 0
                num_recived_ips_alerts = 0
                status_code = 200
                body = "ips alerts counters were resest"
            else:
                status_code = 403
                body = "Error in url path"
        else:
            status_code = 403
            body = "No length in headers"
        sendResponse(s, status_code, body)




class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""



# ---------------------------------------------------------------------
#   server launch
# ---------------------------------------------------------------------

if __name__ == '__main__':

    # if(ENABLE_SSL == True):
    #     server_class = SecureHTTPServer
    #     httpd = server_class((HOST_NAME, PORT_NUMBER), SecureHTTPRequestHandler)
    # else:
    server_class = ThreadedHTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    s_logger.log.info(time.asctime() + "Server Starts - " + str(HOST_NAME) + ":" + str(PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        s_logger.log.debug("Ctrl-c received!")  # Sending kill to threads")

    httpd.server_close()
    s_logger.log.info(time.asctime() + "Server Stops - " + str(HOST_NAME) + ":" + str(PORT_NUMBER))
