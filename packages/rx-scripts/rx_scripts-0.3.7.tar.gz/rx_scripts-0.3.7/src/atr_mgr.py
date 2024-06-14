import utils_noroot as utnr
import pprint
import os

from log_store import log_store

#TODO:Skip attributes that start with Take< in a betterway
#------------------------
class mgr:
    log=log_store.add_logger('rx_scripts:atr_mgr')
    #------------------------
    def __init__(self, df):
        self.d_in_atr = {}
        
        self.__store_atr(df)
    #------------------------
    def __store_atr(self, df):
        self.d_in_atr = self.__get_atr(df)
    #------------------------
    def __get_atr(self, df):
        l_atr = dir(df)
        d_atr = {}
        for atr in l_atr:
            val = getattr(df, atr)
            d_atr[atr] = val

        return d_atr
    #------------------------
    def add_atr(self, df):
        d_ou_atr = self.__get_atr(df)

        key_in_atr = set(self.d_in_atr.keys())
        key_ou_atr = set(     d_ou_atr.keys())

        key_to_add = key_in_atr.difference(key_ou_atr)

        for key in key_to_add:
            val = self.d_in_atr[key]
            if key.startswith('Take<') and key.endswith('>'):
                continue

            self.log.info(f'Adding attribute {key}')
            setattr(df, key, val)

        return df
    #------------------------
    def to_json(self, json_path):
        json_dir = os.path.dirname(json_path)
        os.makedirs(json_dir, exist_ok=True)

        t_type   = (list, str, int, float)
        d_fl_atr = { key : val for key, val in self.d_in_atr.items() if isinstance(val, t_type) and isinstance(key, t_type) }

        utnr.dump_json(d_fl_atr, json_path)
#------------------------
class ldr:
    log=utnr.getLogger('ldr')
    #------------------------
    def __init__(self, rdf):
        self._rdf = rdf
    #------------------------
    def from_json(self, json_path):
        d_atr = utnr.load_json(json_path)

        for key, val in d_atr.items():
            self.log.info(f'Adding attribute: {key}')
            setattr(self._rdf, key, val)

        return self._rdf
#------------------------
