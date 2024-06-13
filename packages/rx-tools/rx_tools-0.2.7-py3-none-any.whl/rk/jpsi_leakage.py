from log_store import log_store

import read_selection as rs

import os
import glob 
import ROOT
import zfit
import pprint 

log=log_store.add_logger('rx_tools:jpsi_leakage')
#----------------------------------------
class jpsi_leakage:
    def __init__(self, obs=None, trig=None, q2bin=None, dset=None):
        self._obs  = obs
        self._trig = trig
        self._q2bin= q2bin 
        self._dset = dset
        self._vers = 'v10.21p2'

        self._mass_var = None
        self._initialized = False
    #----------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._mass_var = self._get_mass_var()

        self._initialized = True 
    #----------------------------------------
    def _get_mass_var(self):
        if   self._q2bin == 'high':
            var = 'B_M'
        elif self._q2bin == 'psi2':
            var = 'B_const_mass_psi2S_M[0]'
        else:
            log.error(f'Invalid q2bin: {self._q2bin}')
            raise

        return var
    #----------------------------------------
    def _get_paths(self):
        cas_dir = os.environ['CASDIR']
        if   self._dset == 'r1':
            l_ntp_wc  = [
                    f'{cas_dir}/tools/apply_selection/jpsi_leak/ctrl/{self._vers}/2011_{self._trig}/*.root',
                    f'{cas_dir}/tools/apply_selection/jpsi_leak/ctrl/{self._vers}/2012_{self._trig}/*.root',
                    ]
        elif self._dset == 'r2p1':
            l_ntp_wc  = [
                    f'{cas_dir}/tools/apply_selection/jpsi_leak/ctrl/{self._vers}/2015_{self._trig}/*.root',
                    f'{cas_dir}/tools/apply_selection/jpsi_leak/ctrl/{self._vers}/2016_{self._trig}/*.root',
                    ]
        elif self._dset in ['2017', '2018']:
            l_ntp_wc  = [
                    f'{cas_dir}/tools/apply_selection/jpsi_leak/ctrl/{self._vers}/{self._dset}_{self._trig}/*.root',
                    ]
        else:
            log.error(f'Invalid dataset: {self._dset}')

        l_path = []
        for ntp_wc in l_ntp_wc:
            l_path += glob.glob(ntp_wc)

        if len(l_path) == 0:
            log.error(f'No files found in:')
            pprint.pprint(l_ntp_wc)
            raise

        return l_path
    #----------------------------------------
    def _get_rdf(self):
        l_path = self._get_paths()
        rdf    = ROOT.RDataFrame(self._trig, l_path)
        qsq_cut= rs.get('q2', self._trig, q2bin=self._q2bin, year = self._dset)
        rdf    = rdf.Filter(qsq_cut, 'q2')
        rep    = rdf.Report()
        rep.Print()

        return rdf
    #----------------------------------------
    def _get_pdf(self, suffic, name, arr_mass):
        arr_mass = arr_mass.astype(float)

        return zfit.pdf.KDE1DimFFT(arr_mass, obs=self._obs, bandwidth=10, name=name)
    #----------------------------------------
    def get_pdf(self, suffix=None, name=None):
        self._initialize()

        rdf      = self._get_rdf()
        rdf      = rdf.Define('mass', self._mass_var)
        arr_mass = rdf.AsNumpy(['mass'])['mass']

        pdf = self._get_pdf(suffix, name, arr_mass)

        return pdf
#----------------------------------------
