
import pandas       as pnd
import utils        as utnr
import ROOT
import glob
import os

from log_store import log_store

log=log_store.add_logger('rx_scripts:rdf_loader')
#------------------------------------
class rdf_loader:
    '''
    Class used to load ROOT files into dataframes, optionally apply additional selections and
    provide cutflow and metadata associated.
    '''
    def __init__(self, **kwargs): 
        self._sample  = kwargs['sample']
        self._proc    = kwargs['proc']
        self._asl_vers= kwargs['asl_vers']
        self._ntp_vers= kwargs['ntp_vers']
        self._year    = kwargs['year']
        self._trig    = kwargs['trig']

        self._df_cf   = None
        self._d_arg   = kwargs
        self._d_cut   = None

        self._initialized = False
    #------------------------------------
    @property
    def selection(self):
        return self._d_cut

    @selection.setter
    def selection(self, value):
        if not isinstance(value, dict):
            log.error(f'Invalid value type {type(value)}, expected dict')
            raise

        self._d_cut = value
    #------------------------------------
    def _get_paths(self):
        cas_dir = os.environ['CASDIR']
        if   self._year == 'r1':
            l_path_wc = [
                    f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/2011_{self._trig}/*.root',
                    f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/2012_{self._trig}/*.root'
                    ]
        elif self._year == 'r2p1':
            l_path_wc = [
                    f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/2015_{self._trig}/*.root',
                    f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/2016_{self._trig}/*.root'
                    ]
        elif self._year == 'all':
            l_path_wc = [
                    f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/2011_{self._trig}/*.root',
                    f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/2012_{self._trig}/*.root',
                    f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/2015_{self._trig}/*.root',
                    f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/2016_{self._trig}/*.root',
                    f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/2017_{self._trig}/*.root',
                    f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/2018_{self._trig}/*.root',
                    ]
        else:
            l_path_wc = [f'{cas_dir}/tools/apply_selection/{self._sample}/{self._proc}/{self._ntp_vers}/{self._year}_{self._trig}/*.root']

        self._d_arg['path'] = l_path_wc

        l_path = []
        for path_wc in l_path_wc:
            l_path += glob.glob(path_wc)

        if len(l_path) == 0:
            log.error(f'No file found in: {path_wc}')
            raise FileNotFoundError

        return l_path
    #------------------------------------
    def _filter_rdf(self, rdf):
        if self._d_cut is None:
            return rdf

        for nam, cut in self._d_cut.items():
            rdf = rdf.Filter(cut, nam)

        rep = rdf.Report()
        rep.Print()

        df_cf = utnr.rdf_report_to_df(rep)
        df_cf = df_cf.drop(columns=['cut', 'Efficiency', 'Cummulative'])
        df_cf = df_cf.rename(columns={'All' : 'Total', 'Passed' : 'Pased'})

        l_cut = list(self._d_cut.keys())
        index = pnd.Index(l_cut)
        df_cf = df_cf.set_index(index, drop=True)
        df_cf['Cut'] = self._d_cut.values()

        df_cf = pnd.concat([self._df_cf, df_cf], axis=0)

        self._df_cf = df_cf

        return rdf
    #------------------------------------
    def _get_cutflow(self, l_path):
        l_cut_path = [ path.replace('.root', '_cut.json') for path in l_path ]
        l_eff_path = [ path.replace('.root', '_eff.json') for path in l_path ]

        l_df_eff   = [ pnd.read_json(path).drop(columns=['Efficiency', 'Cumulative']) for path in l_eff_path ]
        l_df_cut   = [ pnd.read_json(path)                                            for path in l_cut_path ]

        df_z     = l_df_eff[0]
        l_df_eff = l_df_eff[1:]

        for df in l_df_eff:
            df_z = df_z.add(df)

        df_cut      = l_df_cut[0]
        l_cut       = df_cut.Cut 
        df_z['Cut'] = l_cut

        return df_z
    #------------------------------------
    def get_rdf(self):
        l_path      = self._get_paths()
        self._df_cf = self._get_cutflow(l_path) 

        rdf  = ROOT.RDataFrame(self._trig, l_path)
        rdf  = self._filter_rdf(rdf)
        d_md = { 'opts' : self._d_arg, 'cut' : self._d_cut }

        return rdf, self._df_cf, d_md
#------------------------------------

