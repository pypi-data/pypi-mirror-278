from setuptools import setup, find_packages

setup(
        name            ='rx_hqm',
        version         ='0.1.9',
        author          ='Qi Shi',
        description     ='',
        package_dir     = {'' : 'hqm'},
        package_data    = {'hqm_data' : ['*.json', 'double_swap/*.json']},
        install_requires= open('requirements.txt').read()
        )
