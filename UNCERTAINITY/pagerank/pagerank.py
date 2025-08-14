import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 1000000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_distribution=dict()
    N=len(corpus)
    if len(corpus[page])==0:
        for p in corpus:
            prob_distribution[p]=1/N
        return prob_distribution
    for key in corpus.keys():
        prob_distribution[key]=(1-damping_factor)/N
        if key in corpus[page]:
            prob_distribution[key]+=(damping_factor/len(corpus[page]))
    return prob_distribution




def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks=dict()
    for key in corpus:
        page_ranks[key]=0
    current_page=random.choice(list(corpus.keys()))
    page_ranks[current_page]+=1
    for i in range(1,n):
        trans_probs=transition_model(corpus,current_page,damping_factor)
        pages=list(trans_probs.keys())
        weights=list(trans_probs.values())
        next_page=random.choices(pages,weights=weights,k=1)[0]
        page_ranks[next_page]+=1
        current_page=next_page
    page_ranks={page: count / n for page, count in page_ranks.items()}
    return page_ranks




    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    corpus=corpus.copy()
    N=len(corpus)
    page_ranks={page:1/N for page in corpus}
    pages=list(corpus.keys())
    for page in corpus:
        if len(corpus[page])==0:
            corpus[page]=pages
    links_in={page:set() for page in corpus}
    for page in corpus:
        for link in corpus[page]:
            links_in[link].add(page)
    converged=False
    while not converged:
        delta=[]
        page_ranks_cp=dict()
        for page in corpus:
            initial_val=page_ranks[page]
            final_val=0
            for page_into in links_in[page]:
                final_val+=(page_ranks[page_into]/len(corpus[page_into]))
            final_val*=damping_factor
            final_val+=(1-damping_factor)/N
            delta.append(final_val-initial_val)
            page_ranks_cp[page]=final_val
        page_ranks=page_ranks_cp
        max_changed=max(abs(x) for x in delta)
        if max_changed<0.00001:
            converged=True
    return page_ranks

        
        





if __name__ == "__main__":
    main()
