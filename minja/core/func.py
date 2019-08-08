# --------------------------------------------------------------------------- #
# func.py
# --------------------------------------------------------------------------- #

import sys
import tempfile
import os
import errno
import os.path
import hashlib
from urllib2 import Request, urlopen, URLError, HTTPError
from pprint import pprint
from core.data import fpr,tc 
from core.data import smtp,smpls,DEBUG
from core.ui.banner import bancls

# --------------------------------------------------------------------------- #
# keep stats value per attachment
# --------------------------------------------------------------------------- #
def astat():

    #from core.data import smtp,smpls,DEBUG
    if True:
        for k in smpls.keys():
            if 'astat' in smpls[k]:
            #    smpls[k]['astat'] = 0 
               if smpls[k]['astat']:
                  return 1 
        for k in smpls['zip'].keys():
            if type(smpls['zip'][k]) is dict:
                if 'astat' in smpls['zip'][k]:
                    if smpls['zip'][k]['astat']:
                       return 1
                #   print smpls['zip'][k]['astat']
        for k in smpls['zip-smpls'].keys():
            if type(smpls['zip-smpls'][k]) is dict:
                if 'astat' in smpls['zip-smpls'][k]:
                    if smpls['zip-smpls'][k]['astat']:
                       return 1
        return 0

# --------------------------------------------------------------------------- #
# flush stats values per attachment
# --------------------------------------------------------------------------- #
def flush_astat():

   #from core.data import smtp,smpls,DEBUG

   if True:
        for k in smpls.keys():
            if 'astat' in smpls[k]:
                smpls[k]['astat'] = 0 
        for k in smpls['zip'].keys():
            if type(smpls['zip'][k]) is dict:
                if 'astat' in smpls['zip'][k]:
                    smpls['zip'][k]['astat'] = 0
        for k in smpls['zip-smpls'].keys():
            if type(smpls['zip-smpls'][k]) is dict:
                if 'astat' in smpls['zip-smpls'][k]:
                    smpls['zip-smpls'][k]['astat'] = 0

# --------------------------------------------------------------------------- #
# check if data content is build from predefeined sample or custom body
# --------------------------------------------------------------------------- #
def mimeuse():

    #from core.data import smtp,DEBUG
    #from core.func import info,waitin

    if smtp['use_mime']:
       return 1
    else:
       bancls()
       info('info','You have alredy defined custom Body Content. ' \
                   'First flush it before trying to build a message with other options.')
       waitin()
       return 0

# --------------------------------------------------------------------------- #
# compress plain text sample and return a zip raw data
# --------------------------------------------------------------------------- #
def get_zipfile(sample,fn=''):

    import zipfile
    try:
         from cStringIO import StringIO

    except:
         from StringIO import StringIO
    
    f = StringIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    if not fn:
        fn='minj-sample.txt'
        #print fn
    #print fn
    z.writestr(fn, sample['val'])
    z.close()

    return  f.getvalue()


# --------------------------------------------------------------------------- #
# fetch sample from remote server 
# --------------------------------------------------------------------------- #
def get_sample(sample):

     #import os
     #import hashlib
     #from urllib2 import Request, urlopen, URLError, HTTPError
     #from core.func import dbginfo

     fpr('Fetching sample .. ')
     fn  = sample['filename']+'.tmp'
     url = sample['url']
     req = Request(url)
     try:
         r = urlopen(req)
         print
     except HTTPError as e:
         dbginfo('error',
           'Err: The server couldn\'t fulfill the request.\n' \
           'Code: %s ' % e.code 
         )
     except URLError as e:
         dbginfo('error',
           'Err: Server can not be reached!\n' \
           'Reason: %s ' % e.reason
         )
     else:
         # everything is fine
         data = r.read()
         fpr.ok('Data fetching')
         with open(fn,"wb") as f:
              if data:
                  try:
                      f.write(data)

                  except IOError:
                      fpr.fail('Temporary file saving')
                      return
                  else:
                      f.close()
                      fpr.ok('Temporary file saving')


                  if os.path.isfile(fn):
                       md5tmpfn =  hashlib.md5(open(fn, 'rb').read()).hexdigest()
                       #print sample['md5'] 
                       #print hashlib.md5(open(fn, 'rb').read()).hexdigest()
                       if sample['md5'] == md5tmpfn:
                            fpr.ok('Hash testing')
                            try:
                                os.rename(fn, sample['filename'])
                            except IOError:
                                fpr.fail('File saving')
                                return
                            else:
                                fpr.ok('File saving')
  
	               else:
                            fpr.fail('Hash testing')
                                                         

              else:
                  fpr.err('No data')
                  return
 
