# fastDSD
Combining DSD (Cao et al. [2013](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0076339), [2014](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4058952/)) runtime optimizations from [reemagit](https://github.com/reemagit/DSD) for a fast, optimized version of DSD / cDSD

## Installation

```bash
git clone git@github.com:samsledje/fastDSD.git
cd fastDSD
pip install .
```

or

```bash
pip install fastdsd
```

## Usage

```bash
usage: fastdsd [-h] [--converge] [-n NRW] [-w PPIP] [-r PATHPROB] [-o OUTFILE] [-q] [-f] [-m {1,2,3}] [--outformat {matrix,list,top}] [-k NTOP] [-t THRESHOLD] [-c]
               [-a] [-p]
               infile

parses PPIs from infile and calculates DSD

positional arguments:
  infile                read PPIs from tab-delimited edge list (with optional weights)

optional arguments:
  -h, --help            show this help message and exit
  --converge            calculate converged DSD
  -n NRW, --nRW NRW     length of random walks, 5 by default
  -w PPIP, --ppip PPIP  directory containing PPI pathway files
  -r PATHPROB, --pathprob PATHPROB
                        probability of remaining on a path given that you are already on it
  -o OUTFILE, --outfile OUTFILE
                        output DSD file name, tab delimited tables, stdout by default
  -q, --quiet           turn off status message
  -f, --force           calculate DSD for the whole graph despite it is not connected if it is turned on; otherwise, calculate DSD for the largest component
  -m {1,2,3}, --outFMT {1,2,3}
                        the format of output DSD file: type 1 for matrix; type 2 for pairs at each line; type 3 for top K proteins with lowest DSD. Type 1 by default
  --outformat {matrix,list,top}
                        the format of output DSD file: 'matrix' for matrix, type 1; 'list' for pairs at each line, type 2; 'top' for top K proteins with lowest DSD,
                        type 3. 'matrix' by default
  -k NTOP, --nTop NTOP  if chosen to output lowest DSD nodes, output at most K nodes with lowest DSD, 10 by default
  -t THRESHOLD, --threshold THRESHOLD
                        threshold for PPIs' confidence score, if applied
  -c, --confidence      use information about interaction confidence (cDSD)
  -a, --augment         augment with high-confidence signaling pathway data (caDSD: requires -c)
  -p, --properties      make use of topological properties of signaling pathways (capDSD: requireds -ca)
```
