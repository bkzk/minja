# 

def ishell():

    import time             # header Comment
    import email.utils      # header Date

    import core.ui.menu as menu
    import core.ui.wizz as wizz
    import core.msg.viewers as viewers
    import core.msg.builder as builder
    import core.msg.content as content
    import core.msg.threads as threads
    import core.msg.csdkim  as contsec
    import core.msg.parser  as parser
    import core.msg.utils as mutils
    import core.msg.dha as dha
    import core.diag.utils as dutils
    import core.diag.eauth as eauth
    import core.sess as sess
    import core.help.info as helpi 
    from core.ui.subm import m2s3_rcptlist

    from core.ui.cmenu import Menu
    from core.ui.banner import banner, bancls, bancls2
    from core.msg.sender import Logger, smtp_sender_new
    from core.data import smtp, smpls, cfgs, fpr, tc, tr, DEBUG
    from core.func import (
       astat, flush_astat, mimeuse, 
       get_single_input, 
       get_inputs, 
       get_filename, 
       get_filename2, 
       get_file_content,
       save_content_asfile,
       set_dval,
       get_yesno_input,
       waitin,
       info,
       dbginfo,
       edit,
    )

    while True: 

        bancls()
        m0_menu = Menu(menu.m)

        # ======================================== #
        # menu: def SMTP Connection Settings
        # ======================================== #
        if m0_menu.op == '1':
           while 1:
             bancls()
             m1_menu = Menu(menu.m1)
             # menu: return
             if m1_menu.op == '':
                break
             # m1_s1:
             if m1_menu.op == '1':
                bancls()
                smtp['connect']['hosts'][0]['host'] = get_single_input(
                     'Please set SMTP Host [Hostname/IPv4]:', smtp['connect']['hosts'][0]['host']
                )
             # m1_s2:
             if m1_menu.op == '2':
                bancls()
                smtp['connect']['hosts'][0]['port'] = get_single_input(
                     'Please set SMTP Port:', smtp['connect']['hosts'][0]['port']
                )

             # m1_s3: set HELO
             if m1_menu.op == '3':
                bancls()
                smtp['connect']['hosts'][0]['helo'] = get_single_input(
                     'Please set HELO/EHLO:', smtp['connect']['hosts'][0]['helo']
                )
             # m1_s4:
             if m1_menu.op == '4':
                while True:
                   bancls()
                   m1s4_menu = Menu(menu.m1s4)
                   # menu: return 
                   if m1s4_menu.op == '':
                      break
                   if m1s4_menu.op == '1':
                      pass 
                   if m1s4_menu.op == '2':
                      pass 


             # m1_s5:
             if m1_menu.op == '5':
                bancls()
                smtp['connect']['hosts'][0]['smtp_auth_user'] = get_single_input(
                     'Please set SMTP AUTH User:', smtp['connect']['hosts'][0]['smtp_auth_user']
                )
             # m1_s6:
             if m1_menu.op == '6':
                bancls()
                smtp['connect']['hosts'][0]['smtp_auth_pass'] = get_single_input(
                     'Please set SMTP password:', smtp['connect']['hosts'][0]['smtp_auth_pass']
                )
             # m1_s7:
             if m1_menu.op == '7':
                bancls()
                if smtp['connect']['hosts'][0].get('tls_mode') == 'NoTLS': 
                   fpr('TLS is Disabled')
                   if get_yesno_input('  Enable TLS mode [y/N]> '):
                      smtp['connect']['hosts'][0]['tls_mode'] = 'TLS'
                elif smtp['connect']['hosts'][0].get('tls_mode') == 'TLS':
                   fpr('TLS is Enabled')
                   if get_yesno_input('  Disable TLS mode [y/N]> '):
                      smtp['connect']['hosts'][0]['tls_mode'] = 'NoTLS'

             # m1_s8:
             if m1_menu.op == '8':
                pass

             # m1_s9:
             if m1_menu.op in ['9','v']:
                bancls()
                viewers.viewConn()

             # m1_s:
             if m1_menu.op == 'w':
                bancls()
                wizz.run_wizzard_host(smtp['connect']['hosts'][0])
             # 
             waitin()
             #break

        # ======================================== #
        # menu: def SMTP Message and Envelope
        # ======================================== #
        if m0_menu.op == '2':
          while 1:
            bancls()
            m2_menu = Menu(menu.m2)
            
            #menu: return
            if m2_menu.op == '':
               break
            # m2_s1: set HELO
            if m2_menu.op == '1':
               bancls()
               smtp['connect']['hosts'][0]['helo'] = get_single_input(
                    'Please set HELO/EHLO:', smtp['connect']['hosts'][0]['helo']
               )
               waitin()
            # m2_s2: set MAIL FROM
            if m2_menu.op == '2':
               bancls()
               smtp['addrlist']['mail_from'] = get_single_input(
                    'Please set MAIL FROM (Envelope Sender):', smtp['addrlist']['mail_from']
               )
               waitin()
            # m2_s3: set RCPT TO
            if m2_menu.op == '3':
               # submenu has been moved to separate file: ui.subm.m2s3 
               # lets see if this solution is a proper one 
               #menu.m2s3['head'] =  'Composer: Envelope Recipients'
               menu.m2s3['head'] =  'Envelope Recipients'
               m2s3_rcptlist() 
