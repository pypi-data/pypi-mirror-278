import os
import toml
import pprint
import matplotlib.pyplot as plt

from log_store import log_store

log=log_store.add_logger('rx_scripts:var_plotter')
#----------------------------------------
class plotter:
    def __init__(self, data=None, cfg=None):
        self._d_df = data 
        self._cfg  = cfg 

        self._d_conf = None
        self._out_dir= None

        self._initialized=False
    #----------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._load_config()
        self._setup_paths()

        self._initialized = True
    #----------------------------------------
    def _setup_paths(self):
        self._out_dir = self._d_conf['paths']['output']
        os.makedirs(self._out_dir, exist_ok=True)
    #----------------------------------------
    def _load_config(self):
        if not os.path.isfile(self._cfg):
            log.error(f'Config file not found: {self._cfg}')
            raise FileNotFoundError

        self._d_conf = toml.load(self._cfg)
    #----------------------------------------
    def _plot_var(self, name):
        l_dst = self._d_conf['datasets']
        d_set = self._d_conf['plots'][name]
        d_sty = self._d_conf['style']

        [bins, minx, maxx] = d_set['binning' ]
        if isinstance(bins, float):
            bins = int(bins)

        scale              = d_set['scale'   ]
        density            = d_set['normalized']
        ylabel             = d_set['ylabel']
        ax = None

        save_fig=False
        for dst in l_dst:
            d_style = d_sty[dst]
            color   = d_style['color']
            alpha   = d_style['alpha']
            histtype= d_style['histtype']

            df = self._d_df[dst]
            if name not in df.columns:
                log.warning(f'Missing variable {name} in dataset {dst}')
                continue

            if 'weight' not in df.columns:
                log.error(f'Missing weight column in dataset {dst}')
                raise

            arr_val = df[name].to_numpy()
            arr_wgt = df['weight'].to_numpy()

            save_fig=True
            plt.hist(
                    arr_val,
                    bins    = bins, 
                    range   = (minx, maxx), 
                    label   = dst, 
                    color   = color, 
                    density = density, 
                    alpha   = alpha, 
                    weights = arr_wgt,
                    histtype= histtype)

        if not save_fig:
            log.warning(f'Not saving figure for: {name}')
            return

        if scale == 'linear':
            plt.ylim(bottom=0)

        plt.legend()
        plt.yscale(scale)
        plt.xlabel(name)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(f'{self._out_dir}/{name}.png')
        plt.close('all')
    #----------------------------------------
    def run(self):
        self._initialize()

        d_plot = self._d_conf['plots']

        for col in d_plot:
            log.info(f'Plotting: {col}')
            self._plot_var(col)
#----------------------------------------

