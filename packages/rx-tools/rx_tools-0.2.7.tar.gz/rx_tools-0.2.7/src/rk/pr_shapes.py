import utils_noroot     as utnr
import read_calibration as rcal
import pandas           as pnd
import read_selection   as rs
import matplotlib.pyplot as plt

from rk.cutflow      import cutflow
from rk.efficiency   import efficiency 
#from rk.inclusive    import corrector  as icor

from rk.inclusive_decays_weights import reader     as inclusive_decays_weights
from rk.inclusive_sample_weights import reader     as inclusive_sample_weights
from atr_mgr                     import mgr        as amgr
from rk.selection                import selection  as rksl
from version_management          import get_last_version 

import os
import re 
import ROOT
import glob
import zfit
import utils
import numpy
import pprint

from log_store import log_store

log=log_store.add_logger('rx_tools:pr_shapes')
#-----------------------------------------------------------
class pr_maker:
    def __init__(self, proc, dset, trig, vers, q2bin):
        self._proc   = proc
        self._dset   = dset 
        self._trig   = trig 
        self._vers   = vers 
        self._q2bin  = q2bin

        self._bkg_cat_cut = 'B_BKGCAT < 60'

        self._l_truth_var = [
                'L1_TRUEID',
                'L2_TRUEID',
                'H_TRUEID',
                'Jpsi_TRUEID',
                'B_TRUEID',
                #-----------------------
                'L1_MC_MOTHER_ID',
                'L2_MC_MOTHER_ID',
                'H_MC_MOTHER_ID',
                'Jpsi_MC_MOTHER_ID',
                #-----------------------
                'L1_MC_GD_MOTHER_ID',
                'L2_MC_GD_MOTHER_ID',
                'H_MC_GD_MOTHER_ID',
                'Jpsi_MC_GD_MOTHER_ID',
                #-----------------------
                'L1_MC_GD_GD_MOTHER_ID',
                'L2_MC_GD_GD_MOTHER_ID',
                'H_MC_GD_GD_MOTHER_ID',
                ]
        self._l_main_var  = ['mass_jpsi', 'mass_psi2', 'mass', 'nbrem', 'BDT_cmb', 'BDT_prc']
        self._l_trig_sel  = ['ETOS', 'GTIS']
        self._l_trig_cal  = ['gtis_inclusive', 'L0TIS_EM', 'L0TIS_MH', 'L0ElectronTIS', 'L0ElectronHAD', 'L0HadronElEL']
        self._l_trig      = self._l_trig_sel + self._l_trig_cal

        self._l_proc = ['bpXcHs_ee', 'bdXcHs_ee', 'bsXcHs_ee']
        self._l_dset = ['2012', '2016', '2017', '2018']
        self._l_vers = ['v10.11tf', 'v10.18is', 'v10.21p2']
        self._l_q2bin= ['jpsi', 'psi2', 'high']

        self._initialized   = False
    #-----------------------------------------------------------
    def  _initialize(self):
        if self._initialized:
            return

        if self._trig == 'GTIS_ee':
            self._trig = 'gtis_inclusive'

        utnr.check_included(self._proc , self._l_proc )
        utnr.check_included(self._vers , self._l_vers )
        utnr.check_included(self._dset , self._l_dset )
        utnr.check_included(self._trig , self._l_trig )
        utnr.check_included(self._q2bin, self._l_q2bin)

        self._initialized = True
    #-----------------------------------------------------------
    def _get_rdf(self, year):
        cas_dir = os.environ['CASDIR']
        file_wc = f'{cas_dir}/tools/apply_selection/prec_shape/{self._proc}/{self._vers}/{year}_{self._trig}/*.root'

        log.debug(f'Data: {file_wc}')
        l_file = glob.glob(file_wc)
        if len(l_file) == 0:
            log.error(f'Found no file in: {file_wc}')
            raise

        rdf = ROOT.RDataFrame(self._trig, l_file)
        rdf = self._filter(rdf, year)
        mgr = amgr(rdf)
        rdf = self._add_columns(rdf)
        rdf = mgr.add_atr(rdf)

        return rdf
    #-----------------------------------------------------------
    def _filter(self, rdf, year):
        q2_cut = rs.get('q2'   , self._trig,  self._q2bin, year)
        ms_cut = rs.get('mass' , self._trig,  self._q2bin, year)
        bd_cut = rs.get('bdt'  , self._trig,  self._q2bin, year)

        d_cut         = {}
        d_cut[ 'bct'] = self._bkg_cat_cut
        d_cut[ 'qsq'] = q2_cut           
        d_cut[ 'bdt'] = bd_cut           

        for cut, val in d_cut.items():
            rdf = rdf.Filter(val, cut)

        rep=rdf.Report()
        rep.Print()

        rep               = rdf.Report()
        df_cfl            = utils.rdf_report_to_df(rep)
        df_cfl['cut_val'] = d_cut.values()

        rdf.df_cfl = df_cfl

        return rdf
    #-----------------------------------------------------------
    def _add_columns(self, rdf):
        true_mass = '''
        ROOT::Math::LorentzVector<ROOT::Math::XYZTVector> v_h( H_TRUEP_X,  H_TRUEP_Y,  H_TRUEP_Z,  H_TRUEP_E);
        ROOT::Math::LorentzVector<ROOT::Math::XYZTVector> v_1(L1_TRUEP_X, L1_TRUEP_Y, L1_TRUEP_Z, L1_TRUEP_E);
        ROOT::Math::LorentzVector<ROOT::Math::XYZTVector> v_2(L2_TRUEP_X, L2_TRUEP_Y, L2_TRUEP_Z, L2_TRUEP_E);

        auto v_b = v_h + v_1 + v_2;

        return v_b.M();
        '''

        rdf = rdf.Define('true_mass', true_mass)
        rdf = rdf.Define('mass'     , 'B_M')
        rdf = rdf.Define('mass_jpsi', 'B_const_mass_M[0]')
        rdf = rdf.Define('mass_psi2', 'B_const_mass_psi2S_M[0]')
        rdf = rdf.Define('nbrem'    , 'L1_BremMultiplicity + L2_BremMultiplicity')

        #cor = icor(rdf)
        #rdf = cor.add_weight(name='wgt_br')

        return rdf
    #-----------------------------------------------------------
    def _get_years(self):
        if   self._proc in ['bpXcHs_ee', 'bdXcHs_ee']   and self._dset in [  'r1', '2011']:
            l_year = []
        elif self._proc == 'bpXcHs_ee'                  and self._dset in ['r2p1', '2015', '2016']:
            l_year = []
        #-----------------------------
        elif self._proc == 'bdXcHs_ee'                  and self._dset == 'r2p1':
            l_year = ['2015', '2016']
        #-----------------------------
        elif                               self._dset in ['2011', '2012', '2015', '2016', '2017', '2018']:
            l_year = [self._dset]
        else:
            log.error(f'Cannot find list of year for process "{self._proc}" and dataset "{self._dset}"')
            raise

        log.debug(f'Using years "{l_year}" for process "{self._proc}" and dataset "{self._dset}"')

        if l_year == []:
            log.warning(f'Cannot get model for dataset "{self._dset}", no corresponding files found, skipping')
            raise

        return l_year
    #-----------------------------------------------------------
    def _save_df(self, rdf, out_dir, add_vars):
        df_cfl = rdf.df_cfl
        d_data = rdf.AsNumpy(self._l_main_var + self._l_truth_var + add_vars)
        df_dat = pnd.DataFrame(d_data)

        dat_path = f'{out_dir}/data.json'
        cfl_path = f'{out_dir}/cutflow.json'

        log.debug(f'Saving to: {dat_path}')
        df_dat.to_json(dat_path, indent=4)

        log.debug(f'Saving to: {cfl_path}')
        df_cfl.to_json(cfl_path, indent=4)
    #-----------------------------------------------------------
    def save_data(self, version=None, add_vars=[]):
        self._initialize()

        if version is None:
            log.error(f'Missing version')
            raise

        l_year = self._get_years()
        for year in l_year:
            rdf = self._get_rdf(year)

            prc_dir = os.environ['PRCDIR']
            out_dir = f'{prc_dir}/{version}/{self._proc}_{self._trig}_{self._q2bin}_{year}'
            os.makedirs(out_dir, exist_ok=True)

            self._save_df(rdf, out_dir, add_vars)
