
import logging 
import logzero
import numpy
import ROOT
import tqdm
import zfit
import sys
import os

import utils
import utils_noroot as utnr

from zutils.plot import plot    as zfp
from log_store   import log_store

import matplotlib.pyplot as plt

log = log_store.add_logger('tools:mcstudy')
#----------------------------------------
class mcstudy:
    def __init__(self, pdf, d_opt={}, d_const=None):
        self._pdf      = pdf 
        self._obs      = pdf.space 
        self._obs_name = pdf.space.name 

        self._mod_name = 'model' 
        self._plot_dir = None
        self._d_opt    = d_opt
        self._d_const  = d_const
        self._d_res    = {} 
        self._sampler  = None

        self._nfit_plots  = 0 
        self._stacked     = False

        self._initialized = False
    #----------------------------------------
    @property
    def plot_dir(self):
        return self._plot_dir

    @plot_dir.setter
    def plot_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
            log.debug(f'Plots directory: {value}')
        except:
            log.error(f'Cannot create {value}')
            raise

        self._plot_dir = value
    #----------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        if not self._pdf.is_extended:
            log.error(f'PDF is not extended, yield is needed to produce toys')
            raise

        zfit.settings.changed_warnings.hesse_name = False

        utnr.check_type(self._obs_name, str) 
        utnr.check_type(self._d_opt   , dict) 

        if 'nplots'  in self._d_opt:
            self._nfit_plots = self._d_opt['nplots']

        if 'stacked' in self._d_opt:
            self._stacked    = self._d_opt['stacked']

        if 'seed'    in self._d_opt:
            zfit.settings.set_seed(self._d_opt['seed'])

        self._sampler   = self._pdf.create_sampler(fixed_params=True)
        self._nll       = zfit.loss.ExtendedUnbinnedNLL(model=self._pdf, data=self._sampler)
        self._minimizer = zfit.minimize.Minuit()
        self._d_var_gen = self._get_gen_val()
        self._check_const()

        self._initialzed = True
    #----------------------------------------
    def _check_const(self):
        if self._d_const is None:
            return

        for var_name in self._d_const:
            log.debug(f'Constraining: {var_name}') 
            if var_name not in self._d_var_gen:
                log.error(f'Cannot constrain {var_name}, missing in PDF')
                raise
    #----------------------------------------
    def _plot_fit(self, res, i_fit):
        if self._plot_dir is None:
            return

        obj   = zfp(data=self._sampler, model=self._pdf, result=res)
        obj.plot(nbins=50, add_pars='all', stacked=self._stacked)
        plt.savefig(f'{self._plot_dir}/fit_{i_fit:03}_lin.png') 

        obj.axs[0].set_ylim(0.1, 1e8)
        obj.axs[0].set_yscale('log')
        plt.savefig(f'{self._plot_dir}/fit_{i_fit:03}_log.png') 
    #----------------------------------------
    def _get_nll_constrained(self):
        if self._d_const is None or len(self._d_const) == 0:
            return self._nll

        l_par = [ par                        for par in self._pdf.get_params(floating=True) if par.name in self._d_const ]
        l_mu  = [ self._d_const[par.name][0] for par in l_par ]
        l_sg  = [ self._d_const[par.name][1] for par in l_par ]
        l_mu  = numpy.random.normal(l_mu, l_sg)
        const = zfit.constraint.GaussianConstraint(params  =l_par,
                                                observation=l_mu,
                                                uncertainty=l_sg)

        nll = self._nll.create_new(constraints=const)

        return nll
    #----------------------------------------
    def _run_dataset(self, i_fit=None):
        self._sampler.resample()

        nll = self._get_nll_constrained()
        try:
            res = self._minimizer.minimize(nll)
        except:
            log.warning(f'Could not run minimization')
            return

        try:
            res.hesse(method='minuit_hesse')
        except:
            log.warning(f'Could not run Hesse')
            return

        if i_fit < self._nfit_plots:
            self._plot_fit(res, i_fit)

        d_par = self._get_parameters(res)

        return d_par
    #----------------------------------------
    def _get_gen_val(self):
        s_par = self._pdf.get_params(floating=True)

        d_par = { par.name : par.value().numpy() for par in s_par}

        return d_par
    #----------------------------------------
    def _check_par_val(self, name=None, value=None, error=None):
        if not isinstance(value, float):
            log.error(f'Value for parameter {name} is not a float')
            log.error(f'Type:  {type(value)}')
            log.error(f'Value: {value}')
            raise ValueError

        if not isinstance(error, float):
            log.error(f'Error for parameter {name} is not a float')
            log.error(f'Type:  {type(error)}')
            log.error(f'Value: {error}')
            raise ValueError
    #----------------------------------------
    def _get_parameters(self, res):
        d_par = {}
        for par, d_val in res.params.items():
            nam = par.name
            val = d_val['value']
            err = d_val['hesse']['error'] 

            self._check_par_val(name=nam, value=val, error=err)

            d_par[f'{nam}_fit'] = val
            d_par[f'{nam}_err'] = err 
            d_par[f'{nam}_gen'] = self._d_var_gen[nam] 

        d_par['valid' ]    = res.valid
        d_par['status']    = res.status
        d_par['converged'] = res.converged

        return d_par 
    #----------------------------------------
    def run(self, ndatasets=None):
        self._initialize()

        utnr.check_type(ndatasets, int)

        iterator = tqdm.trange(ndatasets, file=sys.stdout, ascii=' -')
        for i_dataset in iterator:
            self._d_res[i_dataset] = self._run_dataset(i_dataset)

        return self._d_res
#----------------------------------------

