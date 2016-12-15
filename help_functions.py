#!/usr/bin/python                               

import sys
import os
import getopt
import shutil
import time
import logging

from parameters import default_card

def call_exit(islog=0):
    msg = 'Exiting...'
    if islog:
        log_msg(msg, error=True)
    else:
        print(msg)
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
    if os.path.isfile(logfile):
        print('This job already exists. Check log file:\n{0}'.format(logfile))
        print('Change the jobname in the parameters card.')
        call_exit(0)
    logging.basicConfig(filename=logfile, filemode='w', format='%(message)s', level=logging.INFO)
    log_msg(get_time(mode='time'))
    log_msg('Location of log file:\n{0}'.format(logfile))
    log_msg('Using card:\n{0}'.format(card))
    log_msg(get_time(mode='start'))

def log_msg(msg, error=False):
    print(msg)
    if error:
        logging.error(msg)
    else:
        logging.info(msg)

def check_dirs(dirtype, jobpath, nfiles, start, nsubjobs, logfile, card):
    if os.path.isdir(jobpath):
        msg = 'Directory {0} already exists.\n'.format(jobpath)
        if dirtype == 'new':
            msg += 'But user set job as new.'
            start_log(logfile, card)
            log_msg(msg)
            call_exit(1)
        elif dirtype == 'same':
            msg += 'Using the same directory.'
            make_dirs(jobpath, nfiles, start, nsubjobs, same=True)
        elif dirtype == 'over':
            shutil.rmtree(jobpath)
            make_dirs(jobpath, nfiles, start, nsubjobs)
            msg += 'Removing old dir and creating new.'
        else:
            msg += 'Enter [new], [same] or [over] for dirtype in the parameters.card'
            start_log(logfile, card)
            log_msg(msg)            
            call_exit(1)
        start_log(logfile, card)
        log_msg(msg)
    else:
        msg = 'Directory {0} does not exist.\n'.format(jobpath)
        if dirtype == 'new':
            make_dirs(jobpath, nfiles, start, nsubjobs)
            start_log(logfile, card)
            msg += 'Creating necessary directory structure'
            log_msg(msg)
        elif dirtype == 'same' or dirtype == 'over':
            msg += 'Output directory was not found:\n{0}'.format(jobpath)
            msg += '\nChange parameters.card.'
            print(msg)
            call_exit(0)
        else:
            print(msg + 'Enter [new], [same] or [over] for dirtype in the parameters.card')
            call_exit(0)

def make_dirs(jobpath, nfiles, start, nsubjobs, same=False):
    if not same:
        os.mkdir(jobpath)    
    for i in xrange(start, start+nfiles):
        ijob = os.path.join(jobpath, str(i))
        if not os.path.isdir(ijob):
            os.mkdir(ijob)
        for j in xrange(nsubjobs):
            isub = os.path.join(ijob, str(j))
            if not os.path.isdir(isub):
                os.mkdir(isub)

def is_runfile(runfile):
    if not os.path.isfile(runfile):
        msg = 'Run file not found! Check parameters card:\n{0}'.format(runfile)
        log_msg(msg)
        call_exit(1)

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

def get_time(mode=None):
    t0 = time.asctime( time.localtime(time.time()) )
    if mode == 'start':
        msg = '\nStarting submit_jobs.py:'
    elif mode == 'file':
        msg = '\n' + t0 + ' - Input file {0}: {1}'
    elif mode == 'isub':
        msg = 'Subjob {0}'
    elif mode == 'sleep':
        msg = t0 + ' - {0} jobs already running. Sleeping for {1} minutes.'
    elif mode == 'end':
        msg = '\n' + t0 + '\nFinish sending all the jobs! '
        msg += 'Check job status with:\nqstat -a {0} | grep {1}\n'
    elif mode == 'time':
        msg = t0
    else:
        print('Unknown mode for get_time.')
        call_exit(1)
    return msg

def get_email(isub=False):
    email = 'echo "Sent infile {0} {1} to queue." | mailx -s "Job Sent" {2}'
    if isub:
        email ='echo "Sent infile {0} {1} - subjob {2} - to queue." | mailx -s "Job Sent" {3}'
    return email

def send_email(email):
    os.system(email)

def rm_temp(qsubtemp, queuetemp):
    log_msg('\nRemoving temporary log files...')
    os.remove(qsubtemp)
    os.remove(queuetemp)

def sleep(sleeptime):
    time.sleep(sleeptime)
