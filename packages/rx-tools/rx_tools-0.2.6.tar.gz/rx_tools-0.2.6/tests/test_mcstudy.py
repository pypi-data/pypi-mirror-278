import ROOT
import zfit
import utils_noroot as utnr

from rk.mcstudy      import mcstudy
from rk.const_getter import const_getter as cget

import logging
import math 

log=utnr.getLogger(__name__)
#---------------------------------------------------
class data:
    nevt = 100000
    ndst = 1000
#---------------------------------------------------
def delete_all_pars():
    d_par = zfit.Parameter._existing_params
    l_key = list(d_par.keys())

    for key in l_key:
        del(d_par[key])
#---------------------------------------------------
def get_model():
    obs   = zfit.Space('x', limits=(-10, 10))
    mu    = zfit.Parameter("mu", 2.4, -1, 5)
    sg    = zfit.Parameter("sg", 1.3,  0, 5)
    gaus  = zfit.pdf.Gauss(obs=obs, mu=mu, sigma=sg)
    nevt  = zfit.Parameter("nevt", data.nevt,  0, 2 * data.nevt)
    pdf   = gaus.create_extended(nevt, 'Gaussian')

    return pdf 
#---------------------------------------------------
def test_simple():
    pdf = get_model()

    d_set= dict()
    mcst = mcstudy(pdf, d_opt = d_set)
    mcst.plot_dir = f'tests/mcstudy/simple/fits_{data.ndst:06}'
    d_fit_res = mcst.run(ndatasets=data.ndst)
    utnr.dump_json(d_fit_res, f'tests/mcstudy/simple/nev_{data.ndst:05}/results.json')

    delete_all_pars()
#---------------------------------------------------
def test_constrain():
    pdf = get_model()

    d_set= dict()
    mcst = mcstudy(pdf, d_opt = d_set, d_const={'mu' : (2.4, 0.3)})
    mcst.plot_dir = f'tests/mcstudy/constrain/fits_{data.ndst:06}'
    d_fit_res = mcst.run(ndatasets=data.ndst)
    utnr.dump_json(d_fit_res, f'tests/mcstudy/constrain/nev_{data.ndst:05}/results.json')

    delete_all_pars()
#---------------------------------------------------
def test_seed():
    d_set = dict()
    ifit  = 0
    for seed in [0, 1, 1]:
        d_set['seed'] = seed

        pdf = get_model()
        mcst = mcstudy(pdf, d_opt = d_set)
        mcst.plot_dir = f'tests/mcstudy/seed/fits_{data.ndst:06}'
        d_fit_res = mcst.run(ndatasets=data.ndst)
        utnr.dump_json(d_fit_res, f'tests/mcstudy/seed/nev_{data.ndst:05}/results_{ifit}.json')

        delete_all_pars()
        ifit+=1
#---------------------------------------------------
def main():
    data.nevt=100
    data.ndst=5

    test_seed()
    #test_simple()
    #test_constrain()
#---------------------------------------------------
if __name__ == '__main__':
    main()

