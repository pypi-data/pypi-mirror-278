from np_reader import np_reader as np_rdr
from log_store import log_store
import pprint
import os

log=log_store.add_logger('rk_extractor:test_npreader')
#-----------------------------
def test_simple():
    log.info('simple')
    rdr       = np_rdr(sys='v65', sta='v81', yld='v24')
    rdr.cache = True
    d_eff     = rdr.get_eff()
    cov_sys   = rdr.get_cov(kind='sys')
    cov_sta   = rdr.get_cov(kind='sta')
    df_rjpsi  = rdr.get_rjpsi()
    df_byld   = rdr.get_byields()
    df_ryld   = rdr.get_ryields()

    pprint.pprint(df_ryld , indent=4)
    pprint.pprint(df_rjpsi, indent=4)

    mtos = df_ryld.sign_MTOS.sum()
    etos = df_ryld.sign_ETOS.sum()

    print('MTOS', mtos)
    print('ETOS', etos)
#-----------------------------
def main():
    test_simple()
#-----------------------------
if __name__ == '__main__':
    main()

