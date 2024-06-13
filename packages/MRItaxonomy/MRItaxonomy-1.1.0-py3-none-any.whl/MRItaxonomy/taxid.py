import pandas as pd
import os
import time
import site
import logging

df = None
df2 = None

def load_dbs():
    logger = logging.getLogger(__name__)
    global df
    global df2
    if df is None or df2 is None:
        site_packages = site.getsitepackages()[0]
        for root, dirs, files in os.walk(site_packages):
            if "MRItaxonomy" in dirs:
                nodedb_path = os.path.join(root, "MRItaxonomy")
                break
            else:
                print("Bad installation location")
                raise SystemExit
        
        nodedb_path=nodedb_path+"/dumps/"
        if os.path.exists(nodedb_path+"nodes.dmp") and os.path.exists(nodedb_path+"merged.dmp"):
            logger.warning("Nodes database was last modified: {}".format(time.ctime(os.path.getctime(nodedb_path+"nodes.dmp"))))
            logger.warning("Merged database was last modified: {}".format(time.ctime(os.path.getctime(nodedb_path+"merged.dmp"))))
        else:
            logger.critical("One or more database files are missing. Run update.py to download.")
            raise SystemExit
        
        headers = ("tax_id", "parent", "rank")
        df = pd.read_table(nodedb_path+"nodes.dmp", sep="|", names=headers,index_col=0,usecols=(0,1,2))
        df["rank"] = df["rank"].str.strip()
        mergedheaders = ("original", "merged")
        df2 = pd.read_table(nodedb_path+"merged.dmp", sep="|", names=mergedheaders,index_col=0,usecols=(0,1))
    return df, df2


def getparent(tid):
    df, df2 = load_dbs()
    if tid in df.index:
        return df.loc[tid].parent
    elif tid in df2.index:
        return df.loc[df2.loc[tid]["merged"]].parent
    else:
        return 0
    

def getrank(tid):
    df, df2 = load_dbs()
    if tid in df.index:
        return df.loc[tid]["rank"]
    elif tid in df2.index:
        return df.loc[df2.loc[tid]["merged"]]["rank"]
    else:
        return "na"

def getnodeatrank(tid, selectedrank):
    currentrank = getrank(tid)
    if not getrank(tid) == 'na':

        while(currentrank != selectedrank and tid != 1):
            nextnode = getparent(tid)
            currentrank = getrank(nextnode)
            tid = nextnode
        else:
            if currentrank == selectedrank:
                return tid
            else:
                return 0

    else:
        return 0

def get_merge(tid):
    df, df2 = load_dbs()
    if tid not in df.index:
        if tid in df2.index:
            return df2.loc[tid]['merged']
        else:
            return 0
    else:
        return tid