#              while True:
#                bancls()
#                m2s3_menu = Menu(menu.m2s3)
#                #menu: return
#                if m2s3_menu.op == '':
#                   break
#                #menu: m2s3s1 - Set single recipient
#                if m2s3_menu.op == '1':
#                   bancls()
#                   a = smtp['addrlist']['rcpt_to'] 
#                   smtp['addrlist']['rcpt_to'] = get_single_input(
#                        'Please set single RCPT TO (Envelope Recipient):', smtp['addrlist']['rcpt_to']
#                   )
#                   b = smtp['addrlist']['rcpt_to']
#                   fpr('old: %s\nnew: %s' % (a,b)) 
#                   def upsingleRecipient(items, a, b):
#                       if not b:
#                          if a and a in items:
#                              #return [b if x == a else x for x in items]
#                              # remove a - old 
#                              items.remove(a)
#                              
#                          return items
#                       if a and a in items: 
#                           return [b if x == a else x for x in items]
#                       else:
#                          print a, 'not in ', items
#                          print items.insert(0,b)
#                          print items
#                          return items
#                          
# 
#
#                   print  smtp['addrlist']['rcpts'] 
#                   smtp['addrlist']['rcpts'] = upsingleRecipient( smtp['addrlist']['rcpts'],a,b)
#                   print  smtp['addrlist']['rcpts'] 
#
#
#                   #TODO:
#                   #FIXME:
#                   # aktualizaca listy dla single rcpt - append nie moze byc 
#                   # tylko update lub cos podobnego 
#
#                   waitin()
#                #menu: m2s3s2 - Build list from headers [To:, Cc:, Bcc:]
#                if m2s3_menu.op == '2':
#                   while True:
#                     bancls()
#                     m2s3s2_menu = Menu(menu.m2s3s2)
#                     #menu: return
#                     if m2s3s2_menu.op == '':
#                        break
#                     if m2s3s2_menu.op in ['1','2','3','4']:
#                        bancls()
#                        # load func from msg.builder
#                        builder.rcpt_builder(m2s3s2_menu.op)
#                        waitin()                              
#
#                    #waitin()
#                   
#                #menu: m2s3s3
#                if m2s3_menu.op == '3':
#                   pass
#                #menu: m2s3s4
#                if m2s3_menu.op == '4':
#                   pass
#                #menu: m2s3s5
#                if m2s3_menu.op == '5':
#                   pass
#                #menu: m2s3s6 - Get Recipients from STDIN 
#                if m2s3_menu.op == '6':
#                   bancls()
#                   builder.rcpt_builder_f_inputs()
#                   waitin()
#                                 
#                #menu: m2s3s7
#                if m2s3_menu.op == '7':
#                   bancls()
#                   fpr('Envelope Recipients')
#                   print
#                   viewers.viewMsg('envelope')
#                   if smtp['addrlist']['rcpts']:
#                      viewers.viewEnvelope()
#                   else:
#                      fpr('wtf')
#                   waitin()
#                #menu: m2s3s8
#                if m2s3_menu.op == '8':
#                   print 
#                   mutils.flushRecipients()
#                   waitin()
#                #menu: m2s3sHELP
#                if m2s3_menu.op == '?':
#                   pass

            # m2_s4: set DATA Headers
            if m2_menu.op == '4':
               while mimeuse():
                  bancls()
                  m2s4_menu = Menu(menu.m2s4)
                  #menu: return
                  if m2s4_menu.op == '':
                     break 
                  #h_From:
                  if m2s4_menu.op == '1':
                     bancls()
                     smtp['headers']['h_From'] =  \
                         get_single_input('From: ', smtp['headers'].get('h_From',smtp['addrlist'].get('mail_from','')), nl='')
                     waitin()
                  #h_Sender
                  if m2s4_menu.op == '2':
                     bancls()
                     smtp['headers']['h_Sender'] = \
                         get_single_input('Sender: ' ,  smtp['headers'].get('h_Sender',''), nl='') #\
                     waitin()
                  #h_Return-Path
                  if m2s4_menu.op == '3':
                     bancls()
                     smtp['headers']['h_Return-Path'] = \
                         get_single_input('Return-Path: ' ,  smtp['headers'].get('h_Return-Path',''), nl='') #\
                     waitin()
                  #h_Reply-To
                  if m2s4_menu.op == '4':
                     bancls()
                     smtp['headers']['h_Reply-To'] = \
                         get_single_input('Reply-To: ' ,  smtp['headers'].get('h_Reply-To',''), nl='') #\
                     waitin()
                  #h_To
                  if m2s4_menu.op == '5':
                     bancls()
                     smtp['headers']['h_To']= \
                         get_single_input('To: ' ,  smtp['headers'].get('h_To',smtp['addrlist'].get('rcpt_to','')), nl='') #\
                     waitin()
                  #h_Cc
                  if m2s4_menu.op == '6':
                     bancls()
                     smtp['headers']['h_Cc'] =  \
                         get_single_input('Cc: ' ,  smtp['headers'].get('h_Cc',''), nl='') #\
                     waitin()
                  #h_Bcc
                  if m2s4_menu.op == '7':
                     bancls()
                     smtp['headers']['h_Bcc'] = \
                         get_single_input('Bcc: ' ,  smtp['headers'].get('h_Bcc',''), nl='') #\
                     waitin()
                  #h_Subject
                  if m2s4_menu.op == '8':
                     bancls()
                     smtp['headers']['h_Subject'] = \
                         get_single_input('Subject: ' ,  smtp['headers'].get('h_Subject',''), nl='') #\
                     waitin()
                  #h_Comment
                  if m2s4_menu.op == '9':
                     bancls()
                     defaultComment = 'Message generated by %s (%s)' % ('minja-dev',time.time())
                     smtp['headers']['h_Comment'] = \
                         get_single_input('Commment: ' , smtp['headers'].get('h_Comment',defaultComment), nl='') #\
                     waitin()
                  #h_Date
                  if m2s4_menu.op == '10':
                     bancls()
                     currentDate =  email.utils.formatdate(localtime=True)
                     smtp['headers']['h_Date'] = \
                         get_single_input('Date:',  currentDate, nl='') #or currentDate
                     waitin()
                  #h_X-Custom:
                  if m2s4_menu.op in ['11']:
                     bancls()
                     fpr.info('_'*(tc-4))
                     content.att_custom_header()
                     waitin()
 
                  #viewer   
                  if m2s4_menu.op in ['12','v']:
                     bancls()
                     fpr.info('_'*(tc-4))
                     viewers.viewMsg('headers')
                     waitin()
                  #wizzard        
                  if m2s4_menu.op == 'w':
                     bancls()
                     wizz.run_wizzard_headers()
                     waitin()

            # ---- d a t a  c o n t e n t ---- #

            # m2_s5: set DATA Content
            if m2_menu.op == '5':
               while True:
                 bancls()
                 m2s5_menu = Menu(menu.m2s5)
                 #menu: return
                 if m2s5_menu.op == '':
                    break
                 #menu: m2s5s1 - 
                 if m2s5_menu.op == '1':
                    while True: 
                       bancls()
                       m2s5s1_menu = Menu(menu.m2s5s1)
                       
                       #menu: return
                       if m2s5s1_menu.op == '':
                          break

                       #menu: m2s5s1s1 - define new Content as String
                       if m2s5s1_menu.op == '1':
                          bancls() 
                          if astat():
                             info('info','You have alredy defined some Body Content Parts. ' \
                                         'First flush it before building a custom Body Content!')
                          else:
                             fpr('Build new custom Body content (input text)')
                             info('info','You are going to define custom Body content. '\
                                         'Note: You can not attach predefined Body Parts or Headers to your custom Body. ' \
                                         'But you can build your Message with predefined content parts and headers first and then modify with (e) edit option.')
                             waitin()
                             #bancls()
                             fpr('Use Ctrl-D with new line to continue.')
                             content.att_cont_as_string()
                             flush_astat()
                          waitin()
      

                       if m2s5s1_menu.op == '2':
                          bancls()
                          if astat():
                             info('info','You have alredy defined some Body content parts. ' \
                                         'First flush it before building a custom Body content!')
                          else:
                             fpr('Build new custom Body content (external editor)')
                             info('info','You are going to define custom Body content. '\
                                         'Note: You can not attach predefined Body Parts or Headers to your custom Body. ' \
                                         'But you can build your Message with predefined content parts and headers first and then modify with (e) edit option.')
                             waitin()
                             #status, text = edit('vim')
                             #tmpmsg = builder.msg_builder()
                             #status, text = edit(cfgs['editor'], tmpmsg.as_string(unixfrom=False) )
                             status, text = edit(cfgs['editor'])
                             if status:
                                # Non-zero exit status of the call to the editor indicates 
                                # that sth goes wrong
                                dbgino('warn','Something goes wrong when exiting external editor')
                             elif text:
                                # Zero is goood
                                content.att_cont_as_string(text)
                                #dbginfo('debug',text)
                             else:
                                fpr('No content data was defined !')
                              
                          waitin()
                       #menu: m2s5s1s3 - define new Plain content
                       if m2s5s1_menu.op == '4':
                          #if mimeuse():
                          #   waitin()
                          #else:
                          #   print 'ddd'
 
                          mbody = smtp['content']['text']
                          while mimeuse():
                             bancls()
                             if smpls['userin']['astat'] != 0:
                                fpr('It seems you have already attached this sample')
                                if not raw_input('  Do you want to append another one [y/N]:') in ['y','Y']:
                                   break
                                bancls()
                             fpr('Please provide your own PLAIN content')
                             fpr('Use Ctrl-D with new line to continue.')
                             print 
                             fpr.info('_'*(tc-4))
                             print
                             inputs = get_inputs(nl=True)
                             fpr.info('_'*(tc-4))
      
                             if inputs:
                                print
                                mbody.extend(inputs)
                                smpls['userin']['astat'] += 1
                                fpr('User INPUT TEXT Sample attached (x%d)' % smpls['userin']['astat'])
                                #break
   
                             waitin()
                             break
 
                       #menu: m2s5s1 - load body from file ( Menu )
                       if m2s5s1_menu.op == '3':
                           while mimeuse():
                                  bancls()
                                  fpr('Load message file')
                                  print
                                  fpr('Please provide a full PATH to file (/path/to/file.eml)')
                                  emlfn = raw_input('  > ')
                                  if emlfn:
                                     #content.att_load_eml(smtp['content'].setdefault('string',''),emlfn)
                                     mbody = smtp['content']
                                     content.att_load_eml(mbody,emlfn)
                                     if mbody['string']:
                                         smtp['use_mime'] = False
                                     waitin()
                                     break
                                  print
                                  if raw_input('  Return to menu [y/N]> ') in ['y','Y']:
                                     break
                                

                 #menu: m2s5s2 - define new Attachment ( Menu )
                 if m2s5_menu.op == '2':
                    #while True:
                    while mimeuse():
                      bancls()
                      m2s5s2_menu = Menu(menu.m2s5s2)
                      if m2s5s2_menu.op == '':
                         break
                      #menu: m2s5s2s1: load new file 
                      if m2s5s2_menu.op == '1':
                         while True:
                            bancls()
                            fpr('Load attachment from file')
                            print
                            fpr('Please provide a full PATH to an attachment (/path/to/file.doc)')
                            attfn = raw_input('  > ')
                            if attfn:
                               content.att_load_file(smtp['content']['att'],attfn)
                            print
                            if raw_input('  Return to menu [y/N]> ') in ['y','Y']:
                               break
 
                      #menu: m2s5s2s2: paste base64 attachment
                      if m2s5s2_menu.op == '2':
                         bancls()

                         fpr('Paste your base64 encoded part - an attachment.') 
                         fpr('Note:  All empty lines and whitespaces will be removed!')
                         print 
                         #fpr.info('_'*(tc-4))
                         #while True: 
                         content.att_load_base64(smtp['content']['att'])
                         #   break
                         #fpr.info('_'*(tc-4))
                       
                    waitin()
                 # att SPAM
                 if m2s5_menu.op == '3':
                    if mimeuse():
                       bancls()
                       content.att_plain_sample(smtp['content']['text'], 'spam', menu.sm_spam)
                       waitin()
                 # att VIRUS
                 if m2s5_menu.op == '4':
                    if mimeuse():
                       bancls()
                       content.att_plain_sample(smtp['content']['text'], 'virus', menu.sm_virus)
                       waitin()
                 # att MALWARE
                 if m2s5_menu.op == '5':
                    if mimeuse():
                       bancls()
                       content.att_plain_sample(smtp['content']['text'], 'mal', menu.sm_mal)
                       waitin()
                    
                 # att DLP
                 if m2s5_menu.op == '6':
                    if mimeuse():
                       bancls()
                       content.att_plain_sample(smtp['content']['text'], 'dlp', menu.sm_dlp)
                       waitin()
                 # att VOF
                 if m2s5_menu.op == '7':
                    if mimeuse():
                       bancls()
                       content.att_raw_sample(smtp['content']['vof'], 'vof', menu.sm_vof)
                       waitin()
                 # att ImA
                 if m2s5_menu.op == '8':
                    if mimeuse():
                       bancls()
                       content.att_raw_sample(smtp['content']['img'], 'img', menu.sm_img)
                       waitin()
                 # att TXT
                 if m2s5_menu.op == '9':
                    if mimeuse():
                       bancls()
                       content.att_plain_sample(smtp['content']['text'], 'txt', menu.sm_txt)
                       waitin()
                 # att HTML
                 if m2s5_menu.op == '10':
                    if mimeuse():
                       bancls()
                       content.att_plain_sample(smtp['content']['html'], 'html', menu.sm_html)
                       waitin()
                 #menu: m2s5s11 - zip ATT : Menu :
                 if m2s5_menu.op == '11':
                    #while True:
                    while mimeuse():
                      bancls()
                      m2s5s11_menu = Menu(menu.m2s5s11)
                      #menu: return
                      if m2s5s11_menu.op == '':
                         break
