import zfit
import numpy
import pprint

import zutils.utils      as zut
import pandas            as pnd
import matplotlib.pyplot as plt
import utils_noroot      as utnr

from log_store   import log_store
from zutils.plot import plot      as zfp

#-------------------------------------------------------
class data:
    log = log_store.add_logger('scripts:zutils/utils') 
#-------------------------------------------------------
def res_to_dict(res, frozen=False):
    '''
    Will take a zfit result object and return a dictionary with the parameter values

    Parameters
    ------------------
    res: Zfit result object
    frozen (bool): If true, res.frozen() has been called already

    Returns
    ------------------
    d_par (dict): Dictionary pairing parameter name and tuple with value and error, i.e. {name : (val, err)}
    '''
    noerr = False 
    d_par = {}
    for par, d_val in res.params.items():
        nam = par.name if not frozen else par
        val = d_val['value']
        try:
            err = d_val['hesse']['error'] 
        except:
            noerr = True
            err   = 0 

        d_par[nam] = (val, err)

    if noerr:
        data.log.warning(f'Errors not found')

    return d_par
#-------------------------------------------------------
def copy_model(pdf):
    '''
    Ment to copy PDF's to bypass dropped normlization
    when copying extended PDFs
    '''
    if not pdf.is_extended:
        return pdf.copy()

    yld = pdf.get_yield()

    pdf = pdf.copy()

    pdf = pdf.create_extended(yld)

    return pdf
#-------------------------------------------------------
def result_to_latex(res, tex_path, method='hesse'):
    '''
    Takes result object and dumps table with values of
    parameters to latex table
    '''

    if method not in ['hesse', 'minos']:
        data.log.error(f'Invalid method: {method}')
        raise ValueError

    #Can't freeze twice, freeze just in case
    try:
        res.freeze()
    except AttributeError:
        pass

    d_tab              = {}
    d_tab['Parameter'] = [ nam                     for nam,  _ in res.params.items()]
    d_tab['Value'    ] = [ dc['value']             for   _, dc in res.params.items()]

    try:
        if   method == 'hesse':
            d_tab['Error'    ] = [ dc['hesse']['error']  for   _, dc in res.params.items()]
        elif method == 'minos':
            l_err_low = [ dc['errors']['lower'] for   _, dc in res.params.items()]
            l_err_upr = [ dc['errors']['upper'] for   _, dc in res.params.items()]

            d_tab['Error'    ] = [ 0.5 * (err_low + err_upr) for err_low, err_upr in zip(l_err_low, l_err_upr) ]
    except:
        data.log.warning(f'Not including errors, run: res.hesse(name=\'hesse_np\')')

    df = pnd.DataFrame(d_tab)
    df.to_latex(tex_path, index=False)
#-------------------------------------------------------
def pdf_to_latex(pdf, tex_path):
    '''
    Takes pdf and dumps table with values of
    parameters to latex table
    '''

    l_par = list(pdf.get_params(floating=True)) + list(pdf.get_params(floating=False)) 

    d_tab              = {}
    d_tab['Parameter'] = [ par.name     for par in l_par]
    d_tab['Value'    ] = [ par.numpy()  for par in l_par]
    d_tab['Floating' ] = [ par.floating for par in l_par]

    df = pnd.DataFrame(d_tab)
    df.to_latex(tex_path, index=False)
#-------------------------------------------------------
def get_pdf_params(pdf, floating=True, numeric=True):
    '''
    Takes PDF 
    Returns {parname -> value} dictionary

    Parameters
    ---------------------
    numeric (bool) : If true the values will be numbers otherwise, zfit.parameter instances
    '''

    l_par = pdf.get_params(floating=floating)

    if numeric:
        d_par = { par.name : par.value().numpy() for par in l_par }
    else:
        d_par = { par.name : par                 for par in l_par }

    return d_par
#-------------------------------------------------------
def fix_shape(pdf):
    s_par = pdf.get_params(floating=True, is_yield=False)
    for par in s_par:
        par.floating = False
#-------------------------------------------------------
def fix_pars(pdf, d_par):
    '''
    Will take a pdf and a {var_name -> [val, err]} map. It will fix the values of the parameters
    of the PDF according to the dictionary.

    Returns PDF with fixed parameters
    '''

    l_par     = list(pdf.get_params(floating=True)) + list(pdf.get_params(floating=False))
    d_par_pdf = { par.name : par for par in l_par }

    data.log.info('Fixing PDF parameters')
    for par_name, [val, _] in d_par.items():
        try:
            par = d_par_pdf[par_name]
        except:
            data.log.error(f'Cannot find {par_name} among:')
            data.log.error(d_par_pdf.keys())

        par.set_value(val)
        par.floating = False

        data.log.info(f'{par_name:<30}{"->":20}{val:<20}')

    return pdf
