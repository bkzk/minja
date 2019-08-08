# --------------------------------------------------------------------------- #
# threads 
# --------------------------------------------------------------------------- #

import re                                    # get_rate()
import ctypes                                # get_tid()
import time
import threading
import sys

from core.data import smtp,fpr,tc,tr,DEBUG         # get_threads_no(), get_rcpt_no(), get_msg_no()
from core.data import MAX_THREADS,MAX_RCPT_PER_MSG,MAX_MSG_PER_TH,TH_DELAY

from core.func import get_yesno_input, info, dbginfo
from core.ui.banner import bancls2
from core.msg.builder import msg_builder
from core.msg.sender import smtp_sender_new

# --------------------------------------------------------------------------- #
# function: get_tid - get thread id - returns current threads id 
# - threads do not have pid - process id 
# http://blog.devork.be/2010/09/finding-linux-thread-id-from-within.html
# https://mail.python.org/pipermail/python-list/2009-January/522514.html
# to get the int value of SYS_gettid run on your os: 
#
# #include <stdio.h>
# #include <sys/syscall.h>
#
# int main(void)
# {
#    printf("%d\n", SYS_gettid);
#    return 0;
# }
# 
# it is not reliable, and risky - if we call wrong value $@!#&$%^&#(^@)_@!
# --------------------------------------------------------------------------- #
def get_tid():

    if DEBUG:
        if ctypes.sizeof(ctypes.c_ulong) == 4:
	   SYS_gettid = 224
        elif ctypes.sizeof(ctypes.c_ulong) == 8:
	   SYS_gettid = 186

        if sys.platform.lower() == "linux" or sys.platform.lower() == "linux2":
            #import ctypes
            #SYS_gettid = 186
            libc = ctypes.cdll.LoadLibrary('libc.so.6')
            tid = libc.syscall(SYS_gettid)
            return tid 
        #if sys.platform.lower() == "darwin":
            #SYS_gettid = 186
        #    libc = ctypes.cdll.LoadLibrary('libc.dylib')
        #    tid = libc.syscall(SYS_gettid)
        #    return tid 
        else:
           return None
    else:
        return None

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def get_threads_no():

#    from core.data import smtp,fpr,tc,tr
#    from core.data import MAX_THREADS

#    fpr.info('Threads are treated as seperate connections.')
#    print
#    fpr('Try to keep number of Threads between <1-100>')
#    fpr('NoT can not be greater than number of recipients when NoR > 1')
#    print

    info('info','Note: NOT defines the number of threads where each thread is a new seperate' \
                '       and simultaneous connection. \n' \
                '      * NOT can not be greater then number of recipients (NOR) when \n' \
                '        NOR is greater than one.\n' \
                '      * NOT value should be kept between 1 - %s \n\n' \
                '      ** NOT can be greater than 1 when there is only 1 recipient but\n' \
                '      ** this raise a special case when the same message is sent multiple \n' \
                '      ** times (NOT times) to single recipient using a seperate connection \n' \
                '      ** and bombarding recipient with the same message' % MAX_THREADS, adj='l'
    )
    print


    n = raw_input('  [%s]> ' % smtp['replay']['threads'].get('not',None)) \
        or smtp['replay']['threads'].get('not',None)
    if n == None: 
        return
    if type(n) is int or n.isdigit():
        print
        if 0 < int(n) < MAX_THREADS:
            #smtp['replay']['threads']['not']=int(n)
            #fpr.ok('%s'%n)
            #ret = chThrDep(t=int(n)) 
            #if ret > True: 
            #   #smtp['replay']['threads']['not']=int(n)
            #   smtp['replay']['threads']['not']=ret
            if  chThrDep(t=int(n)): 
                pass
                #fpr.ok('%s'%n)
        else:
            fpr.fail('Setting NoT as %s' % n)



    #chThrDep()

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def get_rcpt_no():

