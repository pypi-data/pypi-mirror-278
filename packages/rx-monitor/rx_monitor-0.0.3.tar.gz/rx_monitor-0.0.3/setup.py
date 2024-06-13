from setuptools import setup, find_packages

import glob

setup(
        name            ='rx_monitor',
        version         ='0.0.3',
        description     ='Project used to carry out several checks',
        scripts         = glob.glob('scripts/*'),
        packages        = ['monitor', 'monitor_data/v4'],
        package_data    = {'monitor_data/v4' : ['*.json']},
        package_dir     = {'' : 'src'},
        install_requires= open('requirements.txt').read()
        )


