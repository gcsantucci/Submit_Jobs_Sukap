#!/usr/bin/python                               

import sys
import os
import getopt
import shutil

from parameters import default_card

def call_exit():
    print('Exiting...')
    sys.exit(0)

def usage():
    usage_message = '''
Usage:\n    
    python submit_jobs.py --card=d (or parameters.card)\n     
 if using the default card in this directory: parameters.card.        
 Otherwise:\n           
    python submit_jobs.py --card=full_path_to_card.'''
    print(usage_message)

def get_card():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                                       'h',
                                       ['help', 'card='])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
        
    card = None
    if len(opts) == 0:
        usage()
        call_exit()
        
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            call_exit()
        elif opt in ('--card'):
            card = arg
        else:
            assert False, 'unhandled option' + opt

    if card == 'd' or card == 'parameters.card':
        card = default_card
    is_card(card)
    return card

#Great function to implement try except catch logic!! Study and implement this! 
def is_card(card):
    if os.path.isfile(card):
        print('\nUsing card: {0}'.format(card))
    else:
        print('Parameters card does not exist!')
        call_exit()

def check_dirs(dirtype, jobpath, nfiles, start, nsubjobs):
    if os.path.isdir(jobpath):
        print('Dir {0} already exists.'.format(jobpath))
        if dirtype == 'new':
            print('But user set job as new.')
            call_exit()
        elif dirtype == 'same':
            print('Using the same directory.')
        elif dirtype == 'over':
            print('Removing old dir and creating new.')
            shutil.rmtree(jobpath)
            make_dirs(jobpath, nfiles, start, nsubjobs)
        else:
            print('Enter [new], [same] or [over] for dirtype in the parameters.card')
            call_exit()
    else:
        print('Dir {0} does not exist.'.format(jobpath))
        if dirtype == 'new':
            print('Creating necessary directory structure')
            make_dirs(jobpath, nfiles, start, nsubjobs)
        elif dirtype == 'same' or dirtype == 'over':
            print('Output directory was not found:\n{0}'.format(jobpath))
            print('Change parameters.card.')
            call_exit()
        else:
            print('Enter [new], [same] or [over] for dirtype in the parameters.card')
            call_exit()

def make_dirs(jobpath, nfiles, start, nsubjobs):
    os.mkdir(jobpath)    
    for i in xrange(start, start+nfiles):
        ijob = os.path.join(jobpath, str(i))
        os.mkdir(ijob)
        for j in xrange(nsubjobs):
            isub = os.path.join(ijob, str(j))
            os.mkdir(isub)

def is_dir(jobpath):
    if not os.path.isdir(jobpath):
        print('Output directory was not found:\n{0}'.format(jobpath))
        call_exit()

def number_jobs(maxjobs, nsubjobs, nfiles):
    if maxjobs == -1:
        maxjobs = nsubjobs * nfiles
    return maxjobs

def get_infiles(inpath, ext, start, nfiles):
    end = start + nfiles
    jobs = sorted(os.listdir(inpath))
    infiles = [infile for infile in sorted(os.listdir(inpath)) if infile.endswith(ext)]
    return infiles[start:end]

def check_njobs(cmd, log):
    os.system(cmd)
    with open(log, 'r') as njobslog:
        njobs = int(njobslog.read().splitlines()[0])
    return njobs

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