#    from core.data import smtp,fpr,tc,tr
#    from core.data import MAX_RCPT_PER_MSG
#    from core.func import info

    info('info','Note: RPM defines a number of recipients used with a single message.\n' \
                '      It\'s a number of RCPT TO commands send with corresponding addresses.\n\n' \
                '      * RPM value can not be greater than number of recipients (NOR) when \n' \
                '        NOR is greater than one.\n' \
                '      * Settinng RPM does not make sense for single recipient. ', adj='l'
        )

    #fpr('RpM can not be greater than number of recipients when NoR > 1')
    #fpr('Settinng RpM does not make sense for single recipient')
    print
    n = raw_input('  [%s]> ' % smtp['replay']['threads'].get('rpm',None)) \
        or smtp['replay']['threads'].get('rpm',None)
 
    if n == None: 
        return

    if type(n) is int or n.isdigit():
        print
        if 0 < int(n) < MAX_RCPT_PER_MSG:
            print
            #ret = chThrDep(rpm=int(n)) 
            #if ret > True: 
            #   smtp['replay']['threads']['rpm']=int(ret)
            if chThrDep(rpm=int(n)):
               fpr.ok('%s'%n)
        else:
           print
           fpr.fail('%s'%n)

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def get_msgs_no():

#    from core.data import smtp,fpr,tc,tr
#    from core.data import MAX_MSG_PER_TH
#    from core.func import info

    info('info','Note: MPT defines a number of messages sent per single thread where each \n' \
                '      thread is a a new SMTP connection which need to be established.\n\n' \
                '      * MPT can not be greater than number of recipients (NOR) when \n' \
                '        NOR is greater than one.\n' \
                '      * Settinng MPT also does not make sense for single recipient. ', adj='l'

        )
    print

    n = raw_input('  [%s]> ' % smtp['replay']['threads'].get('mpt',None)) \
        or smtp['replay']['threads'].get('mpt',None)

    if n == None: 
        return

    if type(n) is int or n.isdigit():
        print
        if 1 <= int(n) <= MAX_MSG_PER_TH:
            print
            #ret = chThrDep(mpt=int(n)) 
            #if ret > True: 
            #   smtp['replay']['threads']['mpt']=int(ret)
            if  chThrDep(mpt=int(n)): 
                fpr.ok('%s'%n)

        else:
           print
           fpr.fail('%s'%n)

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def get_msgs_delay():

#    from core.data import smtp,fpr,tc,tr
#    from core.data import MAX_MSG_PER_TH
#    from core.func import info

    info('info','Note: Delay is number of miliseconds between starting new threads, \n' \
                '      where each new thread is a new SMTP connection.', adj='l'
        )
    #fpr('Specify Delay between running new thread/connection')
    print
    n = raw_input('  [%s]> ' % smtp['replay']['threads'].get('delay',TH_DELAY)) \
           or smtp['replay']['threads'].get('delay',TH_DELAY)
    
    if n and (type(n) is int or n.isdigit()):
        if 0 <= int(n):
            print
            smtp['replay']['threads']['delay']=int(n)
            fpr.ok('%s'%n)
        else:
            print
            fpr.fail('%s'%n)




# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
#def get_rate(rate):
def get_rate():

#    from core.data import smtp,fpr,tc,tr
#    import re

    rate = smtp['replay']['threads'].get('rate','')

    fpr('Allowed values are N, N/Ms, N/Mm, N/Mh')
    fpr('where:')
    fpr('  N - number of Recipients/Messages \
       \n  M - value of s-seconds, m-minutes or h-hours\n')
    print
    r = raw_input('  [%s]> ' % (rate or ''))
    if r:
        m = re.match( r'^(\d+)(\/)*(\d+[smh])*$',r )
        if not m:
        #    print
            fpr.err('Err: Incorrect syntax')
            return False
        else:
            #print type(m.group())
            #if m.group(1):
            #    print m.group(1)
            #if m.group(2):
            #    print m.group(2)
            #if m.group(3):
            #    print m.group(3)
            if m.group(1) and not m.group(2):
                fpr.ok('%s' % m.group() )

                smtp['replay']['threads']['rate'] = m.group()

                return m.group()
            if m.group(3):
                fpr.ok('%s' % m.group() )

                smtp['replay']['threads']['rate'] = m.group()

                return m.group()
    else:
        return (rate or '')





# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def get_rcpts(opt):

#    from core.data import smtp

    # Nomber of Recipients
    if opt == 'NoR':
       nor = len(smtp['addrlist']['rcpts']) 
#       if smtp['addrlist']['rcpt_to'] != '':
#           nor = nor + 1
       return nor
       #return 23 # for TESTS TODO Remove this 

    if opt == 'domains':
        return 0
    if opt == 'hosts':
        return 0

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
# check Threads Dependends
def chThrDep(t=None,rpm=None,mpt=None):

#VERIFY:  In Python 2.x : int/int --> int and int/float --> float In Python 3.x : int/int can result in a float 

    from core.data import smtp,fpr,tc,tr
    from core.func import waitin 
    
    r=get_rcpts('NoR')


    #Warunki Konieczne - Essential Conditions
    # to met WK1, WK2, WK3
    if not t:
       t =  smtp['replay']['threads'].get('not',None)
    elif t and not (1 <= int(t) <= r):
       if r > 1:
          t = r
       if r == 1: #special case
          pass
    if t:
       smtp['replay']['threads']['not'] = int(t)
       
    if not rpm:
       rpm =  smtp['replay']['threads'].get('rpm',None)
    elif rpm and not (1 <= int(rpm) <= r):
       rpm = int(r)
    if rpm:
       fpr.ok('Saving RpM as %s' % rpm)
       smtp['replay']['threads']['rpm'] = int(rpm)
       
    if not mpt:
       mpt =  smtp['replay']['threads'].get('mpt',None)
    elif mpt and not (1 <= int(mpt) <= r):
       mpt = int(r)
    if mpt:
       fpr.ok('Saving MpT as %s' % mpt)
       smtp['replay']['threads']['mpt'] = int(mpt)




    if r:

       # specific feature: the result depends from number of recipients
       # -------------------------------------------------------------------- #
       if t and not rpm and not mpt:
          fpr.warn('%s : %s : %s - %s' % (t,rpm,mpt,r) )
          # allow to set t if no rpm or mpt values and number of rcpt > 1
          # but t must be <= r, so if t greater then r => it will be equal to r
          if r > 1:
             smtp['replay']['threads']['not'] = int(t)
             fpr.ok('Saving NoT as %s' % t)
             return t

          # special case when r == 1 , not related to our Equation 
          # for r = 1 allow to set T > 1 but do not allow than set rpm or mpt
          # in this special case the sam message is flooding a sepcific rcpt 
          # with this smae message in multiple threads/connection !
          if r == 1:
             #pass
             smtp['replay']['threads']['not'] = int(t)
             fpr.ok('Saving NoT as %s' % t)
             return t


       # set initial  
       elif rpm and not t and not mpt:
          fpr.warn('%s : %s : %s - %s' % (t,rpm,mpt,r) )
          if r > 1:
             smtp['replay']['threads']['rpm'] = int(rpm)
             #return rpm
             #return True
          if r ==  1:
             fpr.warn('It doesn\'t make sense to define RpM when NoR = 1')
             return False
       # 
       elif mpt and not t and not rpm:
          fpr.warn('%s : %s : %s - %s' % (t,rpm,mpt,r) )
          if r > 1:
             smtp['replay']['threads']['mpt'] = int(mpt)
             #return mpt
             #return True
          if r ==  1:
             fpr.warn('It doesn\'t make sense to define MpT when NoR = 1')
             return False


    else:
       fpr.err('Recipients not defined. Build a list of recipients first.')
       fpr.err('Flush the values if the recipient list has been modified.')
       return



    # Some maths :)
    #
    # rpm - recipient per message
    # r - number of recipients (all)
    # m - number of messages (all)
    # 
    # rpm = r / m ==> m = r / rpm

    # mpt - messages per thread
    # t - number of threads
    # m - number of messages (all) 
    # 
    # mpt = m / t ==> m = mpt * t
    
    # r / rpm = mpt * t
    #
    # ==>   t = r / (rpm * mpt)
    #
    # ==> rpm = r / (mpt * t)
    #
    # ==> mpt = r / (rpm * t)


    fpr.info('_'*(tc-4))
    print
    fpr.warn('Your limits:')
    fpr.warn('t = %s : rpm = %s : mpt = %s - r = %s' % 
             (smtp['replay']['threads'].get('not',None),
              smtp['replay']['threads'].get('rpm',None),
              smtp['replay']['threads'].get('mpt',None),r) 
           )
    print 
    fpr.err('Maximum possible limits to met Essential Conditions:')
    fpr.err('t = %s : rpm = %s : mpt = %s - r = %s' % (t,rpm,mpt,r) )
    fpr.info('_'*(tc-4))

    print


    def chEque():
       print
       if r:

          # compare float 
          # https://ubuntuforums.org/showthread.php?t=840665
          def float_eq(a, b, epsilon=0.00000001):
             fpr.cyan('<float_eq> %s' % abs(a-b))
             if abs(a - b) < epsilon:
                return True
             return False

          m1 = float(r) / rpm
          m2 = mpt * float(t)
          
          fpr.cyan('r/rpm = %s, mpt * t = %s' % (m1,m2))

          if float_eq(m1,m2):
             fpr.green('Equetion is met')
             waitin()
             return True
          else:
             fpr.err ('Equetion is false')
             waitin()
             return False


    def setReals(t,rpm,mpt):
        
        if t and rpm and mpt :
           smtp['replay']['threads']['reals'].setdefault('not',t)
           smtp['replay']['threads']['reals'].setdefault('rpm',rpm)
           smtp['replay']['threads']['reals'].setdefault('mpt',mpt)

           smtp['replay']['threads']['reals']['not']=t
           smtp['replay']['threads']['reals']['rpm']=rpm
           smtp['replay']['threads']['reals']['mpt']=mpt
           fpr.ok('Reals were set!')

    if r:

       # count the mpt - based on rpm and t
       # -------------------------------------------------------------------- #
       if t and rpm and not mpt:
          fpr.green('%s : %s : %s - %s' % (t,rpm,mpt,r) )

          # m = r / rpm
          # mpt = m / t

          # I - validate MPT - MPT <= R
          mpt = float(r) / (rpm * t)
          fpr.green('counting mpt = %s' % mpt)

          chEque()

          # round up - if there is a remainder 
          if (r % (rpm * t) > 0):
             mpt = r / (rpm * t) + (r % (rpm * t) > 0)
             fpr.green('rounding up mpt = %s' % mpt)


             # find the lowest T for rounded MpT to met RpM
             t_new = float(r) / (rpm * mpt) #+ (r % (rpm * mpt) > 0)
             fpr.green('counting new t = %s' % t_new)

             if (r % (rpm * mpt) > 0): # if remainder
                t_new = r / (rpm * mpt) + ( r % (rpm * mpt) > 0)
                fpr.green('rounding up new t = %s' % t_new)

             fpr.err('realistic returns would be: *t = %s, rpm = %s, mpt = %s  for r = %s' %
                (int(t_new),rpm,int(mpt),r))            
             setReals(int(t_new),rpm,int(mpt))
          else:
             fpr.err('realistic returns would be: t = %s, rpm = %s, mpt = %s  for r = %s' %
                  (t,rpm,int(mpt),r))
             setReals(t,rpm,int(mpt))


       # count the rpm - for mpt and t
       # -------------------------------------------------------------------- #
       elif t and mpt and not rpm:
          fpr.blue('%s : %s : %s - %s' % (t,rpm,mpt,r) )

          # m = mpt * t 
          # m = r / rpm 

          # TODO
          # WK: validate RPM , RPM <= R

          rpm = float(r) / (mpt * t)
          fpr.blue('counting: rpm = %s' % rpm)
          
          chEque()

          # if there is a remainder 
          if (r % (mpt * t) > 0):
             rpm = r / (mpt * t) + (r % (mpt * t) > 0)
             fpr.blue('rounding up rpm = %s' % rpm)


             # find the lowest T for rounded MpT to met RpM
             t_new = float(r) / (rpm * mpt) #+ (r % (rpm * mpt) > 0)
             fpr.green('counting new t = %s' % t_new)

             if (r % (rpm * mpt) > 0): # if remainder
                t_new = r / (rpm * mpt) + ( r % (rpm * mpt) > 0)
                fpr.green('rounding up new t = %s' % t_new)

             fpr.err('realistic returns would be: *t = %s, rpm = %s, mpt = %s  for r = %s' %
                (int(t_new),int(rpm),mpt,r))            
             setReals(int(t_new),int(rpm),mpt)

          else:
             fpr.err('realistic returns would be: t = %s, rpm = %s, mpt = %s  for r = %s' %
                (t,int(rpm),mpt,r))
             setReals(t,int(rpm),mpt)



       # count the mpt ( use t = 1 )
       # -------------------------------------------------------------------- #
       elif rpm and not t and not mpt:
          t=1
          fpr.purple('assuming t eq 1 for equation')
          fpr.purple('%s : %s : %s - %s' % (t,rpm,mpt,r) )

          mpt = float(r) / rpm
          fpr.purple('counting: mpt = %s' % mpt)

          chEque()
          
          #if there is a remainder
          if (r % rpm > 0): 
             
             mpt = r / rpm + (r % rpm > 0)
             fpr.purple('rounding up mpt = %s' % mpt)

             # find the lowest T for rounded MpT to met RpM
             t_new = float(r) / (rpm * mpt) #+ (r % (rpm * mpt) > 0)
             fpr.green('counting new t = %s' % t_new)

             if (r % (rpm * mpt) > 0): # if remainder
                t_new = r / (rpm * mpt) + ( r % (rpm * mpt) > 0)
                fpr.green('rounding up new t = %s' % t_new)

             fpr.err('realistic returns would be: *t = %s, rpm = %s, mpt = %s  for r = %s' %
                (int(t_new),rpm,mpt,r))            
             setReals(int(t_new),rpm,mpt)

          else:
             fpr.err('realistic returns would be: t = %s, rpm = %s, mpt = %s  for r = %s' %
                  (t,rpm,int(mpt),r))
             setReals(t,rpm,int(mpt))






       # count the rpm ( use t = 1 )
       # -------------------------------------------------------------------- #
       elif mpt and not t and not rpm:
          t=1
          fpr.purple('assuming t eq 1 for equation')
          fpr.purple('%s : %s : %s - %s' % (t,rpm,mpt,r) )

          rpm = float(r) / mpt 
          fpr.purple('counting: rpm = %s' % rpm)
          t=1
          chEque()
          
          #if there is a remainder
          if (r % mpt > 0): 
             
             rpm = r / mpt + (r % mpt > 0)
             fpr.purple('rounding up rpm = %s' % rpm)

             # find the lowest T for rounded MpT to met RpM
             t_new = float(r) / (rpm * mpt) #+ (r % (rpm * mpt) > 0)
             fpr.green('counting new t = %s' % t_new)

             if (r % (rpm * mpt) > 0): # if remainder
                t_new = r / (rpm * mpt) + ( r % (rpm * mpt) > 0)
                fpr.green('rounding up new t = %s' % t_new)

             fpr.err('realistic returns would be: *t = %s, rpm = %s, mpt = %s  for r = %s' %
                  (int(t_new),int(rpm),mpt,r))            
             setReals(int(t_new),int(rpm),mpt)

          else:
             fpr.err('realistic returns would be: t = %s, rpm = %s, mpt = %s  for r = %s' %
                  (t,int(rpm),mpt,r))
             setReals(t,int(rpm),mpt)





       # count t - for rpm and mpt
       # -------------------------------------------------------------------- #
       elif mpt and rpm and not t:
          fpr.white('%s : %s : %s - %s' % (t,rpm,mpt,r) )
          print type(mpt)



          # add 1 to round up a result 
          # (r % (rpm * mpt) > 0) it will return True which is 1 
          # if there is a remainder and 0 if not 
          t = float(r) / (rpm * mpt) #+ (r % (rpm * mpt) > 0)

          fpr.white('counted: t = %s' % t)

          chEque()

          # round up 
          if (r % (rpm * mpt) > 0):
             t = r / (rpm * mpt) + (r % (rpm * mpt) > 0)
             fpr.white('rounding up t = %s' % t)
          
          # validate WK
          # t = <1,r>             
          # if t < 1
          if (float(r) / (rpm * mpt)) < 1:
             fpr.info('Now to met equetion for t=1 it is not possible for %s (R) recipients '\
                      'to send %s (MpT) messeges in one thread with %s (RpM) recipient in message' %
                      (r,mpt,rpm))

             print
             fpr.info('New RpM value can be counted based on existing MpT or new MpT ' \
                      'value can be counted based on existing RpM' )
             print
             fpr.info('For simplicity it is assumed that RpM limits is more important so MpT ' \
                      'is going to be recounted to met an equation')
             print 

             mpt_new = float(r) / rpm
             fpr.white('New MpT to met equetion is %s' % mpt_new)
             mpt = mpt_new

             chEque()

             # now just round up
             mpt_new = r / rpm + (r % rpm > 0)
             fpr.white('rounding up new mpt = %s' % mpt_new)


             fpr.err('realistic returns would be: t = %s, rpm = %s, *mpt = %s  for r = %s' %
                  (int(t),rpm,int(mpt_new),r))            
             setReals(int(t),rpm,int(mpt_new))
          else:
             # so if t > 1 and it was counted 
             fpr.err('realistic returns would be: t = %s, rpm = %s, mpt = %s  for r = %s' %
                  (int(t),rpm,int(mpt),r))
             setReals(int(t),rpm,int(mpt))

       # only true if r / rpm = mpt * t
       # -------------------------------------------------------------------- #
       elif t and rpm and mpt:
          fpr.cyan('%s : %s : %s - %s' % (t,rpm,mpt,r) )
          if not chEque():
             fpr.info('_'*(tc-4))
             print
             fpr.warn('It is not recommended trying to set NoT with RpM and MpT.  ' \
                      'Suggested action would be to flush these values.' )
             fpr.info('_'*(tc-4))
             print
             waitin()
             return False
          else:
             fpr.err('realistic returns would be: t = %s, rpm = %s, mpt = %s  for r = %s' %
                  (t,rpm,mpt,r)) 
             setReals(t_new,rpm,mpt)
          

    # for test
    waitin()


