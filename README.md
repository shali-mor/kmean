# kmean
The goal of this repository is to test the kmean functionality. 

k-means is  one of  the simplest unsupervised  learning  algorithms  that  solve  the well  known clustering problem. The procedure follows a simple and  easy  way  to classify a given data set  through a certain number of  clusters (assume k clusters) fixed apriori. The  main  idea  is to define k centers, one for each cluster. These centers  should  be placed in a cunning  way  because of  different  location  causes different  result. So, the better  choice  is  to place them  as  much as possible  far away from each other. The  next  step is to take each point belonging  to a  given data set and associate it to the nearest center. When no point  is  pending,  the first step is completed and an early group age  is done. At this point we need to re-calculate k new centroids as barycenter of  the clusters resulting from the previous step. After we have these k new centroids, a new binding has to be done  between  the same data set points  and  the nearest new center. A loop has been generated. As a result of  this loop we  may  notice that the k centers change their location step by step until no more changes  are done or  in  other words centers do not move any more.


usage =   kmean-consul.py [-h <help>][-k <kmean>][-l <lower>][-u <upper>][-e <epsilon>][-f <file> ][-i <ip>]

                          -h     present this help
                          -k     number of cluster  (default 2)
                          -l     lower bound  value (default 0)
                          -u     upper point value  (default 100)
                          -e     epsilon : optimization has 'converged' and stop updating clusters (default 0.2)
                          -f     JSON file contains pair points as input. example file can be viewed in the current folder (pairs.json)
                          -i     destination ip     (default https://kmean.azurewebsites.net/api/pythonKmean )
                          
Example: kmean-consul.py -k 2 -i https://kmean.azurewebsites.net/api/pythonKmean -f pairs.json

Some important notes: 
1. If you wish to run the client consul , all you need is the client_consul folder !
2. Before running this code , make sure all packages stated in requirements.txt are properly installed.
3. when using the above option to the client consul , when '-f' option is set, 'lower'/'upper' values will be ignored.
4. A plot with the clusters mapping will be available at the end of the run (temp-plot.html file is created and immediatly presented)  
5. The actuall kmean algorithm running at the Azur serverless is run.py . if you wish to run the server locally (using 127.0.0.1) , you 
   will be required to run the kmean-engine.py . this was done due to the specific HTTP server used at Azur. (this is the only  
   difference )  
   pip install --upgrade pip
   pip install --no-cache-dir -r requirements.txt
7. if you have both python 2 and 3 installed , make sure you update both with the packages 