#-----------------------------------------------------------
class pr_loader:
    def __init__(self, proc=None, trig=None, q2bin=None, dset=None, vers=None, d_weight=None):
        '''
        Parameters:
        -------------------------
        proc (str): process, should be among _l_proc (see below)
        trig (str): Trigger, element in _l_trig
        q2bin(str): q2 bin, see _l_q2bin
        dset (str): Year for dataset 
        vers (str): Version of JSON file with masses and PDG ID
        d_weight (dict): Dictionary specifying which weights to use, e.g. {'dec' : 1, 'sam' : 1}
        '''
        self._proc = proc
        self._trig = trig
        self._q2bin= q2bin
        self._dset = dset
        self._vers = vers
        self._d_wg = d_weight

        self._l_proc = ['bsXcHs', 'bdXcHs', 'bpXcHs', 'b*XcHs'] 
        self._l_trig = ['ETOS', 'GTIS'] 
        self._l_q2bin= ['jpsi', 'psi2', 'high'] 
        self._l_dset = ['r1', 'r2p1', '2017', '2018']

        self._val_dir = None
        self._prc_dir = None
        self._nbrem   = None
        self._chan    = None
        self._df      = None
        self._d_fstat = {}

        self._l_ee_trig = ['ETOS', 'GTIS']
        self._l_mm_trig = ['MTOS']
        self._d_match   = None

        self._initialized=False
    #-----------------------------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        try:
            self._prc_dir = os.environ['PRCDIR']
        except:
            log.error('PRCDIR variable not found in environment')
            raise

        self._check_valid(self._proc , self._l_proc,  'proc')
        self._check_valid(self._trig , self._l_trig,  'trig')
        self._check_valid(self._q2bin, self._l_q2bin, 'q2bin')
        self._check_valid(self._dset , self._l_dset,  'dset')
        self._check_weights()

        if self._dset in ['r1', 'r2p1', '2017']:
            self._dset = '2018'

        self._vers    = self._get_version()
        self._d_match = self._get_match_str()
        self._chan    = self._get_channel()
        df            = self._get_df()
        self._df      = self._add_weights(df)

        self._initialized = True
    #-----------------------------------------------------------
    @property
    def val_dir(self):
        return self._val_dir

    @val_dir.setter
    def val_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
        except:
            log.error(f'Cannot make {value}')
            raise

        self._val_dir = value
    #-----------------------------------------------------------
    @property
    def nbrem(self):
        return self._nbrem

    @nbrem.setter
    def nbrem(self, value):
        if value not in [0, 1, 2]:
            log.error(f'Invalid nbrem value of: {value}')
            raise ValueError

        self._nbrem = value
    #-----------------------------------------------------------
    def _check_weights(self):
        try:
            [(k1, v1), (k2, v2)] = self._d_wg.items()
        except:
            log.error(f'Cannot extract two weight flags from: {self._d_wg}')
            raise

        if ([k1, k2] != ['dec', 'sam'])  and ([k1, k2] != ['sam', 'dec']):
            log.error(f'Invalid weight keys: {k1}, {k2}')
            raise

        if (v1 not in [0, 1]) or (v2 not in [0, 1]):
            log.error(f'Invalid weight values: {v1}, {v2}')
            raise
    #-----------------------------------------------------------
    def _check_valid(self, var, l_var, name):
        if var not in l_var:
            log.error(f'Value for {name}, {var}, is not valid')
            raise ValueError
    #-----------------------------------------------------------
    def _get_version(self):
        vers = get_last_version(self._prc_dir)

        if self._vers is None:
            return vers

        if self._vers != vers:
            log.warning(f'Not using last version {vers} but {self._vers}')

        return self._vers
    #-----------------------------------------------------------
    def _get_match_str(self):
        if   self._q2bin == 'jpsi':
            d_match = self._get_match_str_jpsi()
        elif self._q2bin == 'psi2':
            d_match = self._get_match_str_psi2()
        else:
            log.error(f'Invalid q2bin: {self._q2bin}')
            raise

        return d_match
    #-----------------------------------------------------------
    def _get_match_str_jpsi(self):
        bd          = '(abs(B_TRUEID) == 511)'
        bp          = '(abs(B_TRUEID) == 521)'
        bs          = '(abs(B_TRUEID) == 531)'
        
        d_cut                                  = {}
        d_cut[r'$B_d\to c\bar{c}(\to ee)H_s$'] = bd
        d_cut[r'$B^+\to c\bar{c}(\to ee)H_s$'] = bp
        d_cut[r'$B_s\to c\bar{c}(\to ee)H_s$'] = bs

        return d_cut
    #-----------------------------------------------------------
    def _get_match_str_psi2(self):
        bd          = '(abs(B_TRUEID) == 511)'
        bp_psjp     = '(abs(B_TRUEID) == 521) & (abs(Jpsi_TRUEID) == 443) & (abs(Jpsi_MC_MOTHER_ID) == 100443) & (abs(Jpsi_MC_GD_MOTHER_ID) == 521) & (abs(H_MC_MOTHER_ID) == 521)'
        bs          = '(abs(B_TRUEID) == 531)'

        neg_bp_psjp = bp_psjp.replace('==', '!=').replace('&' , '|')
        bp_ex       = f'(abs(B_TRUEID) == 521) & ({neg_bp_psjp})'

        d_cut       = {}
        d_cut[r'$B^+\to \psi(2S)(\to J/\psi X)H_{s}$'] = bp_psjp
        d_cut[r'$B^+\to c\bar{c}(\to ee)H_s$']         = bp_ex
        d_cut[r'$B_d\to c\bar{c}(\to ee)H_s$']         = bd 
        d_cut[r'$B_s\to c\bar{c}(\to ee)H_s$']         = bs

        return d_cut
    #-----------------------------------------------------------
    def _get_match_str_psi2_large(self):
        bp_psjp     = '(abs(Jpsi_MC_MOTHER_ID) == 100443) & (abs(Jpsi_MC_GD_MOTHER_ID) == 521) & (abs(H_MC_MOTHER_ID) == 521)'
        bd_psks     = '(abs(Jpsi_MC_MOTHER_ID) ==    511) & (abs(H_MC_MOTHER_ID) == 313) & (abs(H_MC_GD_MOTHER_ID) == 511) & (abs(Jpsi_TRUEID) == 100443)'
        bp_psks     = '(abs(Jpsi_MC_MOTHER_ID) ==    521) & (abs(H_MC_MOTHER_ID) == 323) & (abs(H_MC_GD_MOTHER_ID) == 521) & (abs(Jpsi_TRUEID) == 100443)'
        
        neg_bp_psjp = bp_psjp.replace('==', '!=').replace('&' , '|')
        neg_bd_psks = bd_psks.replace('==', '!=').replace('&' , '|')
        neg_bp_psks = bp_psks.replace('==', '!=').replace('&' , '|')

        bp_jpkp     = f'(abs(B_TRUEID) == 521) & (abs(H_TRUEID) == 321) & (abs(Jpsi_TRUEID) == 443)'
        bd_jpkp     = f'(abs(B_TRUEID) == 511) & (abs(H_TRUEID) == 321) & (abs(Jpsi_TRUEID) == 443)'
        
        bp_jpkp_ex  = f'({bp_jpkp}) & ({neg_bp_psjp}) & ({neg_bd_psks}) & ({neg_bp_psks})'
        bd_jpkp_ex  = f'({bd_jpkp}) & ({neg_bp_psjp}) & ({neg_bd_psks}) & ({neg_bp_psks})'

        neg_bp_jpkp = bp_jpkp.replace('==', '!=').replace('&' , '|')
        neg_bd_jpkp = bd_jpkp.replace('==', '!=').replace('&' , '|')


        bs          = '(abs(B_TRUEID) == 531)'
        neg_bs      = '(abs(B_TRUEID) != 531)'

        none        = f'({neg_bp_jpkp}) & ({neg_bd_jpkp}) & ({neg_bp_psjp}) & ({neg_bd_psks}) & ({neg_bp_psks}) & ({neg_bs})'
        
        d_cut            = {}
        d_cut['bp_psjp'] = bp_psjp
        d_cut['bp_psks'] = bp_psks
        d_cut['bp_jpkp'] = bp_jpkp_ex
        
        d_cut['bd_psks'] = bd_psks
        d_cut['bd_jpkp'] = bd_jpkp_ex

        d_cut['bs']      = bs

        d_cut['unmatched'] = none

        return d_cut
    #-----------------------------------------------------------
    def _get_match_str_psi2_all(self):
        d_cut           = {}
        d_cut['jpsi']   = '(Jpsi_TRUEID == 443)' 
        d_cut['nojpsi'] = '(Jpsi_TRUEID != 443)' 

        return d_cut
    #-----------------------------------------------------------
    def _get_channel(self):
        if   self._trig in self._l_ee_trig: 
            chan = 'ee' 
        elif self._trig in self._l_mm_trig: 
            chan = 'mm' 
        else:
            log.error(f'Invalid trigger: {self._trig}')
            raise

        return chan
    #-----------------------------------------------------------
    def _get_proc(self, path):
        l_part = path.split('/')
        part   = l_part[-2]
        l_part = part.split('_')
        proc   = l_part[0]
        if proc not in self._l_proc:
            log.error(f'Invalid process: {proc}')
            raise

        return proc
    #-----------------------------------------------------------
    def _df_from_path(self, path):
        log.debug(f'Reading data from: {path}')

        df         = pnd.read_json(path)
        df['proc'] = self._get_proc(path)

        return df
    #-----------------------------------------------------------
    def _get_df(self):
        data_path   = f'{self._prc_dir}/{self._vers}/{self._proc}_{self._chan}_{self._trig}_{self._q2bin}_{self._dset}/data.json'
        l_data_path = glob.glob(data_path)
        if len(l_data_path) == 0:
            log.error(f'No file found in: {data_path}')
            raise

        log.debug(f'Loading data from:')
        pprint.pprint(l_data_path)
        try:
            l_df= [ self._df_from_path(data_path) for data_path in l_data_path ]
            df  = pnd.concat(l_df, axis=0)
        except:
            log.error(f'Cannot read:')
            pprint.pprint(l_data_path)
            raise

        if self._nbrem is not None:
            log.debug(f'Applying nbrem = {self._nbrem} requirement')
            df = df[df.nbrem == self._nbrem] if self._nbrem < 2 else df[df.nbrem >= 2]
            df = df.reset_index(drop=True)

        return df
    #-----------------------------------------------------------
    def _print_wgt_stat(self, arr_wgt):
        l_wgt = arr_wgt.tolist()
        s_wgt = set(l_wgt)

        log.debug('-' * 20)
        log.debug(f'{"Frequency":<10}{"Weight":>10}')
        for wgt in s_wgt:
            nwgt = numpy.count_nonzero(wgt == arr_wgt)
            log.debug(f'{nwgt:<10}{wgt:>10.3}')
    #-----------------------------------------------------------
    def _get_df_id(self, df):
        l_col = [
                'L1_TRUEID',
                'L2_TRUEID',
                'Jpsi_TRUEID',
                'Jpsi_MC_MOTHER_ID',
                'Jpsi_MC_GD_MOTHER_ID',
                'H_TRUEID',
                'H_MC_MOTHER_ID',
                'H_MC_GD_MOTHER_ID',
                'B_TRUEID'
                ]

        df = df[l_col]

        return df.reset_index(drop=True)
    #-----------------------------------------------------------
    def _filter_mass(self, df, mass, obs):
        ([[minx]], [[maxx]]) = obs.limits

        cut   = f'({minx} < {mass}) & ({mass} < {maxx})'
        log.debug(f'Applying: {cut}')
        inum  = df.shape[0]
        df    = df.query(cut)
        fnum  = df.shape[0]

        self._d_fstat[cut] = inum, fnum

        return df
    #-----------------------------------------------------------
    def _filter_cut(self, cut):
        if cut is None:
            return self._df

        log.info(f'Applying cut: {cut}')
        inum = self._df.shape[0]
        df   = self._df.query(cut)
        fnum = df.shape[0]

        self._d_fstat[cut] = inum, fnum

        return df
    #-----------------------------------------------------------
    def _plot_data(self, arr_mass, arr_wgt, name=''):
        if self._val_dir is None:
            return

        plt.hist(arr_mass, weights=arr_wgt, bins=30, range=(4500, 6000), histtype='step')

        nbrem = 'all' if self._nbrem is None else self._nbrem

        plot_path = f'{self._val_dir}/distribution_{nbrem}_{name}.png'
        log.debug(f'Saving to: {plot_path}')
        plt.savefig(plot_path)
        plt.close('all')
    #-----------------------------------------------------------
    def _get_pdf(self, mass=None, cut=None, **kwargs):
        '''
        Will take the mass, with values in: 

        mass: Non constrained B mass
        mass_jpsi: Jpsi constrained B mass
        mass_psi2: Psi2S constrained B mass

        The observable.

        Optional arguments:
        Cut 

        **kwargs: These are all arguments for KDE1DimFFT

        and it will return a KDE1DimFFT PDF.
        '''
        df = self._filter_cut(cut)
        df = self._filter_mass(df, mass, kwargs['obs'])

        log.info(f'Using mass: {mass} for component {kwargs["name"]}')
        arr_mass = df[mass].to_numpy()
        arr_wgt  = df['wgt_br'].to_numpy()

        self._plot_data(arr_mass, arr_wgt, name = kwargs["name"])

        df_id        = self._get_df_id(df)

        self._print_cutflow()

        pdf          = zfit.pdf.KDE1DimFFT(arr_mass, weights=arr_wgt, **kwargs) 
        pdf.arr_mass = arr_mass 
        pdf.arr_wgt  = arr_wgt 
        pdf.df_id    = df_id

        return pdf
    #-----------------------------------------------------------
    def _add_weights(self, df):
        dec = self._d_wg['dec']
        sam = self._d_wg['sam']

        if sam == 1:
            log.debug('Adding sample weights')
            obj           = inclusive_sample_weights(df, year=self._dset)
            df['wgt_sam'] = obj.get_weights()
        else:
            log.warning('Not using sample weights')
            df['wgt_sam'] = 1. 

        if dec == 1:
            log.debug('Adding decay weights')
            df['wgt_dec'] = df.apply(inclusive_decays_weights.read_weight, args=('L1', 'L2', 'H'), axis=1)
        else:
            log.warning('Not using decay weights')
            df['wgt_dec'] = 1. 

        df['wgt_br' ] = len(df) * (df.wgt_dec * df.wgt_sam) / (df.wgt_dec * df.wgt_sam).sum()
        arr_wgt       = df.wgt_br.values
        self._print_wgt_stat(arr_wgt)

        return df
    #-----------------------------------------------------------
    def _print_cutflow(self):
        log.debug('-' * 50)
        log.debug(f'{"Cut":<30}{"Total":<20}{"Passed":<20}')
        log.debug('-' * 50)
        for cut, (inum, fnum) in self._d_fstat.items():
            log.debug(f'{cut:<30}{inum:<20}{fnum:<20}')
        log.debug('-' * 50)
    #-----------------------------------------------------------
    def get_sum(self, mass=None, name='unnamed', **kwargs):
        '''Provides extended PDF that is the sum of multiple KDEs representing PRec background

        Parameters:
        mass (str) : Defines which mass constrain to use, choose between "mass", "mass_jpsi", "mass_psi2"
        name (str) : PDF name
        **kwargs: Arguments meant to be taken by zfit KDE1DimFFT

        Returns:
        zfit.pdf.SumPDF instance
        '''
        self._initialize()

        d_pdf     = { name : self._get_pdf(mass, cut, name=name, **kwargs) for name, cut in self._d_match.items()}
        l_pdf     = [pdf for pdf in d_pdf.values()]
        l_wgt_yld = [ sum(pdf.arr_wgt) for pdf in l_pdf ]
        l_frc     = [ wgt_yld / sum(l_wgt_yld) for wgt_yld in l_wgt_yld ]
        l_yld     = [ zfit.param.Parameter(f'f_{pdf.name}', frc, 0, 1) for pdf, frc in zip(l_pdf, l_frc)]
        for yld in l_yld:
            yld.floating = False
        l_df_id   = [ pdf.df_id for pdf in l_pdf ]

        pdf          = zfit.pdf.SumPDF(l_pdf, fracs=l_yld)
        nor          = zfit.param.Parameter('nprc', sum(l_wgt_yld), 0, 1000000)
        pdf          = pdf.create_extended(nor, name=name)

        l_arr_mass   = [ pdf.arr_mass for pdf in l_pdf ] 
        l_arr_wgt    = [ pdf.arr_wgt  for pdf in l_pdf ] 

        pdf.arr_mass = numpy.concatenate(l_arr_mass)
        pdf.arr_wgt  = numpy.concatenate(l_arr_wgt )
        pdf.df_id    = pnd.concat(l_df_id, ignore_index=True)

        return pdf
#-----------------------------------------------------------

