# Submit Jobs

This python package is used to submit multiple jobs using the queue system on sukap machines
(for the Super-Kamiokande experiment).

Parameters need to be set in the parameters.card file located in this directory.
The user must modify the parameters in this file.

More parameters can be added in the main code (submit_jobs.py) by hard coding them. But ideally,
one will change the parameters.py module to read new parameters from parameters.card.

The help_function.py module provides useful functions to build the directories where the output files
will be written. These should not be modified by the user.

In case of any questions or concerns, send an email to Gabriel Santucci at gabrielsantucci@gmail.com .

## Usage:
python submit_jobs.py --card=[1]

[1]: If using the default card in this directory (parameters.card), just enter card=d or card=parameters.card .

To use a different card, enter its name.card, if not in this directory, enter its full path.

## Necessary Structure:
All the files that will be used as input files need to be in the same directory. This directory can contain other files that will not be used as input files. But these extra files can not have the same extension as the input files. For example, if name_00.root and name_01.root will be used as input, there can not be other ROOT files in that same directory. But zbs files or txt files or anything else is ok.

This module will divide each input file into n parts that the user can choose (nsubjobs). It will send each of these parts to the queue and produce a log file on the main output directory will all the information from the jobs. In this main directory it will also produce a log file with all the job id's running in the queue - useful in case the user wants to check specific job status or cancel jobs.

## The parameters card:
This card contains all the necessary parameters to send the jobs to the queue. The user needs to modify this card before running the submit_jobs module.

### Parameters:
### inpath:
The full path for the directory where in input files are located. Ex:

inpath = /disk2/atmpd5/sk4_dst/apr16/fc_mc/zbs_fQv5r0_ntag16c/

### ext:
The type of the input files. For now only zebra (.zbs) and ROOT (.root) files are supported. Ex:

ext = .zbs

### nfiles:
The total number of files to be used as input files. Ex:

nfiles = 75

### startfile:
The number of the first file to be used as input. In case the user wants to run 75 files that range from 200 to 274, just set nfiles to 75 and startfile = 200. Ex:

startfile = 200

### nsubjobs:
The number of files each input file is to be divided. This has to be at least 1, in case the user does not want to divide the input file at all. Ex:

nsubjobs = 50

### nevents:
The number of events each sub part will contain. For example, if the input file has 5000 events and the user wants to divide it in 50 parts, each part will have 100 events. Ex:

nevents = 100

### outpath:
The full path where the directory containing the output files will be located. This directory must exist. Ex:

outpath = /disk2/usr5/user/

### outdirname:
The name of the directory where the output files will be written. This directory may or may not exist, see outdirtype. Ex:

outdirname = test

### outdirtype:
new, same or over:
- If this is a new job and the output directory does not exist, set this to 'new' and the directory structure will be created: outdirtype = new
- If the directory already exists and contains files but the user wants to write the output files of these jobs using the same directories, set this to 'same': outdirtype = same
- If the directory exists but it is to be overwritten, set it to 'over': outdirtype = over

outdirtype = new

### jobname:
The common name all the output files will have. Ex:

jobname = test

### runfile:
The full path location of the main Bash or cShell script that the user wants to run. It is necessary that the it receives first the input file, the number of events each job will run and the number of events to skip, so:

$1 = input_file, $2 = nevents, $3 = nskip. This code will pass the correct arguments for these inputs plus the other necessary parameters that the user has to set (see outfiles). Check the RunJob.csh in this repo for an example. Ex:

runfile = /home/user/RunJob.csh

### outfiles:
The extension for the necessary output files for running the main script. For example, if the user is running 2 analysis on the input file: first apfit and then fiTQun on the output of apfit. Then one possible choice is '_ap.zbs' for the first and '_ap_fq.zbs' for the second. Separate them by a space only. Ex:

outfiles = _fq.zbs _fq.hbk

### email:
The user's email in case an email is to be sent after the jobs are in the queue. In case the user does not want to receive emails, just set it to None or False. Ex:

email = user@domain.com or email = None

### emailrate:
The rate at which emails will be sent, every n = emailrate input files. Ex:

emailrate = 25

### subrate:
The rate for emails, in case the user wants to receive them for every input file but on subpart = subrate. In case the user does not want to receive emails for every input file, just set this to 0. Ex:

subrate = 50

### queue:
The name of the queue to send the jobs, like all or atmpd. Ex:

queue = all

### user:
The name of the user in the queue. Ex:

user = username

### maxjobs:
The maximum number of jobs the user can have running simultaneously in the queue. In case there is no restriction, just set it to -1 and all jobs will be sent without waiting. Ex:

maxjobs = 200

### sleeptime:
The duration of time (in minutes) to wait for a job in the queue to finish in case the max number of jobs in the queue has been reached. Ex:

sleeptime = 20

## Example:
The parameters.card in this repository will get 2 (nfiles=2) atm nu MC files from /disk2/atmpd5/sk4_dst/apr16/fc_mc/zbs_fQv5r0_ntag16c/ with the .zbs extension. Those will be files 9 and 10 (startfile=9). Each input file will be broken in 2 pieces, each piece with 3000 events.

The outputs will be written in /disk2/usr5/user/outputs in a directory called test. The output files will be called test_x1_x2_fq.zbs, where x1 corresponds to the input file number and x2 the subpart of this file.

The main script provided by the user is located in /home/scripts/Test.csh and it runs fiTQun plus fillnt on fiTQun's output. So the first 2 output files will be test_9_0_fq.zbs and test_9_0_fq.hbk.

The user will receive 1 email after each input file has been sent, but no email for subparts. The jobs will run in the queue=all. SK maximum number of jobs is being respect so maxjobs = 200. If the user already has 200 jobs running in that queue, this script will wait 10 minutes before checking again for the current number of jobs running.

In the output directory 2 log files will be produced. jobname.log has the information of all the jobs sent and jobname_running_jobs.log is a list of all job ID's running in the queue that were sent in this section.

## Cancelling Jobs:
To cancel all the jobs that submit_jobs.py sent to the queue, one can run kill_jobs.py (in this repo) with:

python kill_jobs.py --file=/path/to/jobname_running_jobs.log

Where jobname_running_jobs.log is the list with all job ID's sent to the queue by submit_jobs.

## Recommendations
Since sukap has restrictions on the maximum number of jobs a user can send, it is better to run this module using screen. Simply type 'screen' on the terminal to enter a screen. This is a clean shell, so set up again your enviroment if needed and run submit_jobs.py.
Enter Crtl-ad to exit the screen using closing. The user can check how many screens are openned by typing 'screen -ls' and re-enter a screen by 'screen -x screen_id'. Once submit_jobs is done, the user can exit the screen by entering 'exit'. 

## Updates:

- Dec 11th 2016: Module runs fiTQun on zbs and root files.
- Dec 15th 2016: Module runs any software specified by the user on the runfile, provided the necessary number of arguments for output files has been provided.