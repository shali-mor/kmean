"""
# Full Imports


This is a pure Python implementation of the K-Means Clustering algorithmn. The
original can be found here:
http://pandoricweb.tumblr.com/post/8646701677/python-implementation-of-the-k-means-clustering

"""

import sys, getopt, os, json
import requests
plotly = False
try:
    import plotly
    from plotly.graph_objs import Scatter, Scatter3d, Layout
except ImportError:
    print "INFO: Plotly is not installed, plots will not be generated."



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

    def __init__(self, points,centroid):
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
        self.centroid = centroid

    def __repr__(self):
        '''
        String representation of this object
        '''
        return str(self.points)

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

class kmean_consul(json.JSONEncoder):
    def __init__(self, num_of_cluster, min_boundry, max_boundry,epsilon,number_of_points, dst_ip, user_pair_points):
        self.k = num_of_cluster
        self.min_boundry = min_boundry
        self.max_boundry =  max_boundry
        self.number_of_points = number_of_points
        self.epsilon = epsilon
        self.dst_ip = dst_ip
        self.user_pair_points = user_pair_points

def post_request(mean_obj):
    url = "http://127.0.0.1:5555/kmean-calculation"
    r = requests.post(url, data=json.dumps(mean_obj.__dict__), timeout=30)
    if (r.status_code != 200 and r.status_code != 201):
        print r.text, r.status_code
        return False

    print "Response received , build relevent cluster : "
    response = eval(json.loads(r.text))
    clusters=[]
    print ("number of clusters are " + str(len(response)))

    for i in xrange(len(response)):
        print ("\ncluster " +str(i)+ " centroid :" +str(response[i]['centroid']['coords'])+ " elements : ")
        points = []
        print ("--------------------------")
        for j in xrange(len(response[i]['points'])):
            print response[i]['points'][j]['coords']
            points.append(Point(response[i]['points'][j]['coords']))
        clusters.append( Cluster(points,Point(response[i]['centroid']['coords'])))



    # Print our clusters
    for i, c in enumerate(clusters):
        print "\nCluster : " ,i ,"\t Centroid :",clusters[i].centroid
        for p in c.points:
            print "\t  ", p


    print ("plot is coming.... ")
    plotClusters(clusters)


    return True





#------> retrieve the information within the file... <----------

def load_points_params(file_name):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    abs_file_path = os.path.join(script_dir, file_name)
    print abs_file_path
    with open(abs_file_path) as json_data:
        d = json.load(json_data)
        print(d)
    p = d['pairs']
    return p

if __name__ == "__main__":

    k = 2
    lower = 0
    upper = 100
    epsilon = 0000.2
    num_of_samples = 20
    file  = None
    user_pair_points = None
    ip = "127.0.0.1"

    usage = "kmean-consul.py [-k <num>] [-v vector ][-i <host ip>]  \n" + \
            "-h     present this help\n" + \
            "-k     number of cluster  (default 2) \n" + \
            "-l     lower bound  value (defaul 0)\n" +\
            "-u     upper point value  (default 100)\n" + \
            "-e     epsilon : optimization has 'converged' and stop updating clusters (default 0.2)\n" + \
            "-f     file contains pair points as input\n" + \
            "-i     destination ip     (default 127.0.0.1)\n" + \
            "-n     number of samples to create\n" +\
            "Example: kmean-consul.py -k 2 -i 127.0.0.1 -f kmean-sample.json \n"

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hk:v:i:l:u:f:e:n:")
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit(0)
        elif opt in ("-k"):
            k = int(arg)
        elif opt in ("-i"):
            ip = arg
        elif opt in ("-l"):
            lower = int(arg)
        elif opt in ("-u"):
            upper = int(arg)
        elif opt in ("-e"):
            epsilon = float(arg)
        elif opt in ("-f"):
            file = arg
        elif opt in ("-n"):
            num_of_samples = int(arg)

    if(file is not None):
        user_pair_points = load_points_params(file)

    print("num of clusters = "+str(k))
    print("ip = " + str(ip))
    print("lower bound = " + str(lower))
    print("upper bound = " + str(upper))
    print("epsilon = " + str(epsilon))
    print("number of sampels  = " + str(num_of_samples))

    req = kmean_consul(k,lower,upper,epsilon,num_of_samples , ip, user_pair_points)
    res = post_request(req)
    if not res:
        print ("failed to send request")
    else:
        print ("Done")
