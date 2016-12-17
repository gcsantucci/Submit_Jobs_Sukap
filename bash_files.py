#!/usr/bin/python                                                                                               
import help_functions as hf
import os

def get_outpath(jobpath, i, isub):
    return os.path.join(jobpath, '{0}/{1}'.format(i, isub))

def get_outfile(jobpath, jobname, i, isub):
    return os.path.join(jobpath, '{0}/{1}/{2}_{0}_{1}'.format(i, isub, jobname))

def get_outfiles(outfile, outfiles):
    return_outfiles = [outfile+outf for outf in outfiles]
    return ' '.join(return_outfiles)

def write_sendjob(outpath, runcmd):
    errstr = '#@$-o ' + outpath + '/test.err'
    send_file = os.path.join(outpath, 'SendJob.csh')
    with open(send_file, 'w') as bash:
        bash.write('#!/bin/csh')
        bash.write(' Batch mode using NQS\n\n')
        bash.write(errstr)
        bash.write(os.linesep)
        bash.write(os.linesep)
        bash.write(runcmd)
        bash.write(os.linesep)
    return send_file

def prepare_job(infile, jobpath, jobname, i, isub, nevents, runfile, outfiles):
    outpath = get_outpath(jobpath, i, isub)
    outfile = get_outfile(jobpath, jobname, i, isub)
    outfiles = get_outfiles(outfile, outfiles)
    skip = isub*nevents
    sendcmd = 'source {0} {1} {2} {3} {4}'.format(runfile, infile, nevents, skip, outfiles)
    sendfile = write_sendjob(outpath, sendcmd)
    jobfile = os.path.join(outpath, jobname+'.log')
    return sendfile, jobfile

def send_job(queue, jobfile, sendfile, qsubtemp):
    runcmd = 'qsub -q {0} -eo -lm 3gb -o {1} {2} > {3}'.format(queue, jobfile, sendfile, qsubtemp)
    os.system(runcmd)

def log_qsub(qsubtemp, qsublog):
    with open(qsubtemp, 'r') as qsub:
        for line in qsub:
            line = line.strip().split()
            jobID = line[-2]
            break
    with open(qsublog, 'a') as jobs:
        jobs.write(jobID + '\n')
    return jobID
