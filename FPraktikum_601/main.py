# -*- coding: future_fstrings -*-

# This is the stand alone version of the pyFAT moments to create moment maps

#from optparse import OptionParser

from FPraktikum_601.convert_spectrum.convert_spectrum import raw_to_clean
from FPraktikum_601.config.config import process_input
import sys
import traceback
import warnings
from multiprocessing import get_context,Manager

def warn_with_traceback(message, category, filename, lineno, file=None, line=None):
    log = file if hasattr(file,'write') else sys.stderr
    traceback.print_stack(file=log)
    log.write(warnings.formatwarning(message, category, filename, lineno, line))





def main():
    argv = sys.argv[1:]
    cfg = process_input(argv)
    # for some dumb reason pools have to be called from main
    # !!!!!!!!Starts your Main Here
    raw_to_clean(cfg)






if __name__ =="__main__":
    main()
