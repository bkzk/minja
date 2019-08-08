# --------------------------------------------------------------------------- #
# 2.5 Data Content - Message builders 
# --------------------------------------------------------------------------- #
 
import re
# from email.MIMENonMultipart import MIMENonMultipart
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email.mime.application import MIMEApplication

from core.data import smtp,fpr,tc,tr,DEBUG 
from core.func import append_uniq,get_inputs,dbglog,dbginfo
from core.msg.utils import get_addresses

        
# --------------------------------------------------------------------------- #
# msg_builder need to return similar object for non MIME conformant message
#  (which in most cases be true for message content build from user input) 
# as for messages build by email.MIME* modules - this is important for other
# function used in this project
# --------------------------------------------------------------------------- #
class CMessage():

    #body = ''
    def __init__(self,body):
        self.body = body
        import string
        body = string.join(self.body, "")

###        dbginfo('debug','CUSTOM BODY',body)

    def as_string(self,unixfrom=False):
        if type(self.body) is str:
           return self.body
    def __str__(self):
        return self.as_string(unixfrom=False)


 
# --------------------------------------------------------------------------- #
# message builder
# --------------------------------------------------------------------------- #
def msg_builder():

     #import re
     #from core.data import smtp,fpr,DEBUG 
     #from core.func import dbginfo
     # # from email.MIMENonMultipart import MIMENonMultipart
     #from email.MIMEMultipart import MIMEMultipart
     #from email.MIMEText import MIMEText
     #from email.MIMEBase import MIMEBase
     #from email.MIMEImage import MIMEImage
     #from email.mime.application import MIMEApplication
     
     smtp['mime-type'] = 'multipart' 
     #smtp['mime-type'] = 'text'

     # check if some content have been already defined
     #contentKeyLen = []
     #for t in smtp['content'].keys():
     #    print t,len(smtp['content'][t])
     #    contentKeyLen.append(len(smtp['content'][t]))
     contentKeyLen = [len(smtp['content'][t]) for t in smtp['content'].keys() ]           

###     dbginfo('debug', 'type: %s' % contentKeyLen)

     # * * M I M E * * #
     use_mime = 1
     # mime  is used by default evan for simple text message 
     # you need to manually specify to not use it and it would be
     # possible only when content is plain text

     # check if more than one types of content were defined 
     # 0 - other keys does not contain any value
     # 1 - other keys contain some values
     # 2 - the key does not contain any value

     def checkContValue(d={}, k=''):
         #print d
         #print k
         if len(d[k]):
             #print len(d[k])
             for t in d.keys():
                 if t != k and len(d[t]):
                      #print t,k,len(d[t])
                      return 1
             return 0
         else:
             return 2             

     def get_binpart(d={},ctype=''):
         #print d
         if d.get('raw'): 
             if ctype == 'image':
                 att = MIMEImage( d['raw'])
             else:
                 att = MIMEApplication( d['raw'] )
             #del att['Content-Type']
             # check if headers are defined 
             for kh in d.keys():
                 if re.match('^h_(.*)$',kh):
                     #print kh
                     hn = re.match('^h_(.*)$',kh)
                     #att[h.group(1)] = d[kh]
                     # if headers were defined and has some value and 
                     # this same header is defined as a default header with MIME
                     # object than remove the default header before adding your own
                     if att[hn.group(1)] and d[kh] != '':
                         #print 'exist=',att[hn.group(1)]
                         #del att[hn.group(1)]
                         att.replace_header(hn.group(1), d[kh] )
                     elif d[kh] != '':
                         att.add_header(hn.group(1), d[kh] )

         if d.get('b64'):
             att = MIMEBase('application','octet-stream')
             for kh in d.keys():
                  if re.match('^h_(.*)$',kh):
                     #print kh
                     hn = re.match('^h_(.*)$',kh)
                     if att[hn.group(1)] and d[kh] != '':
                         att.replace_header(hn.group(1), d[kh] )
                     
                     elif d[kh] != '':
                         #print 'ddd=',d[kh] 
                         att.add_header(hn.group(1), d[kh] )
                     att.set_payload("\n".join(d['b64']))
                     #print d['b64']
             #print att
         return att
 


     
     if smtp['use_mime'] == 1:
         #######################
         msgdata = MIMEBase

         # smtp dictionary contains different parts of message which are stored under 
         # different types like text, html, img, vof, and att which is for binary in
         # most cases attachments 

         lsOfNonEmptyContKey = [k for k,v in smtp['content'].iteritems() if len(v) > 0]

         if checkContValue(smtp['content'], 'text') == 0:
             msgdata = MIMEText('\n'.join(smtp['content']['text']),'plain')

         elif checkContValue(smtp['content'], 'html') == 0:
             msgdata = MIMEText('\n'.join(smtp['content']['html']),'html')

         elif checkContValue(smtp['content'], 'img')  == 0:

             #print smtp['content']['img']
             if len(smtp['content']['img']) > 1:
                 msgdata = MIMEMultipart()
                 for a in smtp['content']['img'].keys():
                     msgdata.attach(get_binpart(smtp['content']['img'][a]))
             else:
                 for a in smtp['content']['img'].keys():
                     msgdata = get_binpart(smtp['content']['img'][a],'image')

