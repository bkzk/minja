# --------------------------------------------------------------------------- #

import logging

from core.data import smtp,cfgs,fpr,tr,tc,DEBUG
from core.func import dbginfo,info

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
class Logger():



    def __init__(self):

        #import logging
        FORMAT='[%(levelname)s] (%(threadName)-10s) %(message)'

        self.logger = logging.getLogger('threadslogs')
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(cfgs['log_path']+'/minja-thr.log')
        fh.setLevel(logging.DEBUG)
        
        # create console handler with a higher log level
        #ch = logging.StreamHandler()
        #ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        #ch.setFormatter(formatter)
        # add the handlers to the self.logger
        self.logger.addHandler(fh)
        #self.logger.addHandler(ch)
    
        self.logger.debug('-- Logging started for new minj session --')
    
    def run(self):

        print '  Log run ..'


    def close(self):
        #from core.data import DEBUG
        #from core.func import dbginfo

        dbginfo('debug',str(self.logger.handlers))
        self.logger.handlers[0].stream.close()
        self.logger.removeHandler(self.logger.handlers[0])
#        print self.logger.handlers
#        self.logger.handlers[0].stream.close()
#        self.logger.removeHandler(self.logger.handlers[0])
        #print self.logger.handlers
        dbginfo('debug',str(self.logger.handlers))



# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def logs_save(logs,thread_name, logpfx):


    from core.data import cfgs,smtp,fpr,tc,DEBUG
    from core.func import dbginfo
    from datetime import datetime
    logfile = logpfx+datetime.now().strftime('%Y%m%d%H%M%S')
    import os, errno
    import logging

    logger = logging.getLogger('threadslogs')
    

    fn = cfgs['log_path']+'/'+logfile

    try:
       print
       with open(fn, "w") as text_file:
          text_file.write("{0}".format(logs))
          fpr.ok('Saving logs in %s' % logfile )
       logger.info('[%s]: Successful saving logs in file: %s' % (thread_name,logfile) )
    except IOError as ioex:
       fpr.fail('Saving logs in %s' % logfile )
       #fpr.fail('Err: Logs not saved with %s' % logfile )
       print
       fpr.err('Errno: %s' % ioex.errno)
       fpr.err('Err code: %s' % errno.errorcode[ioex.errno])
       fpr.err('Err message: %s' % os.strerror(ioex.errno) )

       logger.info('[%s]: Saving logs in file: %s failed: %s: %s' % (thread_name,logfile,
               errno.errorcode[ioex.errno], os.strerror(ioex.errno) ) )


# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
# this function is deprecated and is going to be removed soon 
def smtp_sender(message, rpm=None, mpt=None, rate=None, rcpts=[], relays={} ,name='T-Single'):


     #from core.data import smtp,fpr,tc 
     from core.data import cfgs,smtp,fpr,tc,DEBUG
     from core.func import dbginfo
     from core.msg.viewers import viewSmtpConv
     from core.msg.threads import get_tid


     # TODO: allow conv logs use with threads
     # for now: use conv logs only with single thread 
     # for 3.1 inject message
     cl = 0
     if name =='T-Single':
        cl = 1


     # ---------------------------------------------------- #
     # log thread session
     import logging
     # create logger
     logger = logging.getLogger('threadslogs')
     logger.info('Starting thread: [%s]' % name)
     logger.debug('[%s]: Pid=%d' % (name,get_tid()) )
     logger.debug('[%s]: rpm=%s ,mpt=%s, rate=%s, rcpts=%s' % (name,rpm,mpt,rate,rcpts) )
     # host
     logger.info('[%s]: H=%s:%s, smtp_auth=(%s,%s)' %
                   ( name,
                     smtp['connect']['hosts'][0].get('host'),
                     smtp['connect']['hosts'][0].get('port'),
                     smtp['connect']['hosts'][0].get('smtp_auth_user'),
                     smtp['connect']['hosts'][0].get('smtp_auth_pass') ) )
     print
     # ---------------------------------------------------- #
     dbginfo('DEBUG','name=%s, rpm=%s ,mpt=%s, rate=%s, rcpts=%s' % (name,rpm,mpt,rate,rcpts) )
     #return 0

     # ---------------------------------------------------- #
     from StringIO import StringIO
     class StderrLogger(object):

        def __init__(self):
           #self.logger = logging.getLogger('threadslogs')
           self.sio = StringIO()

        def write(self, message):
           #self.logger.debug(message)
           self.sio.write(message)
     # ---------------------------------------------------- #

     try:

         import sys
         import smtplib

         # log debuglevel output from smtplib
         # redirect stderr from smtplib to string 
         # 
         # - from smtplib import stderr
         if cfgs['conv_logs'] and cl:
            ostderr = smtplib.stderr
            smtplib.stderr = StderrLogger()


         # run smtp session
         s = smtplib.SMTP(smtp['connect']['hosts'][0]['host'],smtp['connect']['hosts'][0]['port'])

         if cfgs['conv_logs'] and cl:
            s.set_debuglevel('debug')

         # HELO - introduce yourself
         s.ehlo(smtp['connect']['hosts'][0]['helo'])

         # STAARTTLS
         if smtp['connect']['hosts'][0]['tls_mode'] == 'TLS':
             s.starttls()

         # SMTP AUTH
         if smtp['connect']['hosts'][0]['smtp_auth_user'] != '':
             s.login(smtp['connect']['hosts'][0]['smtp_auth_user'],smtp['connect']['hosts'][0]['smtp_auth_pass'])

         # MAIL FROM 
         
         sender = smtp['addrlist']['mail_from']
         #rcpt   = smtp['addrlist']['rcpt_to']

         # for single injection or when mpt value unknown use single message per connection
         if mpt == None:
            mpt = 1
            rpm = len(rcpts)

         # split messages per connection
         for m in range(mpt):
            # m strt from 0 to mpt-1
            # split rcpts per message
            si = m*rpm
            ei = m*rpm + rpm
            m_rcpts = rcpts[si:ei]
            #print (m,si,ei,m_rcpts) 
            if m_rcpts: 
                logger.debug('[%s]: F=%s, MPT=%s/%s R=%s' % (name,sender,(m+1),mpt,m_rcpts)  )
                # SEND 
