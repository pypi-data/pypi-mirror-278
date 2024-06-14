import numpy
import zfit
import math
import re
import os
import pprint
import zutils.utils      as zut
import matplotlib.pyplot as plt
import utils_noroot      as utnr

from scipy.stats           import poisson
from bdt_scale             import scale_reader as scl_rdr
from log_store             import log_store

log = log_store.add_logger(name='rk_extractor:rkex_model')
#----------------------------------------------------
class model:
    def __init__(self, rk=1, preffix='', d_nent=None, channel=None, obs_mm_sp=None):
        '''
        Parameters
        -----------------------
        rk     (float): Value used in model, will impact toy data produced 
        preffix(str)  : Used to name parameters in case multiple models used
        d_nent (dict) : Stores number of B -> llK entries, after selection, e.g. {r1 : 23235}
        l_dset (list) : List of datasets for which the models should be created, if None, do it for all datasets i.e. r1_TOS, r2p1_TOS...
        channel (str) : If used, PDFs and datasets will be restricted to this channel, values 'ee', 'mm'
        obs_mm_sp (zfit.space): Zfit observable to be used in the double swapped di-muon mass.
        '''
        self._rk         = rk
        self._preffix    = preffix
        self._d_nent     = d_nent
        self._chan       = channel 
        self._obs_mm_sp  = obs_mm_sp

        self._l_all_kind = None

        zfit.settings.changed_warnings.hesse_name = False

        self._nbin        = 80
        self._msid_vers   = 'v4'
        self._comb_vers   = 'v1'
        self._d_lumi      = {'r1' : 3, 'r2p1' : 1.9, '2017' : 1.7, '2018' : 2.1}
        self._l_dset      = ['r1', 'r2p1', '2017', '2018']
        self._d_mod       = None
        self._out_dir     = None
        self._mod_dir     = None
        self._kind        = 'nom' 
        self._d_rare_scl  = {}

        self._initialized = False
    #----------------------------------------------------
    def _initialize(self):
        if self._initialized:
            return
        log.info('Starting initialization')

        if self._d_nent is None:
            log.error(f'No B-> Jpsi K yields found')
            raise

        self._set_kinds()
        self._check_kind()
        self._cache_model()
        self._validate_model()

        log.info('Finished initializing')

        if self._out_dir is not None:
            utnr.dump_json(self._d_rare_scl, f'{self._out_dir}/rare_scales.json')

        self._initialized = True
    #----------------------------------------------------
    def _validate_model(self):
        for ds, (mod_mm, mod_ee) in self._d_mod.items(): 
            self._plot_model(f'{ds}_mm', mod_mm)
            self._plot_model(f'{ds}_ee', mod_ee)

            self._print_model(f'{ds}_mm', mod_mm)
            self._print_model(f'{ds}_ee', mod_ee)
    #---------------------------------------------------------------
    def _set_kinds(self):
        log.debug(f'Setting model kinds')
        self._l_all_kind = []
        self._l_all_kind.append(r'sig_MTOS:sys\d{1}')
        self._l_all_kind.append(r'cmb_MTOS:sys\d{1}')

        self._l_all_kind.append(r'sig_ETOS:sys\d{1}')
        self._l_all_kind.append(r'cpr_ETOS:sys\d{1}')
        self._l_all_kind.append(r'cmb_ETOS:sys\d{1}')

        self._l_all_kind.append(r'rpr_ETOS:bts\d+')
        self._l_all_kind.append(r'cpr_ETOS:bts\d+')
    #---------------------------------------------------------------
    def _check_kind(self):
        log.debug(f'Checking model kinds')
        if   self._kind is None:
            log.error(f'Kind not specified')
            raise
        elif self._kind == 'nom':
            log.debug('Using nominal model')
            return

        found = False
        for kind in self._l_all_kind:
            try:
                if re.match(kind, self._kind):
                    found = True
                    break
            except:
                log.error(f'Cannot match {self._kind} to {kind}')
                raise

        if not found: 
            log.error(f'Model of kind {self._kind} not supported')
            raise
        else:
            log.debug(f'Using model of kind: {self._kind}')
    #----------------------------------------------------
    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    def out_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
        except:
            log.error(f'Cannot create: {value}')
            raise

        self._out_dir = value
        self._mod_dir = f'{self._out_dir}/plots/models'
        os.makedirs(self._mod_dir, exist_ok=True)

        log.debug(f'Using output directory: {self._out_dir}')
    #----------------------------------------------------
    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        '''
        Parameters
        -----------------
        kind (str): Will define the type of PDF, e.g. "signal:sys1", if not specified, will use nominal model
        '''
        self._kind = value
    #----------------------------------------------------
    def _get_ds_model(self, ds, nent_mm, nent_ee):
        if self._chan is not None:
            log.warning(f'Picking up model for channel: {self._chan}')
        else:
            log.info('Getting model for both channels')

        if   self._chan is None:
            pdf_mm = self._get_pdf(preffix=f'mm_{ds}', nent=nent_mm)
            pdf_ee = self._get_pdf(preffix=f'ee_{ds}', nent=nent_ee)
        elif self._chan == 'mm':
            pdf_mm = self._get_pdf(preffix=f'mm_{ds}', nent=nent_mm)
            pdf_ee = None
        elif self._chan == 'ee':
            pdf_mm = None
            pdf_ee = self._get_pdf(preffix=f'ee_{ds}', nent=nent_ee)
        else:
            log.error(f'Invalid channel: {self._chan}')
            raise

        return pdf_mm, pdf_ee
    #----------------------------------------------------
    def _cache_model(self):
        log.info('Caching models')
        d_nent = { dset : (nent_mm, nent_ee / self._rk) for dset, [nent_mm, nent_ee] in self._d_nent.items() }
        d_mod  = {}

        for dset, (nent_mm, nent_ee) in d_nent.items():
            mod_mm, mod_ee = self._get_ds_model(dset, nent_mm, nent_ee)
            d_mod[dset]    = mod_mm, mod_ee

        self._d_mod = d_mod
    #----------------------------------------------------
    def get_model(self):
        '''
        Returns
        -----------------
        d_ent (dict): Returns a dictionary: {name : tup} where
            name (str)  : model identifier, e.g. r1
            tup  (tuple): Tuple with muon and electron PDFs, e.g. pdf_mm, pdf_ee 
        '''

        self._initialize()

        return self._d_mod
    #----------------------------------------------------
    def _add_ext_constraints(self, d_par, d_var):
        if d_var is None:
            log.warning(f'Not adding errors for constrained parameters in prefit dictionary')
            return d_par

        d_par_new = {}
        for name, var in d_var.items():
            if name not in d_par:
                log.error(f'Cannot find {name} in prefit dictionary:')
                pprint.pprint(d_par.keys())
                raise

            val = d_par[name][0]
            err = math.sqrt(var)

            d_par_new[name] = [val, err]

        d_par.update(d_par_new)

        return d_par
    #----------------------------------------------------
    def _add_ck(self, d_par):
        regex='nsg_ee_([0-9a-z]+_.*)'
        d_par_ck = {}
        for var_name in d_par:
            mtch = re.match(regex, var_name)
            if not mtch:
                continue

            suffix = mtch.group(1)

            ee_yld_name = var_name
            mm_yld_name = var_name.replace('_ee_', '_mm_')

            ee_yld, _   = d_par[ee_yld_name]
            mm_yld, _   = d_par[mm_yld_name]

            d_par_ck[f'ck_{suffix}'] = [ (self._rk * ee_yld) / mm_yld, 0]

        d_par.update(d_par_ck)

        return d_par
    #----------------------------------------------------
    def _add_ck_constraints(self, d_par, ck_var):
        if ck_var is None:
            log.warning(f'Not adding errors for ck parameters in prefit dictionary')
            return d_par

        try:
            [ck_name] = [ name for name in d_par if name.startswith('ck_') ] 
        except:
            log.error('Expected one and only one CK parameter in:')
            pprint.pprint(d_par)
            raise

        [ck_val, _] = d_par[ck_name]
        ck_err      = math.sqrt(ck_var)

        d_par[ck_name] = [ck_val, ck_err]

        return d_par
    #----------------------------------------------------
    def get_prefit_pars(self, d_var=None, ck_var=None):
        '''
        Used to get model parameters used to make the toy data

        Parameters
        --------------------
        d_var (dict): Dictionary with variances for parameters that are constrained. If pased the
        constraint widths will be added as errors in the prefit dictionary

        ck_var (float): CK variance after combining different datasets 

        Returns 
        --------------------
        d_par (dict): Dictionary storing the prefit parameters (used to build the model) and their
        errors, e.g. {'par_x' : (3, 1)}
        '''
        self._initialize()

        d_model = self.get_model()

        d_par = {}
        for l_mod_mm, mod_ee in d_model.values():
            if l_mod_mm is not None:
                [ mod_bm_mm, mod_qm_mm ] = l_mod_mm
                d_par_bm_mm = { par.name : [ par.value().numpy(), 0] for par in mod_bm_mm.get_params() }
                d_par_qm_mm = { par.name : [ par.value().numpy(), 0] for par in mod_qm_mm.get_params() }
                d_par.update(d_par_bm_mm)
                d_par.update(d_par_qm_mm)

            if mod_ee is not None:
                d_par_ee = { par.name : [ par.value().numpy(), 0] for par in mod_ee.get_params() }
                d_par.update(d_par_ee)

        d_par['rk'] = [self._rk, 0]
        d_par       = self._add_ext_constraints(d_par, d_var)
        d_par       = self._add_ck(d_par)
        d_par       = self._add_ck_constraints(d_par, ck_var)

        return d_par
    #----------------------------------------------------
    def get_data(self, rseed=3):
        '''
        Returns toy data from model

        Parameters:
        -----------------
        rseed  (int):  Random seed

        Returns:
        -----------------
        d_data (dict): Dictionary with dataset and tuple of zfit data objects paired, i.e. {r1_TOS : (zdata_mm, zdata_ee) }

        For muon, TIS dataset is the TOS one.
        '''
        self._initialize()

        zfit.settings.set_seed(rseed)

        d_data     = {}
        zdat_tos_mm= None
        for ds, (pdf_mm, pdf_ee) in self._d_mod.items():
            zdat_mm = self._get_zdata(pdf_mm, ds, 'mm')
            zdat_ee = self._get_zdata(pdf_ee, ds, 'ee')

            if 'TIS' in ds:
                zdat_mm     = zdat_tos_mm 
            else:
                zdat_tos_mm = zdat_mm 

            d_data[ds] = zdat_mm, zdat_ee

        return d_data
    #----------------------------------------------------
    def _get_zdata(self, pdf, ds, chan):
        '''
        Will take either a PDF or a list of PDFs (muon channel), 
        Will return a zfit dataset or a list of zfit datasets.
        '''
        if pdf is None:
            return

        if isinstance(pdf, list):
            l_mod = pdf
        else:
            l_mod = [pdf]

        l_zdat = []
        for mod in l_mod:
            dst  = mod.create_sampler()
            arr  = dst.value().numpy().flatten()
            zdat = zfit.Data.from_numpy(mod.space, array=arr)
            l_zdat.append(zdat)

        if not isinstance(pdf, list):
            return l_zdat[0]

        return l_zdat
    #----------------------------------------------------
    @staticmethod
    def show(d_mod):
        s_dset = { key.split('_')[0] for key in d_mod }
        for dset in s_dset:
            pdf_mm_tos, pdf_ee_tos = d_mod[f'{dset}_TOS']
            pdf_mm_tis, pdf_ee_tis = d_mod[f'{dset}_TIS']

            l_par_name_mm_tos = ', '.join([ par.name for par in pdf_mm_tos.get_params() ])
            l_par_name_mm_tis = ', '.join([ par.name for par in pdf_mm_tis.get_params() ])
            l_par_name_ee_tos = ', '.join([ par.name for par in pdf_ee_tos.get_params() ])
            l_par_name_ee_tis = ', '.join([ par.name for par in pdf_ee_tis.get_params() ])

            log.info('')
            log.info(f'{dset}')
            log.info('-' * 20)
            log.info(f'{"mm TOS":<10}{l_par_name_mm_tos:<60}')
            log.info(f'{"mm TIS":<10}{l_par_name_mm_tis:<60}')
            log.info(f'{"ee TOS":<10}{l_par_name_ee_tos:<60}')
            log.info(f'{"ee TIS":<10}{l_par_name_ee_tis:<60}')
            log.info('-' * 20)
    #----------------------------------------------------
    @staticmethod
    def get_cov(kind='diag_eq', c = 0.01):
        if   kind == 'diag_eq':
            mat = numpy.diag([c] * 8)
        elif kind == 'random':
            mat = numpy.random.rand(8, 8)
            numpy.fill_diagonal(mat, 1)
            mat = mat * c
        else:
            log.error(f'Invalid kind: {kind}')
            raise
    
        return mat 
    #----------------------------------------------------
    @staticmethod
    def get_rjpsi(kind='one'):
        d_rjpsi = {}
    
        if   kind == 'one':
            d_rjpsi['d1'] = 1 
            d_rjpsi['d2'] = 1 
            d_rjpsi['d3'] = 1 
            d_rjpsi['d4'] = 1 
        elif kind == 'eff_bias':
            d_rjpsi['d1'] = 0.83333333 
            d_rjpsi['d2'] = 0.83333333 
            d_rjpsi['d3'] = 0.83333333 
            d_rjpsi['d4'] = 0.83333333 
        else:
            log.error(f'Wrong kind: {kind}')
            raise
    
        return d_rjpsi
    #----------------------------------------------------
    @staticmethod
    def get_eff(kind='equal'):
        d_eff = {}
        if   kind == 'diff':
            d_eff['d1'] = (0.6, 0.3)
            d_eff['d2'] = (0.5, 0.2)
            d_eff['d3'] = (0.7, 0.3)
            d_eff['d4'] = (0.8, 0.4)
        elif kind == 'half':
            d_eff['d1'] = (0.6, 0.3)
            d_eff['d2'] = (0.6, 0.3)
            d_eff['d3'] = (0.6, 0.3)
            d_eff['d4'] = (0.6, 0.3)
        elif kind == 'equal':
            d_eff['d1'] = (0.3, 0.3)
            d_eff['d2'] = (0.3, 0.3)
            d_eff['d3'] = (0.3, 0.3)
            d_eff['d4'] = (0.3, 0.3)
        elif kind == 'bias':
            d_eff['d1'] = (0.6, 0.25)
            d_eff['d2'] = (0.6, 0.25)
            d_eff['d3'] = (0.6, 0.25)
            d_eff['d4'] = (0.6, 0.25)
        else:
            log.error(f'Invalid kind: {kind}')
            raise
    
        return d_eff
#----------------------------------------------------

