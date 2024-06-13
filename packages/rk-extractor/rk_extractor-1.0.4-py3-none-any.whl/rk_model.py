import re
import os
import zfit
import numpy
import pprint
import extset
import zutils.utils      as zut
import utils_noroot      as utnr
import hqm.model         as hqm_model
import matplotlib.pyplot as plt
import read_selection    as rs

from log_store             import log_store
from importlib.resources   import files
from rkex_model            import model
from version_management    import get_last_version
from zutils.utils          import zfsp_1d_input
from phsp_cmb.phsp_cmb     import cmb_pdf                  as phsp_cmb_pdf
from zutils.plot           import plot                     as zfp
from zutils.utils          import split_fit                as zfsp
from scales                import scales                   as scl
from stats.average         import average                  as stav
from misID_tools.zmodel    import misID_real_model_builder as msid
from hqm.model.double_swap import dswp_bmass               as dswpb
from builder               import builder                  as cb_builder

log = log_store.add_logger(name='rk_extractor:rk_model')
#---------------------------------------------------------------
class rk_model(model):
    def __init__(self, **kwargs):
        self._d_val      = {} 
        self._d_var      = {} 
        self._d_plt_set  = {} 

        self._obs        = None
        self._nsig_ee    = None
        self._nsig_mm    = None
        self._read_yields= True

        super().__init__(**kwargs)
    #---------------------------------------------------------------
    @property
    def plt_set(self):
        return self._d_plt_set

    @plt_set.setter
    def plt_set(self, value):
        self._d_plt_set = value
    #---------------------------------------------------------------
    @property
    def read_yields(self):
        return self._read_yields

    @read_yields.setter
    def read_yields(self, value):
        '''
        If true, will try to read yields from JSON files. This is needed to make toys
        not for actual fit to data
        '''
        self._read_yields= value
    #---------------------------------------------------------------
    def _preffix_to_info(self, preffix):
        regex = '(ee|mm)_(r1|r2p1|2017|2018|all)'
        mtch  = re.match(regex, preffix)
        try:
            [chan, dset] = mtch.groups()
        except:
            log.error(f'Cannot extract dataset and trigger from: {preffix}')
            raise

        trig = {'ee' : 'ETOS', 'mm' : 'MTOS'}[chan]

        return dset, trig
    #---------------------------------------------------------------
    def _add_constraints(self, d_cns):
        d_val = { name : cns[0]    for name, cns in d_cns.items() }
        d_var = { name : cns[1]**2 for name, cns in d_cns.items() }

        self._d_val.update(d_val)
        self._d_var.update(d_var)
    #---------------------------------------------------------------
    def _get_ph_combinatorial(self, preffix):
        _, trig = self._preffix_to_info(preffix) 
        qsq_cut = rs.get('q2', trig, q2bin='high', year='2018')
        regex   = '\(Jpsi_M \* Jpsi_M > (15500000.0)\) && \(Jpsi_M \* Jpsi_M < 22000000\.0\)'
        mtch    = re.match(regex, qsq_cut)
        if not mtch:
            log.error(f'Cannot extract minimum q2 from {qsq_cut} with {regex}')
            raise

        qmin = mtch.group(1)
        qmin = float(qmin)
        qmin = qmin / 1e6

        lam=zfit.param.Parameter(f'lam_{preffix}', 2, 1, 3)
        qmi=zfit.param.ConstantParameter(f'qmi_{preffix}', qmin)
        pdf=phsp_cmb_pdf(lam, qmi, self._obs)

        return pdf
    #---------------------------------------------------------------
    def _get_su_combinatorial(self, preffix):
        log.info(f'Getting combinatorial PDF for {preffix}')
        dset, trig    = self._preffix_to_info(preffix) 
        obj           = cb_builder(dset=dset, trigger=trig, version=self._comb_vers) 
        obj.kind      = self._kind 
        log.warning(f'Not using OS-SS correction, just SS to get combinatorial')
        cmb           = obj.get_pdf(obs=self._obs, preffix=f'cb_{preffix}', name='Combinatorial') 

        if 'sb_fits' not in preffix:
            log.warning('Fixing combinatorial shape, not using constraints')
            zut.fix_shape(cmb)
        else:
            log.debug('Not fixing shape of combinatorial')

        return cmb 
    #---------------------------------------------------------------
    def _get_combinatorial(self, preffix, fix_norm=False):
        dset, trig = self._preffix_to_info(preffix) 
        #pdf        = self._get_ph_combinatorial(preffix)
        pdf        = self._get_su_combinatorial(preffix)
        nent       = self._get_entries(nsig=None, kind='cmb', trigger=trig, year=dset)
        ncb        = zfit.Parameter(f'ncb_{preffix}', nent, 0, 100000)
        ncb.floating = not fix_norm 
        pdf.set_yield(ncb)

        return pdf
    #---------------------------------------------------------------
    def _get_rare_scale(self, year, trigger, kind):
        l_all_year = ['2011', '2012', '2015', '2016', '2017', '2018']

        if   year in l_all_year:
            obj      = scl(dset=year, trig=trigger, kind=kind)
            val, err = obj_1.get_scale()

            return val, err
        elif year == 'r1':
            l_year = ['2011', '2012']
        elif year == 'r2p1':
            l_year = ['2015', '2016']
        elif year == 'all':
            l_year = l_all_year 
        else:
            log.error(f'Invalid year: {year}')
            raise

        l_val = []
        l_err = []
        for dset in l_year: 
            obj      = scl(dset=dset, trig=trigger, kind=kind)
            val, err = obj.get_scale()
            l_val.append(val)
            l_err.append(err)

        arr_val     = numpy.array(l_val)
        arr_err     = numpy.array(l_err)
        val, err, _ = stav(arr_val, arr_err)

        return val, err
    #---------------------------------------------------------------
    def _get_entries_from_json(self, kind=None, trig=None, year=None):
        if not self._read_yields:
            log.warning(f'Not reading yields from JSON for {kind}/{trig}/{year}, using zero events')
            return 0

        json_dir  = files('extractor_data').joinpath(f'sb_fits')
        vers      = get_last_version(dir_path=json_dir, version_only=True)
        json_path = f'{json_dir}/{vers}/{year}_{trig}.json'
        if not os.path.isfile(json_path):
            log.error(f'Cannot find: {json_path}')
            raise FileNotFoundError

        d_par = utnr.load_json(json_path)
        for key, [val, _] in d_par.items():
            flg_1 = key.startswith('ncb_') and kind == 'cmb'
            flg_2 = key.startswith('npr_') and kind == 'prc'
            flg_3 = key == 'ncnd_ctrl_sp'  and kind == 'dswp'
            if flg_1 or flg_2 or flg_3:
                return val

        log.error(f'Cannot find yield for {kind} among:')
        pprint.pprint(d_par)
        raise
    #---------------------------------------------------------------
    def _get_entries(self, nsig=None, kind=None, trigger=None, year=None):
        if   kind in ['prc', 'cmb', 'dswp']:
            nent  = self._get_entries_from_json(kind=kind, trig=trigger, year=year)

            log.debug(f'For {trigger}/{year}, taking {kind} yield from JSON as: {nent:.0f}')
        elif kind in ['bpks', 'bdks', 'bsph', 'bpk1', 'bpk2']:
            scale = self._get_rare_scale(year, trigger, kind)
            scl   = scale[0]
            nent  = nsig * scl

            log.debug(f'For {trigger}/{year}, taking {kind} yield as {nent:.0f}={scl:.3f} * {nsig:.0f}')
        else:
            log.error(f'Invalid kind: {kind}')
            raise

        return nent
    #---------------------------------------------------------------
    def _get_systematic(self, trig, kind):
        if trig not in ['ETOS', 'MTOS']:
            log.error(f'Cannot pick up systematic for trigger {trig}')
            raise

        prefix = f'{kind}_{trig}:'
        if self._kind.startswith(prefix):
            syst = self._kind.replace(prefix, '')
            log.info(f'Using {syst} systematic for {kind}/{trig}')
        else:
            syst = 'nom'

        if   syst.startswith('sys') or syst == 'nom':
            return syst
        elif syst.startswith('bts'):
            [bts_index] = re.match(r'bts(\d+)', syst).groups()
            return int(bts_index)
        else:
            log.error(f'Invalid systematic: {syst}')
            raise
    #---------------------------------------------------------------
    def _get_signal(self, preffix, nent=None):
        log.info(f'Getting signal PDF for {preffix}')
        year, trig = self._preffix_to_info(preffix)
        log.warning(f'Using 2018 signal for {year}')
        year = '2018'

        syst       = self._get_systematic(trig, 'sig')
        sig, d_cns = hqm_model.get_signal_shape(dataset=year, trigger=trig, parameter_name_prefix=preffix, systematic=syst)

        self._add_constraints(d_cns)

        nsg    = zfit.Parameter(f'nsg_{preffix}', nent, 0, 100000)
        esig   = sig.create_extended(nsg, name=extset.sig_name)

        if   preffix.startswith('ee_'):
            self._nsig_ee = nsg 
        elif preffix.startswith('mm_'):
            self._nsig_mm = nsg 
        else:
            log.error(f'Invalid preffix: {preffix}')
            raise ValueError

        self._obs = esig.space

        return esig
    #---------------------------------------------------------------
    def _get_rare_kind(self, kind, year, trig):
        log.info(f'Getting rare PDF for {kind}/{year}/{trig}')

        syst       = self._get_systematic(trig, 'rpr')
        syst       = 0 if syst == 'nom' else syst
        if   kind == 'bpks':
            pdf = hqm_model.get_Bu2Ksee_shape(dataset= year, trigger=trig, bts_index=syst)
        elif kind == 'bdks':
            pdf = hqm_model.get_Bd2Ksee_shape(dataset= year, trigger=trig, bts_index=syst)
        elif kind == 'bsph':
            pdf = hqm_model.get_Bs2phiee_shape(dataset=year, trigger=trig, bts_index=syst)
        elif kind == 'bpk1':
            pdf = hqm_model.get_Bu2K1ee_shape(dataset= year, trigger=trig, bts_index=syst)
        elif kind == 'bpk2':
            pdf = hqm_model.get_Bu2K2ee_shape(dataset= year, trigger=trig, bts_index=syst)
        else:
            log.error(f'Invalid kind: {kind}')
            raise ValueError

        return pdf
    #---------------------------------------------------------------
    def _get_rare(self, preffix, nent=None, kind=None):
        year, trig = self._preffix_to_info(preffix)

        if year == 'all':
            d_pdf = { dset : self._get_rare_kind(kind, dset, trig) for dset in self._l_dset }
            pdf   = self._merge_year_pdf(d_pdf, preffix, kind)
        else:
            pdf   = self._get_rare_kind(kind, year, trig) 

        svl, ser = self._get_rare_scale(year, trig, kind)
        nbkg     = zfit.ComposedParameter(f'nr{kind}_{preffix}', lambda ns : ns * svl, params=[self._nsig_ee])
        pdf.set_yield(nbkg)

        self._d_rare_scl[f'{year}_{trig}_{kind}'] = [svl, ser]

        return pdf 
    #---------------------------------------------------------------
    def _merge_year_pdf(self, d_pdf, preffix, kind):
        l_dset  = list(d_pdf.keys())
        l_lumi  = [ self._d_lumi[dset] for dset in l_dset ]
        tot_lum = sum(l_lumi)
        d_frac  = { dset : lumi / tot_lum for dset, lumi in zip(l_dset, l_lumi) }

        l_lfr_par = []
        for dset in d_pdf:
            frac= d_frac[dset]
            lfr = zfit.Parameter(f'lfr_{dset}_{preffix}_{kind}', frac , 0., 1.)
            lfr.floating = False
            l_lfr_par.append(lfr)

        l_lfr_par = l_lfr_par[:-1]
        l_pdf     = [ pdf for pdf in d_pdf.values()]
        pdf       = zfit.pdf.SumPDF(l_pdf, fracs=l_lfr_par, name=kind)

        return pdf
    #---------------------------------------------------------------
    def _get_prec_dset(self, dset=None, trig=None, pref=None):
        syst = self._get_systematic(trig, 'cpr')

        if   isinstance(syst, str):
            pdf, d_cns = hqm_model.get_part_reco(dataset=dset, trigger=trig, parameter_name_prefix=pref, systematic=syst)
        elif isinstance(syst, int):
            pdf, d_cns = hqm_model.get_part_reco(dataset=dset, trigger=trig, parameter_name_prefix=pref, bts_index =syst)
        else:
            log.error(f'Invalid systematic: {syst}')
            raise

        self._add_constraints(d_cns)

        return pdf
    #---------------------------------------------------------------
    def _get_prec(self, preffix):
        log.info(f'Getting cc PRec: {preffix}')

        year, trig = self._preffix_to_info(preffix)

        if year == 'all':
            d_pdf = { dset : self._get_prec_dset(dset=dset, trig=trig, pref=preffix) for dset in self._l_dset }
            pdf   = self._merge_year_pdf(d_pdf, preffix, 'prc')
        else:
            pdf = self._get_prec_dset(dataset=year, trig=trig, pref=preffix)

        nent= self._get_entries(nsig=None, kind='prc', trigger=trig, year=year)
        npr = zfit.Parameter(f'npr_{preffix}', nent, 0, 100000)
        pdf.set_yield(npr)

        return pdf 
    #---------------------------------------------------------------
    def _get_msid(self, preffix):
        log.info(f'Getting mis-ID for: {preffix}')
        dset, trig    = self._preffix_to_info(preffix)

        dset = 'all_int' if dset == 'all' else dset

        bld= msid(name='Mis-ID', version=self._msid_vers, obs=self._obs, preffix=preffix)
        bld.load_model(dset, trig)
        pdf=bld.build_model() 

        return pdf
    #---------------------------------------------------------------
    def _get_scales(self, sig_pdf):
        s_par = sig_pdf.get_params()
        try:
            [scl] = [ par for par in s_par if 'dmu' in par.name ]
            [res] = [ par for par in s_par if 'ssg' in par.name ]
        except:
            log.error(f'Cannot extract resolution and scale from:')
            log.info(s_par)
            raise

        return scl, res
    #---------------------------------------------------------------
    def _get_pdf(self, preffix='', nent=None):
        preffix = f'{preffix}_{self._preffix}'
        log.info(f'Getting real PDF for: {preffix}')

        year, trig   = self._preffix_to_info(preffix)

        #bm = B mass, for electron fits only.
        #sp = Double swaps, added observable and PDFs to muon fits

        #bm PDFs are extended, sp ones are not
        d_pdf            = dict() 
        d_pdf['esig_bm'] = self._get_signal(preffix, nent=nent)
        d_pdf['ecmb_bm'] = self._get_combinatorial(preffix, fix_norm=False)
        if   preffix.startswith('ee_'):
            d_pdf['erbp_bm']  = self._get_rare(preffix, nent=nent, kind='bpks')
            d_pdf['erbd_bm']  = self._get_rare(preffix, nent=nent, kind='bdks')
            d_pdf['erbs_bm']  = self._get_rare(preffix, nent=nent, kind='bsph')
            #d_pdf['erb1_bm']  = self._get_rare(preffix, nent=nent, kind='bpk1')
            #d_pdf['erb2_bm']  = self._get_rare(preffix, nent=nent, kind='bpk2')
            d_pdf['eprc_bm']  = self._get_prec(preffix)
            d_pdf['emis_bm']  = self._get_msid(preffix)
        elif preffix.startswith('mm_'):
            osg_sp = dswpb(self._obs, self._obs_mm_sp, proc='sign', name='sign_sp')
            ocm_sp = dswpb(self._obs, self._obs_mm_sp, proc='cmb' , name= 'cmb_sp')

            oct_sp                = dswpb(self._obs, self._obs_mm_sp, proc='ctrl', name='ctrl_sp')
            sig                   = d_pdf['esig_bm']
            scl, res              = self._get_scales(sig)

            oct_sp.mass_scale     = scl
            oct_sp.mass_resolution= res 

            pdf_sig_bm = d_pdf['esig_bm']
            pdf_cmb_bm = d_pdf['ecmb_bm']

            pdf_ctr_bm, pdf_ctr_sp = oct_sp.get_pdf(extended=True)
            _         , pdf_sig_sp = osg_sp.get_pdf(extended=True)
            _         , pdf_cmb_sp = ocm_sp.get_pdf(extended=True)

            self._set_dswp_yield(pdf_ctr_sp, year)

            d_pdf['ectr_bm'] = pdf_ctr_bm
            d_pdf['esig_sp'] = pdf_sig_sp
            d_pdf['ectr_sp'] = pdf_ctr_sp
        else:
            log.error(f'Preffix does not start with mm_ or ee_: {preffix}')
            raise

        pdf = self._build_pdf(d_pdf, preffix)

        return pdf
    #---------------------------------------------------------------
    def _set_dswp_yield(self, pdf, year):
        nent = self._get_entries(nsig=None, kind='dswp', trigger='MTOS', year=year)
        ndsp = pdf.get_yield()
        ndsp.set_value(nent)
    #---------------------------------------------------------------
    def _build_pdf(self, d_pdf, preffix):
        if   preffix.startswith('mm_'):
            pdf = self._build_pdf_mm(d_pdf)
        elif preffix.startswith('ee_'):
            pdf = self._build_pdf_ee(d_pdf)
        else:
            log.error(f'Invalid preffix: {preffix}')
            raise

        return pdf 
    #---------------------------------------------------------------
    def _send_cmb_to_start(self, d_normal):
        val = d_normal['ecmb']

        del(d_normal['ecmb'])

        d_tmp = {'ecmb' : val}

        d_tmp.update(d_normal)

        return d_tmp
    #---------------------------------------------------------------
    def _order_pdfs(self, d_pdf):
        pdf_sig = d_pdf['esig_bm']
        pdf_cmb = d_pdf['ecmb_bm']
        pdf_ctr = d_pdf['ectr_bm']

        d_pdf_ord = dict()
        d_pdf_ord['ecmb_bm'] = pdf_cmb
        d_pdf_ord['ectr_bm'] = pdf_ctr
        d_pdf_ord['esig_bm'] = pdf_sig

        return d_pdf_ord
    #---------------------------------------------------------------
    def _build_pdf_mm(self, d_pdf):
        d_pdf_bm = { key : pdf for key, pdf in d_pdf.items() if key.endswith('_bm') }
        d_pdf_sp = { key : pdf for key, pdf in d_pdf.items() if key.endswith('_sp') }

        d_pdf_bm = self._order_pdfs(d_pdf_bm)

        l_pdf_bm = [ pdf for key, pdf in d_pdf_bm.items() ]
        l_pdf_sp = [ pdf for key, pdf in d_pdf_sp.items() ]

        pdf_bm   = zfit.pdf.SumPDF(l_pdf_bm, name='bms_pdf')
        pdf_sp   = zfit.pdf.SumPDF(l_pdf_sp, name='swp_pdf')

        return [pdf_bm, pdf_sp]
    #---------------------------------------------------------------
    def _build_pdf_ee(self, d_pdf):
        l_pdf=[]
        l_pdf.append(d_pdf['ecmb_bm'])
        l_pdf.append(d_pdf['eprc_bm'])

        l_pdf.append(d_pdf['erbp_bm'])
        l_pdf.append(d_pdf['erbd_bm'])
        l_pdf.append(d_pdf['erbs_bm'])
        #l_pdf.append(d_pdf['erb1_bm'])
        #l_pdf.append(d_pdf['erb2_bm'])
        l_pdf.append(d_pdf['emis_bm'])
        l_pdf.append(d_pdf['esig_bm'])

        pdf = zfit.pdf.SumPDF(l_pdf)

        return pdf
    #---------------------------------------------------------------
    def _get_pdf_names(self):
        d_leg = {}
        d_leg['prc' ] = r'$c\bar{c}_{prc}+\psi(2S)K^+$'
        d_leg['bpks'] = r'$B^+\to K^{*+}e^+e^-$'
        d_leg['bdks'] = r'$B^0\to K^{*0}e^+e^-$'
        d_leg['bsph'] = r'$B_s\to \phi e^+e^-$'
        d_leg['bpk1'] = r'$B^+\to K_{1}e^+e^-$'
        d_leg['bpk2'] = r'$B^+\to K_{2}e^+e^-$'

        return d_leg
    #---------------------------------------------------------------
    def _get_plt_set(self, ext_txt=None):
        d_plt_set               = {}
        d_plt_set['nbins']      = self._nbin
        d_plt_set['d_leg']      = self._get_pdf_names()
        d_plt_set['ext_text']   = ext_txt 
        d_plt_set['stacked']    = True
        d_plt_set['skip_pulls'] = False
        d_plt_set.update(self._d_plt_set)

        if 'ymax'  in self._d_plt_set:
            [mm_max, ee_max] = self._d_plt_set['ymax']
            ymax = mm_max if ext_txt.endswith('_mm') else ee_max
            d_plt_set['ymax'] = ymax

        return d_plt_set
    #---------------------------------------------------------------
    def _plot_model(self, key, mod):
        log.warning(f'Wont plot model, too time consumming')
        return
        if (self._out_dir is None) or (mod is None):
            return

        #In the case of the muon
        #There are two models
        #one for the B mass and other for
        #the dimuon mass
        log.info(f'Plotting: {key}')
        if isinstance(mod, list):
            l_mod = mod
            l_nam = ['bm', 'mm']
        else:
            l_mod = [mod]
            l_nam = ['bm']

        for pdf, nam in zip(l_mod, l_nam): 
            sam = pdf.create_sampler()
            self._plot_1d_model(key, pdf, sam, nam)
    #---------------------------------------------------------------
    def _plot_1d_model(self, key, mod, dat, nam):
        obj= zfp(data=dat, model=mod)
        d_plt_set = self._get_plt_set(ext_txt=key)
        obj.plot(**d_plt_set)

        log.info(f'Saving to: {self._mod_dir}/{key}_{nam}.png')
        plt.savefig(f'{self._mod_dir}/{key}_{nam}.png')
        plt.close('all')
    #---------------------------------------------------------------
    def _print_model(self, key, mod):
        if (self._mod_dir is None) or (mod is None):
            return

        d_const = {}
        for name in self._d_val:
            val = self._d_val[name]
            var = self._d_var[name]
            d_const[name] = [val, var]

        log.info(f'Saving to: {self._mod_dir}/{key}.txt')

        if isinstance(mod, list):
            l_mod = mod
            l_nam = ['bm', 'qm']
        else:
            l_mod = [mod]
            l_nam = ['bm']

        for pdf, nam in zip(l_mod, l_nam):
            zut.print_pdf(pdf, d_const=d_const, txt_path=f'{self._mod_dir}/{key}_{nam}.txt')
    #---------------------------------------------------------------
    def get_cons(self):
        '''
        Will return constraints on model parameters 

        Returns
        -----------
        d_val, d_var: Tuple of dictionaries pairing parameter name with value (mu of Gaussian) and 
        variance respectively.
        '''
        self._initialize()

        log.debug('-' * 20)
        log.debug(f'{"Name":<60}{"Value":<15}{"Variance":<15}')
        log.debug('-' * 20)
        for name in self._d_val:
            val = self._d_val[name]
            var = self._d_var[name]

            log.debug(f'{name:<60}{val:<15.3f}{var:<15.3f}')
        log.debug('-' * 20)

        return self._d_val, self._d_var
#---------------------------------------------------------------

