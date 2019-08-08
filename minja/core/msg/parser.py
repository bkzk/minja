#
import os
import email
from email.iterators import _structure
from pprint import pprint
try: 
   from cStringIO import StringIO
except:
   from StringIO import StringIO
from core.data import smtp,smpls,fpr,cfgs,tc,tr,DEBUG
from core.func import dbginfo,dbglog,waitin,bancls,get_yesno_input,info
from core.ui.cless import Less
from core.msg.coders import decode_attch
from datetime import datetime



"""

Most non-multipart type messages are parsed as a single message object with a string payload. These objects will return False for is_multipart(). Their get_payload() method will return a string object.

All multipart type messages will be parsed as a container message object with a list of sub-message objects for their payload. The outer container message will return True for is_multipart() and their get_payload() method will return the list of Message subparts.

Most messages with a content type of message/* (e.g. message/delivery-status and message/rfc822) will also be parsed as container object containing a list payload of length 1. Their is_multipart() method will return True. The single element in the list payload will be a sub-message object.

Some non-standards compliant messages may not be internally consistent about their multipart-edness. Such messages may have a Content-Type header of type multipart, but their is_multipart() method may return False. If such messages were parsed with the FeedParser, they will have an instance of the MultipartInvariantViolationDefect class in their defects attribute list. See email.errors for details.

"""




def mail_body_parser(body):


    if not hasattr(body,'as_string'):
        fpr.err('Message can not be processed or not loaded !')
        return

    b = email.message_from_string(body.as_string())
    btype=b.get_content_type()

    dbginfo('debug', 'btype is %s' % btype)
    print

    # parse the body and save split parts in dictionary
    dparts = dict()
    body_parser(dparts,b)

    fpr.cyan('='*(tc-4))
#    pprint(dparts)

    if DEBUG: dbginfo('debug', str(dparts.keys()))

    fpr.cyan('='*(tc-4))

    ## build a dictionary

    print
    if not dparts.keys():
        fpr('No MIME parts found')
        return

    mimemulti = ['multipart/mixed','multipart/alternative']
    print mimemulti

    while True:
       bancls()
       fpr('Message MIME structure')
       print
       fpr('_'*(tc-4))
       print
       bstrio = StringIO()
       _structure(b,bstrio)
       fpr.warn('%s' % bstrio.getvalue() )
       #fpr.warn(_structure(bpart))
       fpr('_'*(tc-4))
       print 
       fpr('MIME parts ready to review:')
       print
       for k in dparts.keys():
           #print k
           #print type(k)
           if dparts[k]['type'] in mimemulti:
               fpr.info('  [%s] %s ' % (k,dparts[k]['type'][:69]) )
           else:
               fpr('  [%s] %s ' % (k,dparts[k]['type'][:69]) )
       print
       op = raw_input('  []> ')
   

       # dparts keys are int not strings
       if op.isdigit():
           k = int(op)
       if op == '':
           break
       while k in dparts.keys():
           bancls()
           fpr('MIME Headers: %s' % k)
           fpr('_'*(tc-4))
           print
           for (h,hv) in dparts[k]['mheaders']:
              fpr('%s: %s' % (h,hv))
           fpr('_'*(tc-4))


           print
