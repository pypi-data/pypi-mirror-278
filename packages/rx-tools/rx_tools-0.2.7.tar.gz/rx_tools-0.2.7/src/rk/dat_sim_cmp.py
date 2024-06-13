import ROOT
import numpy

import utils_noroot      as utnr
import pandas            as pnd 
import matplotlib.pyplot as plt
import read_selection    as rs
import pprint
import utils
import tqdm
import re 
import os 

from log_store import log_store

#-----------------------
class compare:
    log=log_store.add_logger('tools:dat_sim_cmp:compare')
    #-----------------------
    def __init__(self, df_dat, df_sim, d_var_hist):
        self.__df_dat            = df_dat
        self.__df_sim            = df_sim
        self.__d_var_hist        = d_var_hist

        self.__l_var             = None 
        self.__df_dat_wgt        = None 
        self.__df_sim_wgt        = None 

        self.__d_hist_dat        = {}
        self.__d_hist_sim        = {}

        self.__d_dat_ext         = {}
        self.__d_sim_ext         = {}

        self._d_cut              = {}
        self._df_var_eff         = pnd.DataFrame(columns=['Variable', 'Weight', 'Passed', 'Total'])

        self.__nentries_dat      = None 
        self.__nentries_sim      = None 

        self.__arr_weight_dat    = None
        self.__d_arr_weight_sim  = None
        self.__l_sim_weight_name = None

        self.__initialized       = False

        self.__dat_array_name    =   'arr_weight'
        self.__sim_dict_name     = 'd_arr_weight'
        self.__data_wgt_name     = 'weight'
    #-----------------------
    def __setitem__(self, variable, cut):
        if variable not in cut:
            self.log.error(f'Variable {variable} not found in {cut}')
            raise

        if variable in self._d_cut:
            self.log.error(f'Cut for variable {variable} already set')
            raise

        self.log.info(f'Adding cut {cut} on {variable}')

        self._d_cut[variable] = cut
    #-----------------------
    def __initialize(self):
        if self.__initialized:
            return

        #------
        self.__nentries_dat = self.__df_dat.Count().GetValue()
        self.__nentries_sim = self.__df_sim.Count().GetValue()
        #------
        self.__arr_weight_dat   = self.__check_dat_array(self.__df_dat, self.__nentries_dat)
        self.__d_arr_weight_sim = self.__check_sim_dict( self.__df_sim, self.__nentries_sim)
        #------
        if len(self.__d_var_hist) == 0:
            self.log.error('Dictionary of variables -> histogram is empty')
            raise

        self.__l_var = list(self.__d_var_hist.keys())
        #------
        fail_dat = self.__check_vars(self.__df_dat,       'data')
        fail_sim = self.__check_vars(self.__df_sim, 'simulation')

        if fail_dat or fail_sim:
            raise
        #------

        self.__initialized = True
    #-----------------------
    def __check_sim_dict(self, df, nentries):
        utnr.check_attr(df, self.__sim_dict_name)

        d_arr = getattr(df, self.__sim_dict_name)

        if len(d_arr) == 0:
            self.log.error('Empty dictionary of weight arrays for simulation')
            raise

        self.__l_sim_weight_name = list(d_arr.keys())

        for key, arr in d_arr.items():
            self.log.info(f'Using sim weight: {key}')
            if arr.size != nentries:
                self.log.error(f'Array {self.__sim_dict_name} has {arr.size} entries, dataframe has {nentries} entries')
                raise

        return d_arr
    #-----------------------
    def __check_dat_array(self, df, nentries):
        utnr.check_attr(df, self.__dat_array_name)

        arr = getattr(df, self.__dat_array_name)

        if arr.size != nentries:
            self.log.error('Array {} has {} entries, dataframe has {} entries'.format(array_name, arr.size, nentries))
            raise

        return arr
    #-----------------------
    def __check_vars(self, df, kind):
        l_df_col_name = df.GetColumnNames()

        fail=False

        self.__l_var.sort()

        l_var = []
        for var in self.__l_var:
            if var not in l_df_col_name:
                self.log.warning(f'{var} not found in RDataframe for {kind}, skipping it')
                continue

            l_var.append(var)

        self.__l_var = l_var

            #    self.log.error(f'{var} not found in RDataframe for {kind}')
            #    fail=True

        return fail
    #-----------------------
    def __get_df_wgt_ext(self, kind):
        if kind == 'dat':
            d_wgt = {} 
            d_wgt[self.__data_wgt_name] = self.__arr_weight_dat
            d_ext = self.__d_dat_ext

            df = self.__df_dat
        else:
            d_wgt = self.__d_arr_weight_sim 
            d_ext = self.__d_sim_ext

            df = self.__df_sim

        d_tot = df.AsNumpy(self.__l_var) 

        d_tot.update(d_wgt)
        d_tot.update(d_ext)

        try:
            df = ROOT.RDF.FromNumpy(d_tot)
        except:
            self.log.error('Cannot convert dictionary to dataframe')
            for key, val in d_tot.items():
                str_val = numpy.array2string(val, precision=3)
                self.log.info('{0:<40}{1:<40}'.format(key, str_val))
            raise

        return df
    #-----------------------
    def __compare(self, hist_path, effi_path, stat_path):
        current_weight = '(1)'

        self.log.info('Comparing:')
        for var, _ in self.__d_var_hist.items():
            self.log.info(f'  {var}')

        for sim_weight_name in self.__l_sim_weight_name:
            current_weight = ' * '.join([current_weight, sim_weight_name]) 

            self.__fill_dic_hist(current_weight)

        self._save_statistics(stat_path)
        self._save_histograms(hist_path)
        self._save_efficiency(effi_path)
    #-----------------------
    def _save_statistics(self, stat_path):
        l_var     = list(self.__d_hist_sim.keys())
        d_var_nam = dict()
        for var in l_var:
            dat_his   = self.__d_hist_dat[var]
            l_sim_his = self.__d_hist_sim[var]
            l_sim_nam = [wgt for his, wgt in l_sim_his]

            d_var_nam[var] = [dat_his.GetName()] + l_sim_nam

        utnr.dump_json(d_var_nam, stat_path)
    #-----------------------
    def _transform_dict(self, d_hist):
        d_out = {}

        for key, val in d_hist.items():
            if isinstance(val, list):
                l_hist = [ (hist.GetValue(), expr) for (hist, expr) in val] 
                d_out[key] = l_hist
            else:
                d_out[key] = val.GetValue() 

        return d_out
    #-----------------------
    def _save_histograms(self, hist_path):
        self.__d_hist_dat = self._transform_dict(self.__d_hist_dat)
        self.__d_hist_sim = self._transform_dict(self.__d_hist_sim)

        tp_hist = (self.__d_hist_dat, self.__d_hist_sim)

        self.log.info(f'Saving to: {hist_path}')
        utnr.dump_pickle(tp_hist, hist_path)
    #-----------------------
    def _save_efficiency(self, effi_path):
        if effi_path is None:
            return

        self.log.info(f'Saving to: {effi_path}')
        utnr.dump_pickle(self._df_var_eff, effi_path)
    #-----------------------
    def __fill_dic_hist(self, sim_weight):
        sim_weight = sim_weight[6:]
        sim_expr   = sim_weight

        self.log.info('--------------')
        self.log.info('Using weights:')
        self.log.info('--------------')
        self.log.info('{0:<20}{1:<30}'.format('Data'       , self.__data_wgt_name))
        self.log.info('{0:<20}{1:<30}'.format('Simulation' ,           sim_weight))

        #Expressions cannot be used by Dataframes as weights
        if ' * ' in sim_weight:
            self.__df_sim_wgt, sim_weight = utils.add_column_df(self.__df_sim_wgt, sim_weight)
        else:
            sim_weight = sim_expr

        for var in self.__l_var:
            hist  = self.__d_var_hist[var]
            h_sim = self.__df_sim_wgt.Histo1D(hist, var,           sim_weight)
            utnr.add_to_dic_lst(self.__d_hist_sim, var, (h_sim, sim_expr))

            self._calc_eff(sim_weight, var, self.__df_sim_wgt)

            if var not in self.__d_hist_dat:
                h_dat = self.__df_dat_wgt.Histo1D(hist, var, self.__data_wgt_name)
                self.__d_hist_dat[var] = h_dat

                self._calc_eff(self.__data_wgt_name, var, self.__df_dat_wgt)
    #-----------------------
    def _calc_eff(self, weight, var, df):
        cut = self._get_cut(var)
        if cut is None:
            return

        df_pas = df.Filter(cut)
        pas_yd = df_pas.Sum(weight)
        tot_yd = df.Sum(weight)

        self._df_var_eff = utnr.add_row_to_df(self._df_var_eff, [var, weight, pas_yd.GetValue(), tot_yd.GetValue()])
    #-----------------------
    def _get_cut(self, var):
        if var not in self._d_cut:
            return None
        else:
            return self._d_cut[var]
    #-----------------------
    def add_ext_var(self, varname, arr_dat = None, arr_sim = None, hist = None):
        self.log.debug(f'{"Adding":<20}{varname:<20}')

        utnr.check_none(arr_dat)
        utnr.check_none(arr_sim)
        utnr.check_none(hist)

        self.__initialize()

        utnr.check_array_size(arr_dat, self.__nentries_dat, label=      'Data')
        utnr.check_array_size(arr_sim, self.__nentries_sim, label='Simulation')

        self.__d_dat_ext[varname]  = arr_dat
        self.__d_sim_ext[varname]  = arr_sim
        self.__d_var_hist[varname] = hist
    #-----------------------
    def run(self, hist_path, effi_path = None, stat_path=None): 
        self.__initialize()

        self.__df_sim_wgt = self.__get_df_wgt_ext('sim')
        self.__df_dat_wgt = self.__get_df_wgt_ext('dat')

        self.__compare(hist_path, effi_path, stat_path)