#-------------------------------------------------------
def float_pars(pdf, l_par):
    '''
    Will take a pdf and a list of variables. It will float the values of the parameters
    of the PDF 

    Returns PDF with fixed parameters
    '''

    l_par_pdf = list(pdf.get_params(floating=True)) + list(pdf.get_params(floating=False))
    d_par_pdf = { par.name : par for par in l_par_pdf }

    data.log.info('Floating PDF parameters')
    for par_name in l_par: 
        try:
            par = d_par_pdf[par_name]
        except:
            data.log.error(f'Cannot find {par_name} among:')
            data.log.error(d_par_pdf.values())
            raise

        par.floating = True 

        data.log.info(par_name)

    return pdf
#-------------------------------------------------------
def fit_result_to_pandas(res):
    '''
    Will take a results object from zfit after calling hesse and without freezing it 
    Will return a pandas dataframe with a single row and columns corresponding to the variables
    and their fit errors
    '''
    d_data = {}
    for par, d_val in res.params.items():
        name= par.name
        val = d_val['value']
        err = d_val['hesse']['error']

        d_data[f'{name} value'] = [val]
        d_data[f'{name} error'] = [err]

    df = pnd.DataFrame(d_data)

    return df
#-------------------------------------------------------
def pad_data(data, model, low=None, high=None, scale=1.0):
    '''
    Will 
    1. Remove data between low and high
    2. Make fake data from model between said interval
    3. Patch deleted data
    4. Can optionally use a scale factor in case normalization has problems
    '''
    arr_flg = (data > low) & (data < high)
    data_fl = data[~arr_flg]

    frac  = model.numeric_integrate([low, high]).numpy()
    nsb   = data_fl.size
    ntot  = nsb / (1 - frac)
    nsig  = scale * frac * ntot 
    nsig  = int(nsig)

    sdata = model.create_sampler(limits=[low, high], n=nsig)
    dat_sg= sdata.numpy().flatten()

    data  = numpy.concatenate([data_fl, dat_sg])

    return data
#-------------------------------------------------------
def get_const(par, d_const):
    if d_const is None or par.name not in d_const:
        return 'none'

    obj = d_const[par.name]
    if isinstance(obj, (list, tuple)):
        [mu, sg] = obj
        val      = f'{mu:.3e}; {sg:.3e}'
    else:
        val      = str(obj)

    return val
#-------------------------------------------------------
def print_pdf(pdf, d_const=None, txt_path=None, level='info'):
    '''
    Function used to print zfit PDFs

    Parameters
    -------------------
    pdf (zfit.PDF): PDF
    d_const (dict): Optional dictionary mapping {par_name : [mu, sg]}
    txt_path (str): Optionally, dump output to text in this path
    level (str)   : Optionally set the level at which the printing happens in screen, default info
    '''
    s_par_flt = pdf.get_params(floating= True)
    s_par_fix = pdf.get_params(floating=False)

    l_par_flt = list(s_par_flt) 
    l_par_fix = list(s_par_fix) 

    l_par_flt = sorted(l_par_flt, key=lambda par: par.name)
    l_par_fix = sorted(l_par_fix, key=lambda par: par.name)

    str_space = str(pdf.space)

    l_msg=[]
    l_msg.append('-' * 20)
    l_msg.append(f'PDF: {pdf.name}')
    l_msg.append(f'OBS: {str_space}')
    l_msg.append(f'{"Name":<50}{"Value":<15}{"Floating":<10}{"Constraint":<20}')
    l_msg.append('-' * 20)
    for par in l_par_flt:
        value      = par.value().numpy()
        const      = get_const(par, d_const)
        l_msg.append(f'{par.name:<50}{value:<15.3f}{par.floating:<10}{const:<20}')

    for par in l_par_fix:
        value = par.value().numpy()
        const = get_const(par, d_const)
        l_msg.append(f'{par.name:<50}{value:<15.3f}{par.floating:<10}{const:<20}')

    if txt_path is not None:
        data.log.debug(f'Saving to: {txt_path}')
        utnr.dump_list(l_msg, txt_path)
    else:
        for msg in l_msg:
            if   level == 'info':
                data.log.info(msg)
            elif level == 'debug':
                data.log.debug(msg)
            else:
                data.log.error(f'Invalid level: {level}')
                raise
