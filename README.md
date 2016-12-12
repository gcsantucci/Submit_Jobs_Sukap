# Submit Jobs

This python package is used to submit multiple jobs using the queue system on sukap machines
(for the Super-Kamiokande experiment).

Parameters need to be set in the parameters.card file located in this directory.
The user must modify the parameters in this file.

More parameters can be added in the main code (submit_jobs.py) by hard coding them. But ideally,
one will change the parameters.py module to read new parameters from parameters.card.

The help_function.py module provides useful functions to build the directories where the output files
will be written. These should not be modified by the user.

## Usage:
python submit_jobs.py --card=[1]

[1]: If using the default card in this directory (parameters.card), just enter d.
To use a different card, enter its name.card, if not in this directory, enter its full path.

## Necessary Structure:
All the files that are to be used as input files need to be in the same directory, they must have the same name except for a number used to differentiate them. For example, name_???.zbs, where ??? goes from 0 to 499 as in the case of 500 years of atm nu MC.

The directory where the input files are located can contain other files that will not be used as input files. But these extra files can not have the same extension as the input files. For example, if name_???.root will be used as input, there can not be other ROOT files in that same directory. But zbs files or txt files or anything else is ok.

This module will divide each input file into n parts that the user can choose and run the selected software on each part.

## The parameters card:
This card contains all the necessary parameters to send the jobs to the queue. The user needs to modify this card before running the submit_jobs module.

### Parameters:
### inpath
The full path for the directory where in input files are located. Ex:
inpath = /disk2/atmpd5/sk4_dst/apr16/fc_mc/zbs_fQv5r0_ntag16c/

### ext:
The type of the input files. For now only zebra (.zbs) and ROOT (.root) files are supported. Ex:
ext = .zbs

### nfiles:
The total number of files to be used as input files. Ex:
nfiles = 500

### startfile:
The number of the first file to be used as input. In case the user wants to run 100 files that range from 200 to 299, just set nfiles to 100 and startfile = 200. Ex:
startfile = 0

### nsubjobs:
The number of files each input file is to be divided. Ex:
nsubjobs = 50

### nevents:
The number of events each sub part will contain. For example, if the inout file has 5000 events and the user wants to divide it in 50 parts, each part will have 100 events. Ex:
nevents = 100

### outpath:
The full path where the directory containing the output files will be located. This directory must exist. Ex:
outpath = /disk2/usr5/santucci/PDK/MC_events/

### outdirname:
The name of the directory where the output files will be written. This directory may or may not exist, see outdirtype. Ex:
outdirname = test

### outdirtype:
- If this is a new job and the output direcory does not exist, set this to new and the directory structure will be created: outdirtype = new
- If the directory already exists and contains files but the user wants to write the output files of these jobs using the same directory set this to same: outdirtype = same
- If the directory exists but it is to be overwritten: outdirtype = over

### jobname:
The common name all the output files will have. Ex:
jobname = test

### email:
The user's email in case an email is to be sent after the jobs are sent to the queue. In case the user does not want to receive emails, just set it to None or False. Ex:
email = user@domain.com

### emailrate:
The rate at which emails will be sent when n = emailrate input files where sent. Ex:
emailrate = 25

### subrate:
The rate for emails, in case the user wants to receive them for every input file but on subpart = subrate. In case the user does not want to receive emails for every input file, just set this to 0. Ex:
subrate = 50

### queue:
The name of the queue to send the jobs, like all or atmpd. Ex:
queue = all

### user:
The name of the user in the queue to check the number of jobs this user already has. Ex:
user = username

### maxjobs:
The maximum number of jobs the user can have running simultaneously in the queue. In case there is no restriction, just set it to -1 and all jobs will be sent without waiting. Ex:
maxjobs = 200

### sleeptime:
The duration of time (in minutes) to wait for a job in the queue to finish in case the max number of jobs in the queue has been reached. Ex:
sleeptime = 20

## Updates:

- Dec 11th 2016: Module runs fiTQun only on zbs and root files.

*** Explicar screen!!