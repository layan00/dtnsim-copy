#This python script is made to convert .sca files (results generated by dtnsim) into a .pdf file, showing graphics on the various metrics that we have.

import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.backends.backend_pdf import PdfPages

#The input .sca files are supposed to be in /results/
INPUT_PATH = os.getcwd() + "/results/"

# Reference value. You must change it here if you changed them on dtnsim
SIZE_REF="100"
CONSTELLATION_REF="Star"
ROUTING_REF="cgrModelRev17"


## A list of interesting metrics . You can remove as many as you want

# Used to display the bar with min, max, mean, stddev
METRIC_APP=[("appBundleReceivedDelay:histogram","Delay of received bundles"),("appBundleReceivedHops:histogram","Hops of received bundles")]

# Used to display the raw scalar as given
METRICS = [
            ("routeCgrDijkstraCalls:sum", "calls to CgrDijkstra"," "),
            ("routeCgrDijkstraLoops:sum", "Cgr Dijkstra loops"," "),
            ("routeCgrRouteTableEntriesCreated:max", "CGR table entries max"," "),
            ("routeCgrRouteTableEntriesCreated:sum", "CGR table entries sum"," "),

            ("sdrBundleStored:timeavg","Bundles stored time avg"," "),
            ("sdrBundleStored:max","Bundles stored max"," "),
        
            ("dtnBundleSentToCom:count", "bundles sent to Com"," "),
            ("dtnBundleSentToApp:count", "bundles sent to App"," "),
            ("dtnBundleReRouted:count", "blundles re-routed"," "),

]

'''
Function that return the mean of a list
'''
def mean(f):
    s=0
    compt=0
    for i in f:
        if (i!=None and i!=0):
            compt=compt+1
            s+=i
    if (compt==0):
        compt=1
    m=s/compt
    return m

# Initialisation
i=1


'''
part that creates a graph displaying the packet delivery ratio
'''

#f is the list that is gonna store the values (y-axis)
f=[]

#Browse the metrics to get a sum value for each one
#First open the corresponding database (.sca file)
db=sqlite3.connect("%sGeneral-Routing=%s,Constellation=contactPlan#2f%s.txt,Size=%s-#0.sca"% (INPUT_PATH,ROUTING_REF,CONSTELLATION_REF,SIZE_REF))
db.row_factory = sqlite3.Row
cursor=db.cursor()

#Select with SQL the sum of all the values corresponding to our current metric
cursor.execute("SELECT SUM(scalarValue) AS result FROM scalar WHERE scalarName='appBundleSent:count'")
rows0 = cursor.fetchall()
#Add the sum to the list
f.append(rows0[0]["result"])

#Select with SQL the sum of all the values corresponding to our current metric
cursor.execute("SELECT SUM(scalarValue) AS result FROM scalar WHERE scalarName='appBundleReceived:count'")
rows0 = cursor.fetchall()
#Add the sum to the list
f.append(rows0[0]["result"])

#Ratio of both to have the PDR
f=[f[1]/f[0]]
X=[1]

#Display the results with a bar graphic
plt.figure(i)
plt.bar(X,f,width=1,edgecolor="white",color="#8402be")
plt.title(label="Overall Packet Delivery Ratio (PDR)")
i=i+1

'''
The part that generates the graphes with infos such as min and max for concerned metrics
'''
for metric in METRIC_APP :
    #First open the corresponding database (.sca file)
    db=sqlite3.connect("%sGeneral-Routing=%s,Constellation=contactPlan#2f%s.txt,Size=%s-#0.sca"% (INPUT_PATH,ROUTING_REF,CONSTELLATION_REF,SIZE_REF))
    db.row_factory = sqlite3.Row
    cursor=db.cursor()
 
    X=[]
    means=[]
    stddev=[]
    mins=[]
    maxs=[]
    cursor.execute("SELECT statMean,statStddev,statMin,statMax FROM statistic WHERE statName='%s'"%(metric[0]))
    compt=0
    for r in cursor.fetchall():
        if (r[0])!=None:
            means.append(r[0])
            stddev.append(r[1])
            mins.append(r[2])
            maxs.append(r[3])
            X.append(compt)
        compt=compt+1
    X.append(compt)
    mins.append(mean(mins))
    maxs.append(mean(maxs))
    means.append(mean(means))
    stddev.append(mean(stddev))

    plt.figure(i)
    plt.plot(X,means) 
    plt.xlabel("node Id")
    if "Delay" in metric[0]:
        plt.ylabel("time (s)")
    # To use boxplots, the full dataset is needed. We couldn't get them, so we used errorbar that need only stddev, min, max and mean.
    # In grey there is the max and min. The mean is represented by the black dot
    plt.errorbar(X, means, [[b_elt - a_elt for a_elt, b_elt in zip(mins, means)],[b_elt - a_elt for a_elt, b_elt in zip(means, maxs)]],
                fmt='.k', ecolor='gray', lw=2)
    
    # In green the standart deviation is represented
    plt.errorbar(X, means, stddev, fmt='dk', ecolor='green',lw=5)
    plt.xlim(111,124)
    plt.title("%s"%(metric[1]))
    i=i+1

'''
Part that for each metrics, creates a graph displaying the value of the current metric for each node
'''

#Browse the metrics to create a graph for each one 
for metric in METRICS : 
    #f is the list that is gonna store the values (y-axis)
    f=[]
    #X is the list that is gonna store the nodes values (x-axis)
    X=[]

    #First open the corresponding database (.sca file)
    db=sqlite3.connect("%sGeneral-Routing=%s,Constellation=contactPlan#2f%s.txt,Size=%s-#0.sca"% (INPUT_PATH,ROUTING_REF,CONSTELLATION_REF,SIZE_REF))
    db.row_factory = sqlite3.Row
    cursor=db.cursor()

    #Select with SQL the values corresponding to our current metric
    cursor.execute("SELECT scalarValue AS result FROM scalar WHERE scalarName='%s'" % (metric[0]))
    rows0 = cursor.fetchall()

    #Add the values to our lists (only the non-None values)
    for j in range(len(rows0)):
        if (rows0[j]["result"]!=None):
            f.append(rows0[j]["result"])   
            X.append(j)     
    X.append(123)
    f.append(mean(f))

    #Display the results with a bar graphic
    plt.figure(i)
    plt.bar(X,f,width=1,edgecolor="white",color="#8402be")
    plt.title(label="%s"%(metric[1]))
    plt.xlabel("node Id")
    plt.ylabel("%s"%(metric[2]))
    
    i=i+1


'''
Part that concatenates all figures into one pdf 
'''

pdf=PdfPages("figures.pdf")
fig_num=plt.get_fignums()
figs=[plt.figure(n) for n in fig_num]
for fig in figs:
    fig.savefig(pdf,format='pdf')
pdf.close()
