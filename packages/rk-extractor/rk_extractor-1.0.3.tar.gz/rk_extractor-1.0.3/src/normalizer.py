import os
import re
import glob
import ROOT
import math
import zfit
import numpy
import extset
import utils_noroot      as utnr
import zutils.utils      as zut
import matplotlib.pyplot as plt

from rdf_loader    import rdf_loader
from zutils.utils  import zfsp_1d_input
from misid_check   import misid_check
from zutils.utils  import split_fit     as zfsp
from zutils.plot   import plot          as zfp
from fitter        import zfitter
from log_store     import log_store

log = log_store.add_logger(name='rk_extractor:normalizer')
#--------------------------------------
class normalizer:
    '''
    Class used to find normalizations for combinatorial and PRec components
    in the high-q2 signal model
    '''
    #--------------------------------------
    def __init__(self, dset=None, trig=None, d_model=None, d_val=None, d_var=None, blind=False):
        self._d_model = d_model 
        self._dset    = dset
        self._trig    = trig
        self._d_val   = d_val
        self._d_var   = d_var
        self._blind   = blind

        self._l_flt_par= ['lm_cb', 'mu_cb', 'a', 'b', 'ncb', 'npr_ee','ncnd_', 'nsg_mm', 'cmb_sp_lam', 'ctrl_sp_sigma', 'nsg_ee', 'ctrl_sp_mu']
        self._l_scl_par= ['_dmu_', '_ssg_']

        self._d_const  = {}
        self._nbins    = 60 
        self._rng_mm   = 5180, 5600 
        self._rng_ee   = 4500, 6000 
        self._bln_ee   = 5000, 5450
        self._bln_mm   = 5200, 5360

        self._d_data      = None
        self._s_par       = None
        self._d_pre       = None
        self._out_dir     = None
        self._custom_data = False
        self._initialized = False 
    #--------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        os.makedirs(f'{self._out_dir}/pdf', exist_ok=True)

        self._check_none(self._d_model, 'self._d_model')
        self._check_none(self._d_val  , 'self._d_val'  )
        self._check_none(self._d_var  , 'self._d_var'  )

        self._s_par     = self._get_parameters() 
        self._d_pre     = {par.name : par.value().numpy() for par in self._s_par}
        self._d_const   = self._prepare_pars()
        self._d_data    = self._get_data()

        self._initialized = True 
    #--------------------------------------
    def _check_none(self, obj, name):
        if obj is None:
            log.error(f'Object {name} is None')
            raise
    #--------------------------------------
    def _get_parameters(self):
        s_par = set()
        for l_pdf_mm, pdf_ee in self._d_model.values():
            if l_pdf_mm is not None:
                [pdf_bm, pdf_qm] = l_pdf_mm
            else:
                [pdf_bm, pdf_qm] = [None, None] 

            s_mod_par_bm = set() if pdf_bm is None else pdf_bm.get_params()
            s_mod_par_qm = set() if pdf_qm is None else pdf_qm.get_params()
            s_mod_par_ee = set() if pdf_ee is None else pdf_ee.get_params()

            s_par        = s_par.union(s_mod_par_bm)
            s_par        = s_par.union(s_mod_par_qm)
            s_par        = s_par.union(s_mod_par_ee)

        return s_par
    #--------------------------------------
    @property
    def data(self):
        return self._d_data

    @data.setter
    def data(self, value):
        self._custom_data = True
        self._d_data      = value 
    #--------------------------------------
    def _container_tolist(self, arr_mass):
        if isinstance(arr_mass, zfit.Data):
            arr_mass = arr_mass.to_numpy()

        try:
            l_mass = arr_mass.tolist()
        except:
            log.error(f'Cannot convert array to list for:')
            log.info(arr_mass)
            raise

        return l_mass
    #--------------------------------------
    def _get_jpsi_mass(self, rdf):
        df  = misid_check.rdf_to_df(rdf, '(L1|L2|H)_(P\w|ID)$')
        obj = misid_check(df, d_lep={'L1' : 13, 'L2' : 13}, d_had={'H' : 13})
        df  = obj.get_df()

        arr_mass = df.H_swp.to_numpy()

        return arr_mass
    #-------------------------------------
    def _get_mass(self, rdf, kind):
        if   kind == 'bp':
            arr_mass = rdf.AsNumpy(['B_M'])['B_M']
        elif kind == 'mm':
            arr_mass = self._get_jpsi_mass(rdf)
        else:
            log.error(f'Invalid kind: {kind}')
            raise

        return arr_mass.tolist()
    #--------------------------------------
    @utnr.timeit
    def _get_data(self):
        dat_path = f'{self._out_dir}/data/{self._dset}_{self._trig}.json'
        if   self._d_data is not None:
            log.warning(f'Using data passed by user')
            return self._d_data
        elif os.path.isfile(dat_path):
            log.info(f'Loading cached data from: {dat_path}')
            d_dat = utnr.load_json(dat_path)
            return d_dat 

        log.info(f'Caching data: {dat_path}')

        os.makedirs(f'{self._out_dir}/data', exist_ok=True)

        obj              = rdf_loader(sample='blind_fits', proc='data', asl_vers=None, ntp_vers='v10.21p2', year=self._dset, trig=self._trig)
        rdf, df_cf, d_md = obj.get_rdf()

        arr_bp = self._get_mass(rdf, 'bp')
        arr_mm = self._get_mass(rdf, 'mm') 
        d_dat  = {'bp_mass' : arr_bp, 'mm_mass' : arr_mm}

        log.info(f'Saving to: {dat_path}')
        utnr.dump_json(d_dat, dat_path) 

        cf_path = f'{self._out_dir}/data/{self._dset}_{self._trig}_cf.json'
        df_cf.to_json(cf_path, indent=4)

        md_path = f'{self._out_dir}/data/{self._dset}_{self._trig}_md.json'
        utnr.dump_json(d_md, md_path) 

        return d_dat 
    #--------------------------------------
    def _prepare_pars(self):
        for par in self._s_par:
            par.floating = False

        d_const = {}
        for par in self._s_par:
            for scl_par in self._l_scl_par:
                if scl_par in par.name:
                    par.floating = True
                    continue

            for flt_par in self._l_flt_par:
                if par.name.startswith(flt_par):
                    par.floating = True
                else:
                    continue

                if par.name in self._d_val:
                    var = self._d_var[par.name]
                    val = self._d_val[par.name]
                    d_const[par.name] = val, math.sqrt(var)

        return d_const
    #--------------------------------------
    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    def out_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
        except:
            log.error(f'Cannot create directory: {value}')
            raise

        self._out_dir = value
    #--------------------------------------
    def _get_stats(self, zdata, model):
        if self._trig != 'MTOS':
            return ''

        return 'no stats'

        if   isinstance(zdata, (zfit.core.data.SamplerData, zfit.core.data.Data)):
            arr_dat = zdata.numpy()
        elif isinstance(zdata, numpy.ndarray):
            arr_dat = zdata
        else:
            dat_typ = str(type(zdata))
            log.error(f'Cannot get a numpy array from: {dat_typ}')
            raise

        obs     = model.space
        [[minx]], [[maxx]] = obs.limits

        arr_flg = (arr_dat > minx) & (arr_dat < maxx)
        arr_dat = arr_dat[arr_flg]
        ndata   = float(arr_dat.size)

        s_par     = model.get_params(floating=False)
        [pst_val] = [ par.value().numpy() for par      in s_par               if par.name.startswith('nsg_mm_') ]
        [pre_val] = [ val                 for nam, val in self._d_pre.items() if nam.startswith('nsg_mm_')      ]

        v1 = f'Data: {ndata:.0f} $m\in [{minx:.0f}, {maxx:.0f}]$'
        v2 = f'Fitted: {pst_val:.0f}'
        v3 = f'Expected: {pre_val:.0f}'

        return f'{v1}\n{v2}\n{v3}'
    #--------------------------------------
    def _get_pdf_names(self):
        d_leg         = {}
        d_leg['prc']  = r'$c\bar{c}_{prc} + \psi(2S)K^+$'
        d_leg['bpks'] = r'$B^+\to K^{*+}(\to K^+\pi^0)e^+e^-$'
        d_leg['bdks'] = r'$B^0\to K^{*0}(\to K^+\pi^-)e^+e^-$'
        d_leg['bsph'] = r'$B_s\to \phi(\to K^+K^-) e^+e^-$'
        d_leg['bpk1'] = r'$B^+\to K_{1}e^+e^-$'
        d_leg['bpk2'] = r'$B^+\to K_{2}e^+e^-$'

        return d_leg
    #--------------------------------------
    def _get_blinding(self):
        if self._trig == 'MTOS':
            return

        low, hig= self._bln_ee
        l_blnd  = [extset.sig_name, low, hig]

        return l_blnd
    #--------------------------------------
    def _plot_fit(self, data=None, model=None, name=None, result=None, stacked=None):
        l_blnd  = self._get_blinding()
        stats   = self._get_stats(data, model)

        obj= zfp(data=data, model=model, result=None)
        obj.plot(skip_pulls=False, blind=l_blnd, nbins=self._nbins, d_leg=self._get_pdf_names(), stacked=stacked, ext_text=stats)
        obj.axs[0].grid()

        if not self._custom_data:
            if   '_all_' in name and 'MTOS' in name and '_bms_' in name:
                obj.axs[0].set_ylim(0,  250)
            elif '_all_' in name and 'MTOS' in name and '_bms_' in name:
                obj.axs[0].set_ylim(0,   50)
            elif '_all_' in name and 'ETOS' in name:
                obj.axs[0].set_ylim(0,  120)
            elif '_all_' in name and 'GTIS' in name:
                obj.axs[0].set_ylim(0,   50)

        obj.axs[1].set_ylim(-5, 5)
        obj.axs[1].axhline(0, color='r')

        vers  = os.path.basename(self._out_dir)
        title = f'Dataset: {self._dset}; Trigger: {self._trig}; Version: {vers}'
        obj.axs[0].set_title(title)

        os.makedirs(f'{self._out_dir}/fits', exist_ok=True)
        plot_path = f'{self._out_dir}/fits/{name}.png'
        log.info(f'Saving to: {plot_path}')
        plt.savefig(plot_path)
        plt.close('all')
    #--------------------------------------
    def _reformat_mod(self, d_mod):
        l_mod_mm, mod_ee = d_mod['all']

        if   self._trig == 'MTOS':
            return l_mod_mm 
        elif self._trig in ['ETOS', 'GTIS']:
            return [mod_ee]
        else:
            log.error(f'Invalid trigger: {self._trig}')
            raise
    #--------------------------------------
    def _reformat_dat(self, d_dat):
        l_bm = d_dat['bp_mass']
        l_q2 = d_dat['mm_mass']

        arr_bm = numpy.array(l_bm)
        arr_q2 = numpy.array(l_q2)

        if   self._trig == 'MTOS':
            return [arr_bm, arr_q2]
        elif self._trig in ['ETOS', 'GTIS']:
            return [arr_bm]
        else:
            log.error(f'Invalid trigger: {self._trig}')
            raise
    #--------------------------------------
    @utnr.timeit
    def _fit(self, d_mod, d_dat):
        d_fdat  = {}
        d_fmod  = {}
        l_mod   = self._reformat_mod(d_mod)
        l_dat   = self._reformat_dat(d_dat)
        tot_nll = None
        for mod, dat in zip(l_mod, l_dat):
            zdat = zfit.Data.from_numpy(obs=mod.space, array=dat)
            name = mod.name

            d_fdat[name] = dat
            d_fmod[name] = mod

            if self._blind:
                log.info(f'Adding nll for model {name}, blinding')
                nll_1 = zfit.loss.ExtendedUnbinnedNLL(model=mod, data=zdat, fit_range=(4500, 5000))
                nll_2 = zfit.loss.ExtendedUnbinnedNLL(model=mod, data=zdat, fit_range=(5450, 6000))
                nll   = nll_1 + nll_2
            else:
                log.info(f'Adding nll for model {name}, unblinding')
                nll   = zfit.loss.ExtendedUnbinnedNLL(model=mod, data=zdat, fit_range=None)

            tot_nll = nll if tot_nll is None else nll + tot_nll

        minimizer = zfit.minimize.Minuit()
        log.debug('Minimizing')
        result    = minimizer.minimize(tot_nll)

        return result, d_fdat, d_fmod
    #--------------------------------------
    def _print_pdfs(self, prefix):
        for key, (l_mod_mm, mod_ee) in self._d_model.items():
            if l_mod_mm is not None:
                [mod_bm, mod_qm] = l_mod_mm
                zut.print_pdf(mod_bm, txt_path=f'{self._out_dir}/pdf/{prefix}_mm_{key}_{self._dset}_{self._trig}_bm.txt', d_const=self._d_const)
                zut.print_pdf(mod_qm, txt_path=f'{self._out_dir}/pdf/{prefix}_mm_{key}_{self._dset}_{self._trig}_qm.txt', d_const=self._d_const)

            if mod_ee is not None:
                zut.print_pdf(mod_ee, txt_path=f'{self._out_dir}/pdf/{prefix}_ee_{key}_{self._dset}_{self._trig}.txt', d_const=self._d_const)
    #--------------------------------------
    def _plot_fits(self, d_fdat, d_fmod):
        for key in d_fdat:
            arr_mass = d_fdat[key]
            model    = d_fmod[key]

            self._plot_fit(data=arr_mass, model=model, name=f'{self._trig}_{self._dset}_{key}_stk', stacked= True)
    #--------------------------------------
    @utnr.timeit
    def get_fit_result(self):
        self._initialize()

        self._print_pdfs('pre')
        res, d_fdat, d_fmod = self._fit(self._d_model, self._d_data)
        self._print_pdfs('pos')

        self._plot_fits(d_fdat, d_fmod)

        res.hesse()
        res.freeze()

        return res
#--------------------------------------

