# Submit Jobs

This python package is used to submit multiple jobs using the queue system on sukap machines
(for the Super-Kamiokande experiment).

Parameters need to be set in the parameters.card file located in this directory.
The user can modify the parameters in this file according to own needs. 

More parameters can be added in the main code (submit_jobs.py) by hard coding them. But ideally,
one will change the parameters.py module to read new parameters from parameters.card.

The help_function.py module provides useful functions to build the directories where the output files
will be written. These should not be modified by the user.

## Usage:
python submit_jobs.py --card=[1]

[1]: If using the default card in this directory (parameters.card), just enter d.
To use a different card, enter its name.card, if not in this directory, enter its full path.
