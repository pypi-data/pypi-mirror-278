import ROOT

import os
import numpy
import pandas            as pnd
import matplotlib.pyplot as plt

import utils
import utils_noroot as utnr

from rk.kinrwt import rwt as krwt

from hep_cl import hist_reader as hrdr

log=utnr.getLogger(__name__)
#--------------------------------------
class data:
    swt_ver = 'v5'
    ROOT.gInterpreter.Declare('TRandom3 r(1);')
#--------------------------------------
def get_data(inputdir, year, kind, nentries=10000):
    filepath = f'{inputdir}/sweights_{data.swt_ver}/{year}_{kind}_trigger_weights_sweighted.root'
    treename = 'TRG'
    file_dir = utnr.make_dir_path(os.path.dirname(filepath))

    if os.path.isfile(filepath):
        df = ROOT.RDataFrame(treename, filepath)
        log.visible('Reusing input')

        return df

    log.info('Making input')

    df = ROOT.RDataFrame(nentries)
    df = df.Define('w'          , 'r.Uniform(-1, 11);')
    df = df.Define('x'          , 'r.Uniform(-1, 11);')
    df = df.Define('y'          , 'r.Uniform(-1, 11);')
    df = df.Define('z'          , 'r.Uniform(-1, 11);')
    df = df.Define('pid_eff'    ,                  '1')
    df = df.Define('B_TRUEETA'  , 'r.Uniform(+0, +3);')
    df = df.Define('Jpsi_TRUEID',                '443')

    df = df.Define('H_PX'       , 'r.Uniform(1000, 10000);')
    df = df.Define('H_PY'       , 'r.Uniform(1000, 10000);')
    df = df.Define('H_PZ'       , 'r.Uniform(1000, 10000);')
    df = df.Define('Jpsi_M'     , 'r.Uniform(1000,  4000);')

    if   kind == 'dt':
        df = df.Define(f'weight',                  '1')
    elif kind == 'mc':
        df = df.Define(f'weight', 'TMath::Abs(1 + 0.01 * (10 * x - 10 * y + z + 3 * w * w))')

    df.Snapshot(treename, filepath)

    return df
#--------------------------------------
def make_settings(prefix, trigger, year, out_dir, syst, ndim=3):
    d_setting             = dict()
    d_setting['arr_w_1']  = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    d_setting['arr_x_1']  = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    d_setting['arr_y_1']  = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    d_setting['arr_z_1']  = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    d_setting['rwt_vars'] = ['w', 'x', 'y', 'z']
    d_setting['rwt_vars'] = d_setting['rwt_vars'][:ndim]

    set_dir   = utnr.make_dir_path(f'{out_dir}/share')
    json_path = f'{set_dir}/kinematics_{syst}.json'

    utnr.dump_json({f'{prefix}_{trigger}_{year}' : d_setting}, json_path)
#--------------------------------------
def test_toy_hist():
    kind    = 'toy'
    trigger = 'TRG'
    year    = '2018'
    syst    = 'trg' 
    method  = 'hist'
    toy_dir = f'tests/kinrwt/toy_{method}'

    make_settings(kind, trigger, year, toy_dir, syst)

    rdf_dt   = get_data(toy_dir, year, 'dt', nentries=100000)
    rdf_mc   = get_data(toy_dir, year, 'mc', nentries=100000)

    setdir    = utnr.make_dir_path(f'{toy_dir}/share')
    rootdir   = utnr.make_dir_path(f'{toy_dir}/root')
    
    rwt            = krwt(dt=rdf_dt, mc=rdf_mc)
    rwt.wgt_ver    = 'v0.1'
    rwt.wgt_dir    = rootdir 
    rwt.set_dir    = setdir 
    rwt.method     = method
    rwt.syst       = syst 
    rwt.save_reweighter(name=f'{trigger}_{year}_{kind}_{syst}')
    l_var          = rwt.vars
    [h_dt, h_mc]   = rwt.reweighter
    obj            = hrdr(dt=h_dt, mc=h_mc)

    check_weights(obj, rdf_dt, rdf_mc, trigger, method, l_var, 'toy')
#--------------------------------------
def test_toy_hepml(ndim):
    kind    = 'toy'
    trigger = 'TRG'
    year    = '2018'
    syst    = 'trg' 
    method  = 'hep_ml'
    toy_dir = f'tests/kinrwt/toy_{method}_{ndim:03}'

    make_settings(kind, trigger, year, toy_dir, syst, ndim=ndim)

    rdf_dt   = get_data(toy_dir, year, 'dt', nentries=100000)
    rdf_mc   = get_data(toy_dir, year, 'mc', nentries=100000)

    setdir   = utnr.make_dir_path(f'{toy_dir}/share')
    rootdir  = utnr.make_dir_path(f'{toy_dir}/root')
    
    rwt            = krwt(dt=rdf_dt, mc=rdf_mc)
    rwt.wgt_ver    = 'v0.1'
    rwt.wgt_dir    = rootdir 
    rwt.set_dir    = setdir 
    rwt.method     = method
    rwt.save_reweighter(name=f'{trigger}_{year}_{kind}_{syst}')
    l_var          = rwt.vars
    obj            = rwt.reweighter
#--------------------------------------
def add_columns(rdf, l_col):
    v_name = rdf.GetColumnNames()
    l_name = [ name.c_str() for name in v_name ]
    l_var  = []

    for col in l_col:
        if col in l_name:
            l_var.append(col)
            continue

        var = utils.get_var_name(col)
        rdf = rdf.Define(var, col)

        l_var.append(var)

    return rdf, l_var
#--------------------------------------
def main():
    ROOT.gROOT.ProcessLine(".L lhcbStyle.C")
    ROOT.lhcbStyle()

    test_toy_hepml(1)
    test_toy_hepml(2)
    test_toy_hepml(3)
    test_toy_hepml(4)

    return
    test_toy_hist()
#--------------------------------------
if __name__ == '__main__':
    main()

