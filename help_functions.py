#!/usr/bin/python                               

import sys
import os
import getopt
import shutil
import time
import logging

from parameters import default_card

log = logging

def call_exit(islog=0):
    msg = 'Exiting...'
    print(msg)
    if islog:
        log_msg(msg, error=True)
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
        call_exit(0)
        
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            call_exit(0)
        elif opt in ('--card'):
            card = arg
        else:
            assert False, 'unhandled option' + opt

    if card == 'd' or card == 'parameters.card':
        card = default_card
    is_card(card)
    return card

def is_card(card):
    if not os.path.isfile(card):
        print('Parameters card does not exist:\n{0}'.format(card))
        call_exit(0)

def join_path(path, name):
    return os.path.join(path, name)

def start_log(logfile, card):
    log.basicConfig(filename=logfile, format='%(message)s', level=logging.ERROR)
    log_msg('Location of log file:\n{0}'.format(logfile))
    log_msg('Using card:\n{0}'.format(card))
    log_msg(get_time(mode='start'))

def log_msg(msg, error=False):
    print(msg)
    if error:
        log.error('Error!\n' + msg)
    else:
        log.info(msg)

def check_dirs(dirtype, jobpath, nfiles, start, nsubjobs, logfile, card):
    if os.path.isdir(jobpath):
        start_log(logfile, card)
        msg = 'Dir {0} already exists.\n'.format(jobpath)
        if dirtype == 'new':
            msg += 'But user set job as new.'
            log_msg(msg)
            call_exit(1)
        elif dirtype == 'same':
            msg += 'Using the same directory.'
            log_msg(msg)
        elif dirtype == 'over':
            msg += 'Removing old dir and creating new.'
            log_msg(msg)
            shutil.rmtree(jobpath)
            make_dirs(jobpath, nfiles, start, nsubjobs)
        else:
            msg += 'Enter [new], [same] or [over] for dirtype in the parameters.card'
            log_msg(msg)            
            call_exit(1)
    else:
        msg = 'Dir {0} does not exist.\n'.format(jobpath)
        if dirtype == 'new':
            start_log(logfile, card)
            msg += 'Creating necessary directory structure'
            log_msg(msg)
            make_dirs(jobpath, nfiles, start, nsubjobs)
        elif dirtype == 'same' or dirtype == 'over':
            msg += 'Output directory was not found:\n{0}'.format(jobpath)
            msg += '\nChange parameters.card.'
            print(msg)
            call_exit(0)
        else:
            print(msg + 'Enter [new], [same] or [over] for dirtype in the parameters.card')
            call_exit(0)

def make_dirs(jobpath, nfiles, start, nsubjobs):
    os.mkdir(jobpath)    
    for i in xrange(start, start+nfiles):
        ijob = os.path.join(jobpath, str(i))
        os.mkdir(ijob)
        for j in xrange(nsubjobs):
            isub = os.path.join(ijob, str(j))
            os.mkdir(isub)

def number_jobs(maxjobs, nsubjobs, nfiles):
    if maxjobs == -1:
        maxjobs = nsubjobs * nfiles
    return maxjobs

def get_infiles(inpath, ext, start, nfiles):
    end = start + nfiles
    jobs = sorted(os.listdir(inpath))
    infiles = [infile for infile in jobs if infile.endswith(ext)]
    return infiles[start:end]

def check_njobs(cmd, log):
    os.system(cmd)
    with open(log, 'r') as njobslog:
        njobs = int(njobslog.read().splitlines()[0])
    return njobs

def get_time(mode=None, sub=False):
    t0 = time.asctime( time.localtime(time.time()) )
    msg = '\nCurrent time: {0}\n'.format(t0)
    if mode == 'start':
        msg += 'Starting submit_jobs.py'
    elif mode == 'file':
        msg += 'Starting input file {0}:\n{1}'
    elif mode == 'isub':
        msg += 'Starting subjob {0} for input file:\n{1}'
    elif mode == 'sleep':
        msg += '{0} jobs already running. Sleeping for {1} minutes.'
    elif mode == 'end':
        msg += 'Finish sending all the jobs!'
    else:
        print('Unknown mode for get_time.')
        call_exit(1)
    return msg

def get_email(isub=False):
    email = 'echo "Sent infile {0} {1} to queue." | mailx -s "Job Sent" {2}'
    if email:
        email ='echo "Sent infile {0} {1} - subjob {2} - to queue." | mailx -s "Job Sent" {3}'
    return email

def send_email(email):
    log_msg(email)
    os.system(email)

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
