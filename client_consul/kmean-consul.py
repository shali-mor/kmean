"""
# Full Imports


This is a pure Python implementation of the K-Means Clustering algorithmn. The
original can be found here:
http://pandoricweb.tumblr.com/post/8646701677/python-implementation-of-the-k-means-clustering

"""

import sys, getopt, os, json
import requests

from cluster import *
from point import Point


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
    url = mean_obj.dst_ip
    val = os.getenv('ANALYZE',"MICROSOFT")
    header = { "HOME":val }
    print (header)

    r = requests.post(url, headers = header, data=json.dumps(mean_obj.__dict__), timeout=30)
    if (r.status_code != 200 and r.status_code != 201):
        print (r.text)
        print (r.status_code)
        return False

    print ("Response received , build relevant cluster : ")
    response = eval(json.loads(r.text))
    clusters=[]

    for i in range(len(response)):
        points = []
        for j in range(len(response[i]['points'])):
            points.append(Point(response[i]['points'][j]['coords']))
        clusters.append( Cluster(points, Point(response[i]['centroid']['coords'])))

    printClusters(clusters)
    print ("plot is coming.... ")
    plotClusters(clusters)


    return True





#------> retrieve the information within the file... <----------

def load_points_params(file_name):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    abs_file_path = os.path.join(script_dir, file_name)
    print (abs_file_path)
    with open(abs_file_path) as json_data:
        d = json.load(json_data)
        #print(d)
    p = d['pairs']
    return p

if __name__ == "__main__":

    k = 3
    lower = 0
    upper = 100
    epsilon = 0.002
    num_of_samples = 20
    file  = None
    user_pair_points = None

    ip = "https://kmean.azurewebsites.net/api/pythonKmean"

    usage = "kmean-consul.py [-k <num>] [-v vector ][-i <host ip>]  \n" + \
            "-h     present this help\n" + \
            "-k     number of cluster  (default 2) \n" + \
            "-l     lower bound  value (defaul 0)\n" +\
            "-u     upper point value  (default 100)\n" + \
            "-e     epsilon : optimization has 'converged' and stop updating clusters (default 0.2)\n" + \
            "-f     file contains pair points as input\n" + \
            "-i     destination ip     (default https://kmean.azurewebsites.net/api/pythonKmean)\n" + \
            "-n     number of samples to create\n" +\
            "Example: kmean-consul.py -k 2 -i https://kmean.azurewebsites.net/api/pythonKmean -f pairs.json \n"

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hk:v:i:l:u:f:e:n:")
    except getopt.GetoptError:
        print (usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (usage)
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

    if(file is not None  ):
        if (os.path.isfile(file)):
            user_pair_points = load_points_params(file)
            if(len(user_pair_points) <2):
                print ("please add some points as clustering requires at least two points.")
                exit(0)
            print("number of sampels  = " + str(len(user_pair_points)))
        else:
            print("file doesn't exist , exit ")
            exit (0)
    else:
        print("lower bound = " + str(lower))
        print("upper bound = " + str(upper))
        print("number of sampels  = " + str(num_of_samples))

    print("num of clusters = "+str(k))
    print("ip = " + str(ip))

    print("epsilon = " + str(epsilon))


    req = kmean_consul(k,lower,upper,epsilon,num_of_samples , ip, user_pair_points)
    res = post_request(req)
    if not res:
        print ("failed to send request")
    else:
        print ("Done")
