# --------------------------------------------------------------------------- #
# utils.py
# --------------------------------------------------------------------------- #

import os 
import re
from email.header import Header,decode_header
from email.message import Message
import core.msg.coders as coders
from core.data import fpr,tc,tr,DEBUG
from core.func import waitin,dbginfo,get_inputs,get_file_content,dbglog
from core.ui.banner import bancls



# --------------------------------------------------------------------------- #
# decode email headers
# --------------------------------------------------------------------------- #
def d_headers():

    fpr('Diagnostics: Header decoder')
    print 
    if raw_input('  Would you like to decode some headers [y/N]> ') in ['y', 'Y']:
        print
        fpr('Please provide an encoded part of the header:')
        #ehead = raw_input('  ')
        fpr('Use Ctrl-D with new line to continue.')
        fpr.blue('_'*(tc-4))
        print
    
        inputs = get_inputs(nl=True) 
       
        fpr.info('_'*(tc-4))
        # decode multiline email headers
        ehead = coders.decode_mheaders(inputs)
        waitin()
        if ehead.keys():
            fpr('Decoded Headers')
            fpr.info('_'*(tc-4))
            #print
            for k in ehead.keys():
                print 
                dhead, enc = decode_header(''.join(ehead[k]).replace('?==?', '?= =?') )[0]
                if re.match('-no-hn-',k):
                    fpr('Header-name: <None>')
                else:
                    fpr('Header-Name: %s' % k)
                fpr('Header: %s' % dhead)
                ##print dhead
                fpr('Encoding: %s' % enc)
            print
            fpr.blue('_'*(tc-4))
            waitin() 
        # _end_of_decode_multiline_headers    
        else:
            fpr('Sorry! No header to decode')
            waitin()    
        ehead.clear()      
    else:
       waitin()


# --------------------------------------------------------------------------- #
# encode email headers
# --------------------------------------------------------------------------- #
def e_headers():

    fpr('Diagnostics: Header encoder')
    print 
    if raw_input('  Would you like to encode some headers [y/N]> ') in ['y', 'Y']:

        if True:
            print
            fpr('Please provide a header in format: >> Header-name: header-value <<')
            fpr('Use Ctrl-D to continue.')
            fpr.blue('_'*(tc-4))
            print
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
                print
                fpr('Found headers')
                print
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

                if thead.keys():
                    print
                    chset = raw_input('  Define headers encoding or leave empty to use a default one\n  [us-ascii]: ') or 'us-ascii'
                    fpr.blue('_'*(tc-4))
                    print
                    #print
                    if chset:

                        #from email.message import Message
                        #from email.header import Header
                        for hn in thead.keys():
                            try:
                                h = Header(''.join(thead[hn]), charset=chset, maxlinelen=76, header_name=hn)
                                #print h.encode()
                                print
                                msg = Message()
                                msg[hn] = h
                                print msg.as_string()
                            except UnicodeDecodeError,e:
                                print
                                fpr.err('UnicodeDecodeError: %s' % e)
                                print
                                fpr('Try to set proper encoder! ')
                            print 
                    fpr.blue('_'*(tc-4))
 


                waitin()
                """ 
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
                """

    else:
        waitin()


# --------------------------------------------------------------------------- #
# decode base64 input
# --------------------------------------------------------------------------- #
def d_base64(op):

    # load from file
    if op == '1':

            fn = ''
            while True:
               bancls()
               fpr('Diagnostics: Base64 decoder')
               print
               fpr('Please provide a file name:')
               fn = raw_input('  []> ')
               print 
               inputs = get_file_content(fn)
               print
               if inputs:
                  #inputs = f.readlines()          # include \n
                  #inputs = f.read().splitlines()   # exclude \n
                  dbginfo('debug',inputs)
                  print
                  if not coders.isBase64(''.join(inputs)):
                      fpr('File seems to be BASE64 encoded')
                  else:
                      fpr.warn('File does not seems to be Base64 encoded')
                  print

                  decb64 = coders.decode_attch(inputs)

                  if isinstance(decb64,dict):
                      fpr.ok('File content was decoded successful')
                  else: 
                      fpr.fail('File content was not decoded')
                  waitin()
                  return decb64

               elif raw_input('  Return to menu [y/N]> ') in ['y','Y']:
                  break
 
               waitin() 

    # load from input - paste it 
    if op == '2':
        bancls()
        fpr('Diagnostics: Base64 decoder')
        print
        if raw_input('  Would you like to decode some content [y/N]> ') in ['y', 'Y']:
            print
            fpr('Please provide Base64 encoded content')
            fpr('Use Ctrl-D with new line to continue.')
            print 
            fpr.blue('_'*(tc-4))
            print
            inputs = get_inputs()
            fpr.blue('_'*(tc-4))

            if inputs:
                  dbglog(inputs)
                  print
                  if not coders.isBase64('\n'.join(inputs)):
                      fpr('Input seems to be BASE64 encoded')
                  else:
                      fpr.warn('Input does not seems to be Base64 encoded')
                  print

                  decb64 = coders.decode_attch('\n'.join(inputs))
 
                  if isinstance(decb64,dict):
                      fpr.ok('Input content was decoded successful')
                  else: 
                      fpr.fail('Input content was not decoded')
                  waitin()
                  return decb64

            waitin()

# --------------------------------------------------------------------------- #
# encode base64 input
# --------------------------------------------------------------------------- #
def e_base64(op):
    # load from file
    if op == '1':
        fn = ''
        while True:
           bancls()
           fpr('Diagnostics: Base64 encoder')
           print
           fpr('Please provide a file name:')
           fn = raw_input('  []> ')
           print 
           inputs = get_file_content(fn)
           print
           if inputs:
              #inputs = f.readlines()          # include \n
              #inputs = f.read().splitlines()   # exclude \n
              dbginfo('debug',inputs)
              print

              encb64 = coders.encode_attch(inputs)
 
              if isinstance(encb64,dict):
                  fpr.ok('File content was encoded successful')
              else: 
                  fpr.fail('File content was not encoded')
              waitin()
              return encb64
           elif raw_input('  Return to menu [y/N]> ') in ['y','Y']:
              break

           waitin() 
    # load from input - paste it 
    if op == '2':
        bancls()
        fpr('Diagnostics: Base64 encoder')
        print
        if raw_input('  Would you like to encode some content [y/N]> ') in ['y', 'Y']:
            print
            fpr('Please provide some plain content')
            fpr('Use Ctrl-D with new line to continue.')
            print 
            fpr.blue('_'*(tc-4))
            print
            inputs = get_inputs()
            fpr.blue('_'*(tc-4))

            if inputs:
                  dbglog(inputs)
                  print
                  encb64 = coders.encode_attch('\n'.join(inputs))
 
                  if isinstance(encb64,dict):
                      fpr.ok('Input content was encoded successful')
                  else: 
                      fpr.fail('Input content was not encoded')
                  waitin()
                  return encb64
            #print inputs
            waitin()



# --------------------------------------------------------------------------- #
# list generator
# --------------------------------------------------------------------------- #
alphabet = [chr(i) for i in range(ord('a'),ord('z')+1)]
digits = range(10)
special = [] 

# inlucde oreder (asc,dsc) and random

def gen_list(alpha, length):
    """Return  list of all strings of 'alphabet' of length 'length'"""


    c = []
    for i in range(length):
        c = [[x]+y for x in alphabet for y in c or [[]]]

    return c


