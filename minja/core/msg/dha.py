# --------------------------------------------------------------------------- #
# dha threads 
# --------------------------------------------------------------------------- #

import re                                    # get_rate()
import ctypes                                # get_tid()
import time
import threading




from core.data import smtp,fpr,tc,tr,DEBUG        # get_threads_no(), get_rcpt_no(), get_msg_no()
from core.data import MAX_THREADS,MAX_CMD_PER_TH,TH_DELAY,TH_TIMEOUT

from core.func import info, set_dval, get_yesno_input, dbginfo, info
from core.ui.banner import bancls2
from core.msg.threads import get_rcpts

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def get_cpt_no():

#    set_dval(q='  Set CPT', dd=smtp['dha']['threads'], key='cpt', val=None)

    info('info','Note: CPT defines a number of commands sent per single thread where each \n' \
                '      thread is a a new SMTP connection which need to be established.\n\n' \
                '      * CPT = NOR / NOT\n' \
                '      * CPT can not be greater than number of recipients (NOR) \n' \
                '      * CPT is recounted when NOT is changed.\n' \
                '      * CPT is equal NOR by default ', adj='l'

        )
    print



    n = raw_input('  [%s]> ' % smtp['dha']['threads'].get('cpt',None)) \
        or smtp['dha']['threads'].get('cpt',None)
    if n == None: 
        return

    MAX_COMMANDS = 1000
    if type(n) is int or n.isdigit():
        print
        if 0 < int(n) < MAX_COMMANDS:
            #    smtp['dha']['threads']['cpt'] = int(n)
            #    fpr.ok('%s'%n)
            if chDHAThrDep(cpt=int(n)):
               fpr.ok('%s'%n)

        else:
            fpr.fail('Setting CPT as %s' % n)




# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def get_threads_no():

    info('info','Note: NOT defines the number of threads where each thread is a new separate' \
                '      and simultaneous connection. \n' \
                '      * NOT = NOR / CPT \n' \
                '      * NOT is 1 by default \n' \
                '      * NOT value should be keep between 1 - %s \n' \
                '      * NOT is recounted when CPT is changed' % MAX_THREADS, adj='l'

                       
    )
    print





    n = raw_input('  [%s]> ' % smtp['dha']['threads'].get('not',None)) \
        or smtp['dha']['threads'].get('not',None)
    if n == None: 
        return

    if type(n) is int or n.isdigit():
        print
        if 0 < int(n) < MAX_THREADS:
#                smtp['dha']['threads']['not'] = int(n)
#                fpr.ok('%s'%n)
            if chDHAThrDep(t=int(n)):
               fpr.ok('%s'%n)

        else:
            fpr.fail('Setting NoT as %s' % n)


# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def get_delay():

    info('info','Note: Delay is number of miliseconds between starting new threads, \n' \
                '      where each new thread is a new SMTP connection.', adj='l'
        )
    print

    n = raw_input('  [%s]> ' % smtp['dha']['threads'].get('delay',TH_DELAY)) \
           or smtp['dha']['threads'].get('delay',TH_DELAY)
    
    if n and (type(n) is int or n.isdigit()):
        if 0 <= int(n):
            print
            smtp['dha']['threads']['delay']=int(n)
            fpr.ok('%s'%n)
        else:
            print
            fpr.fail('%s'%n)


# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def get_timeout():

    info('info','Note: Time waiting for server reply', adj='l' )
    print

    n = raw_input('  [%s]> ' % smtp['dha']['threads'].get('timeout',TH_TIMEOUT)) \
           or smtp['dha']['threads'].get('timeout',TH_TIMEOUT)
    
    if n and (type(n) is int or n.isdigit()):
        if 0 <= int(n):
            print
            smtp['dha']['threads']['timeout']=int(n)
            fpr.ok('%s'%n)
        else:
            print
            fpr.fail('%s'%n)

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def chDHAThrDep(t=None,cpt=None):

#VERIFY:  In Python 2.x : int/int --> int and int/float --> float In Python 3.x : int/int can result in a float 

    r=get_rcpts('NoR')
    t_s=None
    cpt_s=None

    if not r:
       fpr.err('Recipients not defined. Build a list of recipients first.')
       fpr.err('Flush the values if the recipient list has been modified.')
       return

    if t:
       smtp['dha']['threads']['not'] = int(t)
       
    if cpt:
       smtp['dha']['threads']['cpt'] = int(cpt)
       

    fpr.info('_'*(tc-4))
    print
    fpr.warn('Your limits:')
    fpr.warn('t_set = %s : cpt_set = %s :  r = %s' % 
             (smtp['dha']['threads'].get('not',None),
              smtp['dha']['threads'].get('cpt',None),r) 
           )
    print 
