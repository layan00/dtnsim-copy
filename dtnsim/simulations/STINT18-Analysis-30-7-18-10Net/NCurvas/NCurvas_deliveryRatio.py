import matplotlib.pyplot as plt
import ast
import os

#OUTPUT
FILE_OUTPUT_PATH = os.getcwd() + "/results/deliveryRatio"

#INPUT. Complete path will be computed as DIRECTORY/FILE_PATHS_C1[i]
DIRECTORY = os.getcwd() + "/.."

FILE_PATHS_C1 = [
"RandomNetwork_cgrfa_1x/results/results_random/0.2/METRIC=deliveryRatio-DENSITY=0.2-AMOUNT_CONTACT_PLANS=10-FAULTAWARE=true.txt",
"RandomNetwork_cgr_proactive_1x/results/results_random/0.2/METRIC=deliveryRatio-DENSITY=0.2-AMOUNT_CONTACT_PLANS=10-FAULTAWARE=false.txt",
"RandomNetwork_bruf_1x/results/results_random/0.2/METRIC=deliveryRatio-DENSITY=0.2-AMOUNT_CONTACT_PLANS=10-FAULTAWARE=false.txt",
"RandomNetwork_cgr1_1x/results/results_random/0.2/METRIC=deliveryRatio-DENSITY=0.2-AMOUNT_CONTACT_PLANS=10-FAULTAWARE=false.txt",
"RandomNetwork_cgr3_1x/results/results_random/0.2/METRIC=deliveryRatio-DENSITY=0.2-AMOUNT_CONTACT_PLANS=10-FAULTAWARE=false.txt",
#"RandomNetwork_sprayAndWait_1x/results/results_random/0.2/METRIC=deliveryRatio-DENSITY=0.2-AMOUNT_CONTACT_PLANS=10-FAULTAWARE=false.txt",
#"RandomNetwork_sprayAndWait_4copies_1x/results/results_random/0.2/METRIC=deliveryRatio-DENSITY=0.2-AMOUNT_CONTACT_PLANS=10-FAULTAWARE=false.txt",
#"RandomNetwork_epidemic_1x/results/results_random/0.2/METRIC=deliveryRatio-DENSITY=0.2-AMOUNT_CONTACT_PLANS=10-FAULTAWARE=false.txt"
]

#Calculate complete path
COMPLETE_PATHS_C1 = list(map(lambda x: DIRECTORY + "/" + x, FILE_PATHS_C1))

#Names of plotted functions

NAME_CURVAS_1 = ["$CGR-FaultAware$","$CGR-2$","$BRUF$","$CGR-DelTime$","$CGR-Hops$"]

#Color of ploted functions
COLOR_CURVAS_1 = ['black','orange','red','blue','green']

#Style of plotted function
STYLE_CURVAS_1 = ['--^','--d','--o','--s','--v']


#Number of contact in each contact plan. It must correspond to FILE_PATHS
#NUMBER_OF_CONTACT = [10, 60, 120]

#Defines wich points plot in graph
#DOTS = [0.0,0.1,0.2,0.3,0.4,0.2,0.6,0.7,0.8,0.9,1.0]
#RANGE = [[round(p * i) for p in DOTS] for i in NUMBER_OF_CONTACT

X_LABEL = "Probability of Uncertainties"
Y_LABEL = "Delivery Ratio"

def main():
    c1s = [getListFromFile(fname) for fname in COMPLETE_PATHS_C1]

    # plot results

    lines = []
    for c1,name1,color1,style1, in zip(c1s,NAME_CURVAS_1,COLOR_CURVAS_1,STYLE_CURVAS_1):
        line_up, = plt.plot([x[0] for x in c1],[y[1] for y in c1],style1, color=color1, label=name1,linewidth=1.0)
        lines.append(line_up)
#       	plt.errorbar([x[0] for x in c1],[y[1] for y in c1],[t[2] for t in c1],color='k',linestyle='None',linewidth=0.5, marker='',capsize=4,capthick=0.7)

    plt.legend(handles= lines, loc='lower left')

    #plt.xlim([0.2,0.9])
    #plt.ylim([0.4,1.05])
    plt.xlabel(X_LABEL, fontsize=16)
    plt.ylabel(Y_LABEL, fontsize=16)
    plt.grid(color='gray', linestyle='dashed')
    plt.savefig(FILE_OUTPUT_PATH + ".pdf")
    plt.savefig(FILE_OUTPUT_PATH + ".svg")
    plt.clf()
    plt.cla()
    plt.close()
    print("File save to %s"%FILE_OUTPUT_PATH + ".pdf")
    print("File save to %s"%FILE_OUTPUT_PATH + ".svg")
    #plt.show()

''''
Get a list from file reading first line only
'''
def getListFromFile(path):
    with open(path) as f:
        lines = f.readlines()

    return ast.literal_eval(lines[0])

main()
