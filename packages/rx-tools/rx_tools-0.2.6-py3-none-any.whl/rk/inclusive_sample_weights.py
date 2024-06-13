
import pprint
import glob
import os
import pdg_utils as pu
import pandas    as pnd

from importlib.resources import files
from log_store           import log_store

log = log_store.add_logger('rx_tools:inclusive_sample_weights')
#---------------------------
class reader:
    def __init__(self, df, year=None):
        self._year = int(year)
        self._df   = df
        self._fu   = 0.408
        self._fs   = 0.100

        self._d_bf        = dict() 
        self._d_fev       = dict() 
        self._d_tp_st     = None
        self._initialized = False
    #---------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._d_bf['bpXcHs'] = 0.1596, pu.get_bf('B+ --> J/psi(1S) K+')
        self._d_bf['bdXcHs'] = 0.1920, pu.get_bf('B0 --> J/psi(1S) K0')
        self._d_bf['bsXcHs'] = 0.1077, pu.get_bf('B_s()0 --> J/psi(1S) phi')

        self._cache_stats()

        self._initialized = True
    #---------------------------
    def _get_br_wgt(self, row):
        '''
        Will return pdg_br / decay file br weight
        '''
        #--------------------------------------------
        #Decay B+sig
        #0.1596  MyJ/psi    K+           SVS ;
        #--------------------------------------------
        #Decay B0sig
        #0.1920  MyJ/psi    MyK*0        SVV_HELAMP PKHplus PKphHplus PKHzero PKphHzero PKHminus PKphHminus ;
        #--------------------------------------------
        #Decay B_s0sig
        #0.1077  MyJ/psi    Myphi        PVV_CPLH 0.02 1 Hp pHp Hz pHz Hm pHm;
        #--------------------------------------------

        dec, pdg = self._d_bf[row.proc]

        return pdg / dec
    #---------------------------
    def _get_hd_wgt(self, row):
        '''
        Will return hadronization fractions used as weights
        '''
        if   row.proc in ['bpXcHs', 'bdXcHs']:
            return self._fu
        elif row.proc == 'bsXcHs':
            return self._fs
        else:
            log.error(f'Invalid process: {row.proc}')
            raise
    #---------------------------
    def _get_stats(self, path):
        proc = os.path.basename(path).replace('.json', '')
        df   = pnd.read_json(path)

        return proc, df
    #---------------------------
    def _cache_stats(self):
        if self._d_tp_st is not None:
            return

        stats_wc = files('tools_data').joinpath('inclusive_mc_stats/*.json')
        stats_wc = str(stats_wc)
        l_stats  = glob.glob(stats_wc)
        if len(l_stats) == 0:
            log.error(f'No file found in: {stats_wc}')
            raise

        l_tp_st = [ self._get_stats(path) for path in l_stats ]
        self._d_tp_st = dict(l_tp_st)
    #---------------------------
    def _good_rows(self, r1, r2):
        if {r1.Polarity, r2.Polarity} != {'MagUp', 'MagDown'}:
            log.error(f'Latest rows for {self._year} are not of opposite polarities')
            return False

        if r1.Events <= 0 or r2.Events <= 0:
            log.error(f'Either polarity number of events is negative for {self._year}')
            return False

        return True
    #---------------------------
    def _get_nevt(self, proc):
        '''
        Will return a list with the number of events 
        processed by DaVinci for all the inclusive samples
        and for a given year
        '''

        df = self._d_tp_st[proc]
        df = df[df.Year == self._year]
        df = df.reset_index(drop=True)
        if len(df) < 2:
            log.error(f'Cannot extract enough rows for {self._year}')
            print(self._d_tp_st[proc])
            raise

        r1 = df.loc[0]
        r2 = df.loc[1]

        if not self._good_rows(r1, r2):
            print(r1)
            print(r2)
            raise

        nevt = r1.Events + r2.Events

        return nevt
    #---------------------------
    def _get_st_wgt(self, row):
        '''
        Will return weight for number of events processed by
        ganga.
        '''
        if row.proc in self._d_fev:
            return self._d_fev[row.proc]

        d_nev = { proc : self._get_nevt(proc) for proc in self._d_tp_st }
        l_nev = [ nev for nev in d_nev.values() ]
        max_n = max(l_nev)
        self._d_fev = { key : max_n / nev for key, nev in d_nev.items()}

        return self._d_fev[row.proc]
    #---------------------------
    def _get_weight(self, row):
        w1 = self._get_st_wgt(row)
        w2 = self._get_hd_wgt(row)
        w3 = self._get_br_wgt(row)

        return w1 * w2 * w3
    #---------------------------
    def get_weights(self):
        '''
        Returns:

        Pandas series with sample weights
        '''
        self._initialize()

        sr_wgt = self._df.apply(self._get_weight, axis=1)

        return sr_wgt 
#---------------------------