# https://docs.python.org/2/library/email.message.html#email.message.Message
# as_string([unixfrom])
# Return the entire message flattened as a string. When optional unixfrom is True, the envelope header is included in the returned string. unixfrom defaults to False. Flattening the message may trigger changes to the Message if defaults need to be filled in to complete the transformation to a string (for example, MIME boundaries may be generated or modified).

                response = s.sendmail(sender, m_rcpts, message.as_string(unixfrom=False))



                if response:
                   smtp['addrlist']['r_reject'].update(response)
                   #
                   dbginfo('debug','Sendmail response list:',str(response))
                   dbginfo('debug','Failed recipients:',str(smtp['addrlist']['r_reject']))


                # The response returns a dictionary, with one entry for each recipient that 
                # was refused. Each entry contains a tuple of the SMTP error code and the 
                # accompanying error message sent by the server.
                # 'r_reject': {'': (501, '#5.1.1 bad address'),
                #           "'Joe@domain.not'": (550,'#5.1.0 Address rejected.'),
                #           "'admin@domain.not'": (550,'#5.1.0 Address rejected.'),
                #           "'aleks@domain.not'": (550,'#5.1.0 Address rejected.'),

                # to be compatibile with other features build a r_valid dict
                # m_rcpts - all rcpts per tread 
                for r in m_rcpts:
                    if not r in response.keys():
                        # recipient is valid if not refused
                        smtp['addrlist']['r_valid'].setdefault(r,(250,'OK'))
                    


#         s.sendmail(sender, rcpt, message.as_string(unixfrom=False))

         # quit smtp session
         s.quit()

#FIXME:
# message sent success : nto true when threads with more than one message in it 
# fix this print info 

         if name =='T-Single':
             fpr.ok('Message was sent successfuly')
         smtp['replay']['threads']['ok'].append(name)

         # when only part of recipients/sender failed it looks like than 
         # exception for recipientsRefused is not triggered 
         # remember: to clear refu recipient list before you call out this function

         if response:
            smtp['addrlist']['r_reject'].update(response)
            dbginfo('debug','Sendmail response list:',str(response))
            dbginfo('debug','Failed recipients:',str(smtp['addrlist']['r_reject']))
            
         #from core.msg.viewers import viewRecipientsRefused



    # All recipients were refused. Nobody got the mail. The recipients attribute of 
    # the exception object is a dictionary with information about the refused 
    # recipients (like the one returned when at least one recipient was accepted).

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

         smtp['replay']['threads']['fail'].append(name)

     except smtplib.SMTPException:
         fpr.fail('Error: unable to sent message')
         smtp['replay']['threads']['fail'].append(name)
     # for all other errors like socket, io, rtc errors
     except Exception,error:
         fpr.err('%s' % str(error) )
         smtp['replay']['threads']['fail'].append(name)


     if cfgs['conv_logs'] and cl:
         smtp_conversation = smtplib.stderr.sio.getvalue()
         smtplib.stderr.sio.close()
         print
         viewSmtpConv(smtp_conversation)
         smtplib.stderr = ostderr
         #if cfg['conv_logs_file']:
         if False:
            pass
         
         elif raw_input('  Would you like save conversation logs [y/N]: ') in ['y','Y']:
            logs_save(smtp_conversation,thread_name=name,logpfx='smtp-conv')


     #logging.debug('Exiting: %s' % name)     
     logger.debug('Exiting: %s' % name)     



# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
import smtplib
class SMTPExt(smtplib.SMTP):
    """
    This class extends smtplib.SMTP and overrides the sendmail method
    to not raising SMTPException for SMPTRecipientsRefused 
    """

    def sendmail(self, from_addr, to_addrs, msg, mail_options=[],
                 rcpt_options=[]):
        """
        This method may raise the following exceptions:
         SMTPHeloError          The server didn't reply properly to
                                the helo greeting.
         SMTPRecipientsRefused  The server rejected ALL recipients
                                (no mail was sent).
         SMTPSenderRefused      The server didn't accept the from_addr.
         SMTPDataError          The server replied with an unexpected
                                error code (other than a refusal of
                                a recipient).
        Note: the connection will be open even after an exception is raised.
        """
        self.ehlo_or_helo_if_needed()
        esmtp_opts = []
        if self.does_esmtp:
            # Hmmm? what's this? -ddm
            # self.esmtp_features['7bit']=""
            if self.has_extn('size'):
                esmtp_opts.append("size=%d" % len(msg))
            for option in mail_options:
                esmtp_opts.append(option)

        (code, resp) = self.mail(from_addr, esmtp_opts)
        if code != 250:
            self.rset()
            raise SMTPSenderRefused(code, resp, from_addr)
        senderrs = {}
        if isinstance(to_addrs, basestring):
            to_addrs = [to_addrs]
        for each in to_addrs:
            (code, resp) = self.rcpt(each, rcpt_options)
            if (code != 250) and (code != 251):
                senderrs[each] = (code, resp)
        if len(senderrs) == len(to_addrs):
            # the server refused all our recipients
            self.rset()
            # this raise break connection for srThreads() with multiple message per threads
            # in case when all recipients assign to a message are refused and as a result
            # the connection is closed and all other remaining messages are skipped 
            #raise SMTPRecipientsRefused(senderrs)
        else:
            (code, resp) = self.data(msg)
            if code != 250:
                self.rset()
                raise SMTPDataError(code, resp)
            #if we got here then somebody got our mail
        return senderrs

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
def smtp_sender_new(message, rpm=None, mpt=None, rate=None, rcpts=[], relays={} ,name='T-Single'):


     #from core.data import smtp,fpr,tc 
     from core.data import cfgs,smtp,fpr,tc,DEBUG
     from core.func import dbginfo
     from core.msg.viewers import viewSmtpConv
     from core.msg.threads import get_tid


     dhost=smtp['connect']['hosts'][0]


     # name of Thread define if this function is run as part of single connection or multithread connection
     # use convesation logs onlyin single thread 
     # for 3.1 inject message
     # TODO: enable conv logs for threads
     cl = 0
     if name =='T-Single':
        cl = 1


     # ---------------------------------------------------- #
     # log thread session
     import logging
     # create logger
     logger = logging.getLogger('threadslogs')
     logger.info('Starting thread: [%s]' % name)
     logger.debug('[%s]: Pid=%s' % (name,get_tid()) )
     logger.debug('[%s]: rpm=%s ,mpt=%s, rate=%s, rcpts=%s' % (name,rpm,mpt,rate,rcpts) )
     # host
     logger.info('[%s]: H=%s:%s, smtp_auth=(%s,%s)' %
                   ( name,
                     dhost.get('host'),
                     dhost.get('port'),
                     dhost.get('smtp_auth_user'),
                     dhost.get('smtp_auth_pass') ) )
     print
     # ---------------------------------------------------- #
     dbginfo('DEBUG','name=%s, rpm=%s ,mpt=%s, rate=%s, rcpts=%s' % (name,rpm,mpt,rate,rcpts) )
     #return 0

     # ---------------------------------------------------- #
     from StringIO import StringIO
     class StderrLogger(object):

        def __init__(self):
           #self.logger = logging.getLogger('threadslogs')
           self.sio = StringIO()

        def write(self, message):
           #self.logger.debug(message)
           self.sio.write(message)
     # ---------------------------------------------------- #

     try:

         import sys
         import smtplib

         # log debuglevel output from smtplib
         # redirect stderr from smtplib to string 
         # 
         # - from smtplib import stderr
         if cfgs['conv_logs'] and cl:
            ostderr = smtplib.stderr
            smtplib.stderr = StderrLogger()


         # run smtp session
         if name =='T-Single':
             s = smtplib.SMTP(dhost['host'],dhost['port'])
         else:
             s = SMTPExt(dhost['host'],dhost['port'])

         if cfgs['conv_logs'] and cl:
            s.set_debuglevel('debug')

         # HELO - introduce yourself
         s.ehlo(dhost['helo'])
         #s.ehlo_or_helo_if_needed()

         # STAARTTLS
         fpr.warn(dhost['tls_mode'])
         if dhost['tls_mode'] == 'TLS':
             s.starttls()
             # HELO - introduce yourself
             s.ehlo(dhost['helo'])
             #s.ehlo_or_helo_if_needed()

         # SMTP AUTH
         if dhost.get('smtp_auth_user'):
             s.login(dhost.get('smtp_auth_user'),dhost.get('smtp_auth_pass'))

         # MAIL FROM 
         
         sender = smtp['addrlist']['mail_from']
         #rcpt   = smtp['addrlist']['rcpt_to']

         # for single injection or when mpt value unknown use single message per connection
         if mpt == None:
            mpt = 1
            rpm = len(rcpts)

         # split messages per connection
         for m in range(mpt):
            # m strt from 0 to mpt-1
            # split rcpts per message
            si = m*rpm
            ei = m*rpm + rpm
            m_rcpts = rcpts[si:ei]
            #print (m,si,ei,m_rcpts) 
            if m_rcpts: 
                logger.debug('[%s]: F=%s, MPT=%s/%s R=%s' % (name,sender,(m+1),mpt,m_rcpts)  )

                # SEND 

                # https://docs.python.org/2/library/email.message.html#email.message.Message
                # as_string([unixfrom])
                # Return the entire message flattened as a string. When optional unixfrom is True, 
                # the envelope header is included in the returned string. unixfrom defaults to False. 
                # Flattening the message may trigger changes to the Message if defaults need to be filled 
                # in to complete the transformation to a string (for example, MIME boundaries may be 
                # generated or modified).

                response = s.sendmail(sender, m_rcpts, message.as_string(unixfrom=False))



                if response:
                   smtp['addrlist']['r_reject'].update(response)
                   
                   #dbginfo('debug','Sendmail response list:',str(response))
                   #dbginfo('debug','Failed recipients:',str(smtp['addrlist']['r_reject']))
 
