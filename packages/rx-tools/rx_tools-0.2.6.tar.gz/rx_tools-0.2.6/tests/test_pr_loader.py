import ROOT
import zfit
import os
import mplhep
import logzero
import matplotlib.pyplot as plt

from zutils    import utils     as zut
from log_store import log_store
log = log_store.add_logger('rx_tools:test_pr_loader')

log_store.set_level('rx_tools:pr_shapes', logzero.DEBUG)

from rk.pr_shapes import pr_loader as prld
from zutils.plot  import plot      as zfp

#-----------------------------------------------
class data:
    out_dir = 'tests/pr_loader'
    os.makedirs(out_dir, exist_ok=True)

    bp_psjp     = '(abs(Jpsi_MC_MOTHER_ID) == 100443) & (abs(Jpsi_MC_GD_MOTHER_ID) == 521) & (abs(H_MC_MOTHER_ID) == 521)'
    bd_psks     = '(abs(Jpsi_MC_MOTHER_ID) ==    511) & (abs(H_MC_MOTHER_ID) == 313) & (abs(H_MC_GD_MOTHER_ID) == 511) & (abs(Jpsi_TRUEID) == 100443)'
    bp_psks     = '(abs(Jpsi_MC_MOTHER_ID) ==    521) & (abs(H_MC_MOTHER_ID) == 323) & (abs(H_MC_GD_MOTHER_ID) == 521) & (abs(Jpsi_TRUEID) == 100443)'

    neg_bp_psjp = bp_psjp.replace('==', '!=').replace('&' , '|')
    neg_bd_psks = bd_psks.replace('==', '!=').replace('&' , '|')
    neg_bp_psks = bp_psks.replace('==', '!=').replace('&' , '|')

    bx_jpkp     = f' (abs(H_TRUEID) == 321) & (abs(Jpsi_TRUEID) == 443)  & ({neg_bp_psjp}) & ({neg_bd_psks}) & ({neg_bp_psks})'
    none        = f'((abs(H_TRUEID) != 321) | (abs(Jpsi_TRUEID) != 443)) & ({neg_bp_psjp}) & ({neg_bd_psks}) & ({neg_bp_psks})'

    d_cut            = {}
    d_cut['bp_psjp'] = bp_psjp
    d_cut['bd_psks'] = bd_psks
    d_cut['bp_psks'] = bp_psks
    
    d_cut['bx_jpkp'] = bx_jpkp
    d_cut['none'   ] = none 
#-----------------------------------------------
def delete_all_pars():
    d_par = zfit.Parameter._existing_params
    l_key = list(d_par.keys())

    for key in l_key:
        del(d_par[key])
#-----------------------------------------------
def plot_pdf(pdf, obs, name, maxy=None):
    arr_mass = pdf.arr_mass
    arr_wgt  = pdf.arr_wgt

    obj = zfp(data=arr_mass, model=pdf, weights=arr_wgt)
    obj.plot(stacked=True, ext_text=f'{name}\n#Entries: {arr_mass.size}')
    obj.axs[0].set_ylim(bottom=0, top=maxy)
    obj.axs[0].axvline(x=5080, linestyle=':')
    obj.axs[0].axvline(x=5680, linestyle=':')

    plot_path = f'{data.out_dir}/{name}.png'
    log.info(f'Saving to: {plot_path}')
    plt.savefig(plot_path)
    plt.close('all')

    text_path = plot_path.replace('png', 'txt')
    zut.print_pdf(pdf, txt_path=text_path)
#-----------------------------------------------
def test_bdt():
    obs=zfit.Space('mass', limits=(4500, 6000))

    bdt_cut = "(BDT_cmb > 0.977000) & (BDT_prc > 0.480751)" 
    #bdt_cut = None 

    obp=prld(proc='bdXcHs', trig='ETOS', q2bin='psi2', dset='2018')
    pdf=obp.get_pdf(mass='mass_psi2', cut=bdt_cut, name='PRec', obs=obs, use_weights=True, bandwidth=20)
    plot_pdf(pdf, obs, 'bdt_bpXcHs_psi2_mass_psi2')

    obp=prld(proc='bpXcHs', trig='ETOS', q2bin='psi2', dset='2018')
    pdf=obp.get_pdf(mass='mass_psi2', cut=bdt_cut, name='PRec', obs=obs, use_weights=True, bandwidth=20)
    plot_pdf(pdf, obs, 'bdt_bdXcHs_psi2_mass_psi2')