# THE ZIP SHIIIIT !!!! 
                      #menu: text samples (gtube,eicar,dlp-cpi,plain text and 
                      #      html, even the "vof" sample 
                      if m2s5s11_menu.op in [ '1','2','4','5','7','8']:
                         bancls()
                         opts = { '1': 'spam', '2': 'virus', '4': 'dlp', '5': 'vof',
                                  '7': 'txt', '8': 'html' }
 
                         smtype = opts[m2s5s11_menu.op]
                         mbody  = smtp['content']['att']
                         sn     = '1'

                         content.att_zip_plain_sample(mbody,smtype,sn)
                          
                      #menu: malware
                      if m2s5s11_menu.op == '3':
                         pass
                      #menu: image
                      if m2s5s11_menu.op == '6':
                         bancls()
                         mbody  = smtp['content']['att']
                         sn     = '1'
                         smtype = 'img'
                         content.att_zip_file(mbody,smtype,sn)

                      #menu: user input
                      if m2s5s11_menu.op == '9':
                         bancls()
                         mbody  = smtp['content']['att']
                         sn     = '1'
                         smtype = 'zip-input'
                         content.att_zip_input(mbody,smtype,sn)
                      #menu: zip already loaded attachment
                      if m2s5s11_menu.op == '10':
                         pass
                      #menu: load and zip new file 
                      if m2s5s11_menu.op == '11':
                         bancls()
                         mbody  = smtp['content']['att']
                         sn     = '1'
                         smtype = 'zipfile'

                         while True:
                            bancls()
                            fpr('Load attachment from file')
                            print
                            fpr('Please provide a full PATH to an attachment (/path/to/file.doc)')
                            attfn = raw_input('  > ')
                            if attfn:
                               #att_load_file( attfn )
                               content.att_load_and_zip_file(mbody,smtype,sn,attfn)
                            print
                            if raw_input('  Return to menu [y/N]> ') in ['y','Y']:
                               break
 

                      #menu: help 
                      if m2s5s11_menu.op == '?':
                         pass
                         
                 #menu: m2s5s12 - view Message Body
                 if m2s5_menu.op in ['12','v','vb']:
                    #print
                    bancls()
                    fpr.info('_'*(tc-4))
                    viewers.viewMsg('data')
                    waitin()
                 #menu m2s5ms13 - edit message body
                 if m2s5_menu.op in ['13','e']:
                    bancls()
                    fpr('Customize Body content (external editor)')
                    info('info','You are going to define custom Body content. '\
                                'Note: You can not attach predefined Body Parts or Headers to your custom Body. ' \
                                'But you can build your Message with predefined content parts and headers first and then modify with (e) edit option.')
                    waitin()

                    tmpmsg = builder.msg_builder()
                    #print type(tmpmsg)
                    #print dir(tmpmsg)
                    #if type(tmpmsg) is not int:
                    mcontent = ''                    
                    if hasattr(tmpmsg,'as_string'):
                       #status, text = edit(cfgs['editor'], tmpmsg.as_string(unixfrom=False) )
                       mcontent = tmpmsg.as_string(unixfrom=False)
                    #
                       #icontent = '' 
                    if True:
                       #status, text = edit(cfgs['editor'], tmpmsg.as_string(unixfrom=False) )
                       status, text = edit(cfgs['editor'], mcontent )
                       #dbginfo('debug',"status: %s" % status)
                       #dbginfo('debug',"text: %s" % text)
                       if status:
                          # Non-zero exit status of the call to the editor indicates 
                          # that sth goes wrong
                          dbgino('warn','Something goes wrong with exiting external editor')
                       elif text:
                          # Zero is goood
                          if hasattr(tmpmsg,'as_string'):
                             if text != tmpmsg.as_string(unixfrom=False):
                                content.att_cont_as_string(text)
                                flush_astat()
                             else:
                                fpr('Current DATA Content has not been modified')
                          else:
                             content.att_cont_as_string(text)
                             flush_astat()
                       else: 
                          
                          dbginfo('debug','No text part return by external editor!')
                    #else:
                    #   fpr('No content data was defined !')
                    waitin()


             # m2_s6: set DATA Security
            if m2_menu.op == '6':
               while True:
                 bancls()
                 m2s6_menu = Menu(menu.m2s6)
                 #menu: return
                 if m2s6_menu.op == '':
                    break
                 #menu: m2s6s1 - 
                 if m2s6_menu.op == '1':
                    while True: 
                       bancls()
                       m2s6s1_menu = Menu(menu.m2s6s1)
                       #menu: return
                       if m2s6s1_menu.op == '':
                          break
                       #menu: m2s6s1 - DKIM privkey 
                       if m2s6s1_menu.op == '1':
                          while True:
                             bancls()
                             m2s6s1s1_menu = Menu(menu.m2s6s1s1)

                             n  = smtp['sign']['dkim']['dstat']
                             dn = smtp['sign']['dkim'].setdefault(n,{})

                             #menu: return
                             if m2s6s1s1_menu.op == '':
                                break
                             #menu: input
                             if m2s6s1s1_menu.op == '1':

                                while True:
                                   bancls()
                                   fpr('Please paste your PKCS#1 DKIM private key')
                                   fpr('Use Ctrl-D with new line to continue.')
                                   print 
                                   fpr.info('_'*(tc-4))
                                   print
                                   inputs = get_inputs()
                                   fpr.info('_'*(tc-4))
   
                                   if inputs:
                                      #check if key is correct
                                      # join with \n as line was strip from it
                                      if contsec.dkim_pktest('\n'.join(inputs)):
                                         dn['privkey'] = '\n'.join(inputs)
                                         fpr.ok('Private key saved')
                                      else:
                                         fpr.fail('Private key not found')
                                   break
 
                                waitin()
                             #menu: file
                             if m2s6s1s1_menu.op == '2':
                                
                                fn = get_filename()
                                print
                                if fn:
                                   fpr('Loading content of %s .. ' % fn)
                                   inputs = get_file_content(fn)
                                   #dbginfo('debug',inputs)
                                   if inputs:
                                      # join without \n as line already has it
                                      if contsec.dkim_pktest(''.join(inputs)):
                                         dn['privkey'] = ''.join(inputs)
                                         fpr.ok('Private key saved')
                                      else:
                                         fpr.fail('Private key not found')
                              
                                waitin()
                             #menu: view
                             if m2s6s1s1_menu.op in ['3','v']:
                                k = 0 
                                bancls()
                                fpr('DKIM Private key(s)')
                                while (k <= smtp['sign']['dkim']['dstat']):
                                   print
                                   if k == smtp['sign']['dkim']['dstat']:
                                      fpr.warn( 'Private key #%s' % k, adj='r')
                                   else:
                                      fpr( 'Private key #%s' % k, adj='r')

                                   if smtp['sign']['dkim'].get(k,None): #['privkey']:
                                      info('info', smtp['sign']['dkim'][k]['privkey'] , adj='l' )
                                      print
                                   else:
                                      info('info','No Private key for current key index')
                                   k += 1

                                waitin()
                            
                       #menu: m2s6s1 - DKIM 
                       if m2s6s1_menu.op == '2':
                          while True:
                            bancls()
                          
                            n  = smtp['sign']['dkim']['dstat']
                            dn = smtp['sign']['dkim'].setdefault(n,{})
 
                            m2s6s1s2_menu = Menu(menu.m2s6s1s2)
                            #menu: return
                            if m2s6s1s2_menu.op == '':
                                bancls()
                                break
                            #menu: dkim-tag: version
                            if m2s6s1s2_menu.op in ['1','v']:
                                bancls()
                                pass
                            #menu: dkim-tag: algorithm
                            if m2s6s1s2_menu.op in ['2','a']:
                                bancls()
                                pass
                            #menu: dkim-tag: canonicalization
                            if m2s6s1s2_menu.op in ['3','c']:
                                bancls()