#-----------------------
class plot:
    log=log_store.add_logger('tools:dat_sim_cmp:plot')
    #-----------------------
    def __init__(self, hist_path, d_opt={}):
        self._hist_path = hist_path
        self._d_opt     = d_opt
        self._d_var_df  = {}
        self._d_h_dat   = None
        self._d_h_sim   = None
        self._prefix    = None
        self._l_comp    = ['chi2_ndof', 'diff_quad']
        self._d_kind_lab= {'chi2_ndof': '$\chi2$/Ndof', 'diff_quad' : '$\sum (data-sim)^2 / Ndof$'} 
        self._d_hist    = {}

        self._initialized = False
    #-----------------------
    def _initialize(self):
        if self._initialized:
            return

        self._prefix = self._get_prefix()

        obj = utnr.load_pickle(self._hist_path)
        try:
            self._d_h_dat, self._d_h_sim = obj
        except:
            self.log.error(f'Cannot unpack pair of dictionaries from:')
            utnr.pretty_print(obj)
            raise

        self._remove_corrections()

        self._initialized = True
    #-----------------------
    def override_distribution(self, var_name, dataset, hist):
        self.log.info(f'Overriding distributions for {var_name} in {dataset}')
        self._d_hist[(var_name, dataset)] = hist
    #-----------------------
    def _get_prefix(self):
        dir_path = os.path.dirname(self._hist_path)
        dir_name = os.path.basename(dir_path)

        return dir_name
    #-----------------------
    def _remove_corrections(self):
        if 'remove' not in self._d_opt:
            return

        rm_cor  = self._d_opt['remove']

        d_h_sim = {} 
        for var, l_hist_corr in self._d_h_sim.items():
            l_hist_corr_strp = [ (hist, corr)  for hist, corr in l_hist_corr if rm_cor not in corr ]
            d_h_sim[var]     = l_hist_corr_strp

        self._d_h_sim = d_h_sim
    #-----------------------
    def save(self, plot_dir, l_var=[], l_log_var=[]):
        self._initialize()

        d_axis = {}
        for comp in self._l_comp:
            fig          = plt.figure(figsize=(10, 5))
            axis         = fig.add_subplot(111)
            axis.fig     = fig
            d_axis[comp] = axis

        for var in tqdm.tqdm(self._d_h_dat, ascii=' -'):
            if (l_var != []) and (var not in l_var):
                self.log.debug(f'Skipping: {var}')
                continue

            self.log.debug(f'Plotting {var}')
            log  = True if var in l_log_var else False
            axis = self._plot_var(var, plot_dir, d_axis, log=log)

        for comp, axis in d_axis.items():
            self._plot_gof_over(plot_dir, axis, comp)
    #-----------------------
    def get_df_dic(self):
        return self._d_var_df
    #-----------------------
    def _plot_gof_over(self, plot_dir, axis, comp):
        plotpath = f'{plot_dir}/overlay_{comp}.png'

        axis.legend(loc='center right', bbox_to_anchor=(1.5, 0.5))
        axis.set_ylim(bottom=0)

        plt.figure(axis.fig.number)
        plt.grid()
        plt.title(f'{comp}; {self._prefix}')
        plt.ylabel(self._d_kind_lab[comp])
        plt.xticks(rotation=30)
        plt.tight_layout()
        self.log.debug(f'Saving to: {plotpath}')
        plt.savefig(plotpath, bbox_inches='tight')
        plt.close()
    #-----------------------
    def _shrink_expr(self, wgt_expr):
        l_wgt = re.findall('(\w+)', wgt_expr)

        if len(l_wgt) == 0:
            self.log.error(f'Cannot extract weights from: {wgt_expr}')
            raise

        return l_wgt[-1]
    #-----------------------
    def _get_bdt_score(self, var):
        bdt_cut = rs.get('bdt', 'ETOS', q2bin='high', year = '2018')
        mtch    = re.match('BDT_cmb > ([0-9,\.]+) && BDT_prc > ([0-9,\.]+)', bdt_cut)
        if not mtch:
            log.error(f'Cannot extract scores from: {bdt_cut}')
            raise

        [cmb, prc] = mtch.groups()
        cmb        = float(cmb)
        prc        = float(prc)

        if   var.startswith('BDT_cmb'):
            return cmb
        elif var.startswith('BDT_prc'):
            return prc
        else:
            log.error(f'Invalid BDT variable: {var}')
            raise
    #-----------------------
    def _get_xname(self, var):
        if   var.startswith('B_PT'):
            xname = 'p_{T}(B^{+})'
        elif var.startswith('B_ETA'):
            xname = '\eta(B^{+})'
        elif var.startswith('B_T_L1_CONEPTASYM'):
            xname = 'CONEPTASYM(\ell_1)'
        elif var.startswith('cos_dira_jpsi'):
            xname = '\cos(DIRA)(J/\psi)'
        elif var.startswith('cos_dira'):
            xname = '\cos(DIRA)(B^+)'
        elif var.startswith('cos_theta_L'):
            xname = r'\cos(\theta_L)'
        elif var.startswith('fdchi2'):
            xname = '\chi^2_{FD}(B^+)' 
        elif var.startswith('B_VTXISODCHI2MASSONETRACK'):
            xname = '\log(Iso_{mass}^{1 trk})(B^+)'
        elif var.startswith('K_ETA'):
            xname = '\eta(K^+)' 
        elif var.startswith('K_PT'):
            xname = 'p_{T}(K^{+})' 
        elif var.startswith('h_ipchi2'):
            xname = '\chi^2_{IP}(K^+)' 
        elif var.startswith('Jpsi_FDCHI2_OWNPV'):
            xname = '\chi^2_{FD}(J/\psi)' 
        elif var.startswith('jpsi_ip_chi2'):
            xname = '\chi^2_{IP}(J/\psi)' 
        elif var.startswith('jpsi_pt'):
            xname = 'p_T(J/\psi)' 
        elif var.startswith('Kl1_angle'):
            xname = r'\alpha(K^+, \ell_1)' 
        elif var.startswith('Kl2_angle'):
            xname = r'\alpha(K^+, \ell_2)' 
        elif var.startswith('ll_angle'):
            xname = r'\alpha(e^+, e^-)' 
        elif var.startswith('log_B_VTXISODCHI2ONETRACK_p10'):
            xname = '\log(Iso_{vtx}^{2 trk})(B^+)'
        elif var.startswith('log_B_VTXISODCHI2TWOTRACK_p10'):
            xname = '\log(Iso_{vtx}^{2 trk})(B^+)'
        elif var.startswith('log_B_IPCHI2_PV'):
            xname = '\log(\chi^2_{IP})(B^+)'
        elif var.startswith('ll_max_ipchi2'):
            xname = '\max(\chi^2_{IP}(e^+), \chi^2_{IP}(e-))'
        elif var.startswith('max_lp_cc_mul'):
            xname = '\max(CCMULT(e^+), CCMULT(e-))'
        elif var.startswith('max_lp_cc_spt'):
            xname = '\max(CCSPT(e^+), CCSPT(e-))'
        elif var.startswith('ll_max_ETA'):
            xname = '\max(\eta(e^+), \eta(e^-))' 
        elif var.startswith('ll_max_PT'):
            xname = '\max(p_T(e^+), p_T(e^-))' 
        elif var.startswith('ll_min_ipchi2'):
            xname = '\min(\chi^2_{IP}(e^+), \chi^2_{IP}(e-))'
        elif var.startswith('min_lp_cc_it'):
            xname = '\min(CCIT(e^+), CCIT(e-))'
        elif var.startswith('min_lp_cc_spt'):
            xname = '\min(CCSPT(e^+), CCSPT(e-))'
        elif var.startswith('ll_min_ETA'):
            xname = '\min(\eta(e^+), \eta(e^-))' 
        elif var.startswith('ll_min_PT'):
            xname = '\min(p_T(e^+), p_T(e^-))' 
        elif var.startswith('nPVs'):
            xname = 'nPV' 
        elif var.startswith('nSPDHits'):
            xname = 'nSPD hits' 
        elif var.startswith('nTracks'):
            xname = 'nTracks' 
        elif var.startswith('log_B_VTXCHI2'):
            xname = '\log(\chi^2_{vtx})(B^+)' 
        elif var.startswith('BDT_prc'):
            xname = 'BDT_{prc}'
        elif var.startswith('BDT_cmb'):
            xname = 'BDT_{cmb}'
        elif var.startswith('xbrem'):
            xname = 'n\gamma_{brem}'
        else:
            xname = 'unnamed'

        return xname
    #-----------------------
    def _plot_var(self, var, plot_dir, d_axis, log=None):
        h_dat   = self._d_h_dat[var]
        l_h_sim = self._d_h_sim[var]

        if (var, 'Data') in self._d_hist:
            self.log.debug(f'Replacing data distribution for {var} with external one')
            h_dat = self._d_hist[(var, 'Data')]
            h_dat.SetTitle('Data (fitted)')

            var=f'{var}_fit'
        else:
            h_dat.SetTitle('Data (sWeighted)')
            var=f'{var}_swt'

        if 'suffix' in self._d_opt:
            suf = self._d_opt['suffix']
            var = f'{var}_{suf}'

        self._d_opt['xname'] = self._get_xname(var)

        l_hist = [h_dat]
        d_pval = {}
        for h_sim, wgt_expr in l_h_sim:
            wgt_expr = self._shrink_expr(wgt_expr)

            h_sim.SetTitle(wgt_expr)
            l_hist.append(h_sim)

            chi2_ndof = utils.get_hist_compatibility(h_dat, h_sim, kind='chi2_ndof')
            diff_quad = utils.get_hist_compatibility(h_dat, h_sim, kind='diff_quad')

            utnr.add_to_dic_lst(d_pval, 'weight'   ,  wgt_expr)
            utnr.add_to_dic_lst(d_pval, 'chi2_ndof', chi2_ndof)
            utnr.add_to_dic_lst(d_pval, 'diff_quad', diff_quad)

        df=pnd.DataFrame(d_pval)

        self._d_var_df[var] = df

        d_opt= {'logy' : log}
        d_opt.update(self._d_opt)
        d_opt['miny']   = 0.001
        d_opt['maxy']   = self._get_maxy(var) 
        d_opt['silent'] = True
        if var.startswith('BDT'):
            d_opt['vline'] = self._get_bdt_score(var), 8

        plot_path = f'{plot_dir}/{var}_dst.png'
        utils.plot_histograms(l_hist, plot_path, d_opt = d_opt)

        table_path = f'{plot_dir}/{var}_dst.tex'
        self._save_table(l_hist[0], l_hist[-1], table_path)

        for comp, axis in d_axis.items():
            plotpath = f'{plot_dir}/{var}_{comp}.png'
            self._plot_gof(df, var, plotpath, axis, comp)

        h_dat = l_hist[0]
        h_non = l_hist[1]
        h_ful = l_hist[-1]
        h_non.SetTitle('Uncorrected MC')
        h_ful.SetTitle('Fully corrected MC')

        plot_path = f'{plot_dir}/{var}_lst.png'

        d_opt['legend'] = 21
        if 'BDT' in var:
            d_opt['1_m_cdf'] = True
        utils.plot_histograms([h_dat, h_non, h_ful], plot_path, d_opt = d_opt)

        return d_axis 
    #-----------------------
    def _get_maxy(self, var):
        if   var.startswith('B_PT'):
            return 0.25
        elif var.startswith('B_ETA'):
            return 0.4
        elif var.startswith('BDT_prc'):
            return 1.6
        elif var.startswith('BDT_cmb'):
            return 1.6
        elif var.startswith('B_T_L1_CONEPTASYM'):
            return 0.2
        elif var.startswith('cos_dira_jpsi'):
            return 0.35
        elif var.startswith('cos_dira'):
            return 20.0
        elif var.startswith('cos_theta_L'):
            return 0.35
        elif var.startswith('fdchi2'):
            return 0.40
        elif var.startswith('B_VTXISODCHI2MASSONETRACK'):
            return 0.6
        elif var.startswith('K_ETA'):
            return 0.3
        elif var.startswith('K_PT'):
            return 0.4
        elif var.startswith('h_ipchi2'):
            return 0.1
        elif var.startswith('Jpsi_FDCHI2_OWNPV'):
            return 0.25
        elif var.startswith('jpsi_ip_chi2'):
            return 0.40
        elif var.startswith('jpsi_pt'):
            return 100
        elif var.startswith('Kl1_angle'):
            return 0.3 
        elif var.startswith('Kl2_angle'):
            return 0.3 
        elif var.startswith('ll_angle'):
            return 0.4 
        elif var.startswith('log_B_VTXISODCHI2ONETRACK_p10'):
            return 0.4 
        elif var.startswith('log_B_VTXISODCHI2TWOTRACK_p10'):
            return 0.4 
        elif var.startswith('log_B_IPCHI2_PV'):
            return 0.3 
        elif var.startswith('ll_max_ipchi2'):
            return 0.4 
        elif var.startswith('max_lp_cc_mul'):
            return 100 
        elif var.startswith('max_lp_cc_spt'):
            return 10
        elif var.startswith('ll_max_ETA'):
            return 0.4 
        elif var.startswith('ll_max_PT'):
            return 0.4 
        elif var.startswith('ll_min_ipchi2'):
            return 0.3 
        elif var.startswith('min_lp_cc_it'):
            return 0.3 
        elif var.startswith('min_lp_cc_spt'):
            return 100 
        elif var.startswith('ll_min_ETA'):
            return 0.25 
        elif var.startswith('ll_min_PT'):
            return 0.3 
        elif var.startswith('nPVs'):
            return 100 
        elif var.startswith('nSPDHits'):
            return 0.6
        elif var.startswith('nTracks'):
            return 0.3
        elif var.startswith('log_B_VTXCHI2'):
            return 0.3
        else:
            return 1.0
    #-----------------------
    def _save_table(self, h_dat, h_sim, path):
        nbins = h_dat.GetXaxis().GetNbins()
        l_stat_dat = self._get_hist_stat(h_dat)
        l_stat_sim = self._get_hist_stat(h_sim)
        l_bin      = range(1, nbins + 1)

        df = pnd.DataFrame({'Bin' : l_bin, 'Data' : l_stat_dat, 'MC' : l_stat_sim})
        self.log.debug(f'Saving to: {path}')
        df.style.to_latex(path)
    #-----------------------
    def _get_hist_stat(self, hist):
        nbins = hist.GetXaxis().GetNbins()

        l_stat = []
        for i_bin in range(1, nbins + 1):
            bc = hist.GetBinContent(i_bin)
            be = hist.GetBinError(i_bin)

            l_stat.append(f'{bc:.2e} {be:.2e}')

        return l_stat
    #-----------------------
    def _plot_gof(self, df, var, plotpath, axis, comp):
        ax=df.plot(x='weight', y=comp, legend=False)
        ax.set_ylim(bottom=0)

        plt.title(f'{var}; {self._prefix}')
        plt.ylabel(self._d_kind_lab[comp])
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.grid()
        self.log.debug(f'Saving to: {plotpath}')
        plt.savefig(plotpath)
        plt.close()

        if 'L2' in var or 'PT' in var or 'ETA' in var or var == 'nSPDHits':
            return

        df.plot(x='weight', y=comp, legend=True, label=var, ax=axis)
#-----------------------

