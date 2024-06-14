from var_plotter import plotter as vplotter

from importlib.resources import files

import numpy
import pandas as pnd

#-----------------------------------------
def get_df(weighted=True):
    size = 10000

    d_data      = dict()
    d_data['a'] = numpy.random.uniform(0, 10, size=size)
    d_data['b'] = numpy.random.normal(4, 1,   size=size)
    d_data['c'] = numpy.random.exponential(4, size=size)
    if weighted:
        d_data['weight'] = numpy.random.normal(1, 1.05,   size=size)
    else:
        d_data['weight'] = numpy.ones(size)

    df = pnd.DataFrame(d_data)

    return df
#-----------------------------------------
def test_simple():
    cfg_path= files('scripts_data').joinpath('tests_data/var_plotter_simple.toml')
    df_1 = get_df(weighted=True)
    df_2 = get_df(weighted=False)
    d_df = {'ds1' : df_1, 'ds2' : df_2}

    ptr=vplotter(data=d_df, cfg=cfg_path)
    ptr.run()
#-----------------------------------------
def test_misvar():
    cfg_path= files('scripts_data').joinpath('tests_data/var_plotter_misvar.toml')
    df_1 = get_df(weighted=True)
    df_2 = get_df(weighted=False)
    d_df = {'ds1' : df_1, 'ds2' : df_2}

    ptr=vplotter(data=d_df, cfg=cfg_path)
    ptr.run()
#-----------------------------------------
def main():
    test_misvar()
    test_simple()
#-----------------------------------------
if __name__ == '__main__':
    main()