#                                defcanon = ''
#                                if type (dn.get('canonicalize','relaxed/simple')) is tuple:
                                   #convert tuple to str 
#                                   (l,r) = dn.get('canonicalize')
#                                   defcanon = str(l)+'/'+str(r)
#                                else:
#                                   defcanon = dn.get('canonicalize','relaxed/simple')
                                
                                tcanon = set_dval(q='  Set (c=) tag for canonicalize', dd=dn, key='canonicalize', val='relaxed/simple',ret=True)
                                if contsec.dkim_canontest(tcanon):
                                    dn['canonicalize']=tcanon
                                    fpr.ok('Canonicalization test success:')
                                else: 
                                    print
                                    fpr.fail('Canonicalization test failed')

                                waitin() 
                            #menu: dkim-tag: selector
                            if m2s6s1s2_menu.op in ['4','s']:
                                bancls()
                                set_dval(q='  Set (s=) tag for selector', dd=dn, key='selector', val='x')
                            #menu: dkim-tag: domain
                            if m2s6s1s2_menu.op in ['5','d']:
                                bancls()
                                dom=''
                                if smtp['addrlist'].get('mail_from'):
                                    dom = mutils.get_address_domain(smtp['addrlist'].get('mail_from'))
                                elif smtp['headers'].get('h_From'):
                                    dom = mutils.get_address_domain(smtp['headers'].get('h_From'))

                                if not dn.get('domain') and dom:
                                   fpr('Suggested domain is based first on RFC5321.MailFrom (envelope) and next on  '\
                                       'RFC5322.From (header)')
                                   print
                                set_dval(q='  Set (d=) tag for domain', dd=dn, key='domain', val=dom)

                            #menu: dkim-tag: headers
                            if m2s6s1s2_menu.op in ['6','h']:
                                while True:
                                   bancls()

                                   m2s6s1s2s1_menu = Menu(menu.m2s6s1s2s1)
                                   #menu: return
                                   if m2s6s1s2s1_menu.op == '':
                                      bancls()
                                      break
                                   #menu:
                                   if m2s6s1s2s1_menu.op == '1':
                                      bancls()
                                      fpr('DKIM-Signature > Headers sign')
                                      print
                                      info('info','Include default list of header names for signing: [from : to : subject]',adj='l')
                                      print
                                      if get_yesno_input('  Would you like to set default list [y/N]'):
                                         dn['header'] = 'from : to : subject'
                                         print
                                         fpr.ok('Headers assigned')
                                      else:
                                         fpr.fail('Headers not assigned')
                                   #
                                   # FIXME: include parser for headers
                                   #
                                   #menu:
                                   if m2s6s1s2s1_menu.op == '2':
                                      bancls()
                                      fpr('DKIM-Signature > Headers sign')
                                      print
                                      info('info','Provide list of lowercase header nemas separate by colen',adj='l')
                                      #fpr('_'*(tc-4))
                                      inputs = get_single_input('Headers ',dn.get('header',''))
                                      #fpr('_'*(tc-4))
                                      if inputs:
                                         # parse inputs 
                                         if True:
                                            print
                                            dn['header']  = inputs
                                            fpr.ok('Headers assigned')
                                         else:
                                            fpr.fail('Headers not assigned')
                                   waitin()
                            #menu: dkim-tag: identity
                            if m2s6s1s2_menu.op in ['7','i']:
                                bancls()
                                did=''
                                # suggest identity based on domain tag if exist or based on mail address domain
                                if dn.get('domain'):
                                    did = '@' + dn.get('domain')
                                elif smtp['addrlist'].get('mail_from'):
                                    did = mutils.get_address_domain(smtp['addrlist'].get('mail_from'))
                                    if did:
                                       did = ''.join(('@',did))
                                elif smtp['headers'].get('h_From'):
                                    did = mutils.get_address_domain(smtp['headers'].get('h_From'))
                                    if did:
                                       did = ''.join(('@',did))

                                if not dn.get('identity') and did:
                                   
                                   fpr('Suggested identity is based first on domain name from d= tag and next on '\
                                       'RFC5321.MailFrom (envelope) and next on RFC5322.From (header)')
                                   print

                                set_dval(q='  Set (i=) tag for identity', dd=dn, key='identity', val=did)
                               
                            #menu: dkim-tag: length
                            if m2s6s1s2_menu.op in ['8','l']:
                                bancls()
                                #set_dval(q='  Set (l=) tag for length', dd=dn, key='length', val=None)
                                fpr('The secure option is to keep this tag off.')
                                print
                                dn['length'] = get_yesno_input('  Set (l=) tag for length [yes/No]: ') 
                            #menu: generate sig
                            if m2s6s1s2_menu.op in ['12','g']:
                               bancls()
                               fpr('Generating DKIM-Signature:')
                               tmpmsg = builder.msg_builder()
                               if hasattr(tmpmsg,'as_string'):
                                  #dn['privkey'] = open('/root/minja/minja.project/minja/modules/private_key.dkim','rb').read()
                                  if contsec.dkim_pktest(dn.get('privkey')):
                                     dn['sig'] = contsec.dkim_signature(tmpmsg.as_string(),dn)
                                     if dn.get('sig',None):
                                        info('info','DKIM-Signature: '+dn['sig'],adj='l')
                                     else:
                                        fpr.fail('DKIM Signature was not generated')
                                  else:
                                     fpr.fail('Missing DKIM Private key.')
                                     print
                                     info('info','If you have already attached one signature and need to attach another one ' \
                                                 '   you need to load new private key for each new signature.')

                               else:
                                  print
                                  fpr('No content data was defined !')
                                   
                               waitin() 
                            #menu: view sig
                            if m2s6s1s2_menu.op in ['10','v']:
                                #dbginfo('debug',str(dn))
                                bancls()
                                viewers.viewDKIMSignTag()
                                waitin()
                            #menu: flush sig
                            if m2s6s1s2_menu.op in ['11','f']:
                                bancls()
                                if raw_input('  Flush current Tags and Signature [y/N]:> ') in ['y','Y']:
                                   #print dn
                                   for k in dn.keys():
                                       if k != 'privkey':
                                          del dn[k]
                                   fpr.ok('Current DKIM Signature and Tags were flushed')
                                   #print dn
                                #flushDKIMTags()
                                waitin()
                            #menu: attach sig 
                            if m2s6s1s2_menu.op == '13':
                                bancls()
                                if dn.get('sig',None):
                                   contsec.att_dkim_signature(dn['sig'])
                                elif smtp['sign']['dkim']['dstat'] > 0:
                                   fpr('No new DKIM Signature. Already x%s signature was attached.' % 
                                        smtp['sign']['dkim']['dstat'])
                                else:
                                   fpr('No DKIM Signature was generated ')
                                waitin()
                            #menu: run Wizzard
                            if m2s6s1s2_menu.op == 'w':
                                pass
                            #menu: dbg Option- canonicalization
                            if m2s6s1s2_menu.op in ['9','canon']:
                                bancls()
                                tmpmsg = builder.msg_builder()
                                
                                if hasattr(tmpmsg,'as_string'):
                                    fpr('Message canonicalization')
                                    print
                                    fpr.warn('_'*(tc-4))
                                    print
                                    print tmpmsg.as_string()
                                   # contsec._dkim_canon(dn['canonicalize'],tmpmsg)
                                    (ch,cb) =  contsec.dkim_canon('relaxed/relaxed',tmpmsg.as_string())
                                    if DEBUG:
                                        fpr.purple('_'*(tc-4))
                                        from pprint import pprint 
                                        pprint(ch)
                                        fpr.purple('_'*(tc-4))

                                    fpr.warn('_'*(tc-4))
                                    print
                                    fpr("Canonicalized Headers")
                                    fpr.info('_'*(tc-4))
                                    print
                                    for (hn,hv) in ch:
                                        print "%s:%s" % (hn,hv.rstrip())
                                    fpr.info('_'*(tc-4))
                                    print
                                    fpr("Canonicalized Body")
                                    fpr.info('_'*(tc-4))
                                    print cb
                                    fpr.warn('_'*(tc-4))
                                    
                                waitin()
                       #menu: m2s6s3 - view DKIM 
                       if m2s6s1_menu.op == '3':
                          bancls()
                          viewers.viewDKIMSignTag(_all=True)
                          waitin()
                       #menu: m2s6s3 - flush DKIM 
                       if m2s6s1_menu.op == '4':
                          bancls()
                          mutils.flushDKIMHeaders()
                          waitin()
                          

            # ---- v i e w e r s ---- #
            # m2_s7: view Envelope
            if m2_menu.op in ['7','ve']:
               bancls()
               viewers.viewMsg('envelope')
               if smtp['addrlist']['rcpts']:
                  viewers.viewEnvelope()
               waitin()
            # m2_s8: view Message headers
            if m2_menu.op in ['8','vh']:
               bancls()
               fpr.info('_'*(tc-4))
               viewers.viewMsg('headers')
               waitin()
           # m2_s9: view Message body
            if m2_menu.op in ['9','vb']:
               bancls()
               fpr.info('_'*(tc-4))
               #viewTheMsg()
               viewers.viewMsg('data')
               waitin()
            # m2_s10: view Message structure
            if m2_menu.op in ['10','vs']:
               bancls()
               viewers.viewTheMsg('structure')
               waitin()
            # m2_s11: view Message and Envelope
            if m2_menu.op in ['11','vm']:
               bancls()
               viewers.viewMsg('all')
               waitin()
            if m2_menu.op == 'v':
               bancls()
               fpr.info(' Help: v - viewer shortcuts:') 
               fpr.info('   ve - view envelope') 
               fpr.info('   vh - view headers') 
               fpr.info('   vb - view body') 
               fpr.info('   vm - view message') 
               waitin()

            # ---- f l u s h e r s ---- #
            # m2_s11: flush Envelope recipient
            if m2_menu.op in ['12','fe']:
               bancls()
               mutils.flushRecipients()
               waitin()
            # m2_12: flush Message body
            if m2_menu.op in ['13','fb']:
               bancls()
               mutils.flushMsgContent()
               waitin()
            # m2_s13: flush Message headers
            if m2_menu.op in ['14','fh']:
               bancls()
               mutils.flushMsgHeaders()
               waitin()
            if m2_menu.op == 'f':
               bancls()
               fpr.info(' Help: f - flush shortcuts:') 
               fpr.info('   fe - flush envelope') 
               fpr.info('   fh - flush headers') 
               fpr.info('   fb - flush body') 
               waitin()



        # ======================================== #
        # menu: send/replay Message
        # ======================================== #
        if m0_menu.op == '3':
           while 1:
             bancls()
             m3_menu = Menu(menu.m3) 
             #menu: return
             if m3_menu.op == '':
                break
             # m3_s1: send Message
             if m3_menu.op == '1':
                bancls()
                fpr('SMTP Message: Single injection')
                print
                # print smtp connection setting 
                
                # verify if message was defined

                # build message
                message = builder.msg_builder()
                # confirm  - TODO [ msgx is always true

                if message:
                    
                    #from core.msg.viewers import viewSmtpSess
                    viewers.viewSmtpSess()
                    #from core.msg.threads import get_rcpts
                    #if smtp['addrlist']['rcpt_to'] and smtp['addrlist']['rcpts']:
                    if threads.get_rcpts('NoR') > 1:
                        fpr.warn('_'*(tc-4))
                        print
                        fpr('Multiple recipients were defined !','c')
                        print
                        fpr('All recipients are attached to single message with single connection')
                        fpr('To test MTA limits or restriction try smtp replay option.')
                        fpr.warn('_'*(tc-4))

                    print
                    if not threads.get_rcpts('NoR'): 
                       fpr.err('Please return and define some recipient')
                    
                    elif  raw_input('  Confirm sending [y/N]:> ') in ['y','Y']:
                        # clearr old failed addresses
                        smtp['addrlist']['r_reject'].clear()
                        smtp['addrlist']['r_valid'].clear()
                        # enable logging
                        #from core.msg.sender import Logger
                        logger = Logger()

