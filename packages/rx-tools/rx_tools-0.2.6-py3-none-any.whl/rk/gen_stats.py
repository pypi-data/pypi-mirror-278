import os
import glob
import numpy
import pprint
import pandas as pnd

from log_store import log_store

log = log_store.add_logger('tools:gen_stats')
#-----------------------------------------
def add_cutflows(l_eff_wc):
    '''
    Parameters
    -----------------
    l_eff_wc (list): Each element is a path with a wildcard to JSON files storing the cutflow
    e.g. /a/b/c/*.json

    Returns
    -----------------
    df_eff : Pandas dataframe with cutflow merged from original wildcard 
    '''
    l_eff_path = []
    for eff_wc in l_eff_wc:
        l_eff_path += glob.glob(eff_wc)

    if len(l_eff_path) == 0:
        log.error(f'Found no paths in: ')
        pprint.pprint(l_eff_wc)
        raise

    l_eff_df_1 = [ pnd.read_json(eff_path)  for eff_path in l_eff_path ]
    l_eff_df_2 = [ df.drop(['Efficiency', 'Cumulative'], axis=1) for df in l_eff_df_1 ]
    l_eff_mat  = [ df.to_numpy() for df in l_eff_df_2 ]
    eff_mat    = numpy.sum(l_eff_mat, axis=0)
    df_eff     = pnd.DataFrame(eff_mat, columns=['Total', 'Passed'], index=l_eff_df_2[0].index)

    df_eff['Efficiency']  = df_eff.Passed / df_eff.Total
    df_eff['Cummulative'] = df_eff.Efficiency.cumprod() 

    return df_eff
#-----------------------------------------------------------
def get_ngen(proc, trig, year, sim_ver):
    data_dir= f'{os.environ["ASLDIR"]}/r_fits'
    path    =  f'{data_dir}/{proc}/{sim_ver}/{year}_{trig}/*eff.json'
    df      =  add_cutflows([path])
    ngen    =  df.Total.reco

    return ngen
#-----------------------------------------------------------

