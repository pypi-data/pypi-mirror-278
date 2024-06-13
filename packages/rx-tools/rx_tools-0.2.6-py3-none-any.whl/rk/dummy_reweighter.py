import numpy

#-------------------------------------------
class reweighter:
    def __init__(self, fac=1.0):
        self._fac = fac
    #------------------------------------
    def predict_weights(self, arr_val):
        nentries = arr_val.shape[0]
        arr_one  = numpy.ones(nentries)

        return arr_one * self._fac
#-------------------------------------------

