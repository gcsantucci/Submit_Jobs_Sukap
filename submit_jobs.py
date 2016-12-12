#!/usr/bin/python
'''
This code reads parameters from parameters.card to submit jobs to the queue system in sukap machines.
Documentation and instructions are on the README.md file in this directory.

Author: Gabriel Santucci
gabriel.santucci@stonybrook.edu
Dec 2016
'''

import sys
import os
import time
import logging

import help_functions as hf
from parameters import get_params

def send_jobs(card):
    strparams, intparams = get_params(card)

    nfiles, startfile, nsubjobs, nevents, emailrate, subrate, maxjobs, sleeptime = intparams
    inpath, ext, outpath, outdirname, outdirtype, jobname, email, queue, user = strparams

    maxjobs = hf.number_jobs(maxjobs, nsubjobs, nfiles)

    infiles = hf.get_infiles(inpath, ext, startfile, nfiles)

    jobpath = os.path.join(outpath, outdirname)
    hf.check_dirs(outdirtype, jobpath, nfiles, startfile, nsubjobs)

    logfile = os.path.join(jobpath, jobname + '.log')
    logging.basicConfig(filename=logfile, format='%(message)s', level=logging.INFO)
    print('\nLog file:\n{0}'.format(logfile))

    queue_log = os.path.join(jobpath, '{0}_njobs.log'.format(queue))
    queue_cmd = 'qstat {0} | grep {1} | wc -l > ' + queue_log
    email_cmd = 'echo "Sent infile {0} {1} to queue." | mailx -s "Job Sent" {2}'
    email_sub ='echo "Sent infile {0} {1}  - subjob {2} - to queue." | mailx -s "Job Sent" {3}'

    for i, infile in enumerate(infiles, start=startfile):
        logging.info('Input file {0}: {1}'.format(i, infile))
        isub = 0
        while isub < int(nsubjobs):
            logging.info('Subjob = {0}'.format(isub))
            os.system(queue_cmd.format(queue, user))
            with open(queue_log, 'r') as njobslog:
                currentjobs = int(njobslog.read().splitlines()[0])
            if currentjobs < maxjobs:
                #hf.runfiTQun(ijob, jobname, path, isub,nevents)
                if email and subrate > 0 and isub % subrate == subrate-1:
                    os.system(email_sub.format(i, infile, isub, email))
                isub += 1
            else:
                logging.info(time.asctime( time.localtime(time.time()) ))
                logging.info('sleeping {0} minutes.'.format(sleeptime))
                time.sleep(60*sleeptime)
        if email and i % emailrate == emailrate-1:
            os.system(email_cmd.format(i, infile, email))
    logging.info('Sent all the jobs!')

def main():
    card = hf.get_card()
    print('\nSending jobs! For progress, check log file on output files directory.\n')
    send_jobs(card)
        
if __name__ == "__main__":
    main()