#         elif checkContValue(smtp['content'], 'zip')  == 0:
#             if len(smtp['content']['att']) > 1:
#                 msgdata = MIMEMultipart
#             else:
#                 msgdata = MIMEApplication
 
         # if only att were defined as file(raw data) or base64

         elif checkContValue(smtp['content'], 'vof')  == 0:
             if len(smtp['content']['vof']) > 1:
             #    msgdata = MIMEMultipart()
             #    for a in smtp['content']['vof'].keys():
             #        msgdata.attach(get_binpart(smtp['content']['vof'][a]))
                  fpr('Wrr: It shouldn\'t happened')
             else:
                 #msgdata = MIMEApplication
                 for a in smtp['content']['vof'].keys():
                     msgdata = get_binpart(smtp['content']['vof'][a])

         elif checkContValue(smtp['content'], 'att')  == 0:
             if len(smtp['content']['att']) > 1:
                 msgdata = MIMEMultipart()
                 for a in smtp['content']['att'].keys():
                     msgdata.attach(get_binpart(smtp['content']['att'][a]))
             else:
                 #msgdata = MIMEApplication
                 for a in smtp['content']['att'].keys():
                     msgdata = get_binpart(smtp['content']['att'][a])

         # if more then 1 content parts were defined use MIMEMultipart
         elif len(lsOfNonEmptyContKey) > 1:
###             dbginfo('debug','lsOfNonEmptyContKey=%s' % lsOfNonEmptyContKey)
             altrn = MIMEBase
###             dbginfo('debug','altrn=%s' % str(altrn))
             if 'text' in  lsOfNonEmptyContKey and 'html' in  lsOfNonEmptyContKey:
                 # it can be a multipart/alternative 
                 fpr('Message has TEXT and HTML parts. ')
                 if raw_input ("  Would you like use MIME multipart/alternative [y/N]: > ") in ['y','Y']:
                      print
                      fpr('Creating multipart/alternative ')
                      print 
                      altrn = MIMEMultipart('alternative')
                      # RFC say use text before html part  
                      altrn.attach( MIMEText('\n'.join(smtp['content']['text']),'plain') )
                      altrn.attach( MIMEText('\n'.join(smtp['content']['html']),'html')  )
                      # this can be a inner part of mimemultipart
                      # - remove text and html key 
                      # - include alternative key to mark this operataion
                      lsOfNonEmptyContKey.remove('text')
                      lsOfNonEmptyContKey.remove('html')
                      lsOfNonEmptyContKey.append('multipart/alternative')
             # if user decide to use text and html parts as multipart/alternative AND
             # there is no other parts set msgdata as alternative
             # else use multipart/mixed 
             #print altrn
             #print type(altrn)
             #print lsOfNonEmptyContKey
             #print len(lsOfNonEmptyContKey)
             if altrn != MIMEBase  and  len(lsOfNonEmptyContKey) == 1:
                 dbginfo('debug','msgdata is altrn which is %s' % str(altrn)) 
                 #print 'msgdata=altrn'
                 msgdata = altrn
             else:
                 dbginfo('debug','msgdata is MIMEMultipart') 
                 msgdata = MIMEMultipart()
                 for k in lsOfNonEmptyContKey:
                     #print k
                     if k == 'multipart/alternative':
                         #print k
                         msgdata.attach(altrn)
                     if k == 'text':
                         msgdata.attach( MIMEText('\n'.join(smtp['content']['text']),'plain') )
                     if k == 'html':
                         msgdata.attach( MIMEText('\n'.join(smtp['content']['html']),'html') )
                     if k == 'img':
                         for a in smtp['content']['img'].keys():
                             msgdata.attach(get_binpart(smtp['content']['img'][a]))
                     if k == 'vof':
                         for a in smtp['content']['vof'].keys():
                             msgdata.attach( get_binpart(smtp['content']['vof'][a]) )
                     if k == 'att':
                         for a in smtp['content']['att'].keys():
                             #tmp = get_binpart(smtp['content']['att'][a])
                             #msgdata.attach(tmp)
                             msgdata.attach( get_binpart(smtp['content']['att'][a]) )
                 
         # HEADERS 
         # can not be added header when there is no data and no msgdata type was 
         # set to something different than MIMEBase
         # fpr.warn(str(msgdata))
         if msgdata == MIMEBase:
             #if DEBUG:
             #    fpr.warn('No content data was defined !')
             return 0
         #msg['Subject'] = smtp['headers'].get('h_Subject')
         for k in smtp['headers'].keys():
             #dbglog(k) #DEBUG
             if re.match('^h\d*_',k):
                 #fpr.warn(k) #DEBUG
                 h = re.match('^h\d*_(.*)$',k)
                 #fpr.cyan(str(h)) #DEBUG
                 #print (k,h.group(1)) #DEBUG
                 if smtp['headers'][k] != '':
                     if type(smtp['headers'].get(k)) is str:
                         #fpr.green(smtp[k])
                         msgdata[h.group(1)] = smtp['headers'].get(k)
                     # list is for custom headers
                     if type(smtp['headers'].get(k)) is list:
                         msgdata[h.group(1)] =  "\n".join(smtp['headers'].get(k))
                 #else:
                 #    print ('%s has empty value', k) #DEBUG


     ### NO MIME ###
     else:
         """ No MIME message - ascii plain text message """ 
         dbginfo('info', 'No MIME message, building as it is ;)' )

         #if False:
         #    import email
         #    msgdata = email.message_from_string(smtp['content']['string']) 
         #    dbginfo('debug', str(msgdata)) 
         msgdata = CMessage(smtp['content']['string'])

         #dbginfo('debug', str(msgdata)) 

     #print msg2
     #return msgdata.as_string()
     return msgdata






