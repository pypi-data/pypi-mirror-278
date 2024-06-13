from grid.dat_thresholds import d_tck_thr_el as d_thr_el
from grid.dat_thresholds import d_tck_thr_mu as d_thr_mu
from grid.dat_thresholds import d_tck_thr_kp as d_thr_kp
from grid.sim_thresholds import d_tck_prb    as d_prb

from log_store import log_store

import pprint

log = log_store.add_logger('tools:trig_thresholds')
#----------------------------------
class reader:
    def __init__(self, tag_trigger=None, year=None):
        self._tag_trig = tag_trigger
        self._year     = int(year)
        self._d_thr    = None
        self._l_tck_thr= None

        self._initialized = False
    #----------------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._pick_threshold()
        self._set_tck_thr_list()

        self._initialized = True 
    #----------------------------------
    def _set_tck_thr_list(self):
        [dn_tp, up_tp] = [ (pol, l_tck, l_thr) for (year, pol), (l_tck, l_thr) in d_prb.items() if year == self._year]
        l_tck_thr      = []
        l_tck_thr     += self._get_thr_list(dn_tp)
        l_tck_thr     += self._get_thr_list(up_tp)

        self._l_tck_thr = l_tck_thr
    #----------------------------------
    def _get_thr_list(self, pol_tup):
        pol, l_tck, l_thr = pol_tup

        l_tck_thr = [ (pol * tck, thr) for tck, thr in zip(l_tck, l_thr) ]

        return l_tck_thr
    #----------------------------------
    def _pick_threshold(self):
        if   'L0Electron' in self._tag_trig:
            d_thr = d_thr_el
            log.debug(f'Picking electron trigger for tagging trigger: {self._tag_trig}')
        elif 'L0Hadron'   in self._tag_trig:
            d_thr = d_thr_kp
            log.debug(f'Picking hadron trigger for tagging trigger: {self._tag_trig}')
        elif 'L0Muon'     in self._tag_trig:
            d_thr = d_thr_mu
            log.debug(f'Picking muon trigger for tagging trigger: {self._tag_trig}')
        else:
            log.error(f'Unrecognized tagging trigger: {self._tag_trig}')
            raise

        cnv = 1
        if   'L0Muon' in self._tag_trig and self._year in [2011, 2012]:
            cnv = 40
        elif 'L0Muon' in self._tag_trig: 
            cnv = 50

        self._d_thr = {tck : thr * cnv for (tck, year), thr in d_thr.items() if year == self._year }
    #----------------------------------
    def _average(self):
        tot = 0
        num = 0
        for tck, prb in self._l_tck_thr:
            tck=abs(tck)
            thr=self._d_thr[tck]

            if thr <= 0:
                log.error(f'Invalid threshold {thr} found for TCK {tck} with lumi fraction {prb}')
                raise

            tot+=prb
            num+=thr * prb

        return num/tot
    #----------------------------------
    def get_threshold(self):
        self._initialize()

        return self._average()
#----------------------------------

