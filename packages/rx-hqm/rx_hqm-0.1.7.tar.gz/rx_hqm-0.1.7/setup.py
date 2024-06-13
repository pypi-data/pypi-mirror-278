from setuptools import setup, find_packages

setup(
        name            ='rx_hqm',
        version         ='0.1.7',
        author          ='Qi Shi',
        description     ='',
        packages        = find_packages(),
        package_data    = {'hqm_data' : ['*.json', 'double_swap/*.json']},
        install_requires= open('requirements.txt').read()
        )
