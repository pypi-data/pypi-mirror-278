from log_store import log_store

import os
import glob
import pprint
import utils_noroot as utnr

log = log_store.add_logger('rx_tools:cut_checker')
#TODO:
#Implement HLT2 comparison
#Do not check 2016 if r2p1 but actual year
#-------------------------------
class cut_checker:
    '''
    Used to check if cuts used to get efficiencies and yilds are the same
    '''
    def __init__(self, yld=None, eff=None):
        self._yld_path = yld 
        self._eff_path = eff 

        self._initialized = False
    #-------------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._eff_path = self._get_efficiency_path()

        self._check_file(self._yld_path)
        self._check_file(self._eff_path)

        self._initialized = True
    #-------------------------------
    def _get_efficiency_path(self):
        if   '_r2p1_' in self._eff_path:
            eff_wc = self._eff_path.replace('_r2p1_', '_2016_')
        elif   '_r1_' in self._eff_path:
            eff_wc = self._eff_path.replace(  '_r1_', '_2011_')
        else:
            eff_wc = self._eff_path

        l_eff_path = glob.glob(eff_wc)
        try:
            eff_path = l_eff_path[0]
        except:
            log.error(f'Cannot find at least one path in: {eff_wc}')
            raise 

        return eff_path
    #-------------------------------
    def _check_file(self, path):
        if not os.path.isfile(path):
            log.error(f'File not found: \"{path}\"')
            raise FileNotFoundError
    #-------------------------------
    def _compare_cuts(self, d_yld, d_eff):
        s_both = self._get_common_cuts(d_yld, d_eff)
        fail=False
        for common_cut in s_both:
            if common_cut in ['hlt2', 'truth']:
                continue

            yld_cut = d_yld[common_cut]
            eff_cut = d_eff[common_cut]
            if yld_cut != eff_cut:
                fail=True
                log.warning(common_cut)
                log.warning(f'{"Yield cut":<20}{yld_cut}')
                log.warning(f'{"Efficiency cut":<20}{eff_cut}')

        if fail:
            log.error(f'Failed comparison')
            raise
    #-------------------------------
    def _get_common_cuts(self, d_yld, d_eff):
        s_eff_cut = { eff_cut for eff_cut in d_eff }
        s_yld_cut = { yld_cut for yld_cut in d_yld }

        s_both    = s_eff_cut.intersection(s_yld_cut)
        s_eff     = s_eff_cut.difference(s_yld_cut)
        s_yld     = s_yld_cut.difference(s_eff_cut)

        log.debug(f'Common cuts: {s_both}')
        log.debug(f'Efficiency only: {s_eff}')
        log.debug(f'Yields only: {s_yld}')

        return s_both
    #-------------------------------
    def _fix_yld_keys(self, d_yld):
        d_yld['bdt'] = d_yld.pop('BDT')
        d_yld['qsq'] = d_yld.pop('QSQ')
        d_yld['mass']= d_yld.pop('MASS')

        return d_yld
    #-------------------------------
    def check(self):
        self._initialize()

        d_yld = utnr.load_json(self._yld_path)['Cut']
        d_eff = utnr.load_json(self._eff_path)['Cut']
        d_yld = self._fix_yld_keys(d_yld)

        self._compare_cuts(d_yld, d_eff)
#-------------------------------

