# --------------------------------------------------------------------------- #
# viewers.py
# --------------------------------------------------------------------------- #

import re
import sys 

from email.MIMEBase  import MIMEBase
from email.iterators import _structure
from email.message import Message

from core.data import cfgs,smtp,fpr,tc,tr,DEBUG
from core.func import dbginfo,info,get_yesno_input
from core.ui.cless import Less
from core.msg.builder import msg_builder
from core.msg.threads import get_rcpts

try:
   from cStringIO import StringIO
except:
   from StringIO import StringIO
    

#from core.ui.cmenu import Menu
#import core.ui.menu as menu
#from core.ui.banner import banner, bancls, bancls2
#import core.diag.eauth as eauth


#print smtp

__all__ = [
  'viewConn',
  'viewEnvelope',
  'viewMsg',
  'viewTheMsg',
  'viewSmtpConv',
  'viewSmtpSess',
  'viewRefusedAddresses',
  'viewAcceptedAddresses',
  'viewDKIMSignTag',
  'viewRawContent',
  'viewSPFvalues',
]



   
    

# --------------------------------------------------------------------------- #
# view SPF values
# --------------------------------------------------------------------------- #
def viewSPFvalues(dd):
    

    if 'id' in dd:
        fpr('SPF values')
        print

        fpr('  Identities') 
        fpr('    id MAIL FROM        : %s' %  dd['id'].get('mfrom','') )
        fpr('    id HELO/EHLO        : %s' %  dd['id'].get('helo','') )
        fpr.info('    id PRA              : %s' %  dd['id'].get('pra','') )
        fpr('  Client IP             : %s' %  dd.get('ip','') )
        print
        fpr('  Receiver address      : %s' %  dd.get('receiver','') )
        print
    else:
        fpr('No SPF values') 




# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #
def viewRawContent(raw):


    dl = len(raw.splitlines())  
    if dl > tr:
        fpr('Content data is bigger than your screen (%s lines)' % dl)
        if raw_input('  Would like to use system pager to view it [y/N]:> ') in ['y', 'Y']:
            fpr.blue( '_'*(tc-4))
            print
            pager=Less(num_lines=tr)  
            print raw | pager
        else:
            fpr.blue( '_'*(tc-4))
            print
            fpr('%r' % raw)
    else:
        fpr.blue( '_'*(tc-4))
        print
        fpr('%r' % raw)
    fpr.blue( '_'*(tc-4))
 


# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #
def viewDKIMSignTag(_all=0):
#TODO:
# add Less funct with condition 
# 

    d = smtp['sign']['dkim']
    if not d.get(0):
       fpr('No DKIM Signature')
       return

    for k in range(d['dstat']+1):
        #print d
        #print k

        # if not _all then show current only 
        if not _all and k != d['dstat']:
           k += 1
        else:
            if k in d:        
               dn = d[k]
            if smtp.get('h'+str(k)+'_DKIM-Signature'):
               fpr('Signature attached (#%s)' % k ,adj='r')
            else:
               fpr('Signature not attached (current #%s)' % k ,adj='r')
            fpr.info('_'*(tc-4))
            print
            fpr('DKIM signature set tags:')
            print 
            fpr('  version            : v=%s' %  dn.get('version','1') )
            fpr('  alghoritm          : a=%s' %  dn.get('alghoritm','rsa-sha256') )
            fpr('  canonicalization   : c=%s' %  dn.get('canonicalize','') )
            fpr('  selector           : s=%s' %  dn.get('selector','') )
            fpr('  domain             : d=%s' %  dn.get('domain','') )
            fpr('  header             : h=%s' %  dn.get('header',"from : to : subject") )
            fpr('  identity           : i=%s' %  dn.get('identity','') )
            fpr('  length             : l=%s' %  dn.get('length','') )
    
            print
            if dn.get('privkey'):
               fpr('Private Key  status   : -- Loaded -- '  )
            else:
               fpr.warn('Private Key  status   : -- Not loaded -- ' )
    
            print 
            if dn.get('sig'):
               fpr('DKIM-Signature: %s' % dn.get('sig',''), adj='l' )
            else:
               fpr.warn('DKIM-Signature: -- Not generated --')
    
            print
            if smtp['headers'].get('h'+str(k)+'_DKIM-Signature'):
               fpr('DKIM-Signature was attached')
            else:
               fpr.warn('DKIM-Signature was not attached')
             
            print
          
    fpr.info('_'*(tc-4))




# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #
def viewAcceptedAddresses():
   fpr('Accepted Addresses')
   print 
   for k in smtp['addrlist']['r_valid']:
       (e,m) = smtp['addrlist']['r_valid'][k] # unpack tuple
       fpr ("  %-30s | %4s  | %s " % (k,e,m) )
   print
   #fpr('Total number of addresses: %d' % len([smtp['addrlist']['rcpt_to']]+smtp['addrlist']['rcpts'])) 
   fpr('Total number of addresses: %d' % len(smtp['addrlist']['rcpts'])) 
   fpr('Total number of refused addresses: %d' % len(smtp['addrlist']['r_reject'].keys())) 
   fpr.white('Total number of accepted addresses: %d' % len(smtp['addrlist']['r_valid'].keys())) 



# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #
def viewRefusedAddresses():

   fpr('Refused Addresses')
   print
   # dictionary = { key: (tuple), }
   for k in smtp['addrlist']['r_reject']:
       (e,m) = smtp['addrlist']['r_reject'][k] # unpack tuple
       fpr ("  %-30s | %4s  | %s " % (k,e,m) )
   print
   #fpr('Total number of addresses: %d' % len([smtp['addrlist']['rcpt_to']]+smtp['addrlist']['rcpts'])) 
   fpr('Total number of addresses: %d' % len(smtp['addrlist']['rcpts'])) 
   fpr.white('Total number of refused addresses: %d' % len(smtp['addrlist']['r_reject'].keys())) 
   fpr('Total number of accepted addresses: %d' % len(smtp['addrlist']['r_valid'].keys())) 


# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #
def viewSmtpSess():


    #from core.msg.builder import msg_builder
    size = len( msg_builder().as_string(unixfrom=False) )
    #from core.msg.threads import get_rcpts

    unknown = '-- undefined --'

    if cfgs['conv_logs']:
       fpr.green('Conversation Logs: ON','r')

    fpr.info('_'*(tc-4))
    print

    #FIXME: 
    d = smtp['connect']['hosts'][0]

    fpr('SMTP Host             : %s:%s' % (d.get('host',unknown), d.get('port',unknown)))
    if d.get('smtp_auth_user'):
       fpr('SMTP Authentication   : %s:%s' % (d.get('smtp_auth_user',unknown), d.get('smtp_auth_pass',unknown)))
    else:
       fpr('SMTP Authentication   : NoAuth')
    fpr('SMTP Encryption       : %s' % d.get('tls_mode',unknown))
    fpr('SMTP HELO             : %s' % d.get('helo',unknown))

    print
    if smtp['addrlist']['mail_from']:
       fpr('Envelope Sender       : %s' % smtp['addrlist']['mail_from'])
    else:
       fpr.err('Envelope Sender       : %s' % unknown)

    # shown only 1st rcpt if more than one 
    r = list(smtp['addrlist']['rcpts'])
    #if smtp['addrlist']['rcpt_to']:
    #   r.insert(0,smtp['addrlist']['rcpt_to'])
    if r:
       if len(r) > 1:
          fpr('Envelope Recipient(s) : %s .. + %d more' % (r[0],len(r)-1) )
       else: 
          fpr('Envelope Recipient(s) : %s' % r[0] )
    else:
          fpr.err('Envelope Recipient(s) : %s' % unknown )
    del r[:]

    print
    fpr('Number of Recipients  : %s' % get_rcpts('NoR') )
    fpr('Message Size          : %s bytes' % size)
    fpr('Message Subject       : %s' % smtp['headers'].get('h_Subject',unknown))

    fpr.info('_'*(tc-4))
    print
 



# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #
def viewSmtpConv(s):

    #import re
    #import sys 
    #from StringIO import StringIO
    #from core.ui.cless import Less

    if s:
       if raw_input('  Would you like to view SMTP conversation [y/N]:> ') not in ['y', 'Y']:
          return True
       else:
          print

    dl = len(s.splitlines())  

    for line in s.splitlines():
       if len(line) > tc:
          dl += len(line) / tc 

    if dl > tr:
        fpr('SMTP conversation logs are much bigger than your screen (%s lines)' % dl)
        if raw_input('  Would like to use system pager to view it [y/N]:> ') in ['y', 'Y']:
           fpr.blue( '_'*(tc-4))
           print
           # use Less if output is much bigger than one screen
           pager=Less(num_lines=tr)
           # fetch output from fancy print as Less input must be a string
           # make copy of original stdout han redirect stdout to string 
           sto = sys.stdout
           sys.stdout = StringIO()

           for line in s.splitlines():
               if re.search('^send:',line):
                  fpr.cyan(line)
               elif re.search('^reply:',line):
                  fpr.green(line)
               elif re.search('^data:',line):
                  fpr.purple(line)
               else:
                  fpr.info(line)
 
           x = sys.stdout.getvalue()
           sys.stdout.close()
           sys.stdout = sto
           print x | pager

           return True
        #else:
        #   fpr.blue( '_'*(tc-4))
        #   print
        #   fpr.blue( '_'*(tc-4))

    #else:
    fpr.blue( '_'*(tc-4))
    print
    for line in s.splitlines():
          if re.search('^send:',line):
             fpr.cyan(line)
          elif re.search('^reply:',line):
             fpr.green(line)
          elif re.search('^data:',line):
             fpr.purple(line)
          else:
             fpr.info(line)
    fpr.blue( '_'*(tc-4))

    #print (dl,tr)




# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #
def viewConn():

    #FIXME:
    d = smtp['connect']['hosts'][0]
 
    fpr('Connection settings')
    print
    fpr('  SMTP Host           : %s' % d.get('host',''))
    fpr('  SMTP Port           : %s' % d.get('port',''))
    fpr('  SMTP HELO/EHLO      : %s' % d.get('helo',''))
    print
    fpr('  SMTP AUTH Mechanism : %s' % d.get('smtp_auth_method',''))
    fpr('  SMTP Auth Username  : %s' % d.get('smtp_auth_user',''))
    fpr('  SMTP Auth Password  : %s' % d.get('smtp_auth_pass',''))
    print
    fpr('  Encryption Mode     : %s' % d.get('tls_mode','NoTLS'))



# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #
def viewEnvelope():

    #from core.ui.cless import Less
    


    if smtp['addrlist']['rcpts']:
        if len(smtp['addrlist']['rcpts']) > (tr-5):
            if get_yesno_input('  Would like to use system pager to view it [y/N]:> '):
                pager=Less(num_lines=tr)
                print "\n".join(smtp['addrlist']['rcpts']) | pager
                #print "\n".join(list('       RCPT TO | ' + r for r in smtp['addrlist']['rcpts'])) | pager
                return
        print 
        print "\n".join(list('       RCPT TO | ' + r for r in smtp['addrlist']['rcpts']))


# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #
def viewTheMsg(s=0):

#    from core.ui.cless import Less
#    from core.msg.builder import msg_builder
#    try:
#        from cStringIO import StringIO
#    except:
#        from StringIO import StringIO
#    
    fs = StringIO()
#
#    from email.MIMEBase  import MIMEBase
#    from email.iterators import _structure
#    from email.message import Message

    msgdata = msg_builder()

    if DEBUG > 1:
       from pprint import pprint
       print '----'
       pprint(msgdata)
       print 'type:',type(msgdata)
       print 'repr:',repr(msgdata)
       print 'dir :', dir(msgdata)
       print '__len__():',msgdata.__len__()  # no. of headers
       print '__str__():',msgdata.__str__()
       print 'len():', len(msgdata)
       print msgdata.get_payload()
       print '----'

    if hasattr(msgdata,'as_string'):

        fpr.blue( '_'*(tc-4))
        print
        #if msgdata != MIMEBase:
        if True:
            # view the message mime structure 
            if s:
                #email.iterators._structure(msgdata, fs)
                if hasattr(msgdata,'get_content_typ'):
                    _structure(msgdata, fs)
                    #fpr.blue('%s' % email.iterators._structure(msgdata) )
                    fpr.warn('%s' % fs.getvalue())
                else:
                    fpr.warn('For custom message currently MIME structure is not checked !')
            # view message data
            else:
                #print fpr.GRAY
                #dl = len(str(msgdata).splitlines())  
                dl = len(msgdata.as_string(unixfrom=False).splitlines())  
                if dl > tr:
                    fpr('Message data is bigger than your screen (%s lines)' % dl)
                    if raw_input('  Would like to use system pager to view it [y/N]:> ') in ['y', 'Y']:
                        fpr.blue( '_'*(tc-4))
                        print
                        pager=Less(num_lines=tr)  
                        print msgdata.as_string(unixfrom=False) | pager
                    else:
                        fpr.blue( '_'*(tc-4))
                        print
                        print msgdata.as_string(unixfrom=False)
                else:
                    print msgdata.as_string(unixfrom=False)
                        
                #print len(str(msgdata).splitlines()),tr

                #print msgdata
                #print fpr.RCL
        #else:
        #    fpr.info('No content data was defined !')



