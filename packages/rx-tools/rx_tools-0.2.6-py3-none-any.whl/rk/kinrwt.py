import ROOT

import re
import os
import pickle
import numpy
import logging 
import matplotlib.pyplot as plt

import hep_gb
import hep_cl

import utils_noroot   as utnr
import pandas         as pnd
import read_selection as rs
import utils

from version_management  import get_last_version 
from importlib.resources import files
from rk.wgt_mgr          import wgt_mgr

#----------------------------------------
class rwt:
    log = utnr.getLogger(__name__)
    #-------------------------------
    def __init__(self, dt=None, mc=None): 
        self._rdf_dt      = dt 
        self._rdf_mc      = mc 

        #Built from args
        self._method      = None
        self._wgt_ver     = None
        self._wgt_dir     = None
        self._plt_dir     = None
        self._set_dir     = None
        self._syst        = None

        self._l_var       = None
        self._rwt         = None 

        #Used for checks
        self._l_valid_methods = ['hep_ml', 'hist']
        self._l_valid_cal_sys = ['000', 'nom']

        self._out_id     = None
        self._set_key    = None

        self._mat_dt_val = None
        self._mat_mc_val = None
        self._arr_dt_wgt = None
        self._arr_mc_wgt = None

        self._initialized = False
    #-------------------------------
    @property
    def wgt_ver(self):
        return self._wgt_ver

    @wgt_ver.setter
    def wgt_ver(self, value):
        self._wgt_ver = value 
    #-------------------------------
    @property
    def set_dir(self):
        return self._set_dir

    @set_dir.setter
    def set_dir(self, value):
        self._set_dir = value 
    #-------------------------------
    @property
    def wgt_dir(self):
        return self._wgt_dir

    @wgt_dir.setter
    def wgt_dir(self, value):
        self._wgt_dir = utnr.make_dir_path(value)
    #-------------------------------
    @property
    def reweighter(self):
        self._initialize()

        return self._rwt
    #-------------------------------
    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        if value not in self._l_valid_methods:
            self.log.error(f'Invalid method {value}, choose amont: {self._l_valid_methods}')
            raise

        self._method = value 
    #-------------------------------
    @property
    def vars(self):
        self._initialize()
        return self._l_var
    #-------------------------------
    def _initialize(self):
        if self._initialized:
            return

        try:
            os.makedirs(self._plt_dir, exist_ok=True)
        except:
            self.log.error(f'Cannot make: {self._plt_dir}')
            raise

        self._set_binning()

        self._rdf_dt = utils.add_vars(self._rdf_dt, self._l_var)
        self._rdf_mc = utils.add_vars(self._rdf_mc, self._l_var)

        self.log.info('Filtering data')
        self._rdf_dt = self._filter_bounds(self._rdf_dt)

        self.log.info('Filtering mc')
        self._rdf_mc = self._filter_bounds(self._rdf_mc)
        self._rwt    = self._get_reweighter()

        self._initialized = True
    #-------------------------------
    def _get_axes(self):
        nvar = len(self._l_var)

        if   nvar == 1:
            return ['x']
        elif nvar == 2:
            return ['x', 'y']
        elif nvar == 3:
            return ['x', 'y', 'z']
        elif nvar == 4:
            return ['w', 'x', 'y', 'z']
        else:
            self.log.error(f'Cannot set axes for {nvar} variables')
            raise
    #-------------------------------
    def _filter_bounds(self, rdf):
        for ivar, _ in enumerate(self._l_var):
            rdf = self._filter_bound(rdf, axis=ivar)

        rep = rdf.Report()

        if self.log.level == logging.DEBUG:
            rep.Print()

        for cut in rdf.l_cut:
            self.log.debug(cut)

        return rdf
    #-------------------------------
    def _filter_bound(self, rdf, axis=None):
        var     = self._l_var[axis]
        l_bin   = self._l_l_axs[axis]

        min_bnd = l_bin[0]
        max_bnd = l_bin[-1]

        cut = f'{min_bnd:0.3f} < {var} && {var} < {max_bnd:0.3f}'

        if hasattr(rdf, 'l_cut'):
            l_cut = rdf.l_cut
        else:
            l_cut = []

        rdf = rdf.Filter(cut, var)

        l_cut.append(cut)
        rdf.l_cut = l_cut
        
        return rdf
    #-------------------------------
    def _set_binning(self):
        if self._set_dir is None:
            self._set_dir = files('kinematics').joinpath('share')

        set_path = f'{self._set_dir}/kinematics_{self._syst}.json'

        if not os.path.isfile(set_path):
            self.log.error(f'Cannot find: {set_path}')

        self.log.info(f'Picking up settings from: {set_path}')

        d_data = utnr.load_json(set_path)
        d_data = d_data[self._set_key]

        self._l_var   = d_data['rwt_vars']
        l_axs         = self._get_axes()
        self._l_l_axs = [ d_data[f'arr_{var}_1'] for var in l_axs ]

        if self._method != 'hist':
            self.log.debug(f'Skipping binning for method: {self._method}')
            return

        self.log.info('Using binning:')
        for var in self._l_var:
            l_bin = d_data[var]
            self.log.info(f'{var}: {l_bin}')
    #-------------------------------
    def _get_arrays(self, is_sim):
        rdf = self._rdf_mc if is_sim else self._rdf_dt

        d_data = rdf.AsNumpy(self._l_var + ['weight'])
        l_val  = [ d_data[var] for var in self._l_var ]
        arr_val= numpy.array(l_val).T
        arr_wgt= d_data['weight'] 

        return arr_val, arr_wgt
    #-------------------------------
    def _get_reweighter(self):
        mat_dt_val, mat_dt_wgt = self._get_arrays(is_sim=False)
        mat_mc_val, mat_mc_wgt = self._get_arrays(is_sim= True)

        if   self._method == 'hist':
            maker = hep_cl.hist_maker(mat_mc_val, mat_dt_val, arr_original_weight=mat_mc_wgt, arr_target_weight=mat_dt_wgt)
            maker.arr_bin_x = self._l_l_axs[0] 
            maker.arr_bin_y = self._l_l_axs[1] 
            maker.arr_bin_z = self._l_l_axs[2] 

            h_dt, h_mc = maker.get_maps()

            rwt  = [h_dt, h_mc]
        elif self._method == 'hep_ml':
            hml = hep_gb.BDT(mat_mc_val, mat_dt_val, arr_sim_wgt=mat_mc_wgt, arr_dat_wgt=mat_dt_wgt)
            hml.fit()
            rwt=hml.rwt
        else:
            log.error(f'Wrong method: {self._method}')
            raise

        self._mat_dt_val = mat_dt_val
        self._mat_mc_val = mat_mc_val
        self._arr_dt_wgt = mat_dt_wgt
        self._arr_mc_wgt = mat_mc_wgt

        return rwt
    #----------------------------------------
    def _get_names(self, name):
        rgx = '(.*)_(.*)_(.*)_(.*)$'
        mtc = re.match(rgx, name)
        if not mtc:
            log.error(f'Cannot match {rgx} to {name}')
            raise

        trig = mtc.group(1)
        year = mtc.group(2) 
        pref = mtc.group(3) 
        syst = mtc.group(4) 

        self._out_id = f'{trig}_{year}_{pref}_{syst}' 
        self._set_key= f'{pref}_{trig}_{year}' 
        self._syst   = 'trg' if syst == 'nom' else syst
        self._plt_dir= f'{self._wgt_dir}/{self._wgt_ver}/{self._out_id}/plots'
    #-------------------------------
    def _validate(self):
        self.log.info('Validating')

        arr_wgt_rw = self._rwt.predict_weights(self._mat_mc_val)

        plt.hist(arr_wgt_rw, bins=100)
        plt.title('Weights')
        plt.savefig(f'{self._plt_dir}/weights.png')
        plt.close('all')

        nvar = self._mat_dt_val.shape[1]
        for ivar in range(nvar):
            self._validate_var(arr_wgt_rw, ivar)
    #-------------------------------
    def _validate_var(self, arr_wgt, ivar):
        var_name = self._l_var[ivar]
        arr_dt   = self._mat_dt_val.T[ivar]
        arr_mc   = self._mat_mc_val.T[ivar]
        l_bin    = self._l_l_axs[ivar]

        self.log.debug(f'Val data: {arr_dt.shape}')
        self.log.debug(f'Val MC  : {arr_mc.shape}')
        self.log.debug(f'Wgt DT  : {self._arr_dt_wgt.shape}')
        self.log.debug(f'Wgt MC  : {self._arr_mc_wgt.shape}')
        self.log.debug(f'RWT     : {arr_wgt.shape}')

        plt.subplots(figsize=(10,6))
        plt.hist(arr_mc, bins=l_bin, linewidth=2,    alpha=   0.3, density=True, label='MC org', weights=self._arr_mc_wgt          , color='r')
        plt.hist(arr_mc, bins=l_bin, linewidth=2,    alpha=   0.3, density=True, label='MC rwt', weights=self._arr_mc_wgt * arr_wgt, color='b')
        plt.hist(arr_dt, bins=l_bin, linewidth=2, histtype='step', density=True, label='Data'  , weights=self._arr_dt_wgt          , color='k')

        plt.grid()
        plt.legend()
        plt.savefig(f'{self._plt_dir}/{var_name}.png')
        plt.close('all')
    #-------------------------------
    def save_reweighter(self, name=None):
        '''Will save reweighter object
        Parameters
        ------------------
        prefix (str): String of the form rec_ETOS_2018
        '''
        self._get_names(name)
        self._initialize()

        file_dir = f'{self._wgt_dir}/{self._wgt_ver}'

        os.makedirs(file_dir, exist_ok=True)
        if   self._method ==   'hist':
            file_path = f'{file_dir}/{self._out_id}.root'
            ofile = ROOT.TFile(file_path, 'recreate')
            for hist in self._rwt:
                hist.Write()
            ofile.Close()
        elif self._method == 'hep_ml':
            file_path = f'{file_dir}/{self._out_id}.pickle'
            utnr.dump_pickle(self._rwt, file_path)
            self._validate()
        else:
            log.error(f'Wrong method: {self._method}')
            raise

        self.log.visible(f'Saving to: {file_path}')
#----------------------------------------

