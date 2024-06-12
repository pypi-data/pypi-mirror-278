import os
import wget
import site
import pandas as pd
import numpy as np
import marisa_trie
import subprocess
import shutil
import gzip

#functions called by commands at command line

def build_trie(directory):
    print('Building accession2taxid trie datafiles...')
    chunk_size = 50000
    trie_keys = []
    tax_ids = []
    for chunk in pd.read_csv(f'{directory}/dumps/nucl_gb.accession2taxid', sep='\t', usecols=[1, 2], chunksize=chunk_size, header=0):
        #print(chunk)
        #print(chunk.iloc[:,1].astype(int).tolist())
        #assert(False)
        if all(isinstance(item, int) for item in chunk.iloc[:,1].astype(int).tolist()):
            trie_keys.extend(chunk.iloc[:,0].astype(str).tolist())
            tax_ids.extend(chunk.iloc[:,1].astype(int).tolist())
            #print("Taxids completed: ",len(tax_ids))
        else:
            #print(chunk)
            #print(chunk.iloc[:,1].astype(int).tolist())
            #chunk[2] = pd.to_numeric(chunk[2], errors='coerce')
            #filtered_chunk = chunk.dropna(subset=[2])
            #trie_keys.extend(chunk[1].astype(str).tolist())
            #tax_ids.extend(chunk[2].tolist())
            #print("Taxids done post clean :",len(tax_ids))
            continue
    
    trie = marisa_trie.Trie(trie_keys)
    trie_indices = [trie[k] for k in trie_keys]
    ordered_tax_ids = [x for _, x in sorted(zip(trie_indices, tax_ids))]
    tax_ids_array = np.array(ordered_tax_ids, dtype=np.int32)
    np.save(f'{directory}/dumps/ordered_tax_ids.npy', tax_ids_array)
    trie.save(f'{directory}/dumps/accession_trie.marisa')

def initialize():
    site_packages = site.getsitepackages()[0]
    for root, dirs, files in os.walk(site_packages):
        if "MRItaxonomy" in dirs:
            directory = os.path.join(root, "MRItaxonomy")
            break
        else:
            print("Bad installation location")
            raise SystemExit

    if not os.path.exists(f'{directory}/dumps'):
        os.makedirs(f'{directory}/dumps') #make sure this is here

    print('Initializing...')
    if not os.path.exists(f'{directory}/dumps/new_taxdump.tar.gz.md5'):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz.md5', out=f'{directory}/dumps/new_taxdump.tar.gz.md5')
    if not os.path.exists(f'{directory}/dumps/new_taxdump.tar.gz'):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz', out=f'{directory}/dumps/new_taxdump.tar.gz')
    print(f'\nTaxonomy dump files downloaded to {directory}/dumps.')
    if not os.path.exists(f'{directory}/dumps/nucl_gb.accession2taxid.gz'):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz', out=f'{directory}/dumps/nucl_gb.accession2taxid.gz')
    if not os.path.exists(f'{directory}/dumps/nucl_gb.accession2taxid.gz.md5'):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz.md5', out=f'{directory}/dumps/nucl_gb.accession2taxid.gz.md5')
    if not os.path.exists(f'{directory}/dumps/prot.accession2taxid.gz'):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz', out=f'{directory}/dumps/prot.accession2taxid.gz')
    if not os.path.exists(f'{directory}/dumps/prot.accession2taxid.gz.md5'):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz.md5', out=f'{directory}/dumps/prot.accession2taxid.gz.md5')
    print(f'\nAccession2taxid dump files downloaded to {directory}/dumps.')
    #could replace these with the gzip and tarfile modules, but they return file and tarfile objects, so this os.subprocess is cleaner. Change this if portability becomes an issue
    #os.system(f'gunzip -c {directory}/dumps/nucl_gb.accession2taxid.gz > {directory}/dumps/nucl_gb.accession2taxid')
    print('Unzipping nucl_gb.accession2taxid.gz')
    subprocess.run(f'gunzip -c {directory}/dumps/nucl_gb.accession2taxid.gz > {directory}/dumps/nucl_gb.accession2taxid', shell=True, text=True, capture_output=True)
    #os.system(f'gunzip -c {directory}/dumps/prot.accession2taxid.gz > {directory}/dumps/prot.accession2taxid')
    print('Unzipping prot.accession2taxid.gz')
    subprocess.run(f'gunzip -c {directory}/dumps/prot.accession2taxid.gz > {directory}/dumps/prot.accession2taxid', shell=True, text=True, capture_output=True)
    #os.system(f'tar -C {directory}/dumps -xzf {directory}/dumps/new_taxdump.tar.gz')
    print('Untarring new_taxdump.tar.gz')
    subprocess.run(f'tar -C {directory}/dumps -xzf {directory}/dumps/new_taxdump.tar.gz', shell=True, text=True, capture_output=True)
    build_trie(directory)

    
