from setuptools import setup, find_packages

import glob

setup(
        name            ='rx_prec_accepance',
        version         ='0.0.5',
        description     ='Scripts used to calculate acceptance for rare PRec decays',
        long_description='',
        scripts         = glob.glob('scripts/*'), 
        packages        = find_packages(where='src'), 
        package_data    = {'prec_acceptances_data' : ['*/*.json']},
        package_dir     = {'' : 'src'}
        )

