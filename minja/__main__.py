#!/usr/bin/env python

""" minja - dev version """


import signal
import sys
import os
# from core.main import main
from core.init import iworkspace
from core.ui.shell import ishell
from core.data import fpr,tr,tc
from core.func import waitin

__author__    = 'Bartosz Kozak (bakozak@cisco.com)'
__copyright__ = 'Copyright (c) 2016-2018 Bartosz Kozak'
__license__   = 'GNU GPL2'
__version__   = 'dev'
__status__    = 'Dev'


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print sys.path


def sig_handler(signal, frame):
    print
    print 
    fpr.warn('Leaving the session? Press Ctrl+D to leave it, press Enter to return')
    print  


def main():
    try:
        signal.signal(signal.SIGINT, sig_handler)
        iworkspace()
        ishell()
    # except Ctrl+C, Ctrl+D
    # except (KeyboardInterrupt, EOFError):
    except EOFError:
        print
        print
        fpr.err('Interrupted by user! Session lost!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception,error:
        print
        fpr.warn('> Unpredictable Exception has been catched') 
        fpr.err('>>> %s' % str(error) )
        fpr('> Need help regarding the error, please send me a copy. Thank you.')
        fpr.warn('> Restarting main() to keep the session.\n> Please save the session and restart me..')
        waitin()
        main()


if __name__ == '__main__':
    main()

