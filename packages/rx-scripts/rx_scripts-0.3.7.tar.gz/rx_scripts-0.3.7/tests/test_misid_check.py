import os
import re
import ROOT
import glob
import pprint
import logzero
import pandas            as pnd
import matplotlib.pyplot as plt

from importlib.resources import files
from log_store           import log_store

log_store.set_level('misid_check', logzero.INFO)

from misid_check import misid_check

#---------------------------------
class data:
    casdir = os.environ['CASDIR']
#---------------------------------
def get_columns_needed(rdf):
    v_col_name = rdf.GetColumnNames()
    l_col_name = [ col_name.c_str() for col_name in v_col_name ]
    l_col_need = [ col_name         for col_name in l_col_name if re.match('(L1|L2|H)_(P\w|ID)$', col_name) ]

    return l_col_need
#---------------------------------
def get_df():
    json_path  = files('scripts_data').joinpath('misid_data/bpd0kpienu.json')
    if os.path.isfile(json_path):
        df = pnd.read_json(json_path)
        return df

    trig       = 'ETOS'
    file_wc    = f'{data.casdir}/tools/apply_selection/sl_bkg_rej/bpd0kppienu/v10.21p2/2018_{trig}/*.root'
    rdf        = ROOT.RDataFrame(trig, file_wc)
    l_col_name = get_columns_needed(rdf)
    d_data     = rdf.AsNumpy(l_col_name)
    df         = pnd.DataFrame(d_data)

    df.to_json(json_path, indent=4)

    return df
#---------------------------------
def test_simple():
    df  = get_df()

    obj = misid_check(df, d_lep={'L1' : 211, 'L2' : 211}, d_had={'H' : 321})
    df  = obj.get_df()
    df.H_swp.hist(bins=40, range=(1800, 1950) , histtype='step', label='Swapped')
    df.H_org.hist(bins=40, range=(1800, 1950) , histtype='step', label='Original')
    plt.axvline(x=1864, color='r', label='$D_0$')
    plt.grid(False)
    plt.legend()
    os.makedirs('tests/misid_check', exist_ok=True)
    plt.savefig('tests/misid_check/simple.png')
    plt.close('all')
#---------------------------------
def test_compare():
    df    = get_df(real=True, nentries=10000)

    obj_1 = misid_check(df, d_lep={'L1' : 211, 'L2' : 211}, d_had={'H' : 321})
    df_1  = obj_1.get_df()

    obj_2 = misid_check(df, d_lep={'L1' :  11, 'L2' :  11}, d_had={'H' : 321})
    df_2  = obj_2.get_df()

    ax=None
    ax=df_1.H.hist(bins=40, range=(1500, 2500) , histtype='step', ax=ax)
    ax=df_2.H.hist(bins=40, range=(1500, 2500) , histtype='step', ax=ax)

    plt.legend(['Changed', 'Original'])
    plt.show()
#---------------------------------
def test_rdf_to_df():
    trig       = 'ETOS'
    file_wc    = f'{data.casdir}/tools/apply_selection/sl_bkg_rej/bpd0kppienu/v10.21p2/2018_{trig}/*.root'
    l_file     = glob.glob(file_wc)
    rdf        = ROOT.RDataFrame(trig, l_file)

    df         = misid_check.rdf_to_df(rdf, '(L1|L2|H)_(P\w|ID)$')

    print(df)
#---------------------------------
def main():
    test_rdf_to_df()
    return
    test_simple()
#---------------------------------
if __name__ == '__main__':
    main()