#           pprint(dparts)
#           waitin()
           if dparts[k].get('type') in mimemulti:
               fpr.warn('This part is not directly viewable')
               waitin()
               break 
           elif dparts[k].get('payload'):
               fpr('Choose option:')
               print
               fpr('  1) view payload')
               fpr('  2) save payload')
               fpr.off('  3) attach payload to composer [?future feature?]')
               print
               op = raw_input('  []> ')
               if op == '':
                   waitin()
                   break
               # --- view payload --- 
               if op in ['1']:
                   bancls()
                   fpr('MIME Payload ')
                   print
                   fpr.warn('%s' % dparts[k].get('type'))
                   print

                   xe = 0
                   for (h,hv) in dparts[k].get('mheaders'):
                      #fpr('%s: %s' % (h,hv))
                      if h.lower() == 'content-transfer-encoding':
                          #part['encext'] = '.'+hv.lower() 
                          if hv in ['base64']:
                             info('info','This payload is base64 encoded. You can view it as it is or try to decode it first.')
                             print
                             if get_yesno_input('  Would like to decode the payload first [y/N]:> '):
    
                                 dp = decode_attch(dparts[k]['payload'])
                                 #pprint(dp)
                                 #print len(dp.get('raw'))
                                 #print len(str(dp))
                                 if len(dp.get('raw')) > tr:
                                 #if True:
                                     if get_yesno_input('  Would like to use system pager to view it [y/N]:> '):
              
                                         fpr('_'*(tc-4))
                                         print 
                                         pager=Less(num_lines=tr)
                                         print dp.get('raw') | pager
                                         fpr('_'*(tc-4))
                                     else:
                                         fpr('_'*(tc-4))
                                         print
                                         fpr(dp.get('raw'))
                                         print
                                         fpr('_'*(tc-4))
 

                                 waitin()
                                 xe = 1
                                 break
                   # if viewed decoded part do not display encoded one
                   if xe:
                      break 
                   print
                   if len(dparts[k].get('payload')) > tr:
                       if get_yesno_input('  Would like to use system pager to view it [y/N]:> '):

                           fpr('_'*(tc-4))
                           print 
                           pager=Less(num_lines=tr)
                           print dparts[k]['payload'] | pager
                           fpr('_'*(tc-4))
                       else:
                           fpr('_'*(tc-4))
                           print
                           fpr(dparts[k]['payload'])
                           print
                           fpr('_'*(tc-4))
                   else:

                       fpr('_'*(tc-4))
                       print
                       if type(dparts[k].get('payload')) is not 'str':
                           fpr.err('An error occured')
                       else:
                           fpr(dparts[k].get('payload'))
                       print
                       fpr('_'*(tc-4))
   
                   waitin()
               if op in ['2']:
                   bancls()
                   fpr('MIME Payload export')
                   
                   fpr('Choose option:')
                   print
                   fpr('  1) save payload, as it is (no decoding)')
                   fpr('  2) save payload - base64 decoded')
                   print
                   op = raw_input('  []> ')
                   print
                   if op == '':
                       waitin()
                       break
                   if op in ['1']:
                       bancls()
                       mpart_saver(dparts[k],1)
                       waitin()
                   if op in ['2']:
                       bancls()
                       mpart_saver(dparts[k],2)
                       waitin()
               break
           else:
               fpr.warn('Wrr: Empty payloyd. Message malformed or parsing has failed.')   
               waitin()
               break



def mpart_saver(part,op):


    if op == 1: #save as it is, no decoding
        #pprint(part)
        part['encext'] = None
        for (h,hv) in part['mheaders']:
            #fpr('%s: %s' % (h,hv))
            if h.lower() == 'content-transfer-encoding':
                part['encext'] = '.'+hv.lower() 
       
        print
        if not get_yesno_input('  Would you like to save this part: [y/N]> '): 
            return
 
        print
        if part['filename']:
            fn = part['filename'] + part['encext']
        else:
            fn ='minja-'+part['type'].replace('/','_')+'-'+datetime.now().strftime('%Y%m%d%H%M%S')+part['encext']

        print 
        fn = raw_input('  [%s]> ' % fn) or fn
        print    
 
        #if sf == sessfile or not os.path.dirname(sf):
        #   sf =  cfgs['sess_path']+'/'+sf
        if not os.path.dirname(fn):
            fn =  cfgs['mparts_path']+'/'+fn
        if os.path.exists(fn):
            fpr('File already exist')
        else:
            if os.access(os.path.dirname(fn), os.W_OK):
                #the file does not exists but write privileges are given
                fpr('Saving under %s\n' % fn)
                try:
                #f = codecs.open(fn, 'w', encoding='utf-8')
                   f = open(fn, 'w')
                   f.write(part['payload'])
                   f.close()
                   fpr.ok('Session saving')
                except IOError as e:
                   fpr.err('Saving file failed: %s' % e)
            else:
               fpr.fail('Missing write permission')

    if op == 2: #decode base64 first

        print
        if not get_yesno_input('  Would you like to save this part: [y/N]> '): 
            return
 
        print
        if part['filename']:
            fn = part['filename']
        else:
            fn ='minja-'+part['type'].replace('/','_')+'-'+datetime.now().strftime('%Y%m%d%H%M%S')

        print 
        fn = raw_input('  [%s]> ' % fn) or fn
        print    
 
        #if sf == sessfile or not os.path.dirname(sf):
        #   sf =  cfgs['sess_path']+'/'+sf
        if not os.path.dirname(fn):
            fn =  cfgs['mparts_path']+'/'+fn

        if os.path.exists(fn):
            fpr('File already exist')
        else:
            if os.access(os.path.dirname(fn), os.W_OK):
                #the file does not exists but write privileges are given
                fpr('Saving under %s\n' % fn)
                try:
                #f = codecs.open(fn, 'w', encoding='utf-8')
                   f = open(fn, 'wb')

                   d = decode_attch(part['payload'])
                   #pprint(d)
                   f.write(d['raw'])

                   f.close()
                   fpr.ok('Session saving')
                except IOError as e:
                   fpr.err('Saving file failed: %s' % e)
            else:
               fpr.fail('Missing write permission')   
 




        



