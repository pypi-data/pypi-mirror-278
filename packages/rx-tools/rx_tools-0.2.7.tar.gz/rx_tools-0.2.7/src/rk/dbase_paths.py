from log_store import log_store
import os

log = log_store.add_logger('rk_tools:dbase_paths')
#-----------------------------------
class dbase_paths:
    def __init__(self):
        self._l_kind = ['bdt_prc', 'bdt_cmb']
    #-----------------------------------
    def _check_path(self, path):
        is_dir = os.path.isdir(path)
        is_fil = os.path.isfile(path)

        if (not is_dir) and (not is_fil):
            log.error(f'Path {path} not a file or directory')
            raise
    #-----------------------------------
    def __call__(self, kind):
        if kind not in self._l_kind:
            log.error(f'Invalid kind {kind}, choose from: {self._l_kind}')
            raise

        if   kind == 'bdt_prc':
            path = f'{os.environ["MVADIR"]}/electron/bdt_v10.18is.prec'
        elif kind == 'bdt_cmb':
            path = f'{os.environ["MVADIR"]}/electron/bdt_v10.11tf.a0v2ss'
        else:
            log.error(f'Invalid kind: {kind}')
            raise

        self._check_path(path)

        return path
#-----------------------------------
