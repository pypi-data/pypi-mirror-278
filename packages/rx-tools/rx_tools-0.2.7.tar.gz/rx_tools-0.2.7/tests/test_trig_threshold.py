
from log_store import log_store

import os
import mplhep
import logzero
import matplotlib.pyplot as plt

log_store.set_level('tools:trig_thresholds', logzero.DEBUG)

from rk.trig_threshold import reader as th_reader

#----------------------------------------------
class data:
    l_year   = ['2011', '2012', '2015', '2016', '2017', '2018']
    d_trig   = {'L0ElectronTIS' : 'eTOS', 'L0HadronTIS' : 'hTOS', 'L0MuonTIS' : 'mTOS'}
    test_dir = 'tests/tck_thresholds'
#----------------------------------------------
def test_simple():
    for tag, prb in data.d_trig.items():
        l_thr = []
        for year in data.l_year:
            obj=th_reader(tag_trigger=tag, year=year)
            thr=obj.get_threshold()
            l_thr.append(thr)

        plt.plot(data.l_year, l_thr, label=prb)

    plt.ylim(0, 4000)
    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Threshold [MeV]')
    plt.grid()
    plt.savefig(f'{data.test_dir}/simple.png')
    plt.close('all')
#----------------------------------------------
def main():
    os.makedirs(data.test_dir, exist_ok=True)
    plt.style.use(mplhep.style.LHCb2)

    test_simple()
#----------------------------------------------
if __name__ == '__main__':
    main()

