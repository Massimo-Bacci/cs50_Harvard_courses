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
    num_pages = len(corpus)
    return {p: (1 - damping_factor) / num_pages + damping_factor / len(corpus[page]) if p in corpus[page] else (1 - damping_factor) / num_pages for p in corpus}



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {p: 0 for p in corpus}
    p = random.choice(list(corpus))
    for _ in range(n):
        rank[p] += 1 / n
        probs = transition_model(corpus, p, damping_factor)
        p = random.choices(list(probs.keys()), weights=probs.values(), k=1)[0]
    return rank
    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    rank = {page: 1 / num_pages for page in corpus}
    while True:
        new_rank = {page: (1 - damping_factor) / num_pages for page in corpus}
        diff = 0
        for page in corpus:
            for link, linked_pages in corpus.items():
                if not linked_pages:
                    linked_pages = set(corpus)
                if page in linked_pages:
                    new_rank[page] += damping_factor * (rank[link] / len(linked_pages))
        for page in corpus:
            diff += abs(new_rank[page] - rank[page])
        rank = new_rank
        if diff < 0.001:
            break
    return rank


if __name__ == "__main__":
    main()