#                                 kwargs=dict(message=self.msg,
#                                         rpm=self.rpm,
#                                         mpt=self.mpt,
#                                         rate=self.rate,
#                                         rcpts=t_rcpts,
#                                         name='T-%d' % i,) , 
#                                   name='T-%d' % i, verbose=None,  )
                            
                        #s_rcpts = [smtp['addrlist']['rcpt_to']]+smtp['addrlist']['rcpts'] 
                        s_rcpts = smtp['addrlist']['rcpts'] 
                        #smtp_sender(message=message,name='T-Single', rcpts=s_rcpts)
                        smtp_sender_new(message=message,name='T-Single', rcpts=s_rcpts)

                        logger.close()
                else:
                    #fpr('No content data was defined !')
                    print
                    fpr('No content data was defined !')
                    print
                    fpr.err('Return to compose message DATA')

                waitin()
             # m3_s2: smtp Replay
             if m3_menu.op == '2':
                while True:
                  bancls()
                  m3s2_menu = Menu(menu.m3s2)
                  # menu: return
                  if m3s2_menu.op == '':
                     break
                  #menu: m3s2s1 - set Threads
                  if m3s2_menu.op == '1':
                     bancls()
                     fpr('%s: NOT - Number Of Threads' % menu.m3s2['head'])
                     print
                     threads.get_threads_no()
                     print
                     waitin()
                  #menu: m3s2s2 - set Rates & Limits
                  if m3s2_menu.op == '2':
                     while True:
                        bancls()
                        m3s2s2_menu = Menu(menu.m3s2s2)
                        #menu: 
                        if m3s2s2_menu.op == '':
                           break
                        #menu: 
                        if m3s2s2_menu.op == '1':
                           bancls()
                           fpr('%s: RPM - Recipients Per Message' % menu.m3s2['head'])
                           print
                           threads.get_rcpt_no()
                           waitin() 
                        #menu: 
                        if m3s2s2_menu.op == '2':
                           bancls()
                           fpr('%s: MPT - Messages Per Thread ( SMTP connection )' %  menu.m3s2['head'] )
                           print
                           threads.get_msgs_no()
                           waitin()
                        #menu: 
                        if m3s2s2_menu.op == '3':
                           bancls()
                           fpr('%s: RATE - Recipients per Hour/ Minute / Seconds' % menu.m3s2['head'])
                           print
                           threads.get_rate()
                           waitin()
                        #menu: 
                        if m3s2s2_menu.op == '4':
                           bancls()
                           fpr('%s: DELAY' %  menu.m3s2['head'])
                           threads.get_msgs_delay()
                           print
                           waitin()
                  #menu: m3s2s3 - set Interfaces
                  if m3s2_menu.op == '3':
                     """
                     Bind to source address was inluded in 
                      - https://bugs.python.org/issue11281
                      - https://hg.python.org/cpython/rev/26839edf3cc1
                     """
                     #bancls() 
                     #fpr.info('-- TODO --',adj='c')
                     #print
                     #fpr.info('Binding to specific source address in a machine with multiple \
                     #          interfaces is part of smtplib in python > 3.3 ')
                     #waitin()
                     pass
                  #menu: m3s2s4 - set Relay/Dest Hosts
                  if m3s2_menu.op == '4':
                     pass
                  #menu: m3s2s5 - set Proxy
                  if m3s2_menu.op == '5':
                     pass
                  #
                  if m3s2_menu.op in ['6','v']:
                     bancls() 
                     threads.viewThreadsSummary()
                     waitin()
                  #menu: m3s2s7 - flush
                  if m3s2_menu.op in ['7','f']:
                     bancls()
                     #fpr('Flushing threads settings ..')
                     threads.flushThrValues()
                     waitin() 
                  #menu: m3s2s8 - run Threads
                  if m3s2_menu.op in ['8','r']:
                     bancls() 
                     #threads.viewThreadsSummary()
                     #print 
                     threads.runThreads()
                     waitin()
                  #menu: m3s2s? - help
                  if m3s2_menu.op == '?':
                     pass
                
             # menu: DHA
             if m3_menu.op == '3':
                while True:
                   bancls()
                   m3s3_menu = Menu(menu.m3s3)
                   #menu: return
                   if m3s3_menu.op == '':
                      break
                   #menu:set USERLIST 
                   if m3s3_menu.op == '1':
                      # redirect to the same menu used for message builder
                      menu.m2s3['head'] =  menu.m3s3['head']+': Envelope Recipients'
                      m2s3_rcptlist()
                      #while True:
                         #bancls()
                         #m3s3s1_menu = Menu(menu.m3s3s1)
                         #if m3s3s1_menu.op == '':
                         #   break

                   #menu: SMTP COMMAND Method  
                   if m3s3_menu.op == '2':
                       pass
                       while True:
                         bancls()
                         #fpr('Current method: %s' % smtp['dha'].get('cmd'))
                         m3s3s2_menu = Menu(menu.m3s3s2)
                         smtp_cmd = {'1': 'EXPN', '2': 'VRFY', '3': 'RCPT TO'}
                         #menu: return
                         if m3s3s2_menu.op == '':
                            break
                         #menu: 
                         if m3s3s2_menu.op in smtp_cmd.keys():
                            smtp['dha']['cmd'] = smtp_cmd[m3s3s2_menu.op]
                            fpr('Saving %s method' % smtp_cmd[m3s3s2_menu.op] )
                            waitin()
                   #menu: 
                   if m3s3_menu.op == '3':
                      bancls()
                      fpr('%s: NOT - Number Of Threads' % menu.m3s3['head'])
                      print
                      dha.get_threads_no()
                      waitin()
                   #menu: 
                   if m3s3_menu.op == '4':
                      bancls()
                      fpr('%s: CPT - Number Of Commands per thread (connection)' % menu.m3s3['head'])
                      print
                      dha.get_cpt_no()
                      waitin()
                      
                   #menu: 
                   if m3s3_menu.op == '5':
                      bancls()
                      fpr('%s: TIMEOUT - query response time' % menu.m3s3['head'])
                      print
                      dha.get_timeout()
                      waitin()
                      
                   #menu: 
                   if m3s3_menu.op == '6':
                      bancls()
                      fpr('%s: DELAY - between running threads' % menu.m3s3['head'])
                      print
                      dha.get_delay()
                      waitin()
                   #menu: 
                   if m3s3_menu.op in ['7','v']:
                      bancls() 
                      fpr('%s: Settings' % menu.m3s3['head'])
                      dha.viewDHAThreadsSummary()
                      waitin()
                   #menu: 
                   if m3s3_menu.op in ['8','f']:
                      bancls() 
                      #fpr('Flushing threads settings ..')
                      dha.flushDHAThrValues()
                      waitin() 
                   if m3s3_menu.op in ['9','r']:
                      bancls() 
                      #dha.viewDHAThreadsSummary()
                      #print 
                      dha.runDHAThreads()
                      waitin()
                   if m3s3_menu.op == 'e':
                      bancls()
                      if get_yesno_input('  Would you like to proceed with the command enumeration test [y/N]: '):
                          dha.enumSMTPcmd(v=True,dhost=smtp['connect']['hosts'][0])
                      waitin()
                   #menu: m3s3s? - help
                   if m3s3_menu.op == '?':
                      pass
                





             # m3_s4: view Connection settings
             if m3_menu.op in ['4','vc']:
                bancls()
                viewers.viewConn()
                waitin()
             # m3_s5: view Message and Envelope
             if m3_menu.op in ['5','vm']:
                bancls()
                fpr.info('_'*(tc-4))
                #viewTheMsg()
                viewers.viewMsg('all')
                waitin()
 
             if m3_menu.op in ['6','vr']:
                 while True:
                    bancls()
                    m3s6_menu = Menu(menu.m3s6)
                    #menu: return
                    if m3s6_menu.op == '':
                       break
                    if m3s6_menu.op == '1':
                       bancls()
                       viewers.viewRefusedAddresses()
                    if m3s6_menu.op == '2':
                       bancls()
                       viewers.viewAcceptedAddresses()

                    waitin()
             if m3_menu.op == 'v':
                 bancls()
                 fpr.info(' Help: v - viewer shortcuts:') 
                 fpr.info('   vc - view connection') 
                 fpr.info('   vm - view message') 
                 fpr.info('   vr - view results') 
                 waitin()


           

        # ======================================== #
        # menu: run analyses
        # ======================================== #
        if m0_menu.op == '4':
            smtp.setdefault('parser',dict())
            while True:
                mbody = smtp['parser']
                tmpmsg = ''
                bancls()

                m4_menu = Menu(menu.m4)
                #menu: return
                if m4_menu.op == '':
                    break
                #m4s1: load message
                if m4_menu.op in ['1','l']:
                    fpr('Analyses: Load Message')
                    print
                    fn = get_filename2(mode='load',title='Analyses: Load Message')
                    print
                    if fn:
                        content.att_load_eml(mbody,fn)
                        if 'string' in mbody:
                            mbody['eml'] = fn
                            fpr.ok('File content loaded')
                        print
                                
                    waitin()
                #m4s4: view loaded message
                if m4_menu.op in ['2','v']:
                   bancls()
                   fpr('Analyses: View Message ')
                   fpr.info('_'*(tc-4) +'\n\n')
                   if 'string' in mbody:
                       viewers.viewRawContent(builder.CMessage(smtp['parser']['string']).as_string())
                   else:
                       fpr('No message has been loaded')
                   fpr.info('_'*(tc-4))
                   waitin()
                    
                #m4s3: message parser
                if m4_menu.op in ['3','rp']:
                    while True:
                       bancls()
                       m4s2_menu = Menu(menu.m4s2)
                       if m4s2_menu.op == '':
                           break
                       if m4s2_menu.op == '1': 
                           bancls()
                           fpr('Analyses: Message Parser')
                           print
                           parser.mail_body_parser(builder.msg_builder())
                           waitin()
                       if m4s2_menu.op == '2':
                           bancls()
                           fpr('Analyses: Message Parser')
                           print
                           if 'string' in smtp['parser']:
                               parser.mail_body_parser(builder.CMessage(smtp['parser']['string']) )
                           else:
                               fpr.err('Message can not be processed or not loaded !')
                           waitin()
                #m4s4: spf/sidf verification
