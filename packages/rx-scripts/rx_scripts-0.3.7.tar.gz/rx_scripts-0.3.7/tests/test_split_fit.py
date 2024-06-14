from zutils.utils import split_fit as zfsp 
from zutils.plot  import plot      as zfp
from zutils.utils import zfsp_1d_input 
from log_store    import log_store

import matplotlib.pyplot as plt
import zutils.utils      as zut 
import zfit
import os

log=log_store.add_logger('rx_scripts:test_split_fit')
#---------------------------------------------
class data:
    obs_x = zfit.Space('x', limits=(0, 10))
    obs_y = zfit.Space('y', limits=(0, 10))
#---------------------------------------------
def get_pdf(name, obs=None):
    sg  = zfit.Parameter(f'sg_{name}', 1.0,  0, 5)

    if   '1' in name:
        mu  = zfit.Parameter(f'mu_{name}', 2.0, -1, 9)
    elif '2' in name:
        mu  = zfit.Parameter(f'mu_{name}', 5.0, -1, 9)
    elif '3' in name:
        mu  = zfit.Parameter(f'mu_{name}', 8.0, -1, 9)
    else:
        log.error(f'Invalid name: {name}')
        raise

    pdf = zfit.pdf.Gauss(obs=obs, mu=mu, sigma=sg, name=f'g_{name}')

    return pdf
#---------------------------------------------
def test_prod():
    pdf_x = get_pdf('x', obs=data.obs_x)
    pdf_y = get_pdf('y', obs=data.obs_y)
    pdf   = zfit.pdf.ProductPDF([pdf_x, pdf_y])
    sam   = pdf.create_sampler(n=1000)

    obj          = zfsp(data=sam, model=pdf)
    l_mod, l_dat = obj.split()
#---------------------------------------------
def get_2d_input():
    pdf_x1 = get_pdf('x1', obs=data.obs_x)
    pdf_y1 = get_pdf('y1', obs=data.obs_y)

    pdf_x2 = get_pdf('x2', obs=data.obs_x)
    pdf_y2 = get_pdf('y2', obs=data.obs_y)

    pdf_x3 = get_pdf('x3', obs=data.obs_x)
    pdf_y3 = get_pdf('y3', obs=data.obs_y)

    pdf_1  = zfit.pdf.ProductPDF([pdf_x1, pdf_y1])
    pdf_2  = zfit.pdf.ProductPDF([pdf_x2, pdf_y2])
    pdf_3  = zfit.pdf.ProductPDF([pdf_x3, pdf_y3])

    nev_1  = zfit.param.Parameter('nev_1', 50000, 0, 100000)
    nev_2  = zfit.param.Parameter('nev_2', 30000, 0, 200000)
    nev_3  = zfit.param.Parameter('nev_3', 20000, 0, 300000)

    pdf_1.set_yield(nev_1)
    pdf_2.set_yield(nev_2)
    pdf_3.set_yield(nev_3)

    pdf   = zfit.pdf.SumPDF([pdf_1, pdf_2, pdf_3])
    sam   = pdf.create_sampler()

    return sam, pdf
#---------------------------------------------
def test_sum():
    dat, pdf     = get_2d_input()

    obj          = zfsp(data=dat, model=pdf)
    l_mod, l_dat = obj.split()
    l_nam        = ['m1', 'm2']

    out_dir = 'tests/test_split_fit/sum'
    os.makedirs(out_dir, exist_ok=True)

    for mod, dat, nam in zip(l_mod, l_dat, l_nam):
        obj = zfp(data=dat, model=mod)
        obj.plot(nbins=50, plot_range=(0, 10), stacked=False)

        plt.savefig(f'{out_dir}/{nam}.png')
        plt.close()
#---------------------------------------------
def test_1d():
    pdf = get_pdf('x', obs=data.obs_x)
    sam = pdf.create_sampler(n=1000)

    try:
        obj          = zfsp(data=sam, model=pdf)
        l_mod, l_dat = obj.split()
    except zfsp_1d_input:
        log.info(f'Successfully raised 1d exception')
    else:
        log.error('Did not raise exception')
        raise
#---------------------------------------------
def main():
    test_sum()
    return
    test_prod()
    test_1d()
#---------------------------------------------
if __name__ == '__main__':
    main()

