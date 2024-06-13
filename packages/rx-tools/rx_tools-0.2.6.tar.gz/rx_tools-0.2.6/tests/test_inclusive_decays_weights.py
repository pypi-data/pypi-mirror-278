import ROOT
import pandas            as pnd
import matplotlib.pyplot as plt

from rk.inclusive_decays_weights import reader
#-----------------------------------------------
def rdf_to_idf(rdf):
    v_name=rdf.GetColumnNames()
    l_name=[ name.c_str() for name in v_name ]
    l_name=[ name for name in l_name if 'TRUEID' in name or 'MOTHER_ID' in name]
    
    d_id = rdf.AsNumpy(l_name)
    
    df = pnd.DataFrame(d_id)

    return df
#-----------------------------------------------
def test_simple():
    file_path = '/publicfs/lhcb/user/campoverde/Data/cache/tools/apply_selection/prec_shape/bpXcHs_ee/v10.18is/2018_ETOS/4_10.root'
    rdf=ROOT.RDataFrame('ETOS', file_path)
    df = rdf_to_idf(rdf)
    df['weight'] = df.apply(reader.read_weight, args=('L1', 'L2', 'H'), axis=1)
    print(df)
#-----------------------------------------------
def main():
    test_simple()
#-----------------------------------------------
if __name__ == '__main__':
    main()