# ===================================================== SPF ==============================================================
                if m4_menu.op in ['4','rs']: 
                    #FIXME: move me to core.data ? 
                    deauth=dict()
                    deauth.setdefault('spf',dict( {'id': {'mfrom': '', 'helo': '', 'pra': '' }, 'ip': None} ) )



                    def menu_SPF_pv(sh):

                              
                             sh_no = len(sh['Authentication-Results'].keys())+len(sh['Received-SPF'].keys())
                             
                             while True:
                                 bancls()
                                 fpr('Headers parsed: %s' % sh_no)
                                 fpr('  Received-SPF: %s' % len(sh['Received-SPF'].keys()))
                                 fpr('  Authentication-Results: %s' % len(sh['Authentication-Results'].keys()))

                                 m4s4_sh_menu = Menu(menu.m4s4_sh)
                                 if m4s4_sh_menu.op == '':
                                     break
                                 if m4s4_sh_menu.op == '1':
                                     bancls() 
                                     eauth.list_spfHeaders(sh)
                             
                                     waitin()
                                 #if m4s4_sh_menu.op == '2':
                                 #    bancls() 
                                 #    waitin()
                                 if m4s4_sh_menu.op == '2':
                                     bancls()
                                     #from pprint import pprint
                                     #pprint(sh)
                                     info('info','For further investigtion load SPF value from parsed SPF headers.\n' 
                                          'Received-SPF and Authentication-Results header fields are supported.')
                                     print
                                     n = 0
                                     for i in sh:
                                         fpr("%s" % i)
                                         for j in sh[i]:
                                             n += 1
                                             if i == 'Received-SPF':
                                                 fpr('_' *(tc-4))
                                                 print
                                                 fpr('%2s) Header value: \n\n%s' % (n,sh[i][j].get('h_value')))
                                                 print
                                                 fpr(' Parsed SPF values:\n\n  id: %s, results: %s, mfrom: %s,\n  ip: %s, .. ' % 
                                                       ( sh[i][j].get('identity'), sh[i][j].get('result'),
                                                         sh[i][j].get('envelope-from'),
                                                         sh[i][j].get('client-ip')
                                                       )
                                                    )
                                                 fpr('_' *(tc-4))
                                                 #n += 1
                                             if i == 'Authentication-Results':
                                                 fpr('_' *(tc-4))
                                                 print
                                                 fpr('%2s) Header value: \n\n%s' % (n,sh[i][j].get('h_value')))
                                                 print
                                                 fpr(' Parsed SPF values:\n\n')
                                                 if sh[i][j].get('spf'): 
                                                     if sh[i][j]['spf'].get('helo'): 
                                                         fpr('  id: helo, result: %s, value: %s' % 
                                                            (sh[i][j]['spf']['helo'].get('result'), sh[i][j]['spf']['helo'].get('value')))
                                                     if sh[i][j]['spf'].get('mailfrom'): 
                                                         fpr('  id: mailfrom, result: %s, value: %s' % 
                                                            (sh[i][j]['spf']['mailfrom'].get('result'), sh[i][j]['spf']['mailfrom'].get('value')))
                                                     if sh[i][j]['spf'].get('pra'): 
                                                         fpr('  id: pra, result: %s, value: %s' % 
                                                            (sh[i][j]['spf']['pra'].get('result'), sh[i][j]['spf']['pra'].get('value')))
                                                 fpr('_' *(tc-4))

                                               
                                                 #n += 1
                                             

                                             #fpr('[Authentication-Results]  id: %s, mfrom: %s', (sh[i].get('identity'), sh[i].get('value')) )

                                     print 
                                     xhv = get_single_input(
                                          'Choose header number:', ''
                                     )
                                     if xhv and (int(xhv) >0 and int(xhv) <= n):
                                         fpr('Loading SPF values from %s header ..' % xhv)
                                         # deauth - dictionary with current SPF values
                                         # sh - dictionary with parsed headers
                                         # xhv - header number
                                         bancls()
                                         eauth.setSPFvalues(deauth, sh, int(xhv))

                                     else:
                                         fpr.err('No such header number')

                                     waitin()
                          
                    while True:
                       bancls()
                       m4s4_menu = Menu(menu.m4s4)
                       if m4s4_menu.op == '':
                           break
                       if m4s4_menu.op == '1':
                           pass

                       if m4s4_menu.op == '2':
                           pass
                       # m4s4 - parse SPF from input
                       if m4s4_menu.op == '3':
                           bancls()
                           fpr('Analyses: SPF/SIDF Verification')
                           sh = eauth.get_spfHeaders()
                          # waitin()
                           if sh:
                               sh_no = len(sh['Authentication-Results'].keys())+len(sh['Received-SPF'].keys())
                               print
                               if sh_no:
                                   if deauth.get('i_parsed'):
                                       deauth['i_parsed'] = sh
                                   else:
                                       deauth.setdefault('i_parsed',sh)
                                   menu_SPF_pv(sh) 
                           waitin()


                       if m4s4_menu.op == '4':
                            while True:
                               bancls()
                               #fpr('Analyses: SPF/SIDF Verification')

                               m4s4s4_menu = Menu(menu.m4s4s4)
                               if m4s4s4_menu.op == '':
                                   break
                               if m4s4s4_menu.op == '1':
                                   bancls() 
                                   deauth['spf']['id']['mfrom'] = get_single_input(
                                          'Please set MAIL FROM identity:', deauth['spf']['id']['mfrom']
                                   )
                                   waitin()
                               if m4s4s4_menu.op == '2':
                                   bancls()
                                   set_dval(q='  Please set HELO/EHLO identity', dd=deauth['spf']['id'], key='helo', val=deauth['spf']['id']['helo'])
                                   waitin()
                               if m4s4s4_menu.op == '3':
                                   bancls() 
                                   deauth['spf']['id']['pra'] = get_single_input(
                                          'Please set PRA identity:', deauth['spf']['id']['pra']
                                   )
                                   waitin()
                                   
                               if m4s4s4_menu.op == '4':
                                   bancls() 
                                   deauth['spf']['ip']= get_single_input(
                                          'Please set Client IPv4/IPv6 address:', deauth['spf']['ip']
                                   )
                                   waitin()
                                   
                               if m4s4s4_menu.op == '5':
                                   bancls()
                                   info('warn','The Receiver email address is used only when generating a SPF header ') 
                                   set_dval(q='  set Receiver address', dd=deauth['spf'], key='receiver', val=deauth['spf'].get('receiver'))
                                   #deauth['spf']['receiver']= get_single_input(
                                   #       'set Receiver address:', deauth['spf']['receiver']
                                   #)
                                   waitin()
                                   
