import os
import pprint
import pandas as pnd

from log_store import log_store

log = log_store.add_logger('rx_scripts:tmva_log_reader')
#-----------------------------------
class reader:
    def __init__(self, log_path):
        self._log_path = log_path
        self._l_line   = None
    #-----------------------------------
    def _initialize(self):
        if not os.path.isfile(self._log_path):
            log.error(f'File not found: {self._log_path}')
            raise FileNotFoundError

        with open(self._log_path) as ifile:
            self._l_line = ifile.read().splitlines()
    #-----------------------------------
    def _read_info(self, substring, name):
        try:
            l_head   = [ line for line in self._l_line if substring in line ]
            [header] = l_head
        except:
            log.error(f'One header not found for \"{substring}\" in: {self._log_path}')
            log.error(f'Found:')
            pprin.pprint(l_head)
            raise

        ind_head   = self._l_line.index(header) + 1
        head       = self._l_line[ind_head]
        l_tail_line= self._l_line[ind_head+1:]
        ind_tail   = l_tail_line.index(head)

        d_data = {'Variable' : [], name : []}
        for i_line in range(ind_head + 1, ind_head + ind_tail + 1):
            line = self._l_line[i_line]
            l_pt = line.split(':')

            var  = l_pt[2]
            var  = var.replace('_', ' ')
            val  = l_pt[3]

            d_data['Variable'].append(var)
            d_data[name      ].append(val)

        return pnd.DataFrame(d_data)
    #-----------------------------------
    def get_table(self, kind=None):
        self._initialize()

        if   kind == 'importance':
            df = self._read_info('Variable Importance', 'Importance')
            return df
        elif kind == 'separation':
            df = self._read_info(': Separation'       , 'Separation')
            return df
        else:
            log.error(f'Invalid kind: {kind}')
            raise
#-----------------------------------
