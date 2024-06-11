# MRItaxonomy - MRIGlobals Taxonomy Library

A compendium of convenient taxonomic related operations interfacing with NCBI

### installation
```
pip install MRItaxonomy
```

### import the whole module, or sub-modules
```
import MRItaxonomy
```
or
```
from MRItaxonomy import NCBI_fetch
from MRItaxonomy import accession2taxid
from MRItaxonomy import nnID
from MRItaxonomy import nucDL
from MRItaxonomy import protacc2taxid
from MRItaxonomy import slidingwindow
from MRItaxonomy import taxid
from MRItaxonomy import taxid2name
```

### NCBI_fetch
functions to intially set up and update the NCBI data pulls. running initialize() once after pip installation is reccomended as this step is time consuming up front, but does not have to be done again unless updating is desired
```
from MRItaxonomy import NCBI_fetch
NCBI_fetch.initialize()
```
to re-pull the latest from NCBI (will not re-download if no change)
```
NCBI_fetch.update()
```

### accession2taxid
contains a method that loads the accession-to-taxid mapping data object, and a function that reports the associated taxid for the passed accession
```
from MRItaxonomy import accession2taxid
accession2taxid.load_trie()    # note: does not have to be called. will automatically be applied the first time get_taxid() is run
accession2taxid.get_taxid(accession)
```

### nnID
contains a method that, from a given taxon, returns a list of taxonomies that are near neighbors to the given taxon
```
from MRItaxonomy import nnID
nnID.get_id(taxon)
```

### nucDL
contains methods to access NCBI's ftp site and download nucleotide records. takes in a taxid, thread count (for parallelism), a working directory, and a database choise between genbank/refseq
```
from MRItaxonomy import nucDL
nucDL.dl(tax, threads, path, db='genbank'/'refseq')
```

### protacc2taxid
works similarly as accession2taxid does, but with protein accessions instead of nucleotide
```
from MRItaxonomy import protacc2taxid
protacc2taxid.load_dataframe()    # note: does not have to be called. will automatically be applied the first time get_taxid() is run
protacc2taxid.get_taxid(prot_accession)
```

### slidingwindow
this module slides a window across a folder of nucleotide records and outputs window-sized reads along the length of the input nucleotide record. can specify what suffix to use for each chunked output (default=.fna)
```
from MRItaxonomy import slidingwindow
slidingwindow.reads_generation(path_of_fasta_folder, window_size=150, extension='.fna')
```

### taxid
this module handles operations having to do with the taxonomic trees via the NCBI nodes.dmp and merged.dmp files
```
from MRItaxonomy import taxid
taxid.load_dbs()    # note: does not have to be called. will automatically be applied the first time another MRItaxonomy.taxid() function needs the databases

taxid.get_parent(taxid)    # returns the parent taxid for the given taxid

taxid.get_rank(taixd)    # returns the rank of the given taxid (superkingdom, kingdom, phylum, class, order, family, genus, species)

taxid.getnodeatrank(taxid, selected rank)    # returns the taxid at the taxonomic rank (superkingdom, kingdom, phylum, class, order, family, genus, species) for the given taxid

taxid.get_merge(taxid)    # if the taxid is in the nodes.dmp database, returns the taxid. otherwise, if it's in the merged database, return the associated merged.dmp entry. If neither is true, returns 0.
```


### taxid2name
this module takes in a taxid and returns the associated scientific name
```
from MRItaxonomy import taxid2name
taxid.get_name(taxid)
```

