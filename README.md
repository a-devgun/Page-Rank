# PAGE  RANK

This script can be used to assign Page Rank to the W2G collection list provided in the below link.

http://www.ccs.neu.edu/course/cs6200f15/wt2g_inlinks

This list has been saved to file - 'wt2g_inlinks.txt' and used from there.

The python file - 'PageRank.py' is used to execute over the collection 'wt2g_inlinks.txt'.
The python file - 'PageRank-Sample.py' runs over the sample links A,B,C,D,E,F which is stored in file 'names.txt'.


## SETUP

1. Download the latest version of python - "Python 3.5.0".
2. Install PyCharm.
3. Execute code. 

## ABOUT THE CODE

PageRank-Sample.py

1. This script will calculate Page Rank upto a 100 iterations.
2. It will print its output to a file named - 'output-sample.txt'


PageRank.py

1. This script is will calculate Page Rank until difference in perplexity of 4 consecutive iterations is less than 1.
2. Perplexity is calculated as 2 to the power Entropy.
3. The output for perplexity value for each iteration is stored in 'Perplexity Values.txt'
4. The output for the first 50 sorted page rank, 50 sorted in links and the proportion of in link count, out link count and pages with page rank less thank initial out of total is stored in 'output.txt'
5. The complete list of Page Ranks sorted by their page Rank is stored in 'Complete Sorted Page Rank.txt'
6. The analysis of Page Rank is stored in a file named - 'Page Rank Analysis.docx'


## CONTACT

Please contact 'Anirudh Devgun' at 'devgun.a@husky.neu.edu' in case of any issues.