from rk.gen_stats import get_ngen

from log_store import log_store

log = log_store.add_logger('tools:test_gen_stats')
#-----------------------------------
class data:
    sim_ver = 'v10.21p2'
#-----------------------------------
def test_get_ngen():
    log.info(80 * '-')
    log.info(f'{"Process":<20}{"Trigger":<20}{"Year":<20}{"Ngen":<20}')
    log.info(80 * '-')
    for proc in ['ctrl', 'psi2']:
        for trig in ['MTOS', 'ETOS', 'GTIS']:
            for year in ['2011', '2012', '2015', '2016', '2017', '2018']:
                ngen = get_ngen('ctrl', trig, year, data.sim_ver)
                log.info(f'{proc:<20}{trig:<20}{year:<20}{ngen:<20}')
#-----------------------------------
def main():
    test_get_ngen()
#-----------------------------------
if __name__ == '__main__':
    main()
