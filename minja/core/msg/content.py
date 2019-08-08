# --------------------------------------------------------------------------- #
# 2.5 - Data Content
# --------------------------------------------------------------------------- #

import os
import re
import email 
#import magic
from mimetypes import guess_type
from email.encoders import encode_base64

from core.data import smtp,smpls,fpr,tc,tr,DEBUG
from core.func import info,waitin,get_inputs,dbglog,dbginfo,get_zipfile,get_sample
from core.msg.coders import isBase64
from core.ui.cmenu import Menu
from core.ui.banner import bancls


# --------------------------------------------------------------------------- #
# build custom body content from input 
# --------------------------------------------------------------------------- #
def att_cont_as_string(content=''):

    #from core.data import smtp,fpr,tc,tr,DEBUG
    #from core.func import waitin,get_inputs,dbglog,dbginfo


    if content:
        fpr('Body content has been created')
        smtp['content']['string'] = content
        dbginfo('debug', smtp['content']['string'] )
        smtp['use_mime'] = False

    else:
        while True:
            #if smpls[smtype]['astat'] != 0:
            #    fpr('It seems you have already attached this type of sample')
            #    if not raw_input('  Do you want to append another one [y/N]:') in ['y','Y']:
            #         break
            fpr.info('_'*(tc-4))
            print
            inputs = get_inputs(nl=True)
            fpr.info('_'*(tc-4))

            if inputs:
                dbglog(inputs)
                smtp['content']['string'] = '\r\n'.join(inputs)         
                dbginfo('debug', smtp['content']['string']  )

                # change the way how msg_builder build the message 
                # even if you paste a proparly formatted mime message do not 
                # treat this as MIME because you are not anymore responsible for building 
                # a mime parts, you only need to attach this content as it is 

                smtp['use_mime'] = False
                # TODO 
                # Since now all other function should be aware when usemime() is FALSE and 
                # than not be able to attach any of predefined sample
                break   
            else: 
                fpr('Leaving ..') 
                break

# --------------------------------------------------------------------------- #
# load file and define MIME headers, file is kept in raw  
# --------------------------------------------------------------------------- #
def att_load_file(mbody,attfn):

    #import os
    #from core.data import smtp,fpr,tc,tr
    #from core.func import waitin,dbginfo

    if os.path.isfile(attfn):
        print
        fpr('Loading %s ..' % attfn)

        #from mimetypes import guess_type
        #from email.encoders import encode_base64
        mimetype, encoding = guess_type(attfn)

        # if no extension try to detect mime type wit a libmagic library 
        # from python-magic package if possible
        if mimetype == None:
            try:
                import magic
                mimetype = magic.from_file(attfn, mime=True)
            except ImportError:
                dbginfo('warrning','Warrning: Missing module: magic. Use: pip install python-magic') 
                print
                mimetype = 'text/plain'
        #mimetype = mimetype.split('/', 1)
        fp = open(attfn, 'rb')
        inputs = fp.read()
        fp.close()

        if not inputs:
            
            dbginfo('error','Err: File has no content. Please verify file size !\n[ %s ]' % attfn)
            #break
            return False

        if inputs:
            info('info','Default Content-* header values are generated based on file extension. If no' \
                        'extension and no \'magic\' module is found than text/plain is suggested by \ndefault.',adj='l')
            print
            fpr('Please define MIME headers for this attachment')
            print
            n = 1
            if mbody.keys():
                #global n 
                n = max(mbody.keys())
                n += 1
                #print max(mbody.keys())

            fpr('Attachment no: %d' % n ,'c')
            print
            mbody.setdefault(n,{})['raw'] = inputs
            #mbody['0']['b64'] = inputs

            mbody[n]['h_Content-Type'] = \
                  raw_input('  Content-Type: [%s]> ' %  mimetype) \
                       or mimetype
            mbody[n]['h_Content-Disposition'] = \
                  raw_input('  Content-Disposition: [%s]> ' %  \
                          'attachments; filename=%s' % os.path.basename(attfn)) \
                       or 'attachments; filename=%s' % os.path.basename(attfn)
            mbody[n]['h_Content-transfer-encoding'] = \
                  raw_input('  Content-transfer-encoding: [%s]> ' %  '') \
                       or ''
            mbody[n]['h_Content-ID'] = \
                  raw_input('  Content-ID: [%s]> ' %  '') \
                       or ''
            mbody[n]['h_Content-Description'] = \
                  raw_input('  Content-Description: [%s]> ' % '') \
                       or ''
        
        waitin()
    else:
       fpr('No such file or you don\'t have a permission to access it')
       print
       return False          