#    fpr.err('Maximum possible limits to met Essential Conditions:')
#    fpr.err('t = %s : rpm = %s : mpt = %s - r = %s' % (t,rpm,mpt,r) )
#    fpr.info('_'*(tc-4))

    print

    def setReals(t,cpt):
        
        if t and cpt :
           smtp['dha']['threads']['reals'].setdefault('not',t)
           smtp['dha']['threads']['reals'].setdefault('cpt',cpt)

           smtp['dha']['threads']['reals']['not']=t
           smtp['dha']['threads']['reals']['cpt']=cpt
           fpr.ok('Reals were set!')



    if r:

       # count the cpt - based on r and t
       # -------------------------------------------------------------------- #
       if t:
           fpr.green('%s : %s : %s' % (t,cpt,r) )
           # cpt = r / t
           # t = r / cpt
           if t >= r:
              t_new = r
              cpt = 1
              fpr.err('realistic returns would be: t = %s, cpt = %s  for r = %s' %
                   (t_new,cpt,r))
              setReals(t_new,cpt)
           if t < r:
             # I - validate CPT - CPT < R
             cpt = float(r) / t
             fpr.green('counted cpt = %s' % cpt)
             # round up - if there is a remainder 
             if (r %  t > 0):
                 cpt = r / t + (r % t > 0)
                 fpr.green('rounding up cpt = %s' % cpt)

                 # find the lowest T for rounded CpT
                 t_new = float(r) / cpt 
                 fpr.green('counted new t = %s' % t_new)
 
                 #if (r % cpt > 0): # if remainder
                 #    t_new = r /  cpt + ( r % cpt > 0)
                 #    fpr.green('rounding up new t = %s' % t_new)
                 #    fpr.err('realistic returns would be: *t = %s, cpt = %s  for r = %s' %
                 #       (int(t_new),int(cpt),r))
                 #    setReals(int(t_new),int(cpt))
                 #else:
                 fpr.err('realistic returns would be: *t = %s, cpt = %s  for r = %s' %
                     (int(t_new),int(cpt),r))
                 setReals(int(t_new),int(cpt))

             else:
                 fpr.err('realistic returns would be: t = %s, cpt = %s  for r = %s' %
                    (t,int(cpt),r))
                 setReals(int(t),int(cpt))
       elif cpt:

           fpr.green('%s : %s : %s' % (t,cpt,r) )
           # cpt = r / t
           # t = r / cpt
           if cpt >= r:
              cpt_new = r
              t = 1
              fpr.err('realistic returns would be: t = %s, cpt = %s  for r = %s' %
                   (t,cpt_new,r))
              setReals(t,cpt_new)
           if cpt < r:
             # I - validate T - t < R
             t = float(r) / cpt
             fpr.green('counted t = %s' % t)
             # round up - if there is a remainder 
             if (r %  cpt > 0):
                 t = r / cpt + (r % cpt > 0)
                 fpr.green('rounding up t = %s' % t)

                 # find the lowest T for rounded CpT
                 cpt_new = float(r) / t 
                 fpr.green('counted new cpt = %s' % cpt_new)
 
                 fpr.err('realistic returns would be: *t = %s, cpt = %s  for r = %s' %
                     (int(t),int(cpt_new),r))
                 setReals(int(t),int(cpt_new))

             else:
                 fpr.err('realistic returns would be: t = %s, cpt = %s  for r = %s' %
                    (t,int(cpt),r))
                 setReals(int(t),int(cpt))
       else:
            fpr.err('err')


    else:
       fpr.err('Recipients not defined. Build a list of recipients first.')
       fpr.err('Flush the values if the recipient list has been modified.')






# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def flushDHAThrValues():



    if get_yesno_input('  Flush DHA thread settings [y/N]: '):
        smtp['dha']['cmd'] = 'RCPT TO'
        smtp['dha']['threads']['not'] = None
        smtp['dha']['threads']['delay'] = TH_DELAY
        smtp['dha']['threads']['timeout'] = TH_TIMEOUT
        smtp['dha']['threads'].pop('cpt', None)
        smtp['dha']['threads']['reals'].pop('not',None)
        smtp['dha']['threads']['reals'].pop('cpt',None)
        fpr.info('DHA threads settings were flushed !')



# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def viewDHAThreadsSummary():

    print
    print
    fpr(' SMTP Command                  : %s' % smtp['dha'].get('cmd') )
    print
    fpr(' Defaults: NOT=1, CPT=NOR')

    fpr.info('                               |   set  | counted ')
    fpr(' NOT - Number Of Threads       :  %4s  |  %4s  ' % 
          ( smtp['dha']['threads'].get('not',None),
            smtp['dha']['threads']['reals'].get('not',None) ) )
    fpr(' CPT - Commands Per Thread     :  %4s  |  %4s  ' % 
          ( smtp['dha']['threads'].get('cpt',None),
            smtp['dha']['threads']['reals'].get('cpt',None) ) )
    print
    fpr(' TIMEOUT between queries run   :  %s ms' % 
            smtp['dha']['threads'].get('timeout',None))
    fpr(' DELAY between threads run     :  %s ms' % 
            smtp['dha']['threads'].get('delay',None))

#    print 
#    fpr.info(' -- recipients --')
    print
    fpr(' NOR - Number of Recipients    : %d' % get_rcpts('NoR')  )
    fpr.info(' Number of Destination Domains : %d' % get_rcpts('domains') )
    fpr.info(' Number of Destination Hosts   : %d' % get_rcpts('hosts')   ) 
    
    print 


# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def runDHAThreads():

    viewDHAThreadsSummary()
    print

    if  smtp['addrlist']['r_reject'].keys() or  smtp['addrlist']['r_valid'].keys():
        fpr('Flushing currently found results (valid/refused recipients) ..')

    del smtp['dha']['threads']['ok'][:]
    del smtp['dha']['threads']['fail'][:]
    smtp['addrlist']['r_reject'].clear()
    smtp['addrlist']['r_valid'].clear()

    from pprint import pprint

    if smtp['dha'].get('cmd') != 'RCPT TO':
        #chek if sysem support EXPN/VRFY command before threading 
        print
        if get_yesno_input('  Would you like to test an SMTP server for %s method before threading [y/N]: ' % smtp['dha'].get('cmd')):
           sc = enumSMTPcmd(v=False,dhost=smtp['connect']['hosts'][0])
           #     enumSMTPcmd(v=True,dhost=smtp['connect']['hosts'][0]):
           #pprint(sc)
           #if smtp['connect']['hosts'][0]['tls_mode'] == 'TLS':
           #print smtp['dha'].get('cmd') 
           if smtp['dha'].get('cmd') in sc['method']:
               fpr.ok('Method %s is supported' % smtp['dha'].get('cmd'))
           else:
               fpr.fail('Method %s is unsupported' % smtp['dha'].get('cmd'))
               print
               fpr('Consider to change an SMTP method!')
               print

    t = srThread()
    t.daemon   = True
    t.delay    = smtp['dha']['threads'].get('delay',1)
    t.threads  = smtp['dha']['threads']['reals'].get(
                   'not',smtp['dha']['threads'].get('not',1)
                 )
    t.cpt      = smtp['dha']['threads']['reals'].get(
                    'cpt',smtp['dha']['threads'].get('cpt',get_rcpts('NoR'))
                 )
    t.method  = smtp['dha'].get('cmd')
    t.rcpts = smtp['addrlist']['rcpts'] 

    #print get_rcpts('NoR')
    if get_rcpts('NoR'):
        if raw_input('  Confirm threading [y/N]:> ') in ['y','Y']:
            # enable logging
            from core.msg.sender import Logger
            logger = Logger()
            t.run()
            logger.close()
        else:
            print 
            fpr.err('Threading were Cancaled!')
    else:
        print
        fpr.err('Err. No recipients defined!')
 
#import time
#import threading
#from core.data import fpr,tc,tr,DEBUG
#from core.func import dbginfo
#from core.msg.sender import smtp_sender

# --------------------------------------------------------------------------- #
# class: srThread
# --------------------------------------------------------------------------- #
class srThread(object):


    msg = None 

    def __init__(self, interval=1,threads=1,daemon=True,delay=1,
                       cpt=1,rate=1,rcpts=[],smtpcmd='RCPT TO'):


        self.interval = interval  # threading join interval
        self.threads  = threads
        self.daemon   = daemon
        #self.rpt      = rpt       # recipient per thread
