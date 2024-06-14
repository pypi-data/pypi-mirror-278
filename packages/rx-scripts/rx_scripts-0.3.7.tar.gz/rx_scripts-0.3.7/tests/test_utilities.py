from plotting.utilities import plot_pull as put_pull

import matplotlib.pyplot as plt
import pandas            as pnd
import os

#----------------------------------------------------
def test_pull():
    df = pnd.DataFrame({'n' : ['a', 'b', 'c'] ,'v' : [0, 0.2, 0.3], 'e' : [1.0, 1.3, 0.5]})
    df = df.sort_values(by=['n'], ascending=True)
    put_pull(df, var='n', val='v', err='e')

    pull_dir = 'tests/plotting'
    os.makedirs(pull_dir, exist_ok=True)

    plt.savefig(f'{pull_dir}/pull.png')
    plt.close('all')
#----------------------------------------------------
def test_size():
    df = pnd.DataFrame({'n' : ['a', 'b', 'c'] ,'v' : [0, 0.2, 0.3], 'e' : [1.0, 1.3, 0.5]})
    df = df.sort_values(by=['n'], ascending=True)
    put_pull(df, var='n', val='v', err='e', fig_size=(10, 18))

    pull_dir = 'tests/plotting'
    os.makedirs(pull_dir, exist_ok=True)

    plt.savefig(f'{pull_dir}/size.png')
    plt.close('all')
#----------------------------------------------------
def main():
    test_pull()
    test_size()
#----------------------------------------------------
if __name__ == '__main__':
    main()