# --------------------------------------------------------------------------- #
# print additional information and dump data object in readable form (pprint)
# --------------------------------------------------------------------------- #

def dbglog(s,f=0):

    #from core.data import DEBUG
    #from pprint import pprint

    global tc
    if DEBUG:
        fpr.purple( ('-'*(tc-4-len('-- DebuG --')) + '-- DebuG --' ))
        if type(s) is str:
            fpr(s)
        else:
            if f:
                pprint(s)
            else:
                fpr('%r' %  s)
      
        fpr.purple('-'*(tc-4))


# --------------------------------------------------------------------------- #
# append uniq elements: when element from b does not exist in a
# --------------------------------------------------------------------------- #
def append_uniq(a,b):

    for i in b:
        if i not in a:
            a.append(i)

# --------------------------------------------------------------------------- #
# get multiline inputs from user, flush newlines and whitespace by default 
# --------------------------------------------------------------------------- #
def get_inputs(nl=False):

    inputs = []
    while True:
        try:
            line = raw_input("")
        except EOFError:
            break
        #  flush empty line by default
        if not nl:
            #if line is not empty line or contain only whitespaces 
            if not len(line.strip()) == 0 :
               inputs.append(line.strip())
        else:
            inputs.append(line)
    return inputs

# --------------------------------------------------------------------------- #
# prompt a filename to load and verify if file exists
# --------------------------------------------------------------------------- #
def get_filename():

    #import os.path
    while True:
        bancls()
        fpr('Load attachment from file')
        print
        fpr('Please provide a full path: ')
        fn = raw_input('  > ')
        if fn:
            #content.att_load_file(smtp['content']['att'],attfn)
            if os.path.exists(fn):
                return fn
            else:
               fpr.fail('File not found')
               print
        if raw_input('  Return to menu [y/N]> ') in ['y','Y']:
            break



def get_filename2(mode='load', title=None):

   while True:
       bancls()
       if title:
           fpr('%s' % title)
       print
       fpr('Please provide a file name:')
       fn = raw_input('  []> ')
       print 
       if fn:
           if mode == 'save':
               if os.path.isfile(fn):
                   if get_yesno_input ('  File already exist. Overwrite it [y/N]: '):
                      return fn
                   #else: 
                   #   return None
               else:
                  return fn
           if mode == 'load':
               if os.path.exists(fn):
                   return fn
               else:
                   fpr.fail('File not found')
                   print
       
 
       if get_yesno_input('  Return to menu [y/N]> '):
           break
     



# --------------------------------------------------------------------------- #
# load file data
# --------------------------------------------------------------------------- #

"""
def get_file_content(fn):
#FIXME: use try / except

    #import os
    fp = open(fn, 'rb')

    inputs = fp.read()
    fp.close()
    if inputs:
        return inputs
    else:      
        dbginfo('error','Err: File has no content. Please verify file size !\n[ %s ]' % fn)
        #break
        return False
"""

def get_file_content(fn,mode='rb'):

    if not os.path.isfile(fn):
        fpr.err('Err: File does not exist !')
        return None
 
    try:
        fp = open(fn, mode)

        inputs = fp.read()
        fp.close()

        if inputs:
            return inputs
        else:
            dbginfo('error','Err: File has no content. Please verify file size !\n[ %s ]' % fn)
            return None

    except:
        fpr.err("Err: Could not open a file !")



def save_content_asfile(content, fn, mode='w'):


#    if os.path.isfile(fn):
#        if not get_yesno_input ('  File already exist. Overwrite it [y/N]: '):
#            return False
    try:
       
       with open(fn, mode) as fo:
          fo.write(content)
          fpr.ok('Saving content in %s' % fn)
    except IOError as ioex:
       fpr.fail('Saving content in %s' % fn )
       #fpr.fail('Err: Logs not saved with %s' % logfile )
       print
       fpr.err('Errno: %s' % ioex.errno)
       fpr.err('Err code: %s' % errno.errorcode[ioex.errno])
       fpr.err('Err message: %s' % os.strerror(ioex.errno) )





# --------------------------------------------------------------------------- #
# prompt for single value, return None or preserver existing for empty input
# --------------------------------------------------------------------------- #
def get_single_input(q,d,nl='\n '):
    # q - question
    # d - default value
    # nl - use or not newline between the question and default value
    
    d = raw_input('  %s%s [%s]> ' % (q,nl,(d or ''))) or (d or None)
    if d == '.':
       return None
    else:
       return d