# --------------------------------------------------------------------------- #
# load base64 encoded input and define MIME headers 
# --------------------------------------------------------------------------- #
def att_load_base64(mbody):

    # attachment: paste base64 encoded part
    #from core.data import smtp,fpr,tc,tr,DEBUG
    #from core.func import waitin,get_inputs,dbglog,dbginfo
    #from core.msg.coders import isBase64

    while True:
        fpr.info('_'*(tc-4))
        print

        inputs = get_inputs()

        fpr.info('_'*(tc-4))

        if inputs != '':
            dbglog(inputs)
            b64result = 1
            for i in inputs:
                if not isBase64(i):

                    dbginfo('error','Err: Line is not a proper base64 line',i)

                    b64result = 0
                    break
            if b64result and inputs:
                print
                fpr('Message seems to have proper base64 lines')
                print
                fpr('Please define MIME headers for this attachment')
                print
                n = 1
                if mbody.keys():
                    #global n 
                    n = max(mbody.keys())
                    n += 1
                    #print max(mbody.keys())
    
                fpr('Attachment no: %d' % n, adj='c')
                print
                mbody.setdefault(n,{})['b64'] = inputs
                #mbody['0']['b64'] = inputs
    
                mbody[n]['h_Content-Type'] = \
                      raw_input('  Content-Type: [%s]> ' %  '') \
                           or ''
                mbody[n]['h_Content-Disposition'] = \
                      raw_input('  Content-Disposition: [%s]> ' % '') \
                           or ''
                mbody[n]['h_Content-transfer-encoding'] = \
                      raw_input('  Content-transfer-encoding: [%s]> ' %  'base64') \
                           or 'base64'
                mbody[n]['h_Content-ID'] = \
                      raw_input('  Content-ID: [%s]> ' %  '') \
                           or ''
                mbody[n]['h_Content-Description'] = \
                      raw_input('  Content-Description: [%s]> ' %  '') \
                           or ''
            waitin()
            break



# --------------------------------------------------------------------------- #
# attach predefined sample: text type sample
# --------------------------------------------------------------------------- #
def att_plain_sample(mbody,smtype,sm):
 
    #from core.data import smpls,fpr,tc,tr
    #from core.ui.cmenu import Menu
    #from core.ui.banner import bancls

    while True:
        bancls()
        if smpls[smtype]['astat'] != 0:
            fpr('It seems you have already attached this type of sample')
            if not raw_input('  Do you want to append another one [y/N]:') in ['y','Y']:
                break
        if True:
            smpl_menu = Menu ( sm )
            if smpl_menu.op == '':
               break
            #if smpl_menu.op == '1':
            if smpl_menu.op in ['1','2','3','4','5','6','7']:
               if smpls[smtype][smpl_menu.op].get('sval','') == '_':
                  mbody.append(smpls[smtype][smpl_menu.op]['val'].replace(smpls[smtype][smpl_menu.op]['sval'],""))
               else:
                  mbody.append(smpls[smtype][smpl_menu.op]['val'])
               smpls[smtype]['astat'] += 1
               fpr.ok('Sample attached (x%d)' % smpls[smtype]['astat'])
               break

#        mbody.append(smpls['spam']['val'])
#        smpls['spam']['astat'] += 1
#        fpr('SPAM Sample attached (x%d)'%smpls['spam']['astat'])
#        break

