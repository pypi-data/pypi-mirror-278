import os
import wget
import site
import pandas as pd
import numpy as np
import marisa_trie
import subprocess

#functions called by commands at command line

def build_trie(directory):
    print('Building accession2taxid trie datafiles...')
    chunk_size = 50000
    trie_keys = []
    tax_ids = []
    for chunk in pd.read_csv('{0}/dumps/nucl_gb.accession2taxid'.format(directory), sep='\t', usecols=[1, 2], chunksize=chunk_size, header=0):
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
    np.save('{0}/dumps/ordered_tax_ids.npy'.format(directory), tax_ids_array)
    trie.save('{0}/dumps/accession_trie.marisa'.format(directory))

def initialize():
    site_packages = site.getsitepackages()[0]
    for root, dirs, files in os.walk(site_packages):
        if "MRItaxonomy" in dirs:
            directory = os.path.join(root, "MRItaxonomy")
            break
        else:
            print("Bad installation location")
            raise SystemExit

    if not os.path.exists('{0}/dumps'.format(directory)):
        os.makedirs('{0}/dumps'.format(directory)) #make sure this is here

    print('Initializing...')
    if not os.path.exists('{0}/dumps/new_taxdump.tar.gz.md5'.format(directory)):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz.md5', out='{0}/dumps/new_taxdump.tar.gz.md5'.format(directory))
    if not os.path.exists('{0}/dumps/new_taxdump.tar.gz'.format(directory)):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz', out='{0}/dumps/new_taxdump.tar.gz'.format(directory))
    print('\nTaxonomy dump files downloaded to {0}/dumps.'.format(directory))
    if not os.path.exists('{0}/dumps/nucl_gb.accession2taxid.gz'.format(directory)):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz', out='{0}/dumps/nucl_gb.accession2taxid.gz'.format(directory))
    if not os.path.exists('{0}/dumps/nucl_gb.accession2taxid.gz.md5'.format(directory)):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz.md5', out='{0}/dumps/nucl_gb.accession2taxid.gz.md5'.format(directory))
    if not os.path.exists('{0}/dumps/prot.accession2taxid.gz'.format(directory)):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz', out='{0}/dumps/prot.accession2taxid.gz'.format(directory))
    if not os.path.exists('{0}/dumps/prot.accession2taxid.gz.md5'.format(directory)):
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz.md5', out='{0}/dumps/prot.accession2taxid.gz.md5'.format(directory))
    print('\nAccession2taxid dump files downloaded to {0}/dumps.'.format(directory))
    #could replace these with the gzip and tarfile modules, but they return file and tarfile objects, so this os.subprocess is cleaner. Change this if portability becomes an issue
    #os.system('gunzip -c {0}/dumps/nucl_gb.accession2taxid.gz > {0}/dumps/nucl_gb.accession2taxid'.format(directory))
    #os.system('gunzip -c {0}/dumps/prot.accession2taxid.gz > {0}/dumps/prot.accession2taxid'.format(directory))
    #os.system('tar -C {0}/dumps -xzf {0}/dumps/new_taxdump.tar.gz'.format(directory))
    gunzip_cmd = f'gunzip -c {0}/dumps/nucl_gb.accession2taxid.gz'.format(directory)
    with open(f'{0}/dumps/nucl_gb.accession2taxid'.format(directory), 'w') as file:
        subprocess.run(gunzip_cmd.split(), stdout=file)
        
    gunzip_cmd = f'gunzip -c {directory}/dumps/prot.accession2taxid.gz'.format(directory)
    with open(f'{0}/dumps/prot.accession2taxid'.format(directory), 'w') as file:
        subprocess.run(gunzip_cmd.split(), stdout=file)
        
    tar_cmd = f'tar -C {0}/dumps -xzf {0}/dumps/new_taxdump.tar.gz'.format(directory)
    subprocess.run(tar_cmd.split())
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
    if not os.path.exists('{0}/dumps'.format(directory)):
        os.makedirs('{0}/dumps'.format(directory)) #make sure this is here

    #os.system('md5sum {0}/dumps/nucl_gb.accession2taxid.gz | cut -d\  -f1 > {0}/dumps/old.md5'.format(directory)) #generate md5sum and push to file. Python doesn't have an elegant way to make md5s or compare them
    command = f'md5sum {0}/dumps/nucl_gb.accession2taxid.gz | cut -d " " -f1 > {0}/dumps/old.md5'.format(directory)
    subprocess.run(command, shell=True, check=True)
    with open('{0}/dumps/old.md5'.format(directory)) as f:
        old5 = f.readlines()[0].strip('\n') #get the md5 of the existing file
    os.remove('{0}/dumps/old.md5'.format(directory)) #remove temp file
    
    if os.path.exists('{0}/dumps/nucl_gb.accession2taxid.gz.md5'.format(directory)):
        os.remove('{0}/dumps/nucl_gb.accession2taxid.gz.md5'.format(directory))
        
    wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz.md5', out='{0}/dumps/nucl_gb.accession2taxid.gz.md5'.format(directory)) #download md5 for comparison to existing file
    #os.rename('nucl_gb.accession2taxid.gz.md5', '{0}/dumps/nucl_gb.accession2taxid.gz.md5'.format(directory)) #move it
    with open('{0}/dumps/nucl_gb.accession2taxid.gz.md5'.format(directory)) as f: #open it and pull the md5 hash from the file
        new5 = f.readlines()[0].split(' ')[0] #because it also contains the filename
    if new5 == old5: #compare
        print('\nThe accession dump files are up to date.\n') #you're done. Congratulations on being up to date

    else: #you got work to do
        if os.path.exists('{0}/dumps/nucl_gb.accession2taxid.gz'.format(directory)):
            os.remove('{0}/dumps/nucl_gb.accession2taxid.gz'.format(directory))
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz', out='{0}/dumps/nucl_gb.accession2taxid.gz'.format(directory))
        #os.rename('nucl_gb.accession2taxid.gz', '{0}/dumps/nucl_gb.accession2taxid.gz'.format(directory))
        
        #os.system('gunzip {0}/dumps/nucl_gb.accession2taxid.gz'.format(directory))
        file_path = f'{0}/dumps/nucl_gb.accession2taxid.gz'.format(directory)
        command = ['gunzip', file_path]
        subprocess.run(command, check=True)
        print('\nUpdated accession2taxid dump files downloaded to {0}/dumps.'.format(directory))
        build_trie(directory)


    #os.system('md5sum {0}/dumps/new_taxdump.tar.gz | cut -d\  -f1 > {0}/dumps/old.md5'.format(directory)) #generate md5sum and push to file. Python doesn't have an elegant way to make md5s or compare them
    command = f'md5sum {0}/dumps/new_taxdump.tar.gz | cut -d " " -f1 > {0}/dumps/old.md5'.format(directory)
    subprocess.run(command, shell=True, check=True)
    with open('{0}/dumps/old.md5'.format(directory)) as f:
        old5 = f.readlines()[0].strip('\n') #get the md5 of the existing file
    os.remove('{0}/dumps/old.md5'.format(directory)) #remove temp file
    
    if os.path.exists('{0}/dumps/new_taxdump.tar.gz.md5'.format(directory)):
        os.remove('{0}/dumps/new_taxdump.tar.gz.md5'.format(directory))
        
    wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz.md5', out='{0}/dumps/new_taxdump.tar.gz.md5'.format(directory))
    #os.rename('new_taxdump.tar.gz.md5', '{0}/dumps/new_taxdump.tar.gz.md5'.format(directory))
    with open('{0}/dumps/new_taxdump.tar.gz.md5'.format(directory)) as f: #open it and pull the md5 hash from the file
        new5 = f.readlines()[0].split(' ')[0] #because it also contains the filename
    if new5 == old5: #compare
        print('\nThe taxonomy dump files are up to date.\n') #you're done. Congratulations on being up to date
    else:
        if os.path.exists('{0}/dumps/new_taxdump.tar.gz'.format(directory)):
            os.remove('{0}/dumps/new_taxdump.tar.gz'.format(directory))
        wget.download('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz', out='{0}/dumps/new_taxdump.tar.gz'.format(directory))
        #os.rename('new_taxdump.tar.gz', '{0}/dumps/new_taxdump.tar.gz'.format(directory))
        tar_cmd = f'tar -C {0}/dumps -xzf {0}/dumps/new_taxdump.tar.gz'.format(directory)
        subprocess.run(tar_cmd.split())
        print('\nUpdated taxonomy dump files downloaded to {0}/dumps.'.format(directory))
































