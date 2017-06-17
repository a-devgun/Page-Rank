import operator
import math
import itertools

##################################################################################
# loop_check: Returns False iff change in perplexity is less than 1 for at least 4
#             consecutive iterations.
##################################################################################

def loop_check(perplexity, i):

    if len(perplexity) < 4:
        return True

    elif abs(perplexity[i-1] - perplexity[i-2]) < 1 and \
            abs(perplexity [i-2] - perplexity[i-3]) < 1 and \
            abs(perplexity [i-3] - perplexity[i-4]) < 1:
        return False

    else:
        return True

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

        # calculate entropy.
        entropy += PR[p] * math.log(PR[p], 2)

    return PR, 2 ** (entropy * -1)

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

    # Iterate till difference between 4 consecutive perplexity has a difference of less than 1
    while loop_check(perplexity_list, i):
        i += 1

        PR, perplexity = get_page_rank(PR, list_P, list_S, dict_M, dict_L, N)

        print("Perplexity for iteration ", i, " is - ", perplexity)

        perplexity_list.append(perplexity)

    # Store the total number of in links to any page
    dict_in_link = {}

    # Get the total number of pages which don't have any in links
    zero_in_link_count = 0
    for docs in dict_M.keys():
        len_docs = len(dict_M[docs])
        dict_in_link[docs] = len_docs
        if len_docs == 0:
            zero_in_link_count += 1

    # Get the total number of pages which don't have any out links
    zero_out_link_count = len(list_S)

    # Get the total number of pages which have PR lower than their initial uniform values
    lower_page_rank_count = 0
    for links in list_P:
        if PR[links] < (1/N):
            lower_page_rank_count += 1

    # sort the Page rank on the basis of the page rank in descending order.
    sortedPR = sorted(sorted(PR.items()), key=operator.itemgetter(1), reverse=True)

    # Sort the In link list on the basis of Number of In links in descending order
    sortedInLink = sorted(sorted(dict_in_link.items()), key=operator.itemgetter(1), reverse=True)

    # Write to a file 'output.txt' the sorted page rank, sorted in links and the proportion of
    #     in link count, out link count and pages with page rank less thank initial out of total
    f = open("output.txt", "w")
    f.write('The document IDs of the top 50 pages as sorted by PageRank - \n')
    f.write('Document Id  Page Rank\n')
    for doc in itertools.islice(sortedPR, 0, 50):
        f.write('{0} \t {1:.16f}\n'.format(doc[0],doc[1]))

    f.write('\n\n\n')
    f.write('The document IDs of the top 50 pages as sorted by in-link count - \n')
    f.write('Document Id  In Link Count\n')
    for doc in itertools.islice(sortedInLink, 0, 50):
        f.write('{0} \t {1}\n'.format(doc[0],doc[1]))

    f.write('\n\n\n')
    f.write('Proportion of pages with no in-links is {0} of {1} which comes out to be {2:.16f}\n'
            .format(zero_in_link_count, N, (zero_in_link_count/N)))

    f.write('Proportion of pages with no out-links is {0} of {1} which comes out to be {2:.16f}\n'
            .format(zero_out_link_count, N, (zero_out_link_count/N)))

    f.write('Proportion of pages whose PageRank is less than their initial is {0} of {1} which comes out to be {2:.16f}\n'
            .format(lower_page_rank_count, N, (lower_page_rank_count/N)))

    f.close()

    return sortedPR, perplexity_list

#################################################################################
# The program starts here with the import of the file
#################################################################################

with open('wt2g_inlinks.txt', 'r') as f:
    link_file = [line.strip() for line in f]

sortedPR, perplexity = compute_page_rank(link_file)

# Write the complete links of sorted Page Ranks
f = open("Complete Sorted Page Rank.txt", "w")
sum = 0
for links in itertools.islice(sortedPR, None, None):
    f.write('{0} \t {1:.16f}\n'.format(links[0], links[1]))
    sum += links[1]
f.close()

print('sum is ', sum)
# Write the output of perplexity to a file name Perplexity Values.txt
f = open("Perplexity Values.txt", "w")
counter = 0
for p in perplexity:
    counter += 1
    f.write('Perplexity for round {0} is {1}\n'.format(counter, p))
f.close()


