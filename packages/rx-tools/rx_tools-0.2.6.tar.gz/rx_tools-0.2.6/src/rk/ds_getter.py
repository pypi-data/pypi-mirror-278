import os
import ROOT
import math
import re
import utils 
import logging
import pprint

import utils_noroot   as utnr
import read_selection as rs
import rk.selection   as rksl

from rk.dbase_paths        import dbase_paths as dbpath
from atr_mgr               import mgr         as amgr
from rk.mva                import mva_man
from rk.cutflow            import cutflow
from rk.efficiency         import efficiency
from rk.efficiency         import ZeroYields
from log_store             import log_store

#-----------------------------------------
class ds_getter:
    log=log_store.add_logger('rx_tools:ds_getter')
    #------------------------------------
    def __init__(self, q2bin, trig, year, version, partition, kind, sel):
        self._q2bin      = q2bin 
        self._year_file  = year
        self._vers       = version
        self._trig       = trig
        self._sel        = sel
        self._kind       = kind
        self._part       = partition
        self._is_sim     = None
        self._d_ext_bdt  = None

        self._l_year     = ['2011', '2012', '2015', '2016', '2017', '2018']
        self._l_version  = ['v10.10tf', 'v10.11tf', 'v10.12', 'v10.13', 'v10.14', 'v10.15', 'v10.17', 'v10.18is', 'v10.18dc', 'v10.21p2', 'v10.21p3']
        self._l_kind_bkg = [
                'bpd0kppienu', 'bpd0kpenuenu', 'bpd0kpenupi', 'ctrl_pi', 'bp_x', 
                'bd_x', 'bs_x', 'bdks', 'bpks', 'bdkpi', 'bpkkk', 'bpkpipi', 'bpk1', 'bpk2', 'bsphi',
                'bdpsi2kst', 'bppsi2kst',
                ]
        self._l_kind_sig = ['ctrl', 'sign', 'psi2']
        self._l_kind_sim = self._l_kind_bkg + self._l_kind_sig
        self._l_kind_dat = ['data', 'cmb']

        self._h_ipchi2  = 'H_IPCHI2_OWNPV > 4'

        self._bdt_dir_cmb = None 
        self._bdt_dir_prc = None 

        self._is_signal = kind in self._l_kind_sig

        #Fake trigger needed to get nspd hits cut, tool needs a trigger
        #but cut does not depend on trigger
        self._dummy_trigger = 'ETOS'

        self._initialized   = False
    #------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._is_sim = self._kind in self._l_kind_sim

        self._set_bdt_paths()

        amgr.log.setLevel(logging.WARNING)
        mva_man.log.setLevel(logging.INFO)
        cutflow.log.setLevel(logging.WARNING)
        efficiency.log.setLevel(logging.WARNING)

        #To find files xxxx_test will work, for everything else, only xxxx works
        self._year   = self._year_file.replace('_test', '')
        self._sample = self._get_sample()

        utnr.check_included(self._year, self._l_year   )
        utnr.check_included(self._vers, self._l_version)
        utnr.check_included(self._kind, self._l_kind_sim + self._l_kind_dat)

        try:
            if self._part is not None:
                i_part, n_part = self._part
        except:
            self.log.error(f'Could not extract partitioning scheme from: {self._part}')
            raise

        self._initialized = True
    #------------------------------------
    def _set_bdt_paths(self):
        db                = dbpath()
        self._bdt_dir_cmb = db('bdt_cmb') 
        self._bdt_dir_prc = db('bdt_prc') 
    #------------------------------------
    @property
    def extra_bdts(self):
        return self._d_ext_bdt

    @extra_bdts.setter
    def extra_bdts(self, value):
        self._d_ext_bdt= value
    #------------------------------------
    def _get_sample(self):
        chan = 'mm' if self._trig == 'MTOS' else 'ee'

        if   self._kind == 'bp_x': 
            proc = 'bpXcHs'
        elif self._kind == 'bd_x': 
            proc = 'bdXcHs'
        elif self._kind == 'bs_x': 
            proc = 'bsXcHs'
        elif self._kind in [
                'bpd0kppienu', 'bpd0kpenuenu', 'bpd0kpenupi', 'data', 'cmb', 'sign', 'ctrl', 
                'ctrl_pi', 'psi2', 'bdks', 'bpks', 'bdkpi', 'bdkpi', 'bpkkk', 'bpkpipi', 
                'bpk1', 'bpk2', 'bsphi',
                'bdpsi2kst', 'bppsi2kst',
                ]:
            proc = self._kind
        else:
            self.log.error(f'Cannot determine process for:')
            self.log.error(f'{"Kind ":<10}{self._kind:<20}')
            self.log.error(f'{"q2bin":<10}{self._q2bin:<20}')
            self.log.error(f'{"Trig ":<10}{self._trig:<20}')
            raise

        return f'{proc}_{chan}' if proc not in ['bpkkk', 'bpkpipi', 'bpd0kppienu', 'bpd0kpenuenu', 'bpd0kpenupi'] else proc
    #------------------------------------
    def _add_reco_cuts(self, d_cut):
        d_cut_extra = {}
        for key, cut in d_cut.items():
            if key != 'truth':
                d_cut_extra[key] = cut
                continue

            d_cut_extra[key]        = cut
            d_cut_extra['K_IPChi2'] = self._h_ipchi2

        return d_cut_extra
    #------------------------------------
    def _filter_bdt(self, rdf, cut, skip_prec):
        self.log.info(f'Picking up combinatorial BDT from: {self._bdt_dir_cmb}')
        man_cmb=mva_man(rdf, self._bdt_dir_cmb, self._trig)
        rdf    =man_cmb.add_scores('BDT_cmb')

        if   not skip_prec:
            self.log.info(f'Picking up PRec BDT from: {self._bdt_dir_prc}')
            man_prc=mva_man(rdf, self._bdt_dir_prc, self._trig)
            rdf    =man_prc.add_scores('BDT_prc')
        elif 'BDT_prc' in cut:
            iprec  = cut.find('&&')
            cut    = cut[:iprec]
        else:
            pass

        self.log.info(f'Using bdt cut: {cut}')

        rdf = rdf.Filter(cut, 'bdt')

        return rdf, cut
    #------------------------------------
    def _add_bdts(self, rdf):
        if self._d_ext_bdt is None:
            self.log.info(f'No extra BDT added')
            return rdf

        self.log.info(f'Adding extra BDTs')
        for var, location in self._d_ext_bdt.items():
            self.log.debug(f'---> {var}')
            man =mva_man(rdf, location, self._trig)
            rdf =man.add_scores(var)

        return rdf
    #------------------------------------
    def _skim_df(self, df):
        if self._part is None:
            return df

        islice, nslice = self._part

        df = utils.get_df_range(df, islice, nslice)

        return df
    #------------------------------------
    def _get_df_raw(self):
        dat_dir   = os.environ['DATDIR']
        file_path = f'{dat_dir}/{self._sample}/{self._vers}/{self._year_file}.root'

        if   self._kind == 'cmb' and self._trig in ['ETOS', 'GTIS']:
            if self._vers == 'v10.18is':
                tree_path = 'KSS'
            else:
                tree_path = 'KSS_ee'
        elif self._kind == 'cmb' and self._trig == 'MTOS': 
            tree_path = 'KSS_mm'
        elif self._trig == 'MTOS':
            tree_path = 'KMM'
        elif self._trig in ['ETOS', 'GTIS']:
            tree_path = 'KEE'
        else:
            log.error(f'Cannot pick tree path, invalid kind/trigger: {self._kind}/{self._trig}')
            raise

        utnr.check_file(file_path)

        self.log.info('------------------------------------')
        self.log.info(f'Retrieving dataframe for:')
        self.log.info(f'{"File path  ":<20}{file_path:<100}')
        self.log.info(f'{"Tree path  ":<20}{tree_path:<100}')
        self.log.info('------------------------------------')

        df = ROOT.RDataFrame(tree_path, file_path)
        df = self._skim_df(df)

        df.filepath = file_path
        df.treename = tree_path
        df.year     = self._year

        return df
    #------------------------------------
    def _get_gen_nev(self):
        dat_dir   = os.environ['DATDIR']
        file_path = f'{dat_dir}/{self._sample}/{self._vers}/{self._year_file}.root'

        utnr.check_file(file_path)
        self.log.debug(f'Retrieving gen statistics:')
        df  = ROOT.RDataFrame('gen', file_path)
        df  = self._skim_df(df)
        nev = df.Count().GetValue()

        return nev 
    #------------------------------------
    def _redefine(self, d_cut, d_redefine):
        for key, new_cut in d_redefine.items():
            if key not in d_cut:
                self.log.error(f'Cannot redefine {key}, not a valid cut, choose from: {d_cut.keys()}')
                pprint.pprint(d_cut)
                raise ValueError

            old_cut    = d_cut[key]
            d_cut[key] = new_cut

            old_cut    = re.sub(' +', ' ', old_cut)
            new_cut    = re.sub(' +', ' ', new_cut)
            self.log.info(f'{key:<15}{old_cut:<70}{"--->":10}{new_cut:<40}')

        return d_cut
    #------------------------------------
    def _add_reco(self, cf, nrec):
        if not self._is_sim:
            return cf

        ngen       = self._get_gen_nev()
        cf['reco'] = efficiency(nrec, ngen - nrec, cut='Reco and Strip')

        return cf
    #------------------------------------
    def get_df(self, remove_cuts=[], d_redefine=None, skip_prec=False):
        self._initialize()

        self._remove_cuts = remove_cuts

        df    = self._get_df_raw()
        dfmgr = amgr(df)

        cf    = cutflow(d_meta = {'file' : df.filepath, 'tree' : df.treename})
        tot   = df.Count().GetValue()
        d_cut = rksl.selection(self._sel, self._trig, self._year, self._sample, q2bin=self._q2bin)
        if self._kind in ['data', 'cmb']:
            d_cut = dict( [('truth', '(1)')] + list(d_cut.items()) )

        d_cut = self._add_reco_cuts(d_cut)

        if d_redefine is not None:
            d_cut = self._redefine(d_cut, d_redefine)

        self.log.info(f'Applying selection: {self._sel}')

        for key, cut in d_cut.items():
            if key in self._remove_cuts:
                self.log.info(f'{"skip":<10}{key:>20}')
                continue
            else:
                self.log.info(f'{"":<10}{key:>20}')

            if key == 'bdt':
                df      = self._add_bdts(df)
                df, cut = self._filter_bdt(df, cut, skip_prec)
            else:
                df = df.Filter(cut, key)

            pas=df.Count().GetValue()

            try:
                eff = efficiency(pas, tot - pas, cut=cut)
            except ZeroYields:
                self.log.error(f'Last cut passed zero events:')
                print(cf)
                raise

            if key == 'truth' and self._is_signal:
                cf = self._add_reco(cf, pas)
            else:
                cf[key]  = eff

            tot=pas

        df          = dfmgr.add_atr(df)
        df.treename = self._trig 
        df.cf       = cf

        return df
#-----------------------------------------

