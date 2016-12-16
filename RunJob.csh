#!/bin/csh     
                                                          
#                                                                               
# Batch mode using NQS
# Usage: [input file] [nevents] [nskip] [FQout.zbs] [FQout.hbk]

#@$ -o /home/santucci/jobs/log/test.out
#@$ -e /home/santucci/jobs/log/test.er

source /home/santucci/fiTQun/setup_sksvn.csh

date
$FITQUN_ROOT/runfiTQun -n $2 -s $3-o $4 $1
date

/home/santucci/fiTQun/PDK_fiTQun/fiTQun/fillnt_simple.sh -o $5 $4

date

