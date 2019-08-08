import os
import re
import errno
import sys
import time
from core.func import os_type
from core.data import cfgs,fpr,DEBUG


def modexists(module_name):
    from pkgutil import iter_modules
    return module_name in (name for loader, name, ispkg in iter_modules())

def iworkspace():

    SECMODE=0700

    fpr('Initialiazing workspace ..') 
    # Directory check
    if os_type() == 'posix':
#        fpr('+ POSIX system found')
#        fpr('+ Directory check')
        for k in cfgs:
            #print k
            if re.match('.*_path$',k):
                #print k,cfgs[k]
                _dir = cfgs[k]
                #if not os.path.exists(_dir):
                if not os.path.isdir(_dir):
                    try:
                        os.makedirs(_dir)
                        fpr.ok('* Creating workspace directory: %s' % _dir )
                    except OSError as exception:
                        fpr.fail('* Creating workspace directory: %s' % _dir )
                        if exception.errno != errno.EEXIST:
                            raise
                        if exception.errno != errno.EACCES:
                            raise
                if os.path.isdir(_dir):
                    if os.path.basename(_dir) in ['keys','logs']:
                        try:
                            os.chmod(_dir,SECMODE)
                        except OSError, e:
                            pass

    if not DEBUG:
        return 0

    # Modules:
    fpr('+ Module checks')
    MODULES=['dkim',]
    for m in MODULES:
        if modexists(m):
            fpr.ok('* module: %s ' % m)
        else:
            fpr.fail('* module: %s ' % m)
        

    # Sessions:  

    # DKIM/S/MIME Keys

    # Certificates


    if DEBUG:
        fpr('Running .. (debug on)')
    else:
        fpr('Running .. ')

    #time.sleep(1)
    #sys.exit(0)