#-------------------------------------------------------
def fit_pull(arr_val, fit_sig=2, plot=False, var_name=None):
    '''
    Will fit pull distribution to Gaussian and optionally plot it

    Parameters:
    --------------------
    arr_val (ndarray): Numpy array storing pull values
    fit_sig (int): Number of sigmas (STDEV) around arithmetic mean of distribution where to fit
    plot (bool): If true, will plot pull and fitting function
    var_name(str): Variable name, used for plot, optional

    Returns:
    --------------------
    Tuple of floats with mean and width from fit
    '''
    ival = int(numpy.random.uniform() * 10e6)

    mu_m = numpy.mean(arr_val)
    sg_m = numpy.std(arr_val)

    mu_v = mu_m if -5  < mu_m < + 5 else 0
    sg_v = sg_m if 0.1 < sg_m < + 5 else 1

    obs   = zfit.Space(f'x_{ival}', limits=(-10, 10))
    mu    = zfit.Parameter(f'mu_{ival}', mu_v, -5.0, 5.0)
    sg    = zfit.Parameter(f'sg_{ival}', sg_v,  0.1, 5.0)
    ne    = zfit.Parameter(f'ne_{ival}', 1000,  0.0, 1e5)
    gauss = zfit.pdf.Gauss(obs=obs, mu=mu, sigma=sg)
    pdf   = gauss.create_extended(ne)

    dat   = zfit.Data.from_numpy(obs=obs, array=arr_val)
    nll   = zfit.loss.ExtendedUnbinnedNLL(model=pdf, data=dat, fit_range=(mu_v - fit_sig * sg_v, mu_v + fit_sig * sg_v))

    minimizer = zfit.minimize.Minuit()
    result    = minimizer.minimize(nll)
    result.hesse(method='minuit_hesse')
    result.freeze()

    mu_v = result.params[f'mu_{ival}']['value']
    sg_v = result.params[f'sg_{ival}']['value']

    mu_e = result.params[f'mu_{ival}']['hesse']['error']
    sg_e = result.params[f'sg_{ival}']['hesse']['error']

    if plot:
        mu_sg_txt = f'$\mu={mu_v:.3f}\pm{mu_e:.3f}$\n$\sigma={sg_v:.3f}\pm{sg_e:.3f}$'
        mu_sg_txt = f'{var_name}\n{mu_sg_txt}' if var_name is not None else var_name
        obj= zfp(data=dat, model=pdf, result=result)
        obj.plot(nbins=50, ext_text=mu_sg_txt, d_leg={'Gauss_ext' : 'Fit', 'Data' : 'Pull'}, plot_range=(mu_v - 4 * sg_v, mu_v + 4 * sg_v))

        val = f'$\mu={mu_v:.3f}\pm{mu_e:.3f}$'
        err = f'$\sigma={sg_v:.3f}\pm{sg_e:.3f}$'

        obj.axs[0].legend(title=f'{val}\n{err}')

        obj.axs[0].set_ylabel('Entries')
        obj.axs[1].set_xlabel('')

        obj.axs[0].axvline(x=mu_v - sg_v, color='red', linestyle=':')
        obj.axs[0].axvline(x=mu_v       , color='red', linestyle='-')
        obj.axs[0].axvline(x=mu_v + sg_v, color='red', linestyle=':')

    return (mu_v, mu_e), (sg_v, sg_e)
#-------------------------------------------------------
def freq_one(df, good_val, quantity):
    sr_qnt = df[quantity]
    ntot   = len(sr_qnt)

    sr_good= sr_qnt[sr_qnt == good_val]
    ngood  = len(sr_good)

    return ngood, ntot - ngood
#-------------------------------------------------------
def add_labels(arr_x, arr_y1, arr_y2, xoff, yoff, l_color=['blue', 'orange'], form='{:.0f}'):
    [color_1, color_2] = l_color
    for x, y1, y2 in zip(arr_x, arr_y1, arr_y2):
        label_1 = form.format(y1)
        label_2 = form.format(y2)

        plt.annotate(label_1, (x,y1), fontsize=22, textcoords="offset points", xytext=(xoff,-yoff), color=color_1, ha='center')
        plt.annotate(label_2, (x,y2), fontsize=22, textcoords="offset points", xytext=(xoff, yoff), color=color_2, ha='center')
