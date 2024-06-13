from rk.plot_pulls import plot_pulls as pltp

#-------------------------------
def test_simple():
    pull_dir = 'tests/mcstudy/constrain/nev_05000'

    po = pltp(dir_name = pull_dir, skip_fit=True)
    po.plot_dir = 'tests/plot_pulls/simple'
    po.save_plots(d_name = {'mu' : '$\mu$', 'sg' : '$\sigma$', 'nev' : '$N_{signal}$'})
#-------------------------------
def main():
    test_simple()
#-------------------------------
if __name__ == '__main__':
    main()

