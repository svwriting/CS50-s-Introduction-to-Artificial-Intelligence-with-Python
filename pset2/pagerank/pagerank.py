import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
    dictionary_={}
    if len(corpus[page])!=0:
        plus_=damping_factor/len(corpus[page])
        base_=(1-damping_factor)/(len(corpus)-1)
    else:
        plus_=0
        base_=1/(len(corpus)-1)
    # according to the description and example in 'Specification',
    # base_ should be(1-damping_factor)/len(corpus);
    # But according to the 'Write an AI to rank web pages by importance',
    #   in corpus0
    #   1.html: 0.2223
    #   3.html: 0.2145
    #   aren't same
    # Also sample_pagerank's ●4
    # 'The values in this dictionary should sum to 1'
    # I have to def base_ as (1-damping_factor)/(len(corpus)-1)
    # which means sample don't link himself with any probability at all

    # Damn, those descriptions are so confusing and contradicting...
    #--------------------------------------------------------
    for page_ in corpus:
        if page!=page_:
            dictionary_[page_]=round(base_,4)
    for page_ in corpus[page]:
        dictionary_[page_]=round(dictionary_[page_]+plus_,4)
    #print(dictionary_)
    return dictionary_
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dictionary_={}
    #count_Dic={}
    for page_ in corpus:
        dictionary_[page_]=0
        #count_Dic[page_]=0
    sample_=random.choice(list(dictionary_.keys()))
    for i in range(n):
        #count_Dic[sample_]+=1
        temp_=transition_model(corpus,sample_,damping_factor)
        next_=random.random()
        #print(temp_)
        for page_ in temp_:
            dictionary_[page_]=round(round(dictionary_[page_],4)+round(temp_[page_],4),4)
        for page_ in temp_:
            next_-=temp_[page_]
            if next_<=0:
                sample_=page_
                break
    #print("////////////")
    #print(corpus)
    #print(count_Dic)
    #print(dictionary_)
    for page_ in dictionary_:
        dictionary_[page_]/=n
    return dictionary_
    raise NotImplementedError


def transition_model0(corpus, page, damping_factor):
    dictionary_={}
    plus_=damping_factor/len(corpus[page])
    base_=(1-damping_factor)/(len(corpus))
    for page_ in corpus:
            dictionary_[page_]=round(base_,4)
    for page_ in corpus[page]:
        dictionary_[page_]=round(dictionary_[page_]+plus_,4)
    #print(dictionary_)
    return dictionary_
    raise NotImplementedError
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N=len(corpus)
    dictionary_={}
    Vcorpus={}
    NumLinks_ofCorpus={}
    for page_ in corpus:
        dictionary_[page_]=1/N
        NumLinks_ofCorpus[page_]=len(corpus[page_])
        Vcorpus[page_]=set()
    for page_ in corpus:
        for page_i in corpus[page_]:
            Vcorpus[page_i].add(page_)
    #print(Vcorpus)
    bool_=True
    #print(corpus)
    while bool_:
        bool_=False
        dictionary_0=dictionary_.copy()
        for page_ in corpus:
            # PR(p)=(1-d)/N + d*E( PR(i)/NumLinks(i) )
            # every i -> p 
            dictionary_[page_]=(1-damping_factor)/N
            for page_i in Vcorpus[page_]:
                dictionary_[page_]+=damping_factor*(dictionary_0[page_i]/NumLinks_ofCorpus[page_i])
        for page_ in corpus:
            if abs(dictionary_[page_]-dictionary_0[page_])>0.01:
                bool_=True
        #print(dictionary_)
    return dictionary_
    raise NotImplementedError


if __name__ == "__main__":
    main()
