# --------------------------------------------------------------------------- #
# class of Fancy print 
# --------------------------------------------------------------------------- #

class Fpr:

    BANNER = '\033[95m'
    CYAN   = '\033[1;36m'
    WHITE  = '\033[1;37m'
    YELLOW = '\033[1;33m'
    GRAY   = '\033[1;30m'
    PURPLE = '\033[1;35m'
    BLUE   = '\033[1;34m'
    GREEN  = '\033[92m'
    RED    = '\033[1;31m'

    INFO = '\033[1;30m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    RCL  = '\033[0m'
    DFLT = None
 
    tsauto = 0 
 
    def __init__(self):
        self.TCL = self.RCL 
        self.TCL = self.INFO
        self.FCL = self.INFO
        self.tc, self.tr = self.get_term_size()

    def __call__(self, text, adj='l', ch=' '):
        # set DFLT to some colour to set a default one
        if (self.DFLT):
            self.TCL = self.DFLT
        else:
            self.TCL = self.RCL

        self.fpr(text, adj, ch)

    def warn(self, text, adj='l', ch=' '):
        self.TCL = self.WARN
        self.fpr(text, adj, ch)

    def err(self, text, adj='l', ch=' '):
        self.TCL = self.FAIL
        self.fpr(text, adj, ch)

    def info(self, text, adj='l', ch=' '):
        self.TCL = self.INFO
        self.fpr(text, adj, ch)

    def green(self, text, adj='l', ch=' '):
        self.TCL = self.GREEN
        self.fpr(text, adj, ch)

    def blue(self, text, adj='l', ch=' '):
        self.TCL = self.BLUE
        self.fpr(text, adj, ch)

    def purple(self, text, adj='l', ch=' '):
        self.TCL = self.PURPLE
        self.fpr(text, adj, ch)

    def cyan(self, text, adj='l', ch=' '):
        self.TCL = self.CYAN
        self.fpr(text, adj, ch)

    def white(self, text, adj='l', ch=' '):
        self.TCL = self.WHITE
        self.fpr(text, adj, ch)

    def ok(self, text, adj='l', ch=' '):
        self.TCL = self.RCL
        line = text + ' ' + self.GREEN + ' OK  '.rjust(self.tc-(2*len(ch))-3-len(text) -len(self.GREEN)) 
        #print len(line)
        self.fpr(line, adj, ch)

    def fail(self, text, adj='l', ch=' '):
        self.TCL = self.RCL
        line = text + ' ' + self.FAIL + ' FAIL '.rjust(self.tc-(2*len(ch))-3-len(text) -len(self.FAIL)) 
        #print len(line)
        self.fpr(line, adj, ch)


    def fpr(self, text, adj, ch):
    #def fpr(self, line, adj='l', ch=' '):

        TCL = self.TCL
        RCL = self.RCL
        FCL = self.FCL or self.GREEN
        
        if self.tsauto:
            self.ts_auto_refresh()
        tc = self.tc
        tr = self.tr
#        print (tc,tr)

        lines = text.splitlines()

        for line in lines:
 
            # not so sophisticated fix length formatting
            ll =  len(line)+2*len(' ')+2*len(ch)  
            if ll > tc:
                # x - length of the console column line minus length of
                #     chars on the frame
                x = tc - (2*len(' ')+2*len(ch)) # x = 76 , tc = 80
                #print x
                # s - start position, e - ed position, ll - line length
                s = 0
                e = s + x
                while  e <= ll:
                    self.fpr(line[s:e],adj=adj,ch=ch)
                    s = e
    
                    if e == ll:
                        break
                    if (ll % (e+x)) < ll:
                        e = e + x
                    else:
                        e = e + (ll % e)
                    #print (s,e,x,ll) #DEBUG
            else:     
                if adj == 'l':
                    print ( FCL + ch+' '+TCL+ line.ljust(tc-(2+2*len(ch))) + ' ' +FCL+ ch +RCL)
                if adj == 'r':
                    print ( FCL + ch+' '+TCL+ line.rjust(tc-(2+2*len(ch)))  + ' ' +FCL+ ch +RCL)
                if adj == 'c':
                    print ( FCL + ch+' '+TCL+ line.center(tc-(2+2*len(ch))) + ' ' +FCL+ ch +RCL)



    def ts_auto_refresh(self):
        self.tc, self.tr = self.get_term_size()
        #tc = self.tc
        #tr = self.tr
        #print (tc,tr)
        if self.tc >=80: 
            self.tc = 80
        return self.tc, self.tr

    
    def get_term_size(self):
        import os
        env = os.environ
        def ioctl_GWINSZ(fd):
            try:
                import fcntl, termios, struct, os
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
            '1234'))
            except:
                return
            return cr
        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
            ### Use get(key[, default]) instead of a try/catch
            #try:
            #    cr = (env['LINES'], env['COLUMNS'])
            #except:
            #    cr = (25, 80)
        (self.tc, self.tr) =  (int(cr[1]), int(cr[0]))
        return int(cr[1]), int(cr[0])