#        self.rpm      = rpm       # recipient per message
#        self.mpt      = mpt       # message per thread
#        self.rate     = rate      # rate - rexipients per s/m/h
        self.cpt      = cpt       # commands per thread
        self.delay    = delay     # delay - delay between starting new thread (connection)
        self.rcpts    = rcpts
        self.method   = smtpcmd

        dbginfo('debug','Init: NoT=%s, CPT=%s SMTPMethod=%s' % (self.threads,self.cpt,self.method))
        dbginfo('debug','Init: %s' % self.rcpts)
 
    def run(self):

        dbginfo('debug','Run: NoT=%s, CpT=%s, SMTPMethod=%s' % (self.threads,self.cpt,self.method))
        dbginfo('debug','Run: Rcpts: %s' % self.rcpts)
        #return 

        # count number of recipients per threads
        rpt = 0
        rpt = self.cpt

        thr = []
        for i in range(self.threads):

            # i - thread number - count from zero 


            # split rcpts list per threads
            si = i*rpt
            ei = i*rpt + rpt
            t_rcpts = self.rcpts[si:ei]

            dbginfo('debug','Thread: Rcpts: %s' % t_rcpts)

            # declare thread
            t = threading.Thread(target=smtp_dha, 
                                 kwargs=dict(
                                         #message=self.msg,
                                         cpt=self.cpt,
                                         #rate=self.rate,
                                         rcpts=t_rcpts,
                                         method=self.method,
                                         name='T-%d' % i,
                                         v=False) , 
                                   name='T-%d' % i, verbose=None,  )
            t.setDaemon(self.daemon)
            #t.setName('t-%d'%i)
            thr.append(t)
            t.start()
            bancls2(thr,i,opt='dha')
            # delay between starting new connection (threads)
            time.sleep(self.delay/1000.0)

        bancls2(thr,0,opt='dha')

        while threading.activeCount()>1:
            i=1
            for j in thr:
                j.join(self.interval)
                i=i+1
                bancls2(thr,i,opt='dha')




# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def enumSMTPcmd(v=None,dhost=smtp['connect']['hosts'][0]):



    #TODO: if no EHLO , use HELO 

    from pprint import pprint

    # secure extn - list of extn received after successfull STARTTLS commands
    scmds = {  'extn' : [], 'secure_extn': [],  'cmds': '', 'method': [], }  


    #pprint(dhost)
    #pprint(scmds)


    print
    try:

         import sys
         import smtplib

         # run smtp session
         if v:
            fpr.white('Establishing the session with %s on port %s' % (dhost['host'],dhost['port']))
         s = smtplib.SMTP(dhost['host'],dhost['port'])

         if v:
            fpr.cyan('>>> %s' % 'HELP')
         r = s.help()
         scmds['scmds'] = r
         if v:
             fpr.green('<<< %s' % r)


#         if cfgs['conv_logs'] and cl:
#            s.set_debuglevel('debug')

         # HELO - introduce yourself
         if v:
            fpr.cyan('>>> %s %s' % ('EHLO',dhost['helo']))
         (c,m) = s.ehlo(dhost['helo'])
         #r = s.helo(smtp['connect']['hosts'][0]['helo'])

            #print (c,m)

         if 200 <= c <= 299:
             if v:
                 fpr.green('<<< %s %s' %(c,m))
             if s.does_esmtp:
                 if v:
                    fpr.white('ESMTP supported and have extn:')
                    #print s.does_esmtp
                    #print s.esmtp_features
                 for (scmd,sarg) in s.esmtp_features.items():
                    if v:
                        fpr.white('  * %s %s' % (scmd,sarg))
                    scmds['extn'].append((scmd,sarg))
         elif 500 <= c <= 599:
             fpr.err('<<< %s %s' %(c,m))

         # STAARTTLS
         if 'starttls' in s.esmtp_features.keys():
             if dhost['tls_mode'] == 'TLS':
                 if v:
                     fpr.white('TLS supported and requested')
                     fpr.white('Establishing TLS session ..')
                     fpr.cyan('>>> %s' % ('STARTTLS'))
                 (c,m) = s.starttls()
                 if 200 <= c <= 299:
                     fpr.green('<<< %s %s' %(c,m))
                     # HELO - introducing yourself on encrypted session should be done as well
                     if v:
                         fpr.cyan('>>> %s %s' % ('EHLO',dhost['helo']))
                     (c,m) = s.ehlo(dhost['helo'])
                     if v:
                        #print (c,m)
                        if 200 <= c <= 299:
                            fpr.green('<<< %s %s' %(c,m))
                            if s.does_esmtp:
                                fpr.white('ESMTP supported and have extn:')
                                #print s.does_esmtp
                                #print s.esmtp_features
                                for (scmd,sarg) in s.esmtp_features.items():
                                    fpr.white('  * %s %s' % (scmd,sarg))
                                    scmds['secure_extn'].append((scmd,sarg))
                        elif 500 <= c <= 599:
                            fpr.err('<<< %s %s' %(c,m))
                 elif 500 <= c <= 599:
                     fpr.err('<<< %s %s' %(c,m))
                  
             else: 
                 if v:
                     fpr.white('TLS supported but not requested')
                     fpr.white('Unencrypted session established')