#        if msgdata == Message:        
#            print msgdata


#        elif smtp['use_mime'] == 0:
    
#        if s:
#           dbginfo('warn','MIME structure view is not supprted for customized content!')
#
#        dl = len(msgdata.as_string(unixfrom=False).splitlines())  
#        print msgdata.as_string(unixfrom=False)
#        print 'len ', dl


	fpr.blue( '_'*(tc-4))
    else:   
        fpr.warn('No content data was defined !')
 

    fs.close()

# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #
def viewMsg(part='all'):

    #import re
    d = { 'p': 0 }
    if part in ['envelope','all']:

        e=0
        #for k in ['helo','mail_from','rcpt_to']:
        for k in ['mail_from','rcpt_to']:
            if not smtp.get(k):
                e+=1
        if e == 3:
            d['p'] += 1
            fpr.info('_'*(tc-4))
            print
            fpr.info ('It looks like you have not specified any envelope field!')
            fpr.info('_'*(tc-4))
        else:
            fpr.info('%-12s | %s' % ('Envelope',' Content'))
            fpr.info('_'*(tc-4))
            print
            #fpr('%+12s | %s' % ('HELO',smtp.get('helo','')))
            fpr('%+12s | %s' % ('MAIL FROM', smtp['addrlist'].get('mail_from','--- not defined ---')))
            #fpr('%+12s | %s' % ('RCPT TO',smtp['addrlist'].get('rcpt_to','')))
            #fpr('%+12s | %s' % ('RCPT TO',smtp['addrlist'].get('rcpts')))
            # shown only 1st rcpt if more than one 
            r = list(smtp['addrlist']['rcpts'])
            if r:
                if len(r) > 1:
                    fpr('%+12s | %s .. + %s more' % ('RCPT TO',r[0],len(r)-1))
                else: 
                    fpr('%+12s | %s' % ('RCPT TO',r[0]))
            #        fpr('RCPT : %s' % r[0] )
            else:
                fpr('%+12s | %s' % ('RCPT TO','-- not defined --'))
            del r[:]



            fpr.info('_'*(tc-4))
    #print d['p']
    if part in ['headers','all']:
        h = 0
        for k in smtp['headers'].keys():
            # find key for smtp headers only, these which start with 'h_'
            if re.match(r'^h\d*_',k):
            #    fpr ('%+12s: %s ' % (k,smtp[k]) ) 
                h+=1
        if h == 0:
            d['p'] += 1
            print
            fpr.info('It looks like you have not included any header !')
            fpr.info('_'*(tc-4))
        else:
            print
            fpr.info('%-15s | %s' % ('Header name','Header content'))
            fpr.info('_'*(tc-4))
            for k in smtp['headers'].keys():
                m = re.match(r'^h\d*_(.*)',k)
                if m:
                    fpr ('%+15s | %s ' % (m.group(1),smtp['headers'][k]) ) 
            fpr.info('_'*(tc-4))

    #print d['p']
    if part in ['data', 'body', 'all']:
        lsOfNonEmptyContKey = [k for k,v in smtp['content'].iteritems() if len(v) > 0]
        #contentKeyLen = [len(smtp['content'][t]) for t in smtp['content'].keys() ]           
        #print contentKeyLen
        #print lsOfNonEmptyContKey
        if not lsOfNonEmptyContKey:
            d['p'] += 1
            print
            fpr.info('It looks like you have not defined any content data !') 
            fpr.info('_'*(tc-4))
        else:
             viewTheMsg() 

    #print d['p']
    if part == 'all':
        #print d['p']
        if d['p'] == 3:
            fpr.info('_'*(tc-4))
            print
            fpr.err('Man what you are doing? Do something! ;)')
            fpr.info('_'*(tc-4))

# --------------------------------------------------------------------------- #

