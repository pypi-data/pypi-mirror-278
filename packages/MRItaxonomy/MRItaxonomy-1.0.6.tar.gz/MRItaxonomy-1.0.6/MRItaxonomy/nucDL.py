"""
This is a module designed to download nucleotides from NCBI's ftp site
It takes taxon as an argument and has two optional arguments:
path - which defaults to the current working directory.
db - which defaults to 'genbank'. Alternate option is 'refseq'

It is now parallelized.
"""

from Bio import Entrez
import os, shutil, pandas as pd, sys, time
import glob
from MRItaxonomy import taxid
from multiprocessing.dummy import Pool
from urllib.error import HTTPError
Entrez.email = 'biofx@mriglobal.org'

def dl(tax,threads,path=os.getcwd(),db='genbank'):
    tax_list = []
#strain level taxIDs are in the assembly_summary_refseq/genbank file and could be parsed as well.
#to do this, check if rank is higher than species and if so, collect all species for the tax_list
#if the rank is species or strain, continue.
#if the rank is strain, the summary file needs to be parsed on the taxid column, not the species_taxid column.
    if taxid.getrank(tax) != 'species': #to be updated
        print('Getting species for {0}\n'.format(tax))
        i=0
        while i<10:
            i+=1
            try:
                tax_list = Entrez.read(Entrez.esearch(db='taxonomy',term='txid{0}[Organism] AND species[Rank]'.format(tax), retmax='1000000'))['IdList'] #gets all taxIDs below the parent rank appropriate to >
            except HTTPError as e:
                time.sleep(1)
                print(e.read())
                print('Download problem at taxid.getrank')
                continue
            break
        print(tax_list)
    else:
        tax_list.append(tax) #keep everything consistent

    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    if os.path.exists('{0}/assembly_summary_{1}.txt'.format(path,db)):
#Assuming we only want complete genomes and not assemblies/scaffolds
        os.system('grep "# assembly_accession\|Complete Genome" {0}/assembly_summary_{1}.txt | cut -f6,7,8,9,20 > {0}/assembly.summary.shrunk.txt'.format(path,db))
    else:
        ftp_url = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/{0}/assembly_summary_{0}.txt'.format(db) #Full ftp path
        i=0 #in case of internet shenanigans
        while i<10:
            i+=1
            try:
                print('Downloading {0} ... attempt {1}'.format(ftp_url, i))
                os.system('wget -c {0}'.format(ftp_url)) #download!
                os.system('grep "# assembly_accession\|Complete Genome" {0}/assembly_summary_{1}.txt | cut -f6,7,8,9,20 > {0}/assembly.summary.shrunk.txt'.format(path,db))
                time.sleep(2)
            except:
                time.sleep(i*i)
                continue
            break


    filenames = [] #set list of files to download. Pushed before the for loop to help parallelize taxa

    for tax in tax_list:
        try:
            print('{0} is the path of the taxon {1}'.format(path,tax))
            tax = int(tax)
            sys.stderr.write('{0} is the downloading taxID\n'.format(tax))
            assaddr = pd.read_csv('{0}/assembly.summary.shrunk.txt'.format(path),sep='\t') #modified from previous to handle the smaller file for improved search speeds.
            ftpaddr = list(assaddr.loc[assaddr['species_taxid'] == tax, ['ftp_path']]['ftp_path'])

            for addr in ftpaddr:
                filenames.append('{0}/{1}_genomic.fna.gz'.format(addr,addr.split('/')[9])) #add to list of files to download both the URL and the filename (10th field /-delimited of the URL)
        except HTTPError as e:
            time.sleep(5)
            print("HTTPError at {0}".format(tax))
            continue
        except KeyError:
#try and handle any updates to refseq that didn't update the taxonomy file
            print('TaxID {0} not found in taxonomy dump files'.format(tax))
            break
#then download with wget or anything else
#parallelize here
    pool = Pool(int(threads))
    pool.map(download,filenames)

def download(file):
    if not os.path.isfile(file):
        os.system('wget -c {0}'.format(file)) #downloads to current directory
        time.sleep(1)
        print(file.split('/')[-1])
