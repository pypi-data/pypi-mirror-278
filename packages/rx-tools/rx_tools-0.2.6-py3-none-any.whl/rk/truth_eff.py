import utils_noroot as utnr
import pandas       as pnd
import os

from log_store import log_store

log = log_store.add_logger('rx_tools:truth_eff') 
#---------------------------------------
def get_eff(sample, year, trig, version, kind):
    cas_dir   = os.environ['CASDIR']
    file_path = f'{cas_dir}/monitor/truth_eff/{version}/{kind}/data.json'
    if not os.path.isfile(file_path):
        log.error(f'Cannot find {file_path}')
        raise

    df = pnd.read_json(file_path)
    df = df.set_index('Sample', drop=True)

    sample = f'{sample}_{trig}_{year}'
    row    = df.loc[sample]
    eff    = row.Efficiency

    return eff 
#---------------------------------------

