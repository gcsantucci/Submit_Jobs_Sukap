#!/usr/bin/python
'''
This code reads parameters from parameters.card to submit jobs to the queue system in sukap machines.
Documentation and instructions are on the README.md file in this directory.

Author: Gabriel Santucci
gabriel.santucci@stonybrook.edu
Dec 2016
'''

import help_functions as hf
import bash_files as bf
from parameters import get_params

def send_jobs(card):
    strparams, intparams = get_params(card)

    nfiles, startfile, nsubjobs, nevents, emailrate, subrate, maxjobs, sleeptime = intparams
    inpath, ext, outpath, outdirname, outdirtype, jobname, email, queue, user, runfile = strparams
    maxjobs = hf.number_jobs(maxjobs, nsubjobs, nfiles)

    # Create directory structure and log file:
    jobpath = hf.join_path(outpath, outdirname)
    logfile = hf.join_path(jobpath, jobname + '.log')
    hf.check_dirs(outdirtype, jobpath, nfiles, startfile, nsubjobs, logfile, card)

    queue_log = hf.join_path(jobpath, 'running_jobs_{0}.txt'.format(queue))
    queue_cmd = ('qstat {0} | grep {1} | wc -l > ' + queue_log).format(queue, user)

    infiles = hf.get_infiles(inpath, ext, startfile, nfiles)
    for i, infile in enumerate(infiles, start=startfile):
        hf.log_msg(hf.get_time(mode='file').format(i, infile))
        isub = 0
        while isub < int(nsubjobs):
            hf.log_msg(hf.get_time(mode='isub').format(isub))
            currentjobs = hf.check_njobs(queue_cmd, queue_log)
            if currentjobs < maxjobs:
                sendfile, jobfile = bf.prepare_job(infile, jobpath, jobname, i, isub, nevents, runfile)
                bf.send_job(queue, jobfile, sendfile)
                if email and subrate > 0 and isub % subrate == subrate-1:
                    hf.send_email(hf.get_email(isub=True).format(i, infile, isub, email))
                isub += 1
            else:
                hf.log_msg(hf.get_time(mode='sleep').format(maxjobs, sleeptime))
                time.sleep(60*sleeptime)
        if email and i % emailrate == emailrate-1:
            hf.send_email(hf.get_email().format(i, infile, email))
    hf.log_msg(hf.get_time(mode='end').format(queue, user))

def main():
    card = hf.get_card()
    print('\nSending jobs! For progress, check log file on output files directory.\n')
    send_jobs(card)
        
if __name__ == "__main__":
    main()
