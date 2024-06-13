from rk.kcabibbo import kcabibbo 

import os
import pandas            as pnd
import matplotlib.pyplot as plt

from log_store import log_store

log = log_store.add_logger('tools:kcabibbo_test')

#-----------------------------
def test_simple():
    for year in ['r1', 'r2p1', '2011', '2012', '2015', '2016', '2017', '2018']:
        for trig in ['ETOS', 'GTIS', 'MTOS']:
            obj=kcabibbo(trig=trig, year=year)
            mid, err =obj.get_factor()
            unc      =err/mid
            log.info(f'{trig:<10}{year:<10}{mid:<10.5f}{err:<10.5f}{unc:<10.3f}')
#-----------------------------
def test_output():
    d_data = {'Trigger' : [], 'Year' : [], 'Value' : [], 'Error' : []}
    for trig in ['ETOS', 'GTIS', 'MTOS']:
        for iyear, year in enumerate(['r1', 'r2p1', '2017', '2018']):
            obj=kcabibbo(trig=trig, year=year)
            mid, err =obj.get_factor()

            d_data['Trigger'].append(trig)
            d_data['Year'   ].append(iyear)
            d_data['Value'  ].append(mid)
            d_data['Error'  ].append(err)

    df = pnd.DataFrame(d_data)

    df.Trigger.replace({'ETOS':'eTOS', 'MTOS' : '$\mu$TOS', 'GTIS':'gTIS!'}, inplace=True)
    fig, ax = plt.subplots(figsize=(8,6))
    for trig, df_t in df.groupby('Trigger'):
        df_t = df_t.drop('Trigger', axis=1)
        df_t = df_t.astype(float)
        df_t.plot(x='Year', y='Value', yerr='Error', ax=ax, label=trig)

    plt.xticks([0.0, 1.0, 2.0, 3.0], ['R1', 'R2.1', '2017', '2018'])
    plt.ylabel('$\mu_{Cabibbo}$')
    plt.grid()

    plot_dir = 'tests/test_kcabibbo/output'
    os.makedirs(plot_dir, exist_ok=True)
    plt.savefig(f'{plot_dir}/summary.png')
#-----------------------------
def main():
    test_output()
    return
    test_simple()
#-----------------------------
if __name__ == '__main__':
    main()