#-----------------------------------------------
def test_bd():
    obs=zfit.Space('mass', limits=(4000, 6000))
    
    obj=prld(proc='bdXcHs', trig='ETOS', q2bin='jpsi', dset='2018')
    pdf_0=obj.get_pdf(mass='mass', cut='0.0 < BDT_cmb < 0.2', obs=obs, bandwidth=20)
    pdf_1=obj.get_pdf(mass='mass', cut='0.2 < BDT_cmb < 0.4', obs=obs, bandwidth=20)
    pdf_2=obj.get_pdf(mass='mass', cut='0.4 < BDT_cmb < 0.6', obs=obs, bandwidth=20)
    pdf_3=obj.get_pdf(mass='mass', cut='0.6 < BDT_cmb < 0.8', obs=obs, bandwidth=20)
    pdf_4=obj.get_pdf(mass='mass', cut='0.8 < BDT_cmb < 1.0', obs=obs, bandwidth=20)
    pdf_5=obj.get_pdf(mass='mass', cut='1.0 < BDT_cmb < 2.0', obs=obs, bandwidth=20)

    plot_pdf(pdf_0, obs, 'bd_bdt_00')
    plot_pdf(pdf_1, obs, 'bd_bdt_01')
    plot_pdf(pdf_2, obs, 'bd_bdt_02')
    plot_pdf(pdf_3, obs, 'bd_bdt_03')
    plot_pdf(pdf_4, obs, 'bd_bdt_04')
    plot_pdf(pdf_5, obs, 'bd_bdt_05')
#-----------------------------------------------
def test_bp():
    obs=zfit.Space('mass', limits=(4000, 6000))
    
    obj=prld(proc='bpXcHs', trig='ETOS', q2bin='jpsi', dset='2018')
    pdf_0=obj.get_pdf(mass='mass', cut='0.0 < BDT_cmb < 0.2', obs=obs, bandwidth=20)
    pdf_1=obj.get_pdf(mass='mass', cut='0.2 < BDT_cmb < 0.4', obs=obs, bandwidth=20)
    pdf_2=obj.get_pdf(mass='mass', cut='0.4 < BDT_cmb < 0.6', obs=obs, bandwidth=20)
    pdf_3=obj.get_pdf(mass='mass', cut='0.6 < BDT_cmb < 0.8', obs=obs, bandwidth=20)
    pdf_4=obj.get_pdf(mass='mass', cut='0.8 < BDT_cmb < 1.0', obs=obs, bandwidth=20)
    pdf_5=obj.get_pdf(mass='mass', cut='1.0 < BDT_cmb < 2.0', obs=obs, bandwidth=20)

    plot_pdf(pdf_0, obs, 'bp_bdt_00')
    plot_pdf(pdf_1, obs, 'bp_bdt_01')
    plot_pdf(pdf_2, obs, 'bp_bdt_02')
    plot_pdf(pdf_3, obs, 'bp_bdt_03')
    plot_pdf(pdf_4, obs, 'bp_bdt_04')
    plot_pdf(pdf_5, obs, 'bp_bdt_05')
#-----------------------------------------------
def test_wt(q2bin='psi2', proc='bpXcHs', mass='mass'):
    obs=zfit.Space('mass', limits=(5100, 5680))
    
    obp=prld(proc=proc, trig='ETOS', q2bin=q2bin, dset='2018')

    bandwidth=15
    if   q2bin == 'jpsi' and mass == 'mass_psi2':
        padding = {'lowermirror' : 1}
    elif q2bin == 'psi2' and mass == 'mass_psi2':
        padding = {'uppermirror' : 1}
    elif q2bin == 'jpsi' and mass == 'mass_jpsi':
        padding = {'uppermirror' : 0.8, 'lowermirror' : 0.0}
        bandwith= 10 
    else:
        padding = {}

    pdf_u=obp.get_pdf(mass=mass, use_weights=False, obs=obs, bandwidth=bandwidth, padding=padding)
    pdf_w=obp.get_pdf(mass=mass, use_weights=True , obs=obs, bandwidth=bandwidth, padding=padding)

    proc = proc.replace('*', 'x')

    plot_pdf(pdf_u, obs, f'{proc}_{q2bin}_{mass}_nwgt')
    plot_pdf(pdf_w, obs, f'{proc}_{q2bin}_{mass}_ywgt')
