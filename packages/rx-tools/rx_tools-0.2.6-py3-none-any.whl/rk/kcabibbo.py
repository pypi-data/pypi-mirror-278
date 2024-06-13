import read_selection as rs
import os
import glob
import math
import ROOT
import jacobi as jac

from log_store import log_store

log=log_store.add_logger('tools:kcabibbo')
#------------------------------
class kcabibbo:
    def __init__(self, trig=None, year=None):
        self._trig = trig
        self._year = year 
        self._vers = 'v10.21p2'

        self._sig_br = 1.02e-3, 0.019e-3 
        self._cab_br = 3.92e-5, 0.080e-5

        self._pid_cut = rs.get('pid', trig, q2bin='jpsi', year = self._year)

        self._initialized = False
    #------------------------
    def _initialize(self):
        if self._initialized:
            return

        if self._year == 'r1':
            self._year = '2012'

        if self._year == 'r2p1':
            self._year = '2016'

        self._initialized = True 
    #------------------------
    def _get_eff(self, rdf):
        ival= rdf.Count().GetValue()
        rdf = rdf.Filter(self._pid_cut)
        fval= rdf.Count().GetValue()

        eff_up = ROOT.TEfficiency.Wilson(ival, fval, 0.68,  True)
        eff_dn = ROOT.TEfficiency.Wilson(ival, fval, 0.68, False)

        eff_err= (eff_up - eff_dn) / 2.
        eff_val= (eff_up + eff_dn) / 2.

        return eff_val, eff_err 
    #------------------------
    def _get_data(self, proc):
        cas_dir = os.environ['CASDIR']
        root_wc = f'{cas_dir}/tools/apply_selection/misid/{proc}/{self._vers}/{self._year}_{self._trig}/*.root'
        l_root  = glob.glob(root_wc)
        if len(l_root) == 0:
            log.error(f'Cannot find: {root_wc}')
            raise FileNotFoundError

        rdf     = ROOT.RDataFrame(self._trig, l_root)

        return rdf
    #------------------------
    def _divide(self, a, b):
        val, var = jac.propagate(lambda x : x[0] / x[1], [a[0], b[0]], [[a[1] ** 2, 0], [0, b[1] ** 2]])
        err = math.sqrt(var)

        return val, err
    #------------------------
    def _multiply(self, a, b):
        val, var = jac.propagate(lambda x : x[0] * x[1], [a[0], b[0]], [[a[1] ** 2, 0], [0, b[1] ** 2]])
        err = math.sqrt(var)

        return val, err
    #------------------------
    def _get_rate(self):
        rdf_sg = self._get_data('ctrl')
        rdf_cs = self._get_data('ctrl_pi')

        eff_sg = self._get_eff(rdf_sg)
        eff_cs = self._get_eff(rdf_cs)

        mid    = self._divide(eff_cs, eff_sg)

        return mid
    #------------------------
    def get_factor(self):
        '''
        Will provide the factor that the number of resonant J/psi candidates has to be
        multiplied by to give the cabibbo suppresed value, i.e.:

        (Br(cabibbo)/Br(signal)) * (eff_cabibbo / eff_signal)

        the return value is a value, error tuple
        '''
        self._initialize()

        rat = self._get_rate()
        rbf = self._divide(self._cab_br, self._sig_br)
        fac = self._multiply(rat, rbf)

        return fac
#------------------------------

