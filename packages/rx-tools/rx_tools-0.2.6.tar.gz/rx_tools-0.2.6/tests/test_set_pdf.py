from rk.set_pdf import set_pdf

import zutils.utils      as zut
import zfit
import os

from rk.model import zmodel

#------------------------------------------
def print_pdf(pdf, name=None):
    out_dir = 'tests/set_pdf'
    os.makedirs(out_dir, exist_ok=True)

    txt_path = f'{out_dir}/{name}.txt'
    zut.print_pdf(pdf, d_const={}, txt_path=txt_path)
#------------------------------------------
def get_model():
    obs = zfit.Space('mass', limits=(5180, 5600) ) 
    mod = zmodel(proc='ctrl', trig='ETOS', q2bin='jpsi', year='2018', obs=obs, mass='mass_jpsi', apply_bdt=True)
    pdf = mod.get_model(suffix='dt', prc_kind='ke')

    pdf.proc = 'ctrl'
    pdf.year = '2018'
    pdf.trig = 'ETOS'

    return pdf
#------------------------------------------
def test_simple():
    pdf = get_model()
    obj = set_pdf(pdf)
    pdf = obj.get_pdf(fit_version = 'v30')

    print_pdf(pdf, name='simple')
#------------------------------------------
def main():
    test_simple()
#------------------------------------------
if __name__ == '__main__':
    main()