#         s.sendmail(sender, rcpt, message.as_string(unixfrom=False))

#FIXME:
# message sent success : nto true when threads with more than one message in it 
# fix this print info 

         fpr.ok('Message was sent successfuly')
         smtp['replay']['threads']['ok'].append(name)

         # when only part of recipients/sender failed it looks like than 
         # exception for recipientsRefused is not triggered 
         # remember: to clear refu recipient list before you call out this function


# when threds than this response is not fetchhe 
# it should be upper

         if response:
            smtp['addrlist']['r_reject'].update(response)
            #
            dbginfo('debug','Sendmail response list:',str(response))
            dbginfo('debug','Failed recipients:',str(smtp['addrlist']['r_reject']))
            

    # All recipients were refused. Nobody got the mail. The recipients attribute of 
    # the exception object is a dictionary with information about the refused 
    # recipients (like the one returned when at least one recipient was accepted).

    # the exception is triggered only when all recipoient failed :(
     except smtplib.SMTPRecipientsRefused, e:
         fpr.fail('Error: Message not sent. All recipients refused.')
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

         smtp['replay']['threads']['fail'].append(name)

     except smtplib.SMTPException:
         fpr.fail('Error: unable to sent message')
         smtp['replay']['threads']['fail'].append(name)
     # for all other errors like socket, io, rtc errors
     except Exception,error:
         fpr.err('%s' % str(error) )
         smtp['replay']['threads']['fail'].append(name)


     try:
     # quit smtp session: keep quit after the exception to close the connection in case of some SMTP Exception
        s.quit()


        if cfgs['conv_logs'] and cl:
            smtp_conversation = smtplib.stderr.sio.getvalue()
            smtplib.stderr.sio.close()
            print
            viewSmtpConv(smtp_conversation)
            smtplib.stderr = ostderr
            #if cfg['conv_logs_file']:
            if False:
               pass
            
            elif raw_input('  Would you like save conversation logs [y/N]: ') in ['y','Y']:
               logs_save(smtp_conversation,thread_name=name,logpfx='smtp-conv')
   

     except NameError:
        # if s is not defined
        fpr.err('SMTP session not established')

     #logging.debug('Exiting: %s' % name)     
     logger.debug('Exiting: %s' % name)     



