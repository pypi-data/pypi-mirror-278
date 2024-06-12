"""
This is a module designed to identify near neighbor taxa to an input taxon. It uses classical taxonomic ranks
instead of sub-phylum or other such ranks. These are shown here:

    "strain":"species",
        "species":"genus",
        "genus":"family",
        "family":"order",
        "order":"class",
        "class":"phylum",
        "phylum":"superkingdom"
This will not return the input taxon
"""

from MRItaxonomy import taxid
from Bio import Entrez
Entrez.email = 'biofx@mriglobal.org'


def get_id(taxon):

#set up taxonomic ranks dictionary to get the correct parent ID.
    ranks = {
        "no rank":"species",
        "strain":"species",
        "species":"genus",
        "genus":"family",
        "family":"order",
        "order":"class",
        "class":"phylum",
        "phylum":"superkingdom"
    }

    rank = taxid.getrank(int(taxon)) #get current rank to use in taxID query

    parent_rank = ranks[rank] #get next classical taxonomic rank up the tree
    parent_id = int(taxid.getnodeatrank(int(taxon),parent_rank)) #get parent id of whatever your input is

    tax_list = Entrez.read(Entrez.esearch(db='taxonomy',term='txid{0}[Organism] AND {1}[Rank]'.format(parent_id,rank), retmax='100000000'))['IdList'] #gets all taxIDs below the parent rank appropriate to the input rank
    if taxon in tax_list:
        tax_list.remove('{0}'.format(taxon)) #get rid of target taxon

    return(tax_list)

