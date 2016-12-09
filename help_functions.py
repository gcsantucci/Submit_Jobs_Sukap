#!/usr/bin/python                               

import sys
import os

from parameters import default_card

def get_card():
    card = raw_input('\nIf you are using the default parameters.card enter [d],\notherwise enter the full path for the card if not in this directory.\n')
    if card == 'd':
        card = default_card
    is_card(card)
    return card

#Great function to implement try except catch logic!! Study and implement this! 
def is_card(card):
    if os.path.isfile(card):
        print('\nUsing card: {0}'.format(card))
    else:
        print('Parameters card does not exist!\n Exiting...')
        sys.exit(0)

def getinfile(i):
    return '/disk/usr3/santucci/PDK/MC_events/pdk_vectors/skdetsim/pdk_100k_sk.zbs'

def WriteSKBash(cmdstr, jobdir):
    name = jobdir + 'NQSjob_nglogL.csh'
    errstr = '#@$-o ' + jobdir + 'test.err'
    outstr = '#@$-o ' + jobdir + 'test.out'
    bash_file = open(name,'w')
    bash_file.write("#!/bin/csh\n")
    bash_file.write("# Batch mode using NQS\n\n")
#    bash_file.write(outstr)
#    bash_file.write(os.linesep)
    bash_file.write(errstr)
    bash_file.write(os.linesep)
    bash_file.write(os.linesep)
    bash_file.write(cmdstr)
    bash_file.write(os.linesep)
    bash_file.close()
    return

def getsubjob(path, jobname, ijob, isub):

    job = str(jobname) + '_' + str(ijob)
    jobdir = path + str(jobname) + '/' + job + '/'
    subjob = job + "_" + str(isub)
    subjobdir = jobdir + 'subjob_' + str(isub) + '/'
    #os.mkdir(subjobdir)
    return subjobdir + subjob, subjobdir
    
def runfiTQun(i, jobname, path, isub,nevents):

    infile = getinfile(isub)

    subjob, subjobdir = getsubjob(path, jobname, i, isub)

    APfile = subjob + '_ap.zbs'
    FQfile = subjob + '_ap_fq_nglogL.zbs'
    HBKfile = subjob + '_ap_fq_nglogL.hbk'
    miurahbk = subjob + '_miura.hbk'

    cmdstr = "source /home/santucci/PDK/pdk_nglogL/RunJob.csh " + APfile + " " + FQfile + " " + str(HBKfile)
        
    WriteSKBash(cmdstr, subjobdir)
        
    runcommand = 'qsub -q all -eo -lm 3gb -o ' + subjobdir + 'out_nglogL.log '  + subjobdir + 'NQSjob_nglogL.csh'
    os.system(runcommand)

    return

def mkjobdir(path, jobname, ijob):
    job = str(jobname) + '_' + str(ijob)
    ijobdir = path + str(jobname) + '/' + job + '/'
    os.mkdir(ijobdir)
    return
