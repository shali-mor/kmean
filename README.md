# kmean
The goal of this repository is to test the kmean functionality. 

usage = "kmean-consul.py [-k <kmean>][-l <lower>][-u <upper>] [-e <epsilon>][-f <file> ][-i <ip>][-h <help>]  \n" + \
            "-h     present this help\n" + \
            "-k     number of cluster  (default 2) \n" + \
            "-l     lower bound  value (defaul 0)\n" +\
            "-u     upper point value  (default 100)\n" + \
            "-e     epsilon : optimization has 'converged' and stop updating clusters (default 0.2)\n" + \
            "-f     file contains pair points as input\n" + \
            "-i     destination ip     (default 127.0.0.1)\n" + \
            "Example: kmean-consul.py -k 2 -i 127.0.0.1 -f /root \n
