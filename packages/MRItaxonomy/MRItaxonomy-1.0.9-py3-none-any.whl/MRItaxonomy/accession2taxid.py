import numpy as np
import os
import time
import logging
import site
from MRItaxonomy.NCBI_fetch import initialize
import marisa_trie

ACCESSION2TAXID_trie = None
ACCESSION2TAXID_txid_arr = None
'''
ACCESSION2TAXID_df = None
def load_dataframe():
    logger = logging.getLogger(__name__)
    global ACCESSION2TAXID_df
    if ACCESSION2TAXID_df is None:
        site_packages = site.getsitepackages()[0]
        for root, dirs, files in os.walk(site_packages):
            if "MRItaxonomy" in dirs:
                db_path = os.path.join(root, "MRItaxonomy")
                break
            else:
                print("Bad installation location")
                raise SystemExit
        db_path=db_path+"/dumps/"
        
        if os.path.exists(db_path+'nucl_gb.accession2taxid'):
            logger.warning("Accession2taxid database was last modified: {}".format(time.ctime(os.path.getctime(db_path+'nucl_gb.accession2taxid'))))
        else:
            initialize()
            if os.path.exists(db_path+'nucl_gb.accession2taxid'):
                logger.warning("Accession2taxid database was last modified: {}".format(time.ctime(os.path.getctime(db_path+'nucl_gb.accession2taxid'))))
            else:
                logger.critical("Database file not found.")
                raise SystemExit
        
        ACCESSION2TAXID_df = pd.read_table(db_path+'nucl_gb.accession2taxid',index_col=0,usecols=(1,2))
    return ACCESSION2TAXID_df

def get_taxid(a_num):
    ACCESSION2TAXID_df = load_dataframe()
    try:
        return ACCESSION2TAXID_df.loc[a_num].taxid
    except: return -1
'''
def load_trie():
    logger = logging.getLogger(__name__)
    global ACCESSION2TAXID_trie
    global ACCESSION2TAXID_txid_arr
    if ACCESSION2TAXID_trie is None:
        site_packages = site.getsitepackages()[0]
        for root, dirs, files in os.walk(site_packages):
            if "MRItaxonomy" in dirs:
                db_path = os.path.join(root, "MRItaxonomy")
                break
            else:
                print("Bad installation location")
                raise SystemExit
        db_path=db_path+"/dumps/"
        if os.path.exists(db_path+'nucl_gb.accession2taxid'):
            logger.warning("Accession2taxid database was last modified: {}".format(time.ctime(os.path.getctime(db_path+'nucl_gb.accession2taxid'))))
        else:
            initialize()
            if os.path.exists(db_path+'nucl_gb.accession2taxid'):
                logger.warning("Accession2taxid database was last modified: {}".format(time.ctime(os.path.getctime(db_path+'nucl_gb.accession2taxid'))))
            else:
                logger.critical("Database file not found.")
                raise SystemExit
        ACCESSION2TAXID_trie = marisa_trie.Trie()
        ACCESSION2TAXID_trie.load(db_path+'accession_trie.marisa')
        ACCESSION2TAXID_txid_arr = np.load(db_path+'ordered_tax_ids.npy')
    return ACCESSION2TAXID_trie, ACCESSION2TAXID_txid_arr


def get_taxid(a_num):
    ACCESSION2TAXID_trie, ACCESSION2TAXID_txid_arr = load_trie()
    try:
        return ACCESSION2TAXID_txid_arr[ACCESSION2TAXID_trie[a_num]]
    except: return -1
    
