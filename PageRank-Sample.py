import operator


##################################################################################
# get_page_rank: Calculates the page rank for 1 particular iteration. Also
#                      calculates and returns perplexity for that iteration.
##################################################################################

def get_page_rank(PR, P, S, M, L, N):

    newPR = {}
    # damping factor is taken as 0.85
    d = 0.85
    entropy = 0
    sinkPR = 0

    # calculate total sink PR
    for p in S:
        sinkPR += PR[p]

    # loop over all the links
    for p in P:

        # teleportation
        newPR[p] = (1 - d) / N

        # spread remaining sink PR evenly
        newPR[p] += (d * sinkPR / N)

        try:
            # pages pointing to p
            for q in M[p]:

                # add share of PageRank from in-links
                newPR[p] += ((d * PR[q]) / L[q])

        except KeyError:
            print("Do Nothing for ",p)

    # assign the page rank to the original variable
    for p in P:
        PR[p] = newPR[p]

    return PR

#################################################################################
# compute_page_rank: Takes in the links file and calculates the page Rank and
#       prints the required output
#################################################################################
def compute_page_rank(link_file):

    # Store all the links in the link_file
    total_links = []

    # Store all the out links in the link_file
    out_links = []

    # Dict for storing the key value combo where key is any page and values are the pages pointing to that page
    dict_M = {}

    # Iterate over the file
    for line in link_file:

        links = line.split()

        total_links += links
        out_links += links[1:]

        dict_M[links[0]] = links[1:]

    # Store all the unique set of pages in the link file
    list_P = set(total_links)

    # Store all the pages which do not have any pages pointing to them
    list_S = list_P - (set(out_links))

    # Dict for storing pages as key and the number of pages these pages are pointing to
    dict_L = {}

    for links in list_P:
        dict_L[links] = 0


    for links in dict_M:
        for values in dict_M[links]:
            dict_L[values] += 1

    # Total Number of Pages
    N = len(list_P)

    # Store the page Rank
    PR = {}

    # Initial Page Rank
    for p in list_P:
        PR[p] = 1/N

    perplexity_list = []
    i = 0

    f = open("output-sample.txt", "w")

    # Iterate till difference between 4 consecutive perplexity has a difference of less than 1
    while i in range(0, 100):
        i += 1

        PR = get_page_rank(PR, list_P, list_S, dict_M, dict_L, N)

        if i == 1 or i==10 or i == 100:
            for page in sorted(PR.items(), key=operator.itemgetter(1), reverse=True):
                f.write("for iteration {0}, PageRank for {1} is {2:.16f}\n".format(i, page[0], page[1]))

    f.close()



#################################################################################
# The program starts here with the import of the file
#################################################################################
with open('names.txt', 'r') as f:
    link_file = [line.strip() for line in f]

compute_page_rank(link_file)