# --------------------------------------------------------------------------- #
# attach predefined sample: raw or b64 encoded type
# --------------------------------------------------------------------------- #
def att_raw_sample(mbody,smtype,sm):


    #from core.data import smpls,fpr,tc,tr
    #from core.ui.cmenu import Menu
    #from core.ui.banner import bancls

    while True:
        bancls()
        if smpls[smtype]['astat'] != 0:
            fpr('It seems you have already attached this type of sample')
            if not raw_input('  Do you want to append another one [y/N]:') in ['y','Y']:
                break
        if True:
            smpl_menu = Menu ( sm )
            if smpl_menu.op == '':
               break
            #if smpl_menu.op == '1':
            if smpl_menu.op in ['1','2','3','4']:


                #FIXME this will not work like that for long tmal
                # fix sampel types in this shity way, the whole code regarding samples need 
                # to be rewritten and reorginize, this is not flexible/scalable 
                if smpls[smtype][smpl_menu.op].get('type') == 'text':
                    #this overwites type under smpls[smtype]['type']
                    if smpls[smtype][smpl_menu.op].get('sval','') == '_':
                    #     mbody.append(smpls[smtype][smpl_menu.op]['val'].replace("_",""))
                        smtp['content']['text'].append(smpls[smtype][smpl_menu.op]['val'].replace(smpls[smtype][smpl_menu.op]['sval'],""))
                    else:
                    #print "wtf: %s - %s" % (smtype,smpls[smtype][smpl_menu.op]['val'])
                    #mbody here is smtp['content']['vof'] - this is dict {} - so overwrite
                    #this with fixed path to 'text' or create a seperate att_plain and add
                    #this as mime plain/text ??? 
                    #mbody.append(smpls[smtype][smpl_menu.op]['val'])
                        smtp['content']['text'].append(smpls[smtype][smpl_menu.op]['val'])

                    smpls[smtype]['astat'] += 1
                    fpr.ok('Sample attached (x%d)' % smpls[smtype]['astat'])
                    break
                else:
                    if smpls[smtype]['type'] == 'b64':
                        #att_b64(mbody,smtype,'1')
                        att_b64(mbody,smtype,smpl_menu.op)
                    elif smpls[smtype]['type'] == 'file':
                        #att_file_sample(mbody,smtype,'1')
                        att_file_sample(mbody,smtype,smpl_menu.op)

                break
#               mbody.append(smpls[smtype]['1']['val'])
#               smpls[smtype]['astat'] += 1
#               fpr.ok('Sample attached (x%d)'%smpls[smtype]['astat'])
#               break


# --------------------------------------------------------------------------- #
# attach predefined sample: file from ~/.minja/samples 
#                           fetch from server if not found in directory
# --------------------------------------------------------------------------- #
def att_file_sample(mbody,smtype,sn):

    #import os
    #from core.data import smpls,fpr,tc,tr,smtp
    #from core.func import waitin,get_sample,dbginfo
    #from core.ui.cmenu import Menu
    #from core.ui.banner import bancls

    while True:
        # you are ask about this in att_XXX_sample function
        #if smpls[smtype]['astat'] != 0:
        #    fpr('It seems you have already attached this type of sample')
        #    if not raw_input('  Do you want to append another one [y/N]:') in ['y','Y']:
        #        break

        if os.path.exists( smpls[smtype][sn]['filename'] ):
            #mbody.append(smpls[smtype]['filename'])
            fp = open(smpls[smtype][sn]['filename'],  'rb')
            inputs = fp.read()
            fp.close()
            if not inputs:

                dbginfo('error',
                  'Err: File has no content. Please verify file size !\n[%s] \
                  \nTry to remove file to download a new one.' % 
                  smpls[smtype][sn]['filename']
                )

                break
            n = 1

            if mbody.keys():
                n = max(mbody.keys())
                n += 1
                #print max(mbody.keys())
            print
            fpr('Attaching %s' % smpls[smtype][sn]['descr'])
            print
            mbody.setdefault(n,{})['raw'] = inputs