#
                       if m4s4_menu.op == '5':
                           bancls() 
                           fpr('Analyses: SPF/SIDF Verification')
                           print

                           if deauth['spf']['id'].get('mfrom'):
                               print
                               eauth.get_rrtxt(deauth['spf']['id'].get('mfrom'))
                           else:
                               fpr('No domain name has been found with SPF identity') 
                           waitin()
                       if m4s4_menu.op == '6':
                           bancls() 
                           fpr('Analyses: SPF/SIDF Verification')
                           print

                           spfpolicy='v=spf1 ?all'
 
                           deauth['spf']['policy']= get_single_input(
                                  'Please set test SPF Policy:', deauth['spf'].get('policy',spfpolicy)
                           )
                           waitin()
                           

                       if m4s4_menu.op in ['7','v']:
                           bancls()
                           fpr('Analyses: SPF/SIDF Verification')
                           print
                           viewers.viewSPFvalues(deauth['spf'])
                           waitin()

                       if m4s4_menu.op in ['8','v']:
                           bancls()
                           fpr('Analyses: SPF/SIDF Verification')
                           print

                           #deauth.setdefault('i_parsed',sh)
                           if deauth.get('i_parsed'):
                               menu_SPF_pv(deauth.get('i_parsed')) 

                           else:
                               fpr('No headers have been parsed')
                           waitin()

                       if m4s4_menu.op in ['9','r']:
                           while True:
                               bancls()
                               m4s4s4s9_menu = Menu(menu.m4s4s4s9)
                               if m4s4s4s9_menu.op == '':
                                   break
                               if m4s4s4s9_menu.op in ['1','2','3','4']:
                                   sm = { '1': 'mfrom', '2': 'helo', '3': 'pra', '4': 'all'}
                                   bancls()
                                   fpr('Analyses: SPF/SIDF Verification > Sender Verification')
                                   print
                                   eauth.auth_spf(deauth['spf'],spfid=sm.get(m4s4s4s9_menu.op))
                                   waitin()

                       if m4s4_menu.op in ['10','vl']:
                           while True:
                               bancls()
                               m4s4s4s10_menu = Menu(menu.m4s4s4s10)
                               if m4s4s4s10_menu.op == '':
                                   break
                               if m4s4s4s10_menu.op == '1':
                                   bancls()
                                   fpr('Analyses: SPF/SIDF Verification > SPF Validation')
                                   print
                                   eauth.auth_spfplflow(deauth['spf'],spfid='mfrom')
                                   print
                                   waitin()
    
                               if m4s4s4s10_menu.op == '2':
                                   bancls()
                                   fpr('Analyses: SPF/SIDF Verification > SPF Validation')
                                   print
                                   eauth.auth_spfplflow(deauth['spf'],spfid='helo')
                                   print
                                   waitin()
    
                               if m4s4s4s10_menu.op == '3':
                                   bancls()
                                   fpr('Analyses: SPF/SIDF Verification > SPF Validation')
                                   pass
    



                if m4_menu.op in ['5','rd']: 

                    while True:
                       bancls()
                       m4s5_menu = Menu(menu.m4s5)
                       if m4s5_menu.op == '':
                           break
                       if m4s5_menu.op == '1': 
                           bancls()
                           fpr('Analyses: Message Verification > DKIM <')
                           print
                           tmpmsg = builder.msg_builder()
                           if hasattr(tmpmsg,'as_string'):
                               contsec.dkim_vrfy(tmpmsg.as_string())
                           else:
                               fpr.err('Message can not be processed or not loaded !')
 
                           waitin()
                       
                       if m4s5_menu.op == '2': 
                           bancls()
                           fpr('Analyses: Message Verification > DKIM <')
                           print
                           if 'string' in smtp['parser']:
                               #if
                               contsec.dkim_vrfy(builder.CMessage(smtp['parser']['string']).as_string() )
                           else:
                               fpr.err('Message can not be processed or not loaded !')

                           waitin()


                if m4_menu.op == 'r':
                    bancls()
                    fpr.info(' Help: r - run shortcuts:') 
                    fpr.info('   rp - run parser') 
                    fpr.info('   rs - run spf verification') 
                    fpr.info('   rd - run dkim verification') 
                    waitin()
    
        
        # ======================================== #
        # menu: run diagnostics
        # ======================================== #
        if m0_menu.op == '5':
          while 1:
            bancls()
            m5_menu = Menu(menu.m5)
            #menu: return
            if m5_menu.op == '':
                break
            # m3_s3: SMTP enumeration
            if m5_menu.op == '3':
                bancls()
                fpr('Diagnostics: SMTP commands check')
                info('info','Enumerating commands supported by an SMTP server through HELP and EHLO\ncommands')
                print
                if get_yesno_input('  Would you like to proceed with the test [y/N]: '):
                    if get_yesno_input('  Would you like to enable verbose mode [y/N]: '):
                       bancls()
                       fpr('Diagnostics: SMTP commands check')
                       print
                       scmds = dha.enumSMTPcmd(v=True,dhost=smtp['connect']['hosts'][0])
                       print
                       waitin()
                       bancls()
                       fpr('Diagnostics: SMTP commands check')
                       print
                    else:
                       scmds = dha.enumSMTPcmd(v=False,dhost=smtp['connect']['hosts'][0])
                    if isinstance(scmds,dict):
                        #for sk in scmds.keys():
                        #   fpr("%s : %s " %  (sk,scmds[sk]))

                        if scmds['extn']:
                            fpr('ESMPT is supported with following extensions:')
                            for e in scmds['extn']:
                                (ec,ea) = e
                                fpr('  %s %s ' % (ec,ea))
                        if scmds['secure_extn']:
                            fpr('ESMTP over TLS is supperted with following extensions:')
                            for e in scmds['secure_extn']:
                                (ec,ea) = e
                                fpr('  %s %s ' % (ec,ea))
                        if scmds['method']:
                            fpr('Supported DHA methods: %s' % ' '.join(map(str,scmds['method'])) )
                        if scmds['scmds']:
                            print
                            fpr('%s' % scmds['scmds'])


                waitin()
            #menu: m5s6 
            if m5_menu.op == '6':
                bancls()
                dutils.d_headers()
            #menu: m5s10
            if m5_menu.op == '7':
                bancls()
                dutils.e_headers()
            

            #menu: m5s8
            if m5_menu.op == '8':
               #d_attachments()
               decb64 = None
               while True:
                  bancls()
                  m5s8_menu = Menu(menu.m5s8)
                  #menu: m5s8s1 - load from file 
                  if m5s8_menu.op == '1':
                      decb64 = dutils.d_base64(m5s8_menu.op)
                      #pass 
                  #menu: m5s8s2 - load from input
                  if m5s8_menu.op == '2':
                      decb64 = dutils.d_base64(m5s8_menu.op)
                      #pass 
                  #menu: m5s8s3 - view
                  if m5s8_menu.op == '3':
                      bancls()
                      fpr('Diagnostics: Base64 decoder')
                      print
                      if isinstance(decb64,dict):
                         fpr('File content is decoded successful')
                         print
                         viewers.viewRawContent(decb64['raw'])
                         waitin()

                  #menu: m5s8s2 - save
                  if m5s8_menu.op == '4':
                      bancls()
                      fpr('Diagnostics: Base64 decoder')
                      print
                      if isinstance(decb64,dict):
                         fpr('File content is decoded successful')
                         print
                         fn = get_filename2(mode='save')
                         if fn:
                             save_content_asfile(decb64['raw'],fn,'wb') 
                         waitin()
                       


                  #menu: return
                  if m5s8_menu.op == '':
                     break                  

            #menu: m5s9 - base64 encoders
            if m5_menu.op == '9':
               #d_attachments()
               encb64 = None
               while True:
                  bancls()
                  m5s9_menu = Menu(menu.m5s9)
                  #menu: m5s8s1 - load from file 
                  if m5s9_menu.op == '1':
                      encb64 = dutils.e_base64(m5s9_menu.op)
                      #pass 
                  #menu: m5s8s2 - load from input
                  if m5s9_menu.op == '2':
                      encb64 = dutils.e_base64(m5s9_menu.op)
                      #pass 
                  #menu: m5s8s3 - view
                  if m5s9_menu.op == '3':
                      bancls()
                      fpr('Diagnostics: Base64 encoder')
                      print
                      if isinstance(encb64,dict):
                         fpr('File content is encoded successful')
                         print
                         viewers.viewRawContent(encb64['b64'])
                         waitin()

                  #menu: m5s9s2 - save
                  if m5s9_menu.op == '4':
                      bancls()
                      fpr('Diagnostics: Base64 encoder')
                      print
                      if isinstance(encb64,dict):
                         fpr('File content is encoded successful')
                         print
                         fn = get_filename2(mode='save')
                         if fn:
                             save_content_asfile(encb64['b64'],fn,'wb') 
                         waitin()
                       


                  #menu: return
                  if m5s9_menu.op == '':
                     break  





            #menu: m5s14
            if m5_menu.op == '14':
               while True:
                  bancls()
                  m5s14_menu = Menu(menu.m5s14)
                  #menu: return
                  if m5s14_menu.op == '':
                     break
                  #menu: m5s14s1
                  if m5s14_menu.op == '1':
                     pass
                  #menu: m5s14s2
                  if m5s14_menu.op == '2':
                     m5s14s2_menu = Menu(menu.m5s14s2)
                     #menu: return
                     if m5s14s2_menu.op == '':
                        break
                     #menu: m5s14s2s1
                     if m5s14s2_menu.op == '1':
                        pass
 
                  #menu: m5s14s3
                  if m5s14_menu.op == '3':
                     pass
                  #menu: m5s14s4
                  if m5s14_menu.op == '4':
                     pass
                  #menu: m5s14s5
                  if m5s14_menu.op == '5':
                     pass

        # ======================================== #
        # menu: session
        # ======================================== #
        if m0_menu.op in ['6']:
            while True:
               bancls()
               m6_menu = Menu(menu.m6)
               #menu: return
               if m6_menu.op == '':
                   break
               #menu: Help
               if m6_menu.op == '1':
                   bancls()
                   fpr('Session management: Save session')
                   sess.dumpSession()
                   waitin()
               if m6_menu.op == '2':
                   bancls()
                   fpr('Session management: Load session')
                   sess.loadSession()
                   waitin()
                
 
        # ======================================== #
        # menu: help, about, license info
        # ======================================== #
        if m0_menu.op in ['i']:
            while True:
               bancls()
               mHelp_menu = Menu(menu.mHelp)
               #menu: return
               if mHelp_menu.op == '':
                   break
               #menu: Help
               if mHelp_menu.op in ['1','h']:
                   bancls()
                   fpr('%s' % menu.mHelp['head']) 
                   info('info',menu.mHelp['info'],adj='l')
                   print
                   helpi.infos('help')
                   waitin()   
               #menu: License
               if mHelp_menu.op in ['2','l']:
                   bancls()
                   fpr('%s' % menu.mHelp['head']) 
                   info('info',menu.mHelp['info'],adj='l')
                   print
                   helpi.infos('license')
                   waitin()   
               #menu: About
               if mHelp_menu.op in ['3','a']:
                   bancls()
                   fpr('%s' % menu.mHelp['head']) 
                   info('info',menu.mHelp['info'],adj='l')
                   print
                   helpi.infos('about')
                   waitin()   




        ###################################################################
        #print dictionary
        ###################################################################
        if m0_menu.op == 'p':
          from pprint import pprint
          while True:
            print
            bancls()
            a = raw_input('  : ')
            if a in ['smtp']:
              pprint(smtp)
              waitin()
            if a in ['smpls']:
              pprint(smpls)
              waitin()
            if a in ['msg']:
              msg = builder.msg_builder
              pprint(msg)
              waitin()
            if a in ['q','x']:
              fpr.info('..bye','r')
              waitin()
              break
            #else: 
              # try to print 
              #implemnet sth like ~ pprint(eval(a))




