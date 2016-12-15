#!/usr/bin/python                                                                                               

import os

def get_outpath(jobpath, i, isub):
    return os.path.join(jobpath, '{0}/{1}'.format(i, isub))

def get_outfile(jobpath, jobname, i, isub):
    return os.path.join(jobpath, '{0}/{1}/{2}_{0}_{1}'.format(i, isub, jobname))

def get_outfiles(outfile, softwares):
    outfiles = []
    outfiles.append(outfile + '_ap_fq.zbs')
    outfiles.append(outfile + '_ap_fq.hbk')
    outfiles.append(outfile + '_miura.hbk')
    return ' '.join(outfiles)

def get_bashfile(jobpath, jobname, softwares):
    run_file = os.path.join(jobpath, jobname + '.csh')
    with open(run_file, 'w') as rfile:
        rfile.write('this is a test on the main run file!')
    return run_file

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

def prepare_job(infile, jobpath, jobname, i, isub, nevents, softwares=None):
    outpath = get_outpath(jobpath, i, isub)
    outfile = get_outfile(jobpath, jobname, i, isub)
    outfiles = get_outfiles(outfile, softwares)
    bashfile = get_bashfile(jobpath, jobname, softwares)
    skip = isub*nevents
    sendcmd = 'source {0} {1} {2} {3}'.format(bashfile, outfiles, nevents, skip)
    send_file = write_sendjob(outpath, sendcmd)
    return send_file

def send_job(queue, joblog, sendfile):
    runcmd = 'qsub -q {0} -eo -lm 3gb -o {1} {2}'.format(queue, joblog, sendfile)
    print runcmd
    call_exit(0)
    os.system(runcmd)
