from rk.inclusive_sample_weights import reader
import numpy
import pandas as pnd

#------------------------------------
def get_df():
    d_data         = {'proc' : [], 'b' : []}
    d_data['proc'] = numpy.random.choice(['bpXcHs', 'bdXcHs', 'bsXcHs'], size=10)
    d_data['b']    = numpy.random.normal(0, 1, size=10)

    return pnd.DataFrame(d_data)
#------------------------------------
def test_simple():
    df            = get_df()
    obj           = reader(df, year=2018)
    df['wgt_sam'] = obj.get_weights()

    print(df)
#------------------------------------
def main():
    test_simple()
#------------------------------------
if __name__ == '__main__':
    main()