# TODO wstaw do content
            mbody[n]['h_Content-Type'] = \
                 raw_input('  Content-Type: [%s]> ' %  smpls[smtype].get('mimetype','') ) \
                     or smpls[smtype].get('mimetype','')

            mbody[n]['h_Content-Disposition'] = \
                 raw_input('  Content-Disposition: [%s]> ' % \
                                'attachments; filename=%s' % \
                     os.path.basename(smpls[smtype][sn]['filename'])) \
                     or 'attachments; filename=%s' % \
                     os.path.basename(smpls[smtype][sn]['filename'])

            mbody[n]['h_Content-Transfer-Encoding'] = \
                 raw_input('  Content-transfer-encoding: [%s]> ' %  'base64') \
                     or 'base64'
            # !! if no cid - client like Mail.app does not 
            #    show the attachment 
            mbody[n]['h_Content-ID'] = \
                 raw_input('  Content-ID: [%s]> ' %  '') \
                     or ''

            mbody[n]['h_Content-Description'] = \
                 raw_input('  Content-Description: [%s]> ' % '') \
                     or ''

            smpls[smtype]['astat'] += 1
            print

            fpr('Sample attached (x%d)' % smpls[smtype]['astat'])

            break

        else:
            fpr('Sample does not exists [%s]' % smpls[smtype][sn]['filename'])
            if raw_input('  Would you like to download this sample [y/N]> ') in ['y','Y']:
                get_sample(smpls[smtype][sn])
            else:
                break
    
    waitin()
 
# --------------------------------------------------------------------------- #
# attach predefined sample: base64 encoded 
# --------------------------------------------------------------------------- #
def att_b64(mbody,smtype,sn):

    #import os
    #import email 

    #from core.data import smpls,fpr,tc,tr,smtp
    #from core.func import waitin,get_sample,dbginfo
    #from core.ui.cmenu import Menu
    #from core.ui.banner import bancls

    while True:
        # you are ask about this in att_XXX_sample function
        #if smpls[smtype]['astat'] != 0:
        #    fpr('It seems you have already attached this sample')
        #    if not raw_input('  Do you want to append another one [y/N]:') in ['y','Y']:
        #        break
        #    #break

        if True:
           if smpls[smtype][sn]['val']:
                
                fpr('Attaching %s' % smpls[smtype][sn]['descr'])
                print
                n = 1

                mbody.setdefault(n,{})['b64'] = []

                mbody.setdefault(n,{})['b64'].append(\
                       email.base64MIME.encode(smpls[smtype][sn]['val']) )

                #print mbody[n]['b64']
                #print type(mbody[n]['b64'])                
                #print "\n".join(mbody[n]['b64'])

                mbody[n]['h_Content-Type'] = \
                raw_input('  Content-Type: [%s]> ' %  smpls[smtype].get('mimetype','')) \
                    or  smpls[smtype].get('mimetype','')

                mbody[n]['h_Content-Disposition'] = \
                raw_input('  Content-Disposition: [%s]> ' %  'attachments; filename=%s' % \
                    os.path.basename(smpls[smtype][sn]['filename'])) \
                    or 'attachments; filename=%s' % \
                    os.path.basename(smpls[smtype][sn]['filename'])

                mbody[n]['h_Content-Transfer-Encoding'] = \
                raw_input('  Content-transfer-encoding: [%s]> ' %  'base64') \
                    or 'base64'

                # if no cid - client like Mail.app does not 
                # show the attachment 
                mbody[n]['h_Content-ID'] = \
                raw_input('  Content-ID: [%s]> ' %  '') \
                    or ''

                mbody[n]['h_Content-Description'] = \
                raw_input('  Content-Description: [%s]> ' % '') \
                    or ''
 
                #print mbody 
                smpls[smtype]['astat'] += 1
                print
                fpr('Sample attached (x%d)' % smpls[smtype]['astat'])
                break
                                        
        waitin()