# --------------------------------------------------------------------------- #
# prompt for single value and do not return value but set it 
# --------------------------------------------------------------------------- #
def set_dval(q,dd,key,val='',ret=0):

    #dd  - destination dict
    #q   - question
    #key - dst key
    #val - default value

    #hide None value:  show [] not [None]
    dbginfo('debug','val=%s , dd[key]=%s' % (val,dd.get(key,'NOKEY')) )
    if val == None:
       if dd.get(key):
           gval = raw_input('%s: [%s]> ' %  (q,dd.get(key)) ) or dd.get(key,val)
       else:
           gval = raw_input('%s: []> ' %  q ) or dd.get(key,val)
    else:
       gval = raw_input('%s: [%s]> ' %  (q, dd.get(key,val)) ) or dd.get(key,val)

    # clear value if dot as value
    if gval == '.':
       #return ''
       dd[key] = None
    else:
       if ret:
           return gval
       else:
           dd[key] = gval


# --------------------------------------------------------------------------- #
# prompt for simple yes/no input 
# --------------------------------------------------------------------------- #
def get_yesno_input(q,v=''):
    if raw_input(q) in ['y','Y']:
        return True
    else:
        return False

# --------------------------------------------------------------------------- #
# request user input before continue 
# --------------------------------------------------------------------------- #
def waitin():
    print; 
    if raw_input('  Press Enter to continue...'):
       print



# --------------------------------------------------------------------------- #
# test os type
# --------------------------------------------------------------------------- #
def os_type():

    #import os

    if os.name == "nt":
        return "nt"
    if os.name == "posix":
        return  "posix"
    else: 
        return None
 
# --------------------------------------------------------------------------- #
# test terminal support for utf-8 characters
# --------------------------------------------------------------------------- #
def utf8Term():

    #import sys

    try:
       u"\u03A9".encode(sys.stdout.encoding)
       return True
    except UnicodeEncodeError:
       return False

# --------------------------------------------------------------------------- #
# print notification with extra frame(top+bottom line)
# --------------------------------------------------------------------------- #
def info(itype,msg,log=None,adj='c',frame='warn'):
#TODO: add color option for frame  
# 
   if itype.lower() == 'info':

      fpr.warn( ('_'*(tc-4-len('__')) + '__' ))
      print
      fpr(msg,adj=adj)
      if log:
         fpr.info('_'*(tc-4))
         print
         fpr.info(log)
         fpr.info('_'*(tc-4))

      fpr.warn('_'*(tc-4))


# --------------------------------------------------------------------------- #
# print debug/warn/error notification with extra frame (top+bottom line)
# --------------------------------------------------------------------------- #
def dbginfo(itype,msg,log=None):

    if itype.lower() == 'error':
        fpr.err( ('-'*(tc-4-len('-- Error --')) + '-- Error --' ))
        fpr.info(msg)
        if log:
            fpr.err('_'*(tc-4))
            print
            fpr(log)
            fpr.err('_'*(tc-4))
        fpr.err('-'*(tc-4))

    if itype.lower() == 'warrning':
        fpr.warn( ('-'*(tc-4-len('-- Warrning --')) + '-- Warrning --' ))
        fpr.info(msg)
        if log:
            fpr.warn('_'*(tc-4))
            print
            fpr(log)
            fpr.warn('_'*(tc-4))
        fpr.warn('-'*(tc-4))

    if itype.lower() == 'debug':
        #from core.data import DEBUG
        if not DEBUG:
            return 0
        fpr.purple( ('-'*(tc-4-len('-- Debug --')) + '-- Debug --' ))
        fpr.info(msg)
        if log:
            fpr.purple('_'*(tc-4))
            print
            fpr(log)
            fpr.purple('_'*(tc-4))
        fpr.purple('-'*(tc-4))

# --------------------------------------------------------------------------- #
# use external editor to create or edit message body content
# --------------------------------------------------------------------------- #
def edit(editor, content=''):
    #import os, tempfile

    f = tempfile.NamedTemporaryFile(mode='w+')
    if content:
        f.write(content)
        f.flush()

    if editor in ['vim', 'gvim', 'vim.basic', 'vim.tiny', 'mvim']:
        editor += ' "+set backupcopy=yes" -f -o'

    command = editor + " " + f.name
#    dbginfo('debug', 'editor: %s' % command)
    status = os.system(command)
#    from subprocess import call
#    call([editor,f.name])

    f.seek(0, 0)
    text = f.read()
#    dbginfo('debug',text)
    f.close()
    assert not os.path.exists(f.name)
    return (status, text)


