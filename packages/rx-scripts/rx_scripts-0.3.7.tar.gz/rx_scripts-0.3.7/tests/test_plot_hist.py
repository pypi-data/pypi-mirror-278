import utils
import ROOT
import numpy

#-------------------------------
class data:
    h_1 = None
    h_2 = None
#-------------------------------
def get_hist():
    if (data.h_1 is not None) and (data.h_2 is not None):
        return [data.h_1, data.h_2]

    arr_val_1 = numpy.random.normal(0, 0.1, 10000)
    arr_val_2 = numpy.random.normal(0, 0.1, 10000)
    
    data.h_1 = utils.arr_to_hist('h1', 'h1', 30, -0.2, 0.2, arr_val_1) 
    data.h_2 = utils.arr_to_hist('h2', 'h2', 30, -0.2, 0.2, arr_val_2) 
    
    return [data.h_1, data.h_2]
#-------------------------------
def plot_ratio():
    outpath='tests/plot_hist/plot_1.png'
    d_opt             = {}
    d_opt['draw_all'] = True
    d_opt['yrange']   = 0, 2000
    d_opt['ratio']    = True

    l_hist = get_hist()
    utils.plotHistograms(l_hist, outpath, d_opt = d_opt)
#-------------------------------
def plot_overlay():
    outpath='tests/plot_hist/plot_2.png'
    d_opt             = {}
    d_opt['draw_all'] = True
    d_opt['yrange']   = 0, 2000
    d_opt['l_text']   = (['line 1', 'line 2'], 10) 

    l_hist = get_hist()
    utils.plotHistograms(l_hist, outpath, d_opt = d_opt)
#-------------------------------
def plot_1mcdf():
    outpath='tests/plot_hist/1mcdf.png'
    d_opt             = {}
    d_opt['draw_all'] = True
    d_opt['width']    = 1000
    d_opt['yrange']   = 0, 1 
    d_opt['ratio']    = True
    d_opt['1_m_cdf']  = True

    l_hist = get_hist()
    utils.plotHistograms(l_hist, outpath, d_opt = d_opt)
#-------------------------------
def main():
    ROOT.gROOT.ProcessLine(".L lhcbStyle.C")
    ROOT.lhcbStyle()

    plot_1mcdf()
    return
    plot_ratio()
    plot_overlay()
#-------------------------------
if __name__ == '__main__':
    main()