# --------------------------------------------------------------------------- #
# attach predefined sample: zip plain type sample
# --------------------------------------------------------------------------- #
def att_zip_plain_sample(mbody,smtype,sn):


    #mbody = smtp['content']['att']
    #sn = '1'

    #from core.data import smpls,fpr,tc,tr
    #from core.func import waitin,get_zipfile,dbginfo

 
    while True:
        #print  smpls['zip'].get(smtype,'dupa') 
        if smpls['zip-smpls'].get(smtype) and smpls['zip-smpls'][smtype]['astat'] != 0:
             fpr('It seems you have already attached this zip  %s sample' % smtype)
             if not raw_input('  Do you want to append another one [y/N]:') in ['y','Y']:
                 break
        else:
            smpls['zip-smpls'].setdefault(smtype,{})['astat'] = 0
        
        #print get_zipfile(smpls['spam']['val'])
        # for VOF test a name of file in archive is important !! 
        if smpls[smtype][sn].get('filename',''): 
            inputs =  get_zipfile(smpls[smtype][sn],fn=smpls[smtype][sn]['filename'])
        else:
            inputs =  get_zipfile(smpls[smtype][sn])
        #print type(inputs)
        if inputs:
            n = 1
            if mbody.keys():
                n = max(mbody.keys())
                n += 1
                #print max(mbody.keys())
            print
            fpr('Attaching zipped %s' % smpls[smtype][sn]['descr'])
            print
            mbody.setdefault(n,{})['raw'] = inputs
            #mbody['0']['b64'] = inputs
   
            mbody[n]['h_Content-Type'] = \
                  raw_input('  Content-Type: [%s]> ' %  'application/zip') \
                       or 'application/zip'
            mbody[n]['h_Content-Disposition'] = \
                   raw_input('  Content-Disposition: [%s]> ' %  \
                   'attachments; filename=%s' % (smtype+'_'+smpls['zip-smpls']['filename'])) \
                       or 'attachments; filename=%s' % (smtype+'_'+smpls['zip-smpls']['filename'])
            mbody[n]['h_Content-transfer-encoding'] = \
                   raw_input('  Content-transfer-encoding: [%s]> ' %  'base64') \
                       or 'base64'
            mbody[n]['h_Content-ID'] = \
                   raw_input('  Content-ID: [%s]> ' %  '') \
                       or ''
            mbody[n]['h_Content-Description'] = \
                   raw_input('  Content-Description: [%s]> ' %  '') \
                       or ''
   
            smpls['zip-smpls']['astat'] += 1
            smpls['zip-smpls'].setdefault(smtype,{})['astat'] += 1
            print 
            fpr('Zipped %s attached (x%d)' % (smpls[smtype][sn]['descr'], smpls['zip-smpls'][smtype]['astat']) )
        else: 
            fpr.err('Err: This should not happened ! ')
        waitin()
        break
 
