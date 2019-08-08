
__all__= [
 'banner',
 'bancls',
 'bancls2',
]


import os          # banner
import threading   # bancls2
from core.data import smtp,fpr,tr,tc

def banner():

    global tc
    global tr 

    tc, tr = fpr.ts_auto_refresh()

    fpr('='*(tc-4),ch='|')
    fpr.DFLT = fpr.GREEN
    fpr('sMtP mInjA (v=dev080819-2325)', 'c', '|' )
    fpr.DFLT = fpr.BLUE
    fpr('='*(tc-4),ch='|')
    fpr.DFLT = fpr.RCL
    print

def bancls():
    os.system('clear')
    banner()

def bancls2(thr=[],i=1,opt='replay'):
    bancls()


    def isActive(t):
    #    print t.getName()
        if t.isAlive():
            return fpr.CYAN+'Active'+fpr.RCL
        elif t.getName() in smtp[opt]['threads']['fail']:
            return fpr.RED+'Failed'+fpr.RCL
        else:
            return fpr.GREEN+'Finish'+fpr.RCL

    if thr:
    #main_thread = threading.currentThread()
        #for t in threading.enumerate():
#        print 'Threads: Total ',len(thr)  ,' Active ',len(threading.enumerate()),' Finish ',len(thr)-len(threading.enumerate()) 
        # remember about MainThread, so -1 or +1 :)
        print            '  Threads: Total ',fpr.GREEN,len(thr),fpr.RCL, \
                         ' Active ',fpr.CYAN,(len(threading.enumerate())-1),fpr.RCL, \
                         ' Finish ',fpr.GREEN,len(thr)-len(threading.enumerate())+1,fpr.RCL, \
                         ' Success ',fpr.GREEN,len(smtp[opt]['threads']['ok']),fpr.RCL, \
                         ' Failed',fpr.RED,len(smtp[opt]['threads']['fail']),fpr.RCL

        fpr.blue('_'*(tc-4))
        print
        status = ''
        line = 80
        s = 0 
        for t in thr:
            mlen = 14
            #print (line % (s+mlen+1) ) 
            if (line % (s+mlen+1) ) < line:
                status += "  %-4s %s "% (t.getName(), isActive(t)) 
                s += mlen + 1
            else:
                status += "\n  %-4s %s " % (t.getName(), isActive(t))
                s = mlen + 1
            #print s

        print '%s' % status
    fpr.blue('_'*(tc-4))
    #print '-' *80
#    print threading.enumerate()

# --------------------------------------------------------------------------- #

