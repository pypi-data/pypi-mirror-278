import random
import glob
import os

from importlib.resources import files
from log_store           import log_store
from read_selection      import read_selection


log = log_store.add_logger('rx_selection:finder')
#---------------------------
class finder:
    '''
    Class needed to find latest version of selection compatible with given selection
    dictionary
    '''
    #---------------------------
    def __init__(self, trig, q2bin, year):
        self._trig = trig
        self._q2bin= q2bin 
        self._year = year 
    #---------------------------
    def _replace_cut(self, cut):
        if   cut in ['ETOS', 'HTOS', 'GTIS']:
            return cut.lower()
        elif cut == 'MTOS':
            return 'L0'
        else:
            return cut
    #---------------------------
    def _check(self, sel_path, d_cut):
        for cut, sto in d_cut.items():
            cut         = self._replace_cut(cut)
            rs          = read_selection(cut, self._trig, q2bin=self._q2bin, year=self._year)
            rs.sel_path = sel_path
            rea         = rs.get()

            if sto != rea:
                log.debug(f'Fail at {cut} for: {sel_path}')
                log.debug(f'Passed: {sto}')
                log.debug(f'Read  : {rea}')
                log.debug('')
                return 0

        return 1
    #---------------------------
    def _get_sel_path(self):
        path_wc = files('selection_data').joinpath('selection_v*.json')
        path_wc = str(path_wc)

        l_path  = glob.glob(path_wc)
        l_path.sort()

        if len(l_path) == 0:
            log.error(f'Found no path in {path_wc}')
            raise

        return l_path
    #---------------------------
    def get_version(self, d_cut):
        l_sel_path = self._get_sel_path()

        l_pat_flg = [ [sel_path, self._check(sel_path, d_cut)] for sel_path in l_sel_path ] 

        val           = next((pat_flg for pat_flg in reversed(l_pat_flg) if pat_flg[1] == 1), None)
        if val is None:
            log.warning(f'No version found with cuts passed')
            return 'not_found'
        else:
            [sel_path, _] = val

        file_name = os.path.basename(sel_path)
        vers      = file_name.replace('selection_', '').replace('.json', '')

        return vers
#---------------------------

