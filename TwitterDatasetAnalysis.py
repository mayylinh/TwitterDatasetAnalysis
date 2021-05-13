import networkx as nx
import matplotlib.pyplot as plt
import statistics


def readDataset(file):
    with open(file, "rb") as fh:
        dg = nx.read_edgelist(file, comments='#', delimiter=' ', create_using=nx.DiGraph, nodetype=int, data=True, encoding='utf-8')
        print(f'----twitter dataset read from {file}----')
    return dg

#Copeland score formula: cop(N,D) = out(N,D) - in(N,D)
#for node N in digraph D, Copeland score cop is indegree in subtracted from outdegree out
def copelandScores(degrees):
    cop = {}    #dictionary with node and copeland score as key-value pairs
    for node in degrees.keys():
        in_out = degrees[node]
        score = in_out[1] - in_out[0]
        cop[node] = score
    return cop

#degree ratio formula: r(N,D) = [out(N,D) + 1]/[in(N,D + 1]
#for node N in digraph D, degree ratio r is outdegree out plus 1 divided by indegree in plus 1
def degreeRatio(degrees):
    r = {}      #dictionary with node and degree ratio as key-value pairs
    for node in degrees.keys():
        in_out = degrees[node]
        ratio = (in_out[1] + 1)/(in_out[0] + 1)
        r[node] = ratio
    return r

def createHistogram(title, rankings):
    #determine width of bins for histogram
    xlow = min(rankings.values())
    xhigh = max(rankings.values())
    width = (xhigh - xlow) / 15
    bins = [xlow]
    x = xlow
    while x < (xhigh-0.001):
        x += width
        bins.append(x)

    #create histogram and label x-axis tick marks, frequencies, axis titiles, histogram
    frequencies = plt.hist(rankings.values(), range=[xlow, xhigh], bins=15, rwidth=0.97)
    plt.xticks(bins, fontsize='xx-small')
    freq = (list(frequencies[0]))
    for i in range(len(freq)):
        plt.annotate('  '+str(int(freq[i])), xy=(bins[i], freq[i]), va='bottom')
    plt.text(0, 600, '*range for ' + title + '\nwith highest frequency of\n' + str(int(max(freq))) + ' exceeds y-axis limit', fontsize='x-small')
    freq.remove(max(freq))
    plt.ylim(0, max(freq) + 50)
    plt.title(title + ' Histogram')
    plt.xlabel(title)
    plt.ylabel('Frequency')
    plt.savefig(title + ' Histogram.png')
    plt.clf()
    print('----histogram drawn to', title, 'Histogram.png----')
    return bins

def meanMedStdev(nodes, rankings):
    ranks = []
    for node, rank in rankings.items():
        for high in nodes:
            if node == high:
                ranks.append(rank)
    mean = statistics.mean(ranks)
    med = statistics.median(ranks)
    stdev = statistics.stdev(ranks)
    return mean, med, stdev


if __name__ == '__main__':
    file_name = 'twitter_combined.txt.gz'
    dg = readDataset(file_name)
    degrees = {}

    # set list of indegree and outdegree as value for node key in degrees dictionary
    for node in dg.nodes():
        degrees[node] = [dg.in_degree(node), dg.out_degree(node)]

    copeland_scores = copelandScores(degrees)
    degree_ratios = degreeRatio(degrees)

    copRange = createHistogram('Copeland Scores', copeland_scores)
    rRange = createHistogram('Degree Ratios', degree_ratios)

    #store nodes with highest copeland scores from last histogram bin in list
    highestCops = []
    for node in copeland_scores.keys():
        if copeland_scores[node] >= copRange[len(copRange) - 2]:
            highestCops.append(node)

    print('\nFor nodes with Copeland scores greater than ' + str(copRange[len(copRange) - 2]) + ':')
    copMean, copMed, copStdev = meanMedStdev(highestCops, copeland_scores)
    print('Copeland score -')
    print('\tmean =', copMean)
    print('\tmedian =', copMed)
    print('\tstandard deviation = ', copStdev)
    rMean, rMed, rStdev = meanMedStdev(highestCops, degree_ratios)
    print('Degree ratio -')
    print('\tmean =', rMean)
    print('\tmedian =', rMed)
    print('\tstandard deviation =', rStdev)