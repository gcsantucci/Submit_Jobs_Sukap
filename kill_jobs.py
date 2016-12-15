import getopt
import os
import sys

def kill_jobs(infile):
    counter = 0
    with open(infile,'r') as kfile:
        for line in kfile:
            line = line.strip()
            kill = 'qdel {0}'.format(line)
            print('Cancelling job {0}'.format(line))
            os.system(kill)
            counter += 1

    print('Canceled {0} jobs!'.format(counter))

def usage():
    usage_msg = '''                                                                     
Usage:\n                                                                                    
    python kill_jobs.py --file=full/path/to/file
'''
    print(usage_msg)

def get_infile():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                                       'h',
                                       ['help', 'file='])
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(2)

    infile = None
    if len(opts) == 0:
        usage()
        sys.exit(0)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('--file'):
            infile = arg
        else:
            assert False, 'unhandled option' + opt

    if os.path.isfile(infile):
        return infile
    else:
        print('File not found:\n{0}\nExiting...'.format(infile))
        sys.exit(0)

def main():
    infile = get_infile()
    print('Using file:\n{0}'.format(infile))
    kill_jobs(infile)

if __name__ == '__main__':
    main()
