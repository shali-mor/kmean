# kmean
The goal of this repository is to test the kmean functionality. 

usage =   kmean-consul.py [-k <kmean>][-l <lower>][-u <upper>][-e <epsilon>][-f <file> ][-i <ip>][-h <help>]
                          -h     present this help
                          -k     number of cluster  (default 2)
                          -l     lower bound  value (default 0)
                          -u     upper point value  (default 100)
                          -e     epsilon : optimization has 'converged' and stop updating clusters (default 0.2)
                          -f     JSON file contains pair points as input
                          -i     destination ip     (default 127.0.0.1)
Example: kmean-consul.py -k 2 -i 127.0.0.1 -f .

Note: if '-f' option is used, lower/upper will be ignored.