#-----------------------------------------------
def do_test_match(q2bin, proc, mass, weights, match):
    obs=zfit.Space('mass', limits=(5100, 5680))
    
    obp=prld(proc=proc, trig='ETOS', q2bin=q2bin, dset='2018')
    pdf=obp.get_pdf(mass=mass, obs=obs, use_weights=weights, padding=0.1, cut=data.d_cut[match])
    plot_pdf(pdf, obs, f'{match}_{proc}_{q2bin}_{mass}', maxy=300)
#-----------------------------------------------
def test_match(weight):
    do_test_match('psi2', 'bpXcHs', 'mass_psi2', weight, 'bp_psjp')
    do_test_match('psi2', 'bdXcHs', 'mass_psi2', weight, 'bd_psks')
    do_test_match('psi2', 'bpXcHs', 'mass_psi2', weight, 'bp_psks')

    do_test_match('psi2', 'bpXcHs', 'mass_psi2', weight, 'bx_jpkp')
    do_test_match('psi2', 'bdXcHs', 'mass_psi2', weight, 'bx_jpkp')
    do_test_match('psi2', 'bpXcHs', 'mass_psi2', weight, 'none')
    do_test_match('psi2', 'bdXcHs', 'mass_psi2', weight, 'none')
#-----------------------------------------------
def test_split():
    obs=zfit.Space('mass', limits=(5100, 5680))
    
    obp  =prld(proc='bpXcHs', trig='ETOS', q2bin='psi2', dset='2018')
    d_pdf=obp.get_components(mass='mass_psi2', obs=obs, use_weights=True, padding=0.1)

    for name, pdf in d_pdf.items():
        plot_pdf(pdf, obs, f'{name}_bxXcHs_psi2_mass_psi2', maxy=300)
#-----------------------------------------------
def test_sum():
    obs=zfit.Space('mass', limits=(4250, 5680))

    for ccbar in ['jpsi', 'psi2']:
        maxy = 2000 if ccbar == 'psi2' else 8000
        for dec in [0, 1]:
            for sam in [0, 1]:
                obp=prld(proc='b*XcHs', trig='ETOS', q2bin=ccbar, dset='2018', d_weight={'dec': dec, 'sam' : sam})
                pdf=obp.get_sum(mass=f'mass_{ccbar}', name='PRec', obs=obs, padding=0.1, bandwidth=10)

                plot_pdf(pdf, obs, f'sum_bxXcHs_{ccbar}_mass_{ccbar}_dec{dec}_sam{sam}', maxy=maxy)
                delete_all_pars()
#-----------------------------------------------
def test_sum_allon():
    obs=zfit.Space('mass', limits=(4250, 5680))

    for ccbar in ['jpsi', 'psi2']:
        maxy = 3000 if ccbar == 'psi2' else 9000
        obp=prld(proc='b*XcHs', trig='ETOS', q2bin=ccbar, dset='2018', d_weight={'dec': 1, 'sam' : 1})
        pdf=obp.get_sum(mass=f'mass_{ccbar}', name='PRec', obs=obs, padding=0.1, bandwidth=10)

        plot_pdf(pdf, obs, f'sum_bxXcHs_{ccbar}_mass_{ccbar}', maxy=maxy)
        delete_all_pars()
#-----------------------------------------------
def test_brem():
    obs=zfit.Space('mass', limits=(4000, 5680))

    for nbrem in [0, 1, 2]:
        obp=prld(proc='b*XcHs', trig='ETOS', q2bin='jpsi', dset='2018')
        obp.val_dir = f'{data.out_dir}/validation'
        obp.nbrem   = nbrem
        pdf=obp.get_sum(mass='mass_jpsi', name='PRec', obs=obs, use_weights=True, padding=0.1)

        plot_pdf(pdf, obs, f'sum_bxXcHs_psi2_mass_psi2_{nbrem}', maxy=3000)

        delete_all_pars()