#         # SMTP AUTH
#         if 'auth' in s.esmtp_features.keys():
#             if smtp['connect']['hosts'][0]['smtp_auth_user'] != '':
#                 if v:
#                     fpr.cyan('>>> %s %s' % ('AUTH PLAIN','*********'))
#                 (c,m) = s.login(smtp['connect']['hosts'][0]['smtp_auth_user'],smtp['connect']['hosts'][0]['smtp_auth_pass'])
#                 if v:
#                     if 200 <= c <= 299:
#                         fpr.green('<<< %s %s' %(c,m))
#                     elif 500 <= c <= 599:
#                         fpr.err('<<< %s %s' %(c,m))
#         else:
#             if smtp['connect']['hosts'][0]['smtp_auth_user'] != '':
#                 if v:
#                     fpr.white('Authentication SET but not available (AUTH not supported)')
#                     fpr.white('Trying without AUTH')
#             else: 
#                 if v:
#                     fpr.white('Authentication not available (AUTH not supported)')
#                     fpr.white('Trying without AUTH')

        #print rcpts
         r = 'postmaster'
         for sm in ['EXPN','VRFY']:

            if v:
                fpr.cyan('>>> %s <%s>' % (sm,r))
            (c,m) = s.docmd('%s' % sm,'<%s>' % r)
            if 200 <= c <= 299:
                if v:
                    fpr.green('<<< %s %s' %(c,m))
                scmds['method'].append(sm)
            elif 500 <= c <= 599:
                if v:
                    fpr.err('<<< %s %s' %(c,m))
            else:
                if v:
                    fpr.err('<<< %s %s' %(c,m))

         if 'rcpt' in scmds['scmds'].lower():
             scmds['method'].append('RCPT')

#         pprint(dhar)
         # quit smtp session
         if v:
             fpr.cyan('>>> %s' % ('QUIT:'))
         (c,m) = s.quit()
         if v:
             if 200 <= c <= 299:
                 fpr.green('<<< %s %s' %(c,m))
                 fpr.white('Session closed successfully')
             elif 500 <= c <= 599:
                 fpr.err('<<< %s %s' %(c,m))
         #pprint(scmds)
         return scmds



    # the exception is triggered only when all recipoient failed :(
    except smtplib.SMTPRecipientsRefused, e:
         fpr.fail('Error: unable to sent message. All recipients refused.')
         fpr.warn(str(e))
    except smtplib.SMTPResponseException, e:
         fpr.fail('Error: unable to sent message')
         fpr.err('%s %s',(e.smtp_code,e.smtp_error))
    except smtplib.SMTPException:
         fpr.fail('Error: unable to sent message')
    # for all other errors like socket, io, rtc errors
    except Exception,error:
         fpr.err('%s' % str(error) )






# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def smtp_dha(cpt=1, rate=None, rcpts=[], method='RCPT TO',relays={} ,name='DHA-T-Single',v=False):


    dhar = dict()

    from pprint import pprint
    from core.data import cfgs,smtp,fpr,tc,DEBUG
    from core.func import dbginfo
    from core.msg.viewers import viewSmtpConv
    from core.msg.threads import get_tid

    dbginfo('DEBUG','name=%s, cpt=%s, method=%s, rate=%s, rcpts=%s' % (name,cpt,method,rate,rcpts) )

    #verbnose
    

    dhost=smtp['connect']['hosts'][0]

    try:

         import sys
         import smtplib

