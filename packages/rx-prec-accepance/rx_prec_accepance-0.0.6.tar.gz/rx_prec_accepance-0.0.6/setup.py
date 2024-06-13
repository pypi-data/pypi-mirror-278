from setuptools import setup, find_packages

import glob

setup(
        name            ='rx_prec_accepance',
        version         ='0.0.6',
        description     ='Scripts used to calculate acceptance for rare PRec decays',
        long_description='',
        scripts         = glob.glob('scripts/*'), 
        package_dir     = {'' : 'src'},
        package_data    = {'prec_acceptances_data' : ['*/*.json']},
        )