# --------------------------------------------------------------------------- #
# attach predefined sample: zip file sample 
# --------------------------------------------------------------------------- #
def att_zip_file(mbody,smtype,sn):

    #mbody  = smtp['content']['att']
    #sn     = '1'
    #smtype = 'img'

    #import os
    #from core.data import smpls,fpr,tc,tr
    #from core.func import waitin,get_zipfile,get_inputs,get_sample,dbginfo

    while True:
       print
       if smpls['zip-smpls'].get(smtype) and smpls['zip-smpls'][smtype]['astat'] != 0:
            fpr('It seems you have already attached this %s sample' % smtype)
            if not raw_input('  Do you want to append another one [y/N]:') in ['y','Y']:
                break
       else:
           smpls['zip-smpls'].setdefault(smtype,{})['astat'] = 0
       if os.path.exists( smpls['img'][sn]['filename'] ):
           #mbody.append(smpls['img']['filename'])
           fp = open(smpls['img'][sn]['filename'],  'rb')
           inputs = fp.read()
           fp.close()

           if not inputs:

               dbginfo('error',
                  'Err: File has no content. Please verify file size !\n[%s] \
                  \nTry to remove file to download a new one.' % 
                  smpls[smtype][sn]['filename']
               )

               break
           n = 1
           if mbody.keys():
               n = max(mbody.keys())
               n += 1
               #print max(mbody.keys())
           print 
           fpr('Attaching zipped %s' % smpls[smtype][sn]['descr'])
           print
           zipinputs = get_zipfile( { 'val': inputs }, fn = os.path.basename(smpls[smtype][sn]['filename'])  )
           #print type(inputs)
           mbody.setdefault(n,{})['raw'] = zipinputs
            
           mbody[n]['h_Content-Type'] = \
                raw_input('  Content-Type: [%s]> ' %  'application/zip') \
                    or 'application/zip'

           mbody[n]['h_Content-Disposition'] = \
                  raw_input('  Content-Disposition: [%s]> ' %  \
                      'attachments; filename=%s' % (smtype+'_'+smpls['zip']['filename'])) \
                      or 'attachments; filename=%s' % (smtype+'_'+smpls['zip']['filename'])

           mbody[n]['h_Content-Transfer-Encoding'] = \
                raw_input('  Content-transfer-encoding: [%s]> ' %  'base64') \
                    or 'base64'
           # if no cid - client like Mail.app does not 
           # show the attachment 
           mbody[n]['h_Content-ID'] = \
                raw_input('  Content-ID: [%s]> ' %  '') \
                    or ''
           mbody[n]['h_Content-Description'] = \
                raw_input('  Content-Description: [%s]> ' % '') \
                    or ''

           #smpls['img']['astat'] += 1
           smpls['zip-smpls']['astat'] += 1
           smpls['zip-smpls'].setdefault(smtype,{})['astat'] += 1
           print 
           fpr('Zipped %s attached (x%d)' % (smpls[smtype][sn]['descr'], smpls['zip-smpls'][smtype]['astat']) )

           waitin()
           break 
       else:
           fpr('Sample does not exists [%s]' % smpls[smtype][sn]['filename'])
           if raw_input('  Would you like to download this sample [y/N]> ') in ['y','Y']:
               get_sample(smpls[smtype][sn])
           else:
               break 
  
# --------------------------------------------------------------------------- #
# attach zip file: load new file and zip it 
# --------------------------------------------------------------------------- #
def att_load_and_zip_file(mbody,smtype,sn,attfn):

    #mbody  = smtp['content']['att']
    #sn     = '1'
    #smtype = 'img'

    #import os
    #from core.data import smpls,fpr,tc,tr,smtp
    #from core.func import waitin,get_zipfile,get_inputs,get_sample,dbginfo

    smtype = 'zipfile'
    while True:

        if smpls['zip'].get(smtype) and smpls['zip'][smtype]['astat'] != 0:
             print
             fpr('It seems you have already attached one file to zip')
             if not raw_input('  Do you want to append another one [y/N]:> ') in ['y','Y']:
                 break
        else:
            smpls['zip'].setdefault(smtype,{})['astat'] = 0
    
        #print
        #fpr('Please provide a full PATH to an attachment (/path/to/your/doc.pdf)')
        #attfn = raw_input('  > ')

        if os.path.isfile(attfn):
            print
            fpr('Loading %s ..' % attfn)
            if False:  # skip checking file type for zip

               from mimetypes import guess_type
               from email.encoders import encode_base64
               mimetype, encoding = guess_type(attfn)

               # if no extension try to detect mime type with a libmagic library 
               # from python-magic package if possible
               if mimetype == None:
                  try:
                     import magic
                     mimetype = magic.from_file(attfn, mime=True)
                  except ImportError:
                     dbginfo('warrning','Warrning: No "magic" library. Use: pip install python-magic') 
                     print
                     mimetype = 'text/plain'

            fp = open(attfn, 'rb')

            inputs = fp.read()
            fp.close()
            if not inputs:
                print
                dbginfo('error','Err: File has no content. Please verify file size !\n[ %s ]' % attfn)
                break

            n = 1
            if mbody.keys():
                n = max(mbody.keys())
                n += 1
                #print max(mbody.keys())
            print 
            fpr('Attaching zipped %s -> %s' %  (os.path.basename(attfn), 
                    ( os.path.splitext(os.path.basename(attfn))[0] +'.zip')) )
            print
            zipinputs = get_zipfile( { 'val': inputs }, fn = os.path.basename(attfn)  )
            #print type(inputs)
            mbody.setdefault(n,{})['raw'] = zipinputs
            
            mbody[n]['h_Content-Type'] = \
                 raw_input('  Content-Type: [%s]> ' %  'application/zip') \
                     or 'application/zip'

            mbody[n]['h_Content-Disposition'] = \
                 raw_input('  Content-Disposition: [%s]> ' % \
                     'attachments; filename=%s' % ( os.path.splitext(os.path.basename(attfn))[0] +'.zip' ) ) \
                     or 'attachments; filename=%s' %  ( os.path.splitext(os.path.basename(attfn))[0] +'.zip' ) 

            mbody[n]['h_Content-Transfer-Encoding'] = \
                 raw_input('  Content-transfer-encoding: [%s]> ' %  'base64') \
                     or 'base64'
            # if no cid - client like Mail.app does not 
            # show the attachment 
            mbody[n]['h_Content-ID'] = \
                 raw_input('  Content-ID: [%s]> ' %  '') \
                     or ''
            mbody[n]['h_Content-Description'] = \
                 raw_input('  Content-Description: [%s]> ' % '') \
                     or ''

            #smpls['img']['astat'] += 1
            #smpls['zip']['astat'] += 1
            smpls['zip'].setdefault(smtype,{})['astat'] += 1
            print 
            fpr('Zipped %s attached (x%d)' % ( os.path.basename(attfn) , smpls['zip'][smtype]['astat']) )
            waitin()
            break                                             
        else:
           fpr('No such file or you don\'t have a permission to access it')
           print
           if raw_input('  Return to menu [y/N]> ') in ['y','Y']:
               break



