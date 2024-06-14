import os
import numpy
import pandas       as pnd
import utils_noroot as utnr

from version_management  import get_last_version 
from importlib.resources import files
from ndict               import ndict
from rk.eff_yld_loader   import eff_yld_loader as eyl
from log_store           import log_store

log = log_store.add_logger('rk_extractor:np_reader')
#----------------------------------------
class np_reader:
    '''
    Class used to read nuisance parameters to calculate RK
    '''
    #------------------------
    def __init__(self, sys=None, sta=None, yld=None):
        '''
        sys (str): Version of efficiencies obtained when assessing systematics
        sta (str): Version of efficiencies obtained when assessing statistical uncertainties with bootstrapping
        yld (str): Version of fitted data yields (only Jpsi and Psi2S)
        '''
        self._sys         = sys 
        self._sta         = sta
        self._yld         = yld

        self._cov_dir     = None
        self._df_yld      = None 
        self._df_eff      = None 

        self._sys_flg     = 'pall_tall_gall_lall_hall_rall_qall_iall_snom'
        self._sta_flg     = 'pnom_tnom_gnom_lnom_hnom_rnom_qnom_inom_sall'
        self._nom_flg     = 'pnom_tnom_gnom_lnom_hnom_rnom_qnom_inom_snom'

        self._l_ds_lab    = ['r1_TOS', 'r1_TIS', 'r2p1_TOS', 'r2p1_TIS', '2017_TOS', '2017_TIS', '2018_TOS', '2018_TIS']
        self._l_dset      = ['r1', 'r2p1', '2017', '2018']
        self._l_trig      = ['MTOS', 'ETOS']
        self._l_proc      = ['sign', 'ctrl']

        self._will_cache  = False
        self._initialized = False 
    #------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._setup_paths()
        self._load_eff_yld()
        self._load_uncertainties()
        self._cache()

        self._initialized = True
    #------------------------
    def _setup_paths(self):
        cache_dir = files('extractor_data').joinpath(f'npr_data/{self._sys}_{self._sta}_{self._yld}')
        os.makedirs(cache_dir, exist_ok=True)

        self._eff_path = f'{cache_dir}/eff.json'
        self._yld_path = f'{cache_dir}/yld.json'
        self._sys_path = f'{cache_dir}/sys.json'
        self._sta_path = f'{cache_dir}/sta.json'
    #------------------------
    def _find_cached(self, path):
        if not os.path.isfile(path):
            log.debug(f'File not cached: {path}')
            return False 

        log.debug(f'File cached: {path}')

        return True
    #------------------------
    def _load_eff_yld(self):
        '''
        For a given channel, ee or mm, it will fill the dictionary of efficiencies for each
        dataset and trigger.
        '''
        is_eyl = self._find_cached(self._eff_path) and self._find_cached(self._yld_path) 
        if is_eyl:
            log.info(f'Cached data found')
            self._df_eff = pnd.read_json(self._eff_path)
            self._df_yld = pnd.read_json(self._yld_path)

            return

        self._will_cache = True
        log.info(f'Cached efficiencies and yields not found, caching')

        d_eff   = self._get_dset_dict()
        d_yld   = self._get_dset_dict()
        l_index = []
        for proc in self._l_proc: 
            for trig in self._l_trig:
                channel      = 'mm' if trig == 'MTOS' else 'ee'

                eff_1, yld_1 = self._get_eff_yld(f'{proc}_{channel}', 'r1'  , trig)
                eff_2, yld_2 = self._get_eff_yld(f'{proc}_{channel}', 'r2p1', trig)
                eff_3, yld_3 = self._get_eff_yld(f'{proc}_{channel}', '2017', trig)
                eff_4, yld_4 = self._get_eff_yld(f'{proc}_{channel}', '2018', trig)

                d_eff['r1'  ].append(eff_1)
                d_eff['r2p1'].append(eff_2)
                d_eff['2017'].append(eff_3)
                d_eff['2018'].append(eff_4)

                d_yld['r1'  ].append(yld_1)
                d_yld['r2p1'].append(yld_2)
                d_yld['2017'].append(yld_3)
                d_yld['2018'].append(yld_4)

                l_index.append(f'{proc}_{trig}')

        self._df_eff = pnd.DataFrame(d_eff, index=l_index).T
        self._df_yld = pnd.DataFrame(d_yld, index=l_index).T
    #------------------------
    def _load_uncertainties(self):
        is_cov = self._find_cached(self._sys_path) and self._find_cached(self._sta_path)
        if is_cov: 
            log.info(f'Cached covariances found, loading them')
            self._cvsys = utnr.load_json(self._sys_path)
            self._cvsta = utnr.load_json(self._sta_path)
            return

        self._will_cache = True
        eff_dir          = os.environ['EFFDIR']
        self._cov_dir    = f'{eff_dir}/../covariance'

        self._cvsys = self._get_cov(kind='sys')
        log.warning(f'Statistical uncertainy covariance was taken from v65')
        self._cvsta = self._get_cov(kind='sta')
    #------------------------
    def _cache(self):
        if not self._will_cache:
            log.debug('Data was not updated, skipping caching')
            return

        log.info(f'Data was updated, caching:')

        self._df_eff.to_json(self._eff_path, indent=4)
        self._df_yld.to_json(self._yld_path, indent=4)

        utnr.dump_json(self._cvsys, self._sys_path)
        utnr.dump_json(self._cvsta, self._sta_path)
    #------------------------
    def _get_dset_dict(self):
        d_data         = dict()
        d_data['r1'  ] = []
        d_data['r2p1'] = []
        d_data['2017'] = []
        d_data['2018'] = []

        return d_data
    #------------------------
    def _get_eff_yld(self, proc, year, trig):
        '''
        Will return numerical value of efficiency and fitted yield, for a specifi process
        in a year and trigger
        '''
        obj          = eyl(proc, trig, year, self._nom_flg)
        obj.eff_var  = 'B_PT'
        t_yld, d_eff = obj.get_values(eff_version = self._sta, yld_version=self._yld)

        ctf  = d_eff['nom', 'B_PT']
        deff = ctf.efficiency
        oeff = deff.efficiency()
        eff  = oeff.val[0]
        yld  = t_yld[0]

        return eff, yld
    #------------------------
    def _get_cov(self, kind=None):
        if kind not in ['sys', 'sta']:
            log.error(f'Invalid uncertainty: {kind}')
            raise ValueError

        eff_ver  = self._sys if kind == 'sys' else self._sta
        pkl_path = f'{self._cov_dir}/{eff_ver}_{self._yld}/rx/matrix_abs_rc/tot.pkl'
        log.info(f'Picking up covariance from: {pkl_path}')
        cov      = utnr.load_pickle(pkl_path)

        return cov.tolist()
    #------------------------
    def get_cov(self, kind=None):
        '''
        Will return covariance matrix (nxn numpy array)
        '''
        self._initialize()

        if kind not in ['sys', 'sta']:
            log.error(f'Invalid covariance kind: {kind}')
            raise ValueError

        cov_mat = self._cvsys if kind == 'sys' else self._cvsta

        return numpy.array(cov_mat)
    #------------------------
    def get_eff(self):
        '''
        Will return rare mode efficiencies

        d_eff (dict): Dictionary {ds : (eff_mm, eff_ee)} with efficiency objects
        '''
        self._initialize()

        l_eff_rare_mm = self._df_eff.sign_MTOS.to_numpy().tolist()
        l_eff_rare_ee = self._df_eff.sign_ETOS.to_numpy().tolist()

        d_eff = {}
        for ds_lab, eff_mm, eff_ee in zip(self._l_ds_lab, l_eff_rare_mm, l_eff_rare_ee):
            d_eff[ds_lab] = eff_mm, eff_ee

        return d_eff 
    #------------------------
    def get_byields(self):
        '''
        Will return dictionary with efficiency corrected yields {ds : yld}
        e.g. {'r1_TIS_ee': 40021323}
        '''
        self._initialize()

        df_yld = self._df_yld.divide(self._df_eff)
        df_yld = df_yld.drop(columns=['sign_MTOS', 'sign_ETOS'])

        return df_yld
    #------------------------
    def get_ryields(self):
        self._initialize()

        br_bpjp_jpmm = self._get_reso_br()
        br_rare      = self._get_rare_br()

        df_yld       = self.get_byields()
        df_yld       = df_yld.divide(br_bpjp_jpmm)

        #This is the number of B mesons, before any selection
        #it will be multiplied by rare BR and efficiencies, so it will be a signal dataframe
        df_yld = df_yld.rename(columns={'ctrl_MTOS' : 'sign_MTOS', 'ctrl_ETOS' : 'sign_ETOS'})
        df_yld = df_yld.multiply(br_rare)

        df_era = self._df_eff.drop(columns=['ctrl_MTOS', 'ctrl_ETOS'])
        df_yld = df_yld.multiply(df_era)

        return df_yld
    #------------------------
    def _get_sfdata(self):
        sf_dir = files('extractor_data').joinpath('rare_sf')
        vers   = get_last_version(dir_path=sf_dir, version_only=True) 
        sf_pat = f'{sf_dir}/{vers}/fr_bf.json'
        if not os.path.isfile(sf_pat):
            log.error(f'File not found: {sf_pat}')
            raise FileNotFoundError

        d_data = utnr.load_json(sf_pat)

        return d_data 
    #------------------------
    def _get_reso_br(self):
        d_data = self._get_sfdata()
        b1, _  = d_data['bf']['bpjk']
        b2, _  = d_data['bf']['jpmm']

        return b1 * b2
    #------------------------
    def _get_rare_br(self):
        d_data = self._get_sfdata()
        br, _  = d_data['bf']['bpkp']

        return br 
    #------------------------
    def get_rjpsi(self):
        '''
        Will return an array with rjpsi for every trigger and dataset 
        '''
        self._initialize()

        df_yld = self.get_byields()

        sr_rjpsi_tos = df_yld.ctrl_MTOS / df_yld.ctrl_ETOS

        df_rjpsi = pnd.DataFrame({'TOS' : sr_rjpsi_tos})

        return df_rjpsi 
#----------------------------------------

