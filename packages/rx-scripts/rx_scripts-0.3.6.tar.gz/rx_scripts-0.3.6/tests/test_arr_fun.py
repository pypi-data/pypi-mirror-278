import arr_fun as af
import numpy

#------------------------------------
def test_repeat_arr():
    arr_val = numpy.arange(10)
    arr_val = af.repeat_arr(arr_val, 2.3)

    assert arr_val.shape[0] == 23
#------------------------------------
def main():
    test_repeat_arr()
#------------------------------------
if __name__ == '__main__':
    main()
