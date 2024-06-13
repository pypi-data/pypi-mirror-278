from setuptools import setup, find_packages

import glob

setup(
        name                ='rx_tools',
        version             ='0.2.6',
        description         ='Project containing tools for RX measurement',
        long_description    ='',
        scripts             = glob.glob('scripts/*'),
        packages            = ['tools_data/trigger', 'rk', 'tools_data/inclusive_mc_stats'],
        package_data        = {'tools_data/inclusive_mc_stats' : ['*.json']},
        package_dir         = {'' : 'src'},
        install_requires    = open('requirements.txt').read().splitlines(),
        )

