from setuptools import setup, find_packages

import glob

setup(
        name            ='rx_differential_crosscheck_fits',
        version         ='0.0.6',
        description     ='Code used to fit jpsi and psi2S mode in bins of different variables',
        package_dir     = {'' : 'python'},
        package_data    = {'rchecks' : ['*.json']},
        install_requires= open('requirements.txt').read()
        )