def update():
    print('Updating all databases')
    site_packages = site.getsitepackages()[0]
    for root, dirs, files in os.walk(site_packages):
        if "MRItaxonomy" in dirs:
            directory = os.path.join(root, "MRItaxonomy")
            break
        else:
            print("Bad installation location")
            raise SystemExit
    if not os.path.exists(f'{directory}/dumps'):
        os.makedirs(f'{directory}/dumps') #make sure this is here

    #os.system(f'md5sum {directory}/dumps/nucl_gb.accession2taxid.gz | cut -d\  -f1 > {directory}/dumps/old.md5') #generate md5sum and push to file. Python doesn't have an elegant way to make md5s or compare them
    subprocess.run(f'md5sum {directory}/dumps/nucl_gb.accession2taxid.gz | cut -d\  -f1 > {directory}/dumps/old.md5', shell=True, text=True, capture_output=True)
    with open(f'{directory}/dumps/old.md5') as f:
        old5 = f.readlines()[0].strip('\n') #get the md5 of the existing file
    os.remove(f'{directory}/dumps/old.md5') #remove temp file
    
    if os.path.exists('{directory}/dumps/nucl_gb.accession2taxid.gz.md5'):
        os.remove('{directory}/dumps/nucl_gb.accession2taxid.gz.md5')
        
    wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz.md5', out=f'{directory}/dumps/nucl_gb.accession2taxid.gz.md5') #download md5 for comparison to existing file
    #os.rename('nucl_gb.accession2taxid.gz.md5', '{0}/dumps/nucl_gb.accession2taxid.gz.md5') #move it
    with open(f'{directory}/dumps/nucl_gb.accession2taxid.gz.md5') as f: #open it and pull the md5 hash from the file
        new5 = f.readlines()[0].split(' ')[0] #because it also contains the filename
    if new5 == old5: #compare
        print('\nThe accession dump files are up to date.\n') #you're done. Congratulations on being up to date

    else: #you got work to do
        if os.path.exists(f'{directory}/dumps/nucl_gb.accession2taxid.gz'):
            os.remove(f'{directory}/dumps/nucl_gb.accession2taxid.gz')
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz', out=f'{directory}/dumps/nucl_gb.accession2taxid.gz')
        #os.rename('nucl_gb.accession2taxid.gz', '{0}/dumps/nucl_gb.accession2taxid.gz')
        
        #os.system(f'gunzip {directory}/dumps/nucl_gb.accession2taxid.gz')
        subprocess.run(f'tar -C {directory}/dumps -xzf {directory}/dumps/new_taxdump.tar.gz',shell=True, text=True, capture_output=True)
        print(f'\nUpdated accession2taxid dump files downloaded to {directory}/dumps.')
        build_trie(directory)


    #os.system(f'md5sum {directory}/dumps/new_taxdump.tar.gz | cut -d\  -f1 > {directory}/dumps/old.md5') #generate md5sum and push to file. Python doesn't have an elegant way to make md5s or compare them
    subprocess.run(f'tar -C {directory}/dumps -xzf {directory}/dumps/new_taxdump.tar.gz',shell=True, text=True, capture_output=True)
    with open(f'{directory}/dumps/old.md5') as f:
        old5 = f.readlines()[0].strip('\n') #get the md5 of the existing file
    os.remove(f'{directory}/dumps/old.md5') #remove temp file
    
    if os.path.exists(f'{directory}/dumps/new_taxdump.tar.gz.md5'):
        os.remove(f'{directory}/dumps/new_taxdump.tar.gz.md5')
        
    wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz.md5', out=f'{directory}/dumps/new_taxdump.tar.gz.md5')
    #os.rename('new_taxdump.tar.gz.md5', '{0}/dumps/new_taxdump.tar.gz.md5')
    with open(f'{directory}/dumps/new_taxdump.tar.gz.md5') as f: #open it and pull the md5 hash from the file
        new5 = f.readlines()[0].split(' ')[0] #because it also contains the filename
    if new5 == old5: #compare
        print('\nThe taxonomy dump files are up to date.\n') #you're done. Congratulations on being up to date
    else:
        if os.path.exists(f'{directory}/dumps/new_taxdump.tar.gz'):
            os.remove(f'{directory}/dumps/new_taxdump.tar.gz')
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz', out=f'{directory}/dumps/new_taxdump.tar.gz')
        #os.rename('new_taxdump.tar.gz', '{0}/dumps/new_taxdump.tar.gz')
        #os.system(f'tar -C {directory}/dumps -xzf {directory}/dumps/new_taxdump.tar.gz')
        subprocess.run(f'tar -C {directory}/dumps -xzf {directory}/dumps/new_taxdump.tar.gz', shell=True, text=True, capture_output=True)
        print(f'\nUpdated taxonomy dump files downloaded to {directory}/dumps.')
































