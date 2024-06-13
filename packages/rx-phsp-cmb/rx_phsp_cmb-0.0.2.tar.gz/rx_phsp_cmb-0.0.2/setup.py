from setuptools import setup, find_packages

import glob

setup(
        name            ='rx_phsp_cmb',
        version         ='0.0.2',
        description     ='Used to get combinatorial shape under PHSP warping assumption',
        long_description='',
        packages        = ['phsp_cmb'],
        package_dir     = {'' : 'src'},
        install_requires= open('requirements.txt').read().splitlines()
        )
