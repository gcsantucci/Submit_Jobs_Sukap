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
    'nfiles',
    'startfile', 
    'nsubjobs',
    'nevents',
    'emailrate',
    'subrate',
    'maxjobs',
    'sleeptime'
]

strparams = [
    'inpath',
    'ext',
    'outpath',
    'outdirname', 
    'outdirtype', 
    'jobname',
    'runfile',
    'email',
    'queue',
    'user'
]

lstparams = [
    'outfiles'
]

parameters = intparams + strparams + lstparams

default_card = '/home/santucci/PDK/submit_jobs/parameters.card'

def get_params(card):
    infile = open(card, 'r')
    return_params = []
    return_intparams = []
    return_lstparams = []
    for line in infile:
        line = line.strip().split()
        if '#' in line:
            continue
        for param in strparams:
            if param in line:
                return_params.append(line[-1])
                continue
        for param in intparams:
            if param in line:
                return_intparams.append(int(line[-1]))
                continue
        for param in lstparams:
            if param in line:
                return_lstparams.append(line[2:])
    return return_params, return_intparams, return_lstparams[0]


def gen_params():
    for param in parameters:
        yield param