# --------------------------------------------------------------------------- #
# recipients builder: build envelope rcpts from headers
# --------------------------------------------------------------------------- #
def rcpt_builder(op):

    #from core.data import smtp,fpr 
    #from core.func import append_uniq 
    #from core.msg.utils import get_addresses

    opmap = { '1': 'h_To', '2': 'h_Cc', '3': 'h_Bcc', }

    print
    fpr.info('Note: Only unique addresses are going to be included')
    print

    ops = []
    if op == '4': # all
        #ops = ['h_To', 'h_Cc', 'h_Bcc']
        ops = ['1', '2', '3']
    else: 
        ops = [op]

    for op in ops:
        if smtp['headers'].get(opmap[op],None):
            fpr('Processing %s header .. ' % opmap[op])
            print
            r = get_addresses(smtp['headers'][opmap[op]])
        
            if type(r) is list:
                append_uniq(smtp['addrlist']['rcpts'],r)
                fpr(' Addresses found with header  : %d' % len(r) )  
                fpr(' Total number of recipients : %d' % len(smtp['addrlist']['rcpts']) )
                print
                #fpr('%s' % smtp['addrlist']['rcpts'] )
            else:
                fpr.err('Header %s: contains unproper list of recipients!' % opmap[op])
                #fpr('Recipients not included!')
        else:
            fpr('No %s header' % op)

# --------------------------------------------------------------------------- #
# recipients builder: build list of rcpts from input
# --------------------------------------------------------------------------- #
def rcpt_builder_f_inputs():

    #from core.data import smtp,fpr,tc,tr
    #from core.func import append_uniq,get_inputs,dbglog
    #from core.msg.utils import get_addresses

    fpr('Load recipients list using input. Press Ctrl+D to proceed.')
    print
    fpr('Paste your recipients in one or multiplea lines seperate by comma or newline')
    fpr('Use Ctrl-D with new line to continue.')

    fpr.info('_'*(tc-4))
    print 
    inputs = get_inputs()
    fpr.info('_'*(tc-4))

    if inputs != '':
        #print inputs
        r =  get_addresses(inputs) 
        append_uniq(smtp['addrlist']['rcpts'],r)
        #print get_addresses(", ".join(inputs))
        dbglog( smtp['addrlist']['rcpts'])
        print
        fpr('Processing recipients ..')
        print
        fpr(' Addresses found with input : %d' % len(r) )  
        fpr(' Total number of recipients : %d' % len(smtp['addrlist']['rcpts']) )