#         # log debuglevel output from smtplib
#         # redirect stderr from smtplib to string 
#         # 
#         # - from smtplib import stderr
#         if cfgs['conv_logs'] and cl:
#            ostderr = smtplib.stderr
#            smtplib.stderr = StderrLogger()


         # run smtp session
         if v:
            fpr.white('Establishing the session ..')
         s = smtplib.SMTP(dhost['host'],dhost['port'])
         

#         if cfgs['conv_logs'] and cl:
#            s.set_debuglevel('debug')

         # HELO - introduce yourself
         if v:
            fpr.cyan('>>> %s %s' % ('EHLO',dhost['helo']))
         (c,m) = s.ehlo(dhost['helo'])
         #r = s.helo(smtp['connect']['hosts'][0]['helo'])
         if v:
            #print (c,m)

            if 200 <= c <= 299:
                fpr.green('<<< %s %s' %(c,m))
                if s.does_esmtp:
                    fpr.white('ESMTP supported and have extn:')
                    #print s.does_esmtp
                    #print s.esmtp_features
                    for (scmd,sarg) in s.esmtp_features.items():
                        fpr.white('  * %s %s' % (scmd,sarg))
            elif 500 <= c <= 599:
                fpr.err('<<< %s %s' %(c,m))





         # STAARTTLS
         if 'starttls' in s.esmtp_features.keys():
             if dhost['tls_mode'] == 'TLS':
                 if v:
                     fpr.white('TLS supported and requested')
                     fpr.white('Establishing TLS session ..')
                     fpr.cyan('>>> %s' % ('STARTTLS'))
                 (c,m) = s.starttls()
                 if 200 <= c <= 299:
                     fpr.green('<<< %s %s' %(c,m))
                     # HELO - introducing yourself on encrypted session should be done as well
                     if v:
                         fpr.cyan('>>> %s %s' % ('EHLO',dhost['helo']))
                     (c,m) = s.ehlo(dhost['helo'])
                     if v:
                        #print (c,m)
                        if 200 <= c <= 299:
                            fpr.green('<<< %s %s' %(c,m))
                            if s.does_esmtp:
                                fpr.white('ESMTP supported and have extn:')
                                #print s.does_esmtp
                                #print s.esmtp_features
                                for (scmd,sarg) in s.esmtp_features.items():
                                    fpr.white('  * %s %s' % (scmd,sarg))
                        elif 500 <= c <= 599:
                            fpr.err('<<< %s %s' %(c,m))
                 elif 500 <= c <= 599:
                     fpr.err('<<< %s %s' %(c,m))
                  
             else: 
                 if v:
                     fpr.white('TLS supported but not requested')
                     fpr.white('Unencrypted session established')




         # SMTP AUTH
         if 'auth' in s.esmtp_features.keys():
             if dhost['smtp_auth_user'] != '':
                 if v:
                     fpr.cyan('>>> %s %s' % ('AUTH PLAIN','*********'))
                 (c,m) = s.login(dhost['smtp_auth_user'],dhost['smtp_auth_pass'])
                 if v:
                     if 200 <= c <= 299:
                         fpr.green('<<< %s %s' %(c,m))
                     elif 500 <= c <= 599:
                         fpr.err('<<< %s %s' %(c,m))
         elif dhost['smtp_auth_user'] != '':
             if v:
                 fpr.white('Authentication SET but not available (AUTH not supported)')
                 fpr.white('Trying without AUTH')

         if method.lower() == 'rcpt to':
             # MAIL FROM 
             sender = smtp['addrlist']['mail_from']
             #rcpt   = smtp['addrlist']['rcpt_to']
            
             if v:
                 fpr.cyan('>>> %s %s' % ('MAIL FROM:',sender))
             (c,m) = s.docmd('MAIL FROM:',sender)
             if v:
                 if 200 <= c <= 299:
                     fpr.green('<<< %s %s' %(c,m))
                 elif 500 <= c <= 599:
                     fpr.err('<<< %s %s' %(c,m))


         # number of recipients to test 
         # rpt - rcpt/thread
         # cpt - command/thread

         if cpt == None:
            cpt = 1
            rpt = len(rcpts)
            cpt = rpt 

         if v:
            fpr.white('Enumerating recipients ..')
            fpr.white('  * %s recipients to test with this thread' % len(rcpts))
            fpr.white('  * method in use: %s' % method.lower())

         #print rcpts
         for r in rcpts:


            if method.lower() == 'rcpt to':
                if v:
                    fpr.cyan('>>> %s: <%s>' % (method,r))
                (c,m) = s.docmd('%s:' % method,'<%s>' % r)
            else:
            # treat results returned from vrfy and expn similar
            # expn should have a separate condition as it could return
            # a list of recipients in case of mailing list but 
            # in modern networks you should be really lucky to find such an SMTP server
            # supporting - good luck with that
            # - it should be implemented just as proof of concept rather than for real use
             
                if v:
                    fpr.cyan('>>> %s <%s>' % (method,r))
                (c,m) = s.docmd('%s' % method,'<%s>' % r)


            if 200 <= c <= 299:
                if v:
                    fpr.green('<<< %s %s' %(c,m))
                dhar.setdefault(r,
                       { 'valid': True, 'code': c, 'msg': m, 'method': method.lower(), 
                         'host':  dhost['host'], 'thread': name }
                )
            elif 500 <= c <= 599:
                if v:
                    fpr.err('<<< %s %s' %(c,m))
                dhar.setdefault(r,
                       { 'valid': False, 'code': c, 'msg': m, 'method': method.lower(),
                         'host':  dhost['host'], 'thread': name }
                )
            else:
                if v:
                    fpr.err('<<< %s %s' %(c,m))
                dhar.setdefault(r,
                       { 'valid': False, 'code': c, 'msg': m, 'method': method.lower(),
                         'host':  dhost['host'], 'thread': name }
                )

            # query timeout - wait before next command
            #sleep(1)