def body_parser(dparts,bpart,x=0):


#    fpr('Message MIME structure')
#    print
#    fpr('_'*(tc-4))
#    from email.iterators import _structure
#    fpr.blue('%s' % _structure(bpart) )
#    #fpr.warn(_structure(bpart))
#    fpr('_'*(tc-4))
    print

    if bpart.is_multipart():

	fpr.warn('~'*(tc-4))
        for part in bpart.walk():
            print part.get_boundary()
            print part.get_content_type()            
            
        print '== multipart =='

        for payload in bpart.get_payload():
            # if payload.is_multipart(): ...
            ptype= payload.get_content_type()

            print '--> ptype: ',ptype
            
            if ptype == 'multipart/alternative':
                #dparts[x]
                for subpart in payload.get_payload():
                    print '> subpart: ', subpart.get_content_type()
                    x += 1
                    body_parser(dparts, subpart,x)

            elif ptype == 'multipart/related':
                print "---- m/realated ----"
                pprint(bpart)
                print dir(bpart)
                print bpart.get_params() 
                print bpart.get_param('start', None) 
                print bpart.get_param('type', None) 

                for i, subpart in enumerate(bpart.get_payload()):
                    print (i, subpart)
                    print '> subpart: ', subpart.get_content_type()
                    x += 1
                    body_parser(dparts, subpart,x)
                    return 
                    #if (not start and i==0) or (start and start==subpart.get('Content-Id')):
                    #    _search_message_bodies(bodies, subpart)
                    #    return              
                
            elif ptype == 'multipart/report':
                fpr.err('multipart/report is not supported')
                return
            elif ptype == 'multipart/signed':
                fpr.err('multipart/signed is not supported')
                retunr
            elif ptype == 'message/rfc822':     
#            if ptype == 
                fpr.err('message/rfc822 trying to parse')
                for subpart in payload.get_payload():
                    print '> m/rfc822 subpart: ', subpart.get_content_type()
                    x += 1
                    body_parser(dparts, subpart,x)



            else:
                print '--else ptype=:',ptype,x
                x += 1
                dparts[x] = dict()
                dparts[x]['mheaders'] = payload.items()
                dparts[x]['type'] = payload.get_content_type()
                dparts[x]['payload'] = payload.get_payload()
                dparts[x]['filename'] = payload.get_filename()
            
    else:

        print '--else no multipart'  
        print bpart.get_content_type()
        print 'x=',x

        dparts[x] = dict()
        dparts[x]['mheaders'] = bpart.items()
        dparts[x]['type'] = bpart.get_content_type()
        dparts[x]['payload'] = bpart.get_payload()
        dparts[x]['filename'] = bpart.get_filename()

        #pprint(dparts[x])
        #x +=1
        #fpr('-- Non MIME Multipart Part --')

        """ 
	fpr.warn('='*(tc-4))
        print bpart.get_payload()

	fpr.warn('='*(tc-4))
        print bpart.get_charset()

        # -- headers ---
	fpr.warn('='*(tc-4))
        print bpart.items()

	fpr.warn('='*(tc-4))
        print bpart.keys()

	fpr.warn('='*(tc-4))
        print bpart.values()

	fpr.warn('='*(tc-4))
        print bpart.get_unixfrom()

	#fpr.warn('='*(tc-4))
        #print bpart.get_()
        """

