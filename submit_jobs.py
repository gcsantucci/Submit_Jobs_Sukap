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

    #check all orders!!!
    nsubjobs, nevents, nfiles, startfile , maxjobs, emailrate, subrate, sleeptime = intparams
    inpath, ext, outdirname, jobname, email, queue, user, outpath, newjob = strparams

    maxjobs = hf.number_jobs(maxjobs, nsubjobs, numFiles)
    hf.num_files(nfiles, startfile, endfile)

    logfile = os.path.join(jobpath, jobname + '.log')
    logging.basicConfig(filename=logfile, level=logging.INFO)
    print('Log file:\n{0}'.format(logfile))

    queue_log = os.path.join(jobpath, '/{0}_njobs.log'.format(queue))
    queue_cmd = 'qstat {0} | grep {1} | wc -l > ' + queue_log
    email_cmd = 'echo "Sent infile {0} to queue." | mailx -s "Job Sent" {1}'
    email_sub ='echo "Sent infile {0}  - subjob {1} - to queue." | mailx -s "Job Sent" {2}'

    infiles = [infile for infile in sorted(os.listdir(inpath)) if infile.endswith(ext)]
    infiles = infiles[startfile:startfile + nfiles]

    jobpath = os.path.join(outpath,jobname)
    hf.check_dirs(newjob, jobpath, len(infiles), nsubjobs)

    for i, infile in enumerate(infiles, start=startfile):
        logging.info('Input file number: {0}:\n{1}'.format(i, infile))
        isub = 0
        while isub < int(nsubjobs):
            os.system(queue_cmd.format(queue, user))
            with open(queue_log, 'r') as njobslog:
                currentjobs = int(njobslog.read().splitlines()[0])
            
            if currentjobs < maxjobs:
                hf.runfiTQun(ijob, jobname, path, isub,nevents)
                #check if -1 is needed or not!!!
                if subrate > 0 and isub % subrate == subrate:
                    os.system(email_sub.format(infile, isub, email))
                isub += 1
            else:
                logging.info(time.asctime( time.localtime(time.time()) ))
                logging.info('sleeping {0} minutes.'.format(sleeptime))
                time.sleep(60*sleeptime)
        if i % emailrate == emailrate:
                    os.system(email_cmd.format(infile, email))
    logging.info('Sent all the jobs!')

def main():
    card = hf.get_card()
    print('\nSending jobs! For progress, check log file on output files directory.\n')
    #send_jobs(card)
        
if __name__ == "__main__":
    main()