#         pprint(dhar)
         # quit smtp session
         if v:
             fpr.cyan('>>> %s' % ('QUIT:'))
         (c,m) = s.quit()
         if v:
             if 200 <= c <= 299:
                 fpr.green('<<< %s %s' %(c,m))
                 fpr.white('Session closed successfully')
             elif 500 <= c <= 599:
                 fpr.err('<<< %s %s' %(c,m))
         if v:
             print
             fpr('To check valid recipients back to the main submenu') 
         #pprint(dhar)    



    # the exception is triggered only when all recipoient failed :(
    except smtplib.SMTPRecipientsRefused, e:
         fpr.fail('Error: unable to sent message. All recipients refused.')
         smtp['replay']['threads']['fail'].append(name)
         #print 'exception smtplib.SMTPRecipientsRefused',a
         fpr.warn(str(e))
         smtp['addrlist']['r_reject'].update(e.recipients)
         #recipients = [r[1] for r in e.recipients.values()]
         #recipients = e.recipients.keys()

    except smtplib.SMTPResponseException, e:

         #print 'smtplib.SMTPResponseException',e.smtp_code,e.smtp_error
         fpr.fail('Error: unable to sent message')
         fpr.err('%s %s',(e.smtp_code,e.smtp_error))

         smtp['dha']['threads']['fail'].append(name)

    except smtplib.SMTPException:
         fpr.fail('Error: unable to sent message')
         smtp['dha']['threads']['fail'].append(name)
     # for all other errors like socket, io, rtc errors
    except Exception,error:
         fpr.err('%s' % str(error) )
         smtp['dha']['threads']['fail'].append(name)




    # store results in global dict - if we would like  to return a value with multi-thread 
    # importing and implementing Queue would be required here
    # temporary worakaround fo viewing the results 
    # to compatible with previously implemented feature for 1. inject and 2. replay 
    smtp['addrlist']['rcpts'] = list()
    for r in dhar.keys():
        if dhar[r].get('valid'):
            smtp['addrlist']['rcpts'].append(r) # for backward
            smtp['addrlist']['r_valid'].setdefault(r,(dhar[r].get('code'),dhar[r].get('msg')))
        else:
            smtp['addrlist']['r_reject'].setdefault(r,(dhar[r].get('code'),dhar[r].get('msg')))



    pprint(dhar)
    return dhar

#    if cfgs['conv_logs'] and cl:
#         smtp_conversation = smtplib.stderr.sio.getvalue()
#         smtplib.stderr.sio.close()
#         print
#         viewSmtpConv(smtp_conversation)
#         smtplib.stderr = ostderr
#         #if cfg['conv_logs_file']:
#         if False:
#            pass
#         
#         elif raw_input('  Would you like save conversation logs [y/N]: ') in ['y','Y']:
#            logs_save(smtp_conversation,thread_name=name,logpfx='smtp-conv')
#
#
#     #logging.debug('Exiting: %s' % name)     
#     logger.debug('Exiting: %s' % name)     







