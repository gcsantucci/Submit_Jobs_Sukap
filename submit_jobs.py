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

import help_functions as hf
from parameters import get_params

def send_jobs(card):
    strparams, intparams = get_params(card)
    nsubjobs, nevents, numFiles, numskip, endfile, MaxNJobs, time_to_sleep = intparams
    filespath, jobname, path = strparams

    for ijob in range(numFiles):

        print 'file = ' , ijob
        hf.mkjobdir(path, jobname, ijob)
        isub = 0
        while isub < int(nsubjobs):
            os.system('qstat all | grep santucci | wc -l > ' + outpath + '/Njobs_logL.log')
            jobfile = open(outpath + "/Njobs_logL.log", "r")
            currentNJobs = int(jobfile.read().splitlines()[0])
            jobfile.close()
            
            if currentNJobs < MaxNJobs:
                hf.runfiTQun(ijob, jobname, path, isub,nevents)
                if (isub % 50 == 49):
                    os.system('echo "Finished isubjob = %d for %s" | mailx -s "Job Done" gabrielsantucci@gmail.com' % (isub, jobname))
                isub += 1
            else:
                print(time.asctime( time.localtime(time.time()) ))
                print ('sleeping ' + str(time_to_sleep) + ' min, ijob = ', ijob)
                time.sleep(60*time_to_sleep)

    print ("Sent all the jobs!")

def main():
    card = hf.get_card()
    run = raw_input('\nIf this card is correct and you wanna proceed enter [y],\notherwise type [n]:\n')
    if run == 'y':
        print('\nSending jobs! For progress, check log file on job directory.\n')
        #send_jobs(card)
    else:
        print('\nUser chose not to proceed. Exiting...\n')
        sys.exit(0)
        
if __name__ == "__main__":
    main()
