'''
This module contains the declaration of parameters set in parameters.card to be
used in the generate_events.py module to run jobs on the queue system 
of sukap machines.
If you introduce a new parameter to the card, you need to define it here, 
change the get_params()function and add it in the main module.

Author: Gabriel Santucci
gabriel.santucci@stonybrook.edu
Dec 2016
'''

intparams = [
    'nsubjobs',
    'nevents',
    'numFiles',
    'numskip',
    'endfile',
    'MaxNJobs',
'time_to_sleep'
]

params = [
    'filespath',
    'jobname',
    'path',
]

default_card = '/home/santucci/PDK/submit_jobs/parameters.card'

def get_params(card):
    if card == 'd':
        params_file = default_card
    else:
        params_file = card
    infile = open(params_file, 'r')
    return_params = []
    return_intparams = []
    for line in infile:
        line = line.strip().split()
        if '#' in line:
            continue
        for param in params:
            if param in line:
                return_params.append(line[-1])
                continue
        for intparam in intparams:
            if intparam in line:
                return_intparams.append(int(line[-1]))
                continue
    print(return_params)
    print(return_intparams)
    return return_params, return_intparams