#-------------------------------------------------------
def plot_qlty(df):
    cnv_y, cnv_n = freq_one(df, 1, 'converged') 
    sta_y, sta_n = freq_one(df, 0, 'status') 
    val_y, val_n = freq_one(df, 1, 'valid') 

    xerr = [0.5, 0.5, 0.5]
    xval = [1.0, 2.0, 3.0]
    plt.errorbar(xval, [cnv_y, sta_y, val_y], xerr=xerr, label='Good' , marker='o', linestyle='None')
    plt.errorbar(xval, [cnv_n, sta_n, val_n], xerr=xerr, label='Bad'  , marker='o', linestyle='None')

    add_labels(xval, [cnv_y, sta_y, val_y], [cnv_n, sta_n, val_n], 40, 20)

    plt.title('Fit quality')
    plt.grid()
    plt.legend()
    plt.ylim(0, 1.2 * len(df))
    plt.xticks(xval, ['Converged', 'Status', 'Valid'])
    plt.tight_layout()
#-------------------------------------------------------
def extend_pdfs(l_pdf, l_evt):
    npdf = len(l_pdf)
    nevt = len(l_evt)

    if npdf != nevt:
        data.log.error('Different number of PDFs and yields: {npdf}/{nevt}')
        raise

    l_pdf_ext = []
    for pdf, evt in zip(l_pdf, l_evt):
        pdf.set_yield(evt)
        l_pdf_ext.append(pdf)

    return l_pdf_ext
#-------------------------------------------------------
class zfsp_1d_input(Exception):
    pass
#-------------------------------------------------------
class split_fit:
    '''
    Class intended to split models and data for multidimensional fits
    '''
    def __init__(self, data=None, model=None):
        '''
        data : zfit sampler
        model: Instance of zfit.pdf.ProductPDF
        '''
        self._dat = data
        self._mod = model 

        self._l_mode = None
        self._l_data = None
        self._ndim   = None

        self._initialized = False 
    #------------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._l_mode = self._split_model(self._mod)
        self._l_data = self._split_data()

        nmode  = len(self._l_mode) 
        ndata  = len(self._l_data)

        if nmode != ndata:
            data.log.error(f'Different number of models and datasets: {nmode}/{ndata}')
            data.log.info('Models:')
            for mode in self._l_mode:
                zut.print_pdf(mode)

            raise

        self._ndim = nmode

        self._initialized = True
    #------------------------------
    def _split_model(self, model):
        #Either it's a product of PDFs or a sum of products
        if not isinstance(model, (zfit.pdf.ProductPDF, zfit.pdf.SumPDF)):
            cls     = type(model)
            str_cls = str(cls)
            raise zfsp_1d_input(f'Cannot split an object of type: {str_cls}')

        if isinstance(model, zfit.pdf.ProductPDF):
            return [ pdf.copy() for pdf in model.pdfs ]

        l_l_pdf = list()
        for pdf in model.pdfs:
            l_pdf = self._split_model(pdf)
            l_l_pdf.append(l_pdf)

        l_nevt= [ pdf.get_yield() for pdf in model.pdfs ]
        l_pdf = self._merge_pdfs(l_l_pdf, l_nevt)

        return l_pdf 
    #------------------------------
    def _merge_pdfs(self, l_l_pdf, l_nevt):
        '''
        Parameters
        -----------------
        l_l_pdf : List of lists of PDFs, the inner list corresponds to each term in a SumPDF
        l_nevt  : List of yields to extend the PDFs in each dimension before adding them

        Returns
        -----------------
        l_sum_pdf: List of SumPDF objects, one for each dimension
        '''
        s_size = { len(l_pdf) for l_pdf in l_l_pdf }
        if len(s_size) != 1:
            data.log.error(f'Not all terms in SumPDF are of the same dimension')
            raise

        ndim      = list(s_size)[0]
        l_sum_pdf = []
        for i_dim in range(ndim):
            l_pdf_dim = [ l_pdf[i_dim] for l_pdf in l_l_pdf ]
            l_pdf_dim = extend_pdfs(l_pdf_dim, l_nevt)
            pdf_dim   = zfit.pdf.SumPDF(l_pdf_dim)

            l_sum_pdf.append(pdf_dim)

        return l_sum_pdf
    #------------------------------
    def _split_data(self):
        if not isinstance(self._dat, (zfit.core.data.SamplerData, zfit.core.data.Data)):
            cls     = type(self._dat)
            str_cls = str(cls)
            data.log.error(f'Invalid data of type: {str_cls}')
            raise

        arr_dat = self._dat.numpy()

        return arr_dat.T
    #------------------------------
    def split(self):
        '''
        Returns

        tupe: First element list of models, second element list of datasets
        '''
        self._initialize()

        return self._l_mode, self._l_data
#------------------------------

