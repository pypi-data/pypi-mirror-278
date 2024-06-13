import ROOT

import utils
import numpy
import math
import os
import re
import tqdm
import pandas as pnd

from stats.covariance import covariance
from log_store        import log_store

import zutils.utils      as zut
import utils_noroot      as utnr
import matplotlib.pyplot as plt

import style

log = log_store.add_logger('tools:plot_pulls')
#-----------------------------------------------------------------
class plot_pulls:
    def __init__(self, dir_name = None, skip_fit=False):
        self._dir_name      = dir_name
        self._skip_fit      = skip_fit
        self._plot_dir      = None
        self._l_var_name    = None
        self._l_json_path   = None
        self._d_name        = None

        self._initialized   = False
    #--------------------------
    def _initialize(self):
        if self._initialized:
            return

        utnr.make_dir_path(self._plot_dir)
        self._l_json_path = self._get_paths()
        self._l_var_name  = self._get_vars()

        self._initialized = True
    #--------------------------
    @property
    def plot_dir(self):
        return self._plot_dir

    @plot_dir.setter
    def plot_dir(self, value):
        self._plot_dir = value
    #--------------------------
    def _get_vars(self):
        json_path = self._l_json_path[0]

        d_par = utnr.load_json(json_path)

        try:
            d_fit = d_par['0']
        except:
            log.error(f'Cannot retrieve zeroth fit from: {json_path}')
            raise

        l_key = [ key for key in d_fit if key not in ['converged', 'status', 'valid'] ]
        s_var = { key.replace('_err', '').replace('_fit', '').replace('_gen', '') for key in l_key }

        log.info(f'Found parameters: {s_var}')

        return s_var
    #--------------------------
    def _get_paths(self):
        l_path = utnr.glob_wc(f'{self._dir_name}/pars_*.json', allow_empty=True)

        if len(l_path) == 0:
            log.error(f'No files found in: {self._dir_name}')
            raise
        else:
            log.info(f'Found {len(l_path)} files')


        return l_path
    #-----------------------------------------------------------
    def _merge_dictionaries(self, l_d_data):
        '''
        Will rename keys in input dictionaries and merge them

        Parameters
        -------------
        l_d_data (list): List of dictionaries 

        Returns
        -------------
        d_data (dict): Dictionary with data of all the input dictionaries
        '''

        log.info('Merging dictionaries with parameters')

        d_data = {}

        l_d_data_renamed = []
        for index, d_data in enumerate(l_d_data):
            d_data_renamed = { f'{index}_{key}' : value for key, value in d_data.items() }
            l_d_data_renamed.append(d_data_renamed)

        for d_data_renamed in tqdm.tqdm(l_d_data_renamed, ascii=' -'):
            d_data.update(d_data_renamed)

        return d_data
    #-----------------------------------------------------------
    def _get_df(self):
        l_d_data = [ utnr.load_json(json_path) for json_path in self._l_json_path ]
        d_data   = self._merge_dictionaries(l_d_data)

        d_var_df = {}
        for var in self._l_var_name:
            d_var_df[var] = self._var_df(var, d_data)

        return d_var_df
    #--------------------------
    def _var_df(self, var, d_data):
        df = pnd.DataFrame(columns=['fit', 'err', 'gen', 'cnv', 'sta', 'val'])
        for ifit, d_fit in d_data.items():
            #This will happen with failed fits
            if d_fit is None:
                df.loc[ifit] = [-999, -1, -888, 0, -1, 0]
                continue

            fit = d_fit[f'{var}_fit']
            err = d_fit[f'{var}_err']
            gen = d_fit[f'{var}_gen']
            cnv = d_fit[ 'converged']
            sta = d_fit[    'status']
            val = d_fit[     'valid']

            df.loc[ifit] = [fit, err, gen, cnv, sta, val]

        df['pull'] = (df.fit - df.gen) / df.err
        df['cnv' ] = df.cnv.astype(int)
        df['val' ] = df.val.astype(int)
        df['sta' ] = df.sta.astype(int)

        return df
    #-----------------------------------------------------------
    def _plot_dist(self, var, df):
        plot_path= f'{self._plot_dir}/{var}_fit.png' 

        arr_fit = df.fit.to_numpy()
        arr_gen = df.gen.to_numpy()
        min_val = min( numpy.quantile(arr_fit, 0.01), numpy.quantile(arr_gen, 0.01))
        max_val = max( numpy.quantile(arr_fit, 0.99), numpy.quantile(arr_gen, 0.99))

        axis = None
        axis = df.plot.hist(column='fit', bins= 30, range=(min_val, max_val), color='blue', alpha=0.5, ax=axis)
        plt.axvline(x=arr_gen[0], color='red')

        var = var if var not in self._d_name else self._d_name[var]
        plt.xlabel(var)
        plt.ylabel('Entries')
        plt.legend(['Fitted', 'Generated'])
        plt.title('Distribution')

        log.info(f'Saving to: {plot_path}')
        plt.savefig(plot_path)
        plt.close('all')
    #-----------------------------------------------------------
    def _plot_error(self, var, df):
        is_yield = var.startswith('n')
        plot_path= f'{self._plot_dir}/{var}_err.png' 

        arr_err = df.err.to_numpy()
        arr_gen = df.gen.to_numpy()

        min_val = numpy.quantile(arr_err, 0.01)
        max_val = numpy.quantile(arr_err, 0.99)


        var = var if var not in self._d_name else self._d_name[var]
        var = var.replace('$', '')

        if is_yield: 
            sqrt_gen = math.sqrt(arr_gen[0])
            min_x = min(min_val, 0.98 * sqrt_gen)
        else:
            min_x = min_val

        df.plot.hist(column='err', bins= 30, range=(min_x, max_val), color='blue', alpha=0.5)
        if is_yield:
            plt.axvline(x=sqrt_gen, color='red')
            plt.legend(['Error', '$\sqrt{Generated}$'])
        else:
            plt.gca().get_legend().remove()

        plt.xlim(min_x, max_val)
        plt.xlabel(f'$\\varepsilon({var})$')
        plt.ylabel('Entries')

        log.info(f'Saving to: {plot_path}')
        plt.savefig(plot_path)
        plt.close('all')
    #-----------------------------------------------------------
    def _plot_pull(self, var, df):
        plot_path= f'{self._plot_dir}/{var}_pull.png' 

        arr_pull = df.pull.to_numpy()

        if self._skip_fit:
            log.warning('Skipping fit to pulls')
            plt.hist(arr_pull, bins=40)
            plt.savefig(plot_path)
            plt.close('all')
            return

        mu, sg = zut.fit_pull(arr_pull, fit_sig=2, plot=True)

        var = var if var not in self._d_name else self._d_name[var]
        plt.xlabel(f'Pull for {var}')
        plt.ylabel('Entries')
        plt.legend()

        log.info(f'Saving to: {plot_path}')
        plt.savefig(plot_path)
        plt.close('all')

        return mu, sg
    #-----------------------------------------------------------
    def _plot_correlation(self, l_arr_fit_val, l_gen_val, l_var_name):
        mat_fit = numpy.array(l_arr_fit_val)
        arr_nom = numpy.array(l_gen_val)

        obj=covariance(mat_fit, arr_nom)
        cov=obj.get_cov()
        cor=utnr.correlation_from_covariance(cov)

        plot_path = f'{self._plot_dir}/correlation.png'
        l_var_name.sort()
        utnr.plot_matrix(plot_path, l_var_name, l_var_name, cor, upper=True, zrange=(-1, +1), form='{:.3f}')
    #-----------------------------------------------------------
    def _plot_quality(self, df):
        df['converged'] = df.cnv
        df['status']    = df.sta
        df['valid']     = df.val

        zut.plot_qlty(df)

        plot_path = f'{self._plot_dir}/quality.png'
        log.info(f'Saving to: {plot_path}')
        plt.savefig(plot_path)
        plt.close('all')
    #--------------------------
    def _vars_pull(self, d_pull):
        l_nam = [ var if var not in self._d_name  else self._d_name[var] for var in d_pull ] 
        l_val = [ val for val, _   in d_pull.values() ] 
        l_err = [ err for   _, err in d_pull.values() ] 

        plt.errorbar(l_nam, y=l_val, yerr=l_err, color='red', capsize=5)

        plot_path = f'{self._plot_dir}/pull_vars.png'
        log.info(f'Saving to: {plot_path}')

        plt.ylabel('Pull')
        plt.axhline(y=-1.00, color='black', linestyle='-.')
        plt.axhline(y= 0.00, color='black', linestyle=':' )
        plt.axhline(y=+1.00, color='black', linestyle='-.')
        plt.grid()
        plt.savefig(plot_path)
    #--------------------------
    def _filter_bad_fits(self, df):
        nin = len(df)

        df = df[df.sta == 0]
        df = df[df.val == 1]
        df = df[df.cnv == 1]

        nou = len(df)

        if nou == 0:
            log.info(f'Input/Good fits: {nin}/{nou}')
            raise

        log.info(f'Input/Good fits: {nin}/{nou}')

        return df
    #--------------------------
    def _get_fit_val(self, df):
        arr_fit_val = df.fit.values
        arr_gen_val = df.gen.values
        gen_val     = arr_gen_val[0]

        return arr_fit_val, gen_val
    #--------------------------
    def save_plots(self, d_name = {}):
        self._d_name = d_name
        self._initialize()

        d_df   = self._get_df()
        d_pull = {}

        l_gen_val     = []
        l_arr_fit_val = []
        l_var_name    = []
        for var, df in d_df.items():
            df_g = self._filter_bad_fits(df)

            self._plot_dist(var, df_g)
            self._plot_error(var, df_g)
            d_pull[var] = self._plot_pull(var, df_g)

            arr_fit_val, gen_val = self._get_fit_val(df)

            l_var_name.append(var)
            l_gen_val.append(gen_val)
            l_arr_fit_val.append(arr_fit_val)

        self._plot_quality(df)
        self._plot_correlation(l_arr_fit_val, l_gen_val, l_var_name)
        #self._vars_pull(d_pull)
#-----------------------------------------------------------

