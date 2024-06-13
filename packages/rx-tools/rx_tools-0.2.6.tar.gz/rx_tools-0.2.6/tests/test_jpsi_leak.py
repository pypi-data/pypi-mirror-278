from rk.jpsi_leakage import jpsi_leakage
from zutils.plot     import plot          as zfp

import ROOT
import zfit
import os

import matplotlib.pyplot as plt

#-----------------------------------
def plot_pdf(pdf, plot_dir, name):
    obj = zfp(data=pdf.create_sampler(n=10000), model=pdf)
    obj.plot(nbins=50, stacked=False)

    os.makedirs(plot_dir, exist_ok=True)
    plt.savefig(f'{plot_dir}/{name}.png')
    plt.close('all')
#-----------------------------------
def test_simple():
    obs = zfit.Space('mass', limits=(5400, 6000))
    obj = jpsi_leakage(obs=obs, trig='ETOS', q2bin='psi2', dset='2018')
    pdf = obj.get_pdf(suffix='simple', name=r'$B^+\to J/\psi(\to ee)K^+$')
    
    plot_pdf(pdf, 'tests/jpsi_leakage/simple', 'pdf')
#-----------------------------------
def main():
    test_simple()
#-----------------------------------
if __name__ == '__main__':
    main()

