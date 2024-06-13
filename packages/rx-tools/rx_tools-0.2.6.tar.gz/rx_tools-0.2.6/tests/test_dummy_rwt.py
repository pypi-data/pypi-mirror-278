from rk.dummy_reweighter import reweighter as drwt

import utils_noroot as utnr
import numpy

#-------------------------------------
def test_simple():
    obj     = drwt()
    out_dir = 'tests/test_dummy_reweighter/simple'
    utnr.dump_pickle(obj, f'{out_dir}/rwt.pickle')

    obj     = utnr.load_pickle(f'{out_dir}/rwt.pickle')
    l_val   = [val for val in range(100)]
    arr_val = numpy.array(l_val)
    arr_wgt = obj.predict_weights(arr_val)
    print(arr_wgt)
#-------------------------------------
def test_factor():
    obj     = drwt(fac=1.2)
    out_dir = 'tests/test_dummy_reweighter/factor'
    utnr.dump_pickle(obj, f'{out_dir}/rwt.pickle')

    obj     = utnr.load_pickle(f'{out_dir}/rwt.pickle')
    l_val   = [val for val in range(100)]
    arr_val = numpy.array(l_val)
    arr_wgt = obj.predict_weights(arr_val)
    print(arr_wgt)

#-------------------------------------
def main():
    test_simple()
    test_factor()
#-------------------------------------
if __name__ == '__main__':
    main()

