import pandas as pd
import os
import time
import logging
import site
from MRItaxonomy.NCBI_fetch import initialize

PROTACC2TAXID_df = None

def load_dataframe():
    logger = logging.getLogger(__name__)
    global PROTACC2TAXID_df
    if PROTACC2TAXID_df is None:
        site_packages = site.getsitepackages()[0]
        for root, dirs, files in os.walk(site_packages):
            if "MRItaxonomy" in dirs:
                db_path = os.path.join(root, "MRItaxonomy")
                break
            else:
                print("Bad installation location")
                raise SystemExit
        db_path=db_path+"/dumps/"
        
        if os.path.exists(db_path+'prot.accession2taxid'):
            logger.warning("Accession2taxid database was last modified: {}".format(time.ctime(os.path.getctime(db_path+'prot.accession2taxid'))))
        else:
            initialize()
            if os.path.exists(db_path+'prot.accession2taxid'):
                logger.warning("Accession2taxid database was last modified: {}".format(time.ctime(os.path.getctime(db_path+'prot.accession2taxid'))))
            else:
                logger.critical("Database file not found.")
                raise SystemExit
        
        PROTACC2TAXID_df = pd.read_table(db_path+'prot.accession2taxid',index_col=0,usecols=(1,2))
    return PROTACC2TAXID_df


def get_taxid(a_num):
    PROTACC2TAXID_df = load_dataframe()
    try:
        return PROTACC2TAXID_df.loc[a_num].taxid
    except: return -1

