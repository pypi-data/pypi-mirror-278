import pandas as pd
import os
import time
import logging
import site
from MRItaxonomy.NCBI_fetch import initialize

TAXID2NAME_df = None
TAXID2NAME_df2 = None

def load_dataframe():
    logger = logging.getLogger(__name__)
    global TAXID2NAME_df
    global TAXID2NAME_df2
    if TAXID2NAME_df is None:

        site_packages = site.getsitepackages()[0]
        for root, dirs, files in os.walk(site_packages):
            if "MRItaxonomy" in dirs:
                nodedb_path = os.path.join(root, "MRItaxonomy")
                break
            else:
                print("Bad installation location")
                raise SystemExit
        nodedb_path=nodedb_path+"/dumps/"
        
        if os.path.exists(nodedb_path+"names.dmp"):
            logger.warning("Names database was last modified: {}".format(time.ctime(os.path.getctime(nodedb_path+"names.dmp"))))
        else:
            initialize()
            if os.path.exists(nodedb_path+"names.dmp"):
                logger.warning("Names database was last modified: {}".format(time.ctime(os.path.getctime(nodedb_path+"names.dmp"))))
            else:
                logger.critical("Database file not found.")
                raise SystemExit
        
        
        headers = ("tax_id", "name","type")
        TAXID2NAME_df = pd.read_table(nodedb_path+"names.dmp", sep="|", names=headers,index_col=0,usecols=(0,1,3))
        TAXID2NAME_df["name"] = TAXID2NAME_df["name"].str.strip()
        TAXID2NAME_df["type"] = TAXID2NAME_df["type"].str.strip()
        TAXID2NAME_df = TAXID2NAME_df[TAXID2NAME_df['type'].str.contains('scientific name')]
        mergedheaders = ("original", "merged")
        TAXID2NAME_df2 = pd.read_table(nodedb_path+"merged.dmp", sep="|", names=mergedheaders,index_col=0,usecols=(0,1))
    
    return TAXID2NAME_df, TAXID2NAME_df2


def get_merge(tid):
    TAXID2NAME_df, TAXID2NAME_df2 = load_dataframe()
    if tid not in TAXID2NAME_df.index:
        if tid in TAXID2NAME_df2.index:
            return TAXID2NAME_df2.loc[tid]['merged']
        else:
            return 0
    else:
	    return tid
	
def get_name(tax):
    TAXID2NAME_df, _ = load_dataframe()
    tax = get_merge(tax)
    return TAXID2NAME_df.loc[tax]['name']
