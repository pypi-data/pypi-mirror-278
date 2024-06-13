import sys
import os

from rk.model import zmodel

import utils_noroot      as utnr
import matplotlib.pyplot as plt
import zutils.utils      as zut
import zfit

from fitter      import zfitter
from zutils.plot import plot    as zfp

log=utnr.getLogger(__name__)

#--------------------------
class data:
    obs = zfit.Space('mass', limits=(5080, 5680))
#--------------------------
def delete_all_pars():
    d_par = zfit.Parameter._existing_params
    l_key = list(d_par.keys())

    for key in l_key:
        del(d_par[key])
#--------------------------
def test_sign(year, trig, obs):
    mod=zmodel(proc='ctrl', trig=trig, year=year, q2bin='jpsi', obs=obs, mass='mass_jpsi')
    pdf=mod.get_model(suffix='', signal=True)
#--------------------------
def test_model(year, trig, proc, suff, obs):
    q2bin = 'jpsi'      if proc == 'ctrl' else proc

    mod   = zmodel(proc=proc, trig=trig, year=year, q2bin=q2bin, obs=obs, apply_bdt=True, mass=f'mass_{q2bin}')
    pdf   = mod.get_model(suffix=suff, skip_csp = True, prc_kind='ke')

    dat  = pdf.create_sampler()
    res  = None
    obj  = zfp(data=dat, model=pdf, result=res)
    obj.plot()

    out_dir = 'tests/zmodel/test_model'

    os.makedirs(out_dir, exist_ok=True)

    plt.savefig(f'{out_dir}/{year}_{trig}_{proc}.png')
    plt.close('all')

    delete_all_pars()
#--------------------------
def test_cabibbo():
    mod   = zmodel(proc='ctrl', trig='ETOS', year='2018', q2bin='jpsi', obs=data.obs, apply_bdt=True, mass='mass_jpsi')
    pdf   = mod.get_model(suffix='cabibbo', prc_kind='ke', reparametrize_cabibbo=True)

    out_dir = f'tests/zmodel/cabibbo'
    os.makedirs(out_dir, exist_ok=True)
    zut.print_pdf(pdf, txt_path=f'{out_dir}/cabibbo.txt')
#--------------------------
def test_simple():
    for proc in ['ctrl', 'psi2']:
        obs = zfit.Space('mass', limits=(5080, 5680))
        test_model('2018', 'ETOS', proc, 'ele', obs)
        test_model('2018', 'GTIS', proc, 'ele', obs)
        test_model('2018', 'MTOS', proc, 'muo', obs)
#--------------------------
def main():
    test_simple()
    return
    test_cabibbo()
#--------------------------
if __name__ == '__main__':
    main()
#--------------------------