# --------------------------------------------------------------------------- #
# attache zip sample: get text user input and zip it 
# --------------------------------------------------------------------------- #
def att_zip_input(mbody,smtype,sn):

    #mbody  = mbody
    #sn     = '1'
    #smtype = 'img'

    #import os
    #from core.data import smpls,fpr,tc,tr,smtp
    #from core.func import waitin,get_zipfile,get_inputs,get_sample,dbginfo


    smtype = 'zip-input'
    while True: 
        if smpls['zip'].get(smtype) and smpls['zip'][smtype]['astat'] != 0:
             fpr('It seems you have already attached one of USER input sample')
             if not raw_input('  Do you want to append another one [y/N]:') in ['y','Y']:
                 break
        else:
            smpls['zip'].setdefault(smtype,{})['astat'] = 0

        fpr.info('Zip your own text content')
        fpr.info('Use Ctrl-D with new line to continue.')
        print 
        fpr.info('_'*(tc-4))
        print

        inputs = get_inputs(nl=True)
        fpr.info('_'*(tc-4))

        if inputs != '':
            print
            if raw_input('  Zip it [Y/n]:> ') in ['N','n']:
                break
            print
            # zipit 
            zipinputs = get_zipfile( { 'val': '\n'.join(inputs) }, fn = 'user-input.txt'  )
        
            n = 1
            if mbody.keys():
                n = max(mbody.keys())
                n += 1
                #print max(mbody.keys())
 

            mbody.setdefault(n,{})['raw'] = zipinputs
            
            mbody[n]['h_Content-Type'] = \
                 raw_input('  Content-Type: [%s]> ' %  'application/zip') \
                     or 'application/zip'

            mbody[n]['h_Content-Disposition'] = \
                 raw_input('  Content-Disposition: [%s]> ' %  'attachments; filename=%s' % 'uin-test.zip' ) \
                     or 'attachments; filename=%s' % 'test.zip' 

            mbody[n]['h_Content-Transfer-Encoding'] = \
                 raw_input('  Content-transfer-encoding: [%s]> ' %  'base64') \
                     or 'base64'

            # if no cid - client like Mail.app does not 
            # show the attachment 
            mbody[n]['h_Content-ID'] = \
                 raw_input('  Content-ID: [%s]> ' %  '') \
                     or ''

            mbody[n]['h_Content-Description'] = \
                 raw_input('  Content-Description: [%s]> ' % '') \
                     or ''
            
            smpls['zip']['astat'] += 1
            smpls['zip'].setdefault(smtype,{})['astat'] += 1
            print 
            fpr('Zipped %s attached (x%d)' % ('INPUT', smpls['zip'][smtype]['astat']) )
        break
    waitin()

# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #

def att_custom_header():
    #import re
    print
    if raw_input('  Would you like to include your own headers [y/N]> ') in ['y', 'Y']:
        while True:
            print
            fpr('Please provide a header in format: >> Header-name: header-value <<')
            fpr('Use Ctrl-D with new line to save it and continue.')
            fpr.blue('_'*(tc-4))
            print
#            inputs = []
#            while True:
#                try:
#                    line = raw_input("")
#                except EOFError:
#                    break
#                inputs.append(line)
            # to preserve new line pass nl=True with get_inputs()
            inputs = get_inputs()
            if inputs != '':
                thead = {}
                ####### TODO: move this to def encode_mheaders()
                for (i,hline) in enumerate(inputs):
                    #print hline                                        
                    m1 = re.match(r'(.*):(.*)',hline)  # it is a header 
                    m2 = re.match(r'^(\s+)(.*)',hline)  # it is a continuation of prev header
                    if hline == '\n':
                        key = ''
                    elif m1:
                         if m1.group(1):
                             key = m1.group(1)
                             thead.setdefault(key,[]).append(m1.group(2))
                    elif m2:
                        if key == '' and inputs[i-1] != '\n':
                            key = '-no-hn-'
                            while key in thead.keys():
                                key += '-'
                        thead.setdefault(key,[]).append(m2.group(1)+m2.group(2))
                #############
                fpr.blue('_'*(tc-4))
                for k in thead.keys():
                    fpr.info('_'*(tc-4)) 
                    print
                    if re.match('-no-hn-',k):
                        fpr('Header-name: <None>')
                    else:
                        fpr('Header-Name: %s' % k)
                        fpr('Header: %s' % thead[k])
                        #fpr('Encoding: %s' % enc)

                    fpr.info('_'*(tc-4)) 
                fpr.blue('_'*(tc-4))
                print
      
                #print theadi
                if thead.keys():
                    if raw_input('  Are your headers parsed correctly [Y/n]:> ') in ['n', 'N']:
                        if raw_input('  Would you like to add them one more time [Y/n]:> ') in ['n','N']:     
                            break
                        else:
                            waitin()

                    else:

# if RFC: format header-name, format header length, 
#                        rfcline = 1
#                        if raw_input('  Should lines follow the RFC or leave it as you put it [Y/n]> ') in ['n', 'N']:
#                            rfcline = 0
                        
                        ####
                        for k in thead.keys():
                            smtp['headers']["h_%s" % k ] = thead[k] 
                        ####
                        dbglog(smtp['headers']) 
                        waitin()
                        break
                else:
                    fpr('No header was specified')
                    waitin()
                    break

# --------------------------------------------------------------------------- #
# load file eml: basic (concepts) 
# --------------------------------------------------------------------------- #
def att_load_eml(mbody,emlfn):

    #import os
    #from core.data import smtp,fpr,tc,tr
    #from core.func import waitin,dbginfo

    if os.path.isfile(emlfn):
        print
        fpr('Loading %s ..' % emlfn)

        fp = open(emlfn, 'rb')

        inputs = fp.read()
        fp.close()

        if not inputs:
            
            dbginfo('error','Err: File has no content. Please verify file size !\n[ %s ]' % emlfn)
            #break
            return False

        if inputs:
            info('info','-- Loaded message: Top dump (view: 500 chars) --','%s' % inputs[:500]+' . . .')
            print
            #dbglog(inputs)
            fpr.ok('Message content has been loaded')

            #smtp['content']['string'] = ''.join(inputs)
            mbody['string'] = ''.join(inputs)
            #smtp['content']['string'] = '\r\n'.join(inputs)         
         
            #smtp['use_mime'] = False
        
        waitin()
    else:
       fpr('No such file or you don\'t have a permission to access it')
       print
       return False          