#-----------------------------------------------
def test_dset():
    obs=zfit.Space('mass', limits=(4000, 5680))

    for dset in ['r1', 'r2p1', '2017', '2018']:
        obp=prld(proc='b*XcHs', trig='ETOS', q2bin='psi2', dset=dset)
        pdf=obp.get_sum(mass='mass_psi2', name='PRec', obs=obs, use_weights=True, padding=0.1)
        plot_pdf(pdf, obs, f'sum_bxXcHs_psi2_mass_psi2_{dset}', maxy=3000)

        delete_all_pars()
#-----------------------------------------------
def test_simple_jpsi():
    obs=zfit.Space('mass', limits=(4500, 6000))
    d_wgt = {'dec' : 1, 'sam' : 1}

    obp=prld(proc='b*XcHs', trig='ETOS', q2bin='jpsi', dset='2018', d_weight=d_wgt)
    pdf=obp.get_pdf(mass='mass_jpsi', name='PRec', obs=obs, bandwidth=10)
    plot_pdf(pdf, obs, 'bdt_bxXcHs_jpsi_mass_jpsi')
#-----------------------------------------------
def test_simple_psi2():
    obs=zfit.Space('mass', limits=(4500, 6000))
    d_wgt = {'dec' : 1, 'sam' : 1}

    obp=prld(proc='b*XcHs', trig='ETOS', q2bin='psi2', dset='2018', d_weight=d_wgt)
    pdf=obp.get_pdf(mass='mass_psi2', name='PRec', obs=obs, bandwidth=10)
    plot_pdf(pdf, obs, 'bdt_bxXcHs_psi2_mass_psi2')
#-----------------------------------------------
def test_split_type():
    obs=zfit.Space('mass', limits=(4500, 6000))

    d_wgt   = {'dec' : 1, 'sam' : 1}
    for qsq, spl in [('jpsi', 'sam'), ('psi2', 'phy')]:
        obp=prld(proc='b*XcHs', trig='ETOS', q2bin='jpsi', dset='2018', d_weight=d_wgt, split=spl)
        pdf=obp.get_sum(mass='mass_jpsi', name='PRec', obs=obs, bandwidth=10)
        plot_pdf(pdf, obs, 'bdt_bxXcHs_jpsi_mass_jpsi')
#-----------------------------------------------
def main():
    plt.style.use(mplhep.style.LHCb2)

    data.out_dir = 'tests/pr_loader/simple_jpsi'
    os.makedirs(data.out_dir, exist_ok=True)
    test_simple_jpsi()

    return

    data.out_dir = 'tests/pr_loader/split_type'
    os.makedirs(data.out_dir, exist_ok=True)
    test_split_type()

    data.out_dir = 'tests/pr_loader/sum_allon'
    os.makedirs(data.out_dir, exist_ok=True)
    test_sum_allon()

    data.out_dir = 'tests/pr_loader/sum'
    os.makedirs(data.out_dir, exist_ok=True)
    test_sum()

    data.out_dir = 'tests/pr_loader/bdt'
    os.makedirs(data.out_dir, exist_ok=True)
    test_bdt()

    data.out_dir = 'tests/pr_loader/dset'
    os.makedirs(data.out_dir, exist_ok=True)
    test_dset()

    data.out_dir = 'tests/pr_loader/brem'
    os.makedirs(data.out_dir, exist_ok=True)
    test_brem()

    data.out_dir = 'tests/pr_loader/split'
    os.makedirs(data.out_dir, exist_ok=True)
    test_split()

    data.out_dir = 'tests/pr_loader/match_ywgt'
    os.makedirs(data.out_dir, exist_ok=True)
    test_match(True)

    data.out_dir = 'tests/pr_loader/match_nwgt'
    os.makedirs(data.out_dir, exist_ok=True)
    test_match(False)

    data.out_dir = 'tests/pr_loader/bdt_bd'
    os.makedirs(data.out_dir, exist_ok=True)
    test_bd()

    data.out_dir = 'tests/pr_loader/bdt_bp'
    os.makedirs(data.out_dir, exist_ok=True)
    test_bp()

    data.out_dir = 'tests/pr_loader/wt'
    os.makedirs(data.out_dir, exist_ok=True)

    for q2bin in ['jpsi', 'psi2']:
        for proc in ['bdXcHs', 'bpXcHs', 'b*XcHs']:
            for mass in ['mass', 'mass_jpsi', 'mass_psi2']:
                test_wt(q2bin=q2bin, proc=proc, mass=mass)

    return
#-----------------------------------------------
if __name__ == '__main__':
    main()

