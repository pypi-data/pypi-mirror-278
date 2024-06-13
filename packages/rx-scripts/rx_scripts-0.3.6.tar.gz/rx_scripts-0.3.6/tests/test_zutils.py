import zutils.utils      as zut
import matplotlib.pyplot as plt
import pandas            as pnd
import numpy

#---------------------------------------------
def get_df():
    d_data = {'converged' : [], 'status' : [], 'valid' : []}
    d_data['converged'] = numpy.random.choice([0, 1], size=1000, p=[0.2, 0.8])
    d_data['status']    = numpy.random.choice([0, 1], size=1000, p=[0.3, 0.7])
    d_data['valid']     = numpy.random.choice([0, 1], size=1000, p=[0.4, 0.6])

    return pnd.DataFrame(d_data)
#---------------------------------------------
def test_plot_qlty():
    df = get_df()
    zut.plot_qlty(df)
    plt.show()
#---------------------------------------------
def test_fit_pull():
    arr_pull = numpy.random.normal(0, 1, size=1000)
    zut.fit_pull(arr_pull, plot=True)
    plt.show()
#---------------------------------------------
def main():
    test_fit_pull()
    return
    test_plot_qlty()
#---------------------------------------------
if __name__ == '__main__':
    main()

