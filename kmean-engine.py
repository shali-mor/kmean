
import random

from client_consul.cluster import *
from client_consul.point  import Point

import json
import os

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn


"""

This is a pure Python implementation of the K-Means Clustering algorithmn. The
original can be found here:
http://pandoricweb.tumblr.com/post/8646701677/python-implementation-of-the-k-means-clustering

"""

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
            return None
        points = []
        for i in xrange(pair_len):
            points.append(Point(user_pair_points[i]))
        print points

    else:
        points = [
            makeRandomPoint( lower, upper) for i in xrange(num_points)
        ]

    clusters = kmeans(points, k, epsilon)

    printClusters(clusters)



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

    def do_POST(s):
        body = ""
        status_code = 403
        print("GOT POST from = " + str(s.client_address[0]))
        s.protocol_version = "HTTP/1.1"
        post_operation = s.path.strip('/')
        print("required operation: " + post_operation)

        length = int(s.headers.getheader('content-length'))
        cluster_list = []
        if length:
            received_body = s.rfile.read(length)

            res = handleKmeanRequest(received_body)
            print res
            if res is None:
                status_code = 500
                body = "can't calculate kmean"

            else :
                body = json.dumps(res,default=obj_dict)
                status_code = 200
        else:
            status_code = 403
            body = "No length in headers"

        sendResponse(s, status_code, (json.dumps(body)))


    def do_PUT(s):
        body = "Put not supported"
        status_code = 403

        sendResponse(s, status_code, body)


    def do_GET(s):
        body = "Get not supported"
        status_code = 403
        sendResponse(s, status_code, body)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""



HOST_NAME = ''  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = int(os.getenv("KMEAN_PORT", 5555))


# ---------------------------------------------------------------------
#   server launch
# ---------------------------------------------------------------------

if __name__ == '__main__':

    server_class = ThreadedHTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    print("Server Starts - " + str(HOST_NAME) + ":" + str(PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Ctrl-c received!")  # Sending kill to threads")

    httpd.server_close()
    print("Server Stops - " + str(HOST_NAME) + ":" + str(PORT_NUMBER))