# Multithread mailer need to met an essential conditions to work. 
# there are two basic equation to met:
#
#   (1) M = R / RPM 
#   (2) M = MPT * T 
#   form (1) and (2) ==> (3)  R / RPM = MPT * T
#
# where R is a number of all recipients 
#       T is a number of threads (a separate connection)
#       M is a number of all messages which need to be created to 
#         met an equetion
#
# and [R,RPM,M,MPT,T] E Reals 
# ** E means belongs to 
# 
# To met these (1) and (2) some restriction need to be met:
#
#  (I)    RPM E <1,R> <=> RPM => 1 ^ RPM <= R
#  (II)   MPT E <1,R> <=> MPT => 1 ^ MPT <= R
#  (III)  foreach(MPT >1) v foreach(RMP >1) T E <1,R>
#
#
# Depending of the number of values received from user the equentions
# need to be met. If all of required values are not put than some 
# default value of 1 is taken to check the equation and met conditions. 
# If the condition(s) can not be met than one or more value need to be changed. 
#
#
# For R = 1 
# It does not make sense to set RPM or MPT when there is only a single recipient (R=1)
# Even when we do that (try to set MPT or RPM when R = 1) the (1) and (2) need to be
# met and to make it true the function will count a new value for RPM or MPT.
#
#   as for R = 1;
#       from (1) ==> M = 1 / RPM
#       from (2) ==> M = MPT *T 
#   (*) when M = RPM ==> 1 / RPM = MPT * T ==> T = 1/(RPM*MPT)  
#   From (*) ==> T is always ~= 1 for (RPM,MPT) E R - Reals
# 
#   also to met boundaries (I) and (II)
# 
#         RPM E <1,1> <=> RPM = 1
#         MPT E <1,1> <=> MPT = 1
# 
#


# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #

def flushThrValues():

    
    if get_yesno_input('  Flush thread settings [y/N]: '):

        smtp['replay']['threads']['delay'] = TH_DELAY
        smtp['replay']['threads'].pop('rate', None)
        smtp['replay']['threads'].pop('not',None)
        smtp['replay']['threads'].pop('rpm',None)
        smtp['replay']['threads'].pop('mpt',None)
        smtp['replay']['threads']['reals'].pop('not',None)
        smtp['replay']['threads']['reals'].pop('rpm',None)
        smtp['replay']['threads']['reals'].pop('mpt',None)
        fpr.info('Threads values were flushed !')

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #

def viewThreadsSummary():

    from core.data import smtp,fpr,tc,tr
    from core.msg.builder import msg_builder 
    from core.func import waitin

#    bancls()
    fpr('Running SMTP Replay:')
    print
#    fpr.info(' -- rate limits --')
#    print
    fpr.info('                               -   set  - counted -')
    fpr(' NOT - Number Of Threads       :  %4s  |  %4s  ' % 
          ( smtp['replay']['threads'].get('not',None),
            smtp['replay']['threads']['reals'].get('not',None) ) )

    fpr(' RPM - Recipients Per Message  :  %4s  |  %4s  ' % 
          ( smtp['replay']['threads'].get('rpm',None),
            smtp['replay']['threads']['reals'].get('rpm',None) ) )
    fpr(' MPT - Message Per Thread      :  %4s  |  %4s  ' % 
          ( smtp['replay']['threads'].get('mpt',None),
            smtp['replay']['threads']['reals'].get('mpt',None) ) )

    fpr.info(' RT  - Recipients Per H/M/S    :  %s ' % 
            smtp['replay']['threads'].get('rate',None))
    fpr(' DELAY between threads run     :  %s ms' % 
            smtp['replay']['threads'].get('delay',None))

 #   print 
 #   fpr.info(' -- recipients --')
    print
    fpr(' NOR - Number of Recipients    : %d' % get_rcpts('NoR')  )
    fpr.info(' Number of Destination Domains : %d' % get_rcpts('domains') )
    fpr.info(' Number of Destination Hosts   : %d' % get_rcpts('hosts')   ) 
    
    print 
    fpr.info(' -- message --')
    
    message = msg_builder()
    # confirm  - TODO [ msgx is always true
    if message:
        print
        fpr(' Message Size     : %s' % repr(len(message.as_string(unixfrom=False)))  )
    else: 
        print
        fpr('No content data was defined !')
        #print

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #

def runThreads():



   # ----------------------------------------------------------- # 
    del smtp['replay']['threads']['ok'][:]
    del smtp['replay']['threads']['fail'][:]

    if  smtp['addrlist']['r_reject'].keys() or  smtp['addrlist']['r_valid'].keys():
        fpr('Flushing currently found results (valid/refused recipients) ..')

    smtp['addrlist']['r_reject'].clear()
    smtp['addrlist']['r_valid'].clear()

    viewThreadsSummary()

    t = srThread()
    t.daemon   = True
    t.delay    = smtp['replay']['threads'].get('delay',1)


    #viewThreadsSummary()
    #print 
    #FIXME: after flushing all values are None 

    t.threads  = smtp['replay']['threads']['reals'].get(
                   'not', smtp['replay']['threads'].get('not',1)
                 )

    t.rpm      = smtp['replay']['threads']['reals'].get(
                   'rpm', smtp['replay']['threads'].get('rpm',1)
                 )
    t.mpt      = smtp['replay']['threads']['reals'].get(
                   'mpt', smtp['replay']['threads'].get('mpt',1)
                 )

    t.rate                = smtp['replay']['threads'].get('rate','1')
    t.th_interval         = smtp['replay']['threads'].get('th_interval',0)

    #t.msg                 = message
    t.msg                 = msg_builder()

    #t.rcpts = [smtp['addrlist']['rcpt_to']]+smtp['addrlist']['rcpts'] 
    t.rcpts = smtp['addrlist']['rcpts'] 
    dbginfo('debug', str(t.rcpts))


    #t.msg                 = msg_builder().as_string(unixfrom=False)
    # ----------------------------------------------------------- # 
    #print t.msg
    if t.msg:
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
        fpr.err('Message can not be processed or not loaded !')
 

#

# --------------------------------------------------------------------------- #
# class: srThread
# --------------------------------------------------------------------------- #
class srThread(object):


    msg = None 

    def __init__(self, interval=1,threads=1,daemon=True,delay=1,
                       rpm=1,mpt=1,rate=1,rcpts=[]):


        self.interval = interval  # threading join interval
        self.threads  = threads
        self.daemon   = daemon
        #self.rpt      = rpt       # recipient per thread
        self.rpm      = rpm       # recipient per message
        self.mpt      = mpt       # message per thread
        self.rate     = rate      # rate - rexipients per s/m/h
        self.delay    = delay     # delay - delay between starting new thread (connection)
        self.rcpts    = rcpts

        dbginfo('debug','Init: NoT=%s,RpM=%s,MpT=%s,' % (self.threads,self.rpm,self.mpt))
        dbginfo('debug','Init: %s' % self.rcpts)
 
    def run(self):

        dbginfo('debug','Run: NoT=%s,RpM=%s,MpT=%s,' % (self.threads,self.rpm,self.mpt))
        dbginfo('debug','Run: Rcpts: %s' % self.rcpts)
        #return 

        if self.msg == None:
            fpr.fail('Message is not defined')
            return 0

        # count number of recipients per threads
        rpt = 0
        if self.rpm and self.mpt:
            rpt = self.rpm*self.mpt

        thr = []
        for i in range(self.threads):

            # i - thread number - count from zero 


            # split rcpts list per threads
            si = i*rpt
            ei = i*rpt + rpt
            t_rcpts = self.rcpts[si:ei]

            dbginfo('debug','Thread: Rcpts: %s' % t_rcpts)
            #return 0

            # special case when rpm/mpt/.. = 1 and rcpt = 1 and not > 1
            if len(self.rcpts) == 1 and (self.rpm and self.mpt) == 1:
                t_rcpts = self.rcpts

                dbginfo('debug', 'Raise Special Case: Thread: Rcpts: %s - %d' % (t_rcpts, len(self.rcpts)))


            # declare thread
            t = threading.Thread(target=smtp_sender_new, 
                                 kwargs=dict(message=self.msg,
                                         rpm=self.rpm,
                                         mpt=self.mpt,
                                         rate=self.rate,
                                         rcpts=t_rcpts,
                                         name='T-%d' % i,) , 
                                   name='T-%d' % i, verbose=None,  )
            t.setDaemon(self.daemon)
            #t.setName('t-%d'%i)
            thr.append(t)
            t.start()
            bancls2(thr,i,opt='replay')
            # delay between starting new connection (threads)
            time.sleep(self.delay/1000.0)

        bancls2(thr,0,'replay')

        while threading.activeCount()>1:
            i=1
            for j in thr:
                j.join(self.interval)
                i=i+1
                bancls2(thr,i,'replay')


