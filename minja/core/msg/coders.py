# --------------------------------------------------------------------------- #
# coders.py
# --------------------------------------------------------------------------- #

import re
import email
import base64


"""
# --------------------------------------------------------------------------- #
There are two limits that this specification places on the number of characters
in a line. Each line of characters MUST be no more than 998 characters, and 
SHOULD be no more than 78 characters, excluding the CRLF.

You can, however, extend the header body beyond a single line with "folding". 
The receiver then "unfolds" the lines.

An unfolded header field has no length restriction and therefore may be 
indeterminately long. The header name cannot be folded, so the header name 
cannot be longer than the line limit.

RFC 5322 specifies line length SHOULD be less than 78 characters and MUST be 998 
or less, including CRLF. (This results in a limit on the length of the header 
name, which cannot be folded, to 74 characters.) 
There is no limit to the number of folds in a header field body, although there 
are probably practical limitations.

RFC 2047 adds further constraints to header line length. in particular it says 
lines containing encoded words MUST be no longer than 76 octets, these 
constraints only apply to header lines where RFC2047 encoding is used.

https://tools.ietf.org/html/rfc5322#page-8
# --------------------------------------------------------------------------- #
"""
# --------------------------------------------------------------------------- #
# decode list of multple email headers 
# --------------------------------------------------------------------------- #

def decode_mheaders(inputs):
    #import re
    # decode multiline email headers
    ehead = {}
    key   = ''
    for (i,line) in enumerate(inputs):
        line = re.sub(r'\s', '', line)   # remove whitespaces from line 
        # print 'line2 %s ' % line
        # clear key when line is empty
        if line == '':
            key = ''
        # if exist use header-name as new key
        # header-name: =?encoded-string?=
        m1 = re.match(r'(.*):(=\?.*\?=)',line)
        if m1:
            #print m1.group()
            #print m1.group(1)
            #print m1.group(2)
            if m1.group(1):
                key = m1.group(1) 
                ehead.setdefault(key,[]).append(m1.group(2))
        # if no header-name and previous line is not a new line 
        # assume it is a sequl and append to the previous key
        # if no header-name and previous line is a new line 
        # append to a new ''unknown'' key 
        # =?encoded-string?=
        m2 = re.match(r'^(\s+)*(=\?.*\?=)',line)
        if m2:
           if key == '' and inputs[i-1] != "\n":
               key = '-no-hn-' 
               while key in ehead.keys():
                  key += '-'
           ehead.setdefault(key,[]).append(m2.group(2))
    return ehead
    #print ehead  #DEBUG
#    waitin()
#    if ehead.keys():
#        print
#        fpr('- '*(tc/2-4))
#        #print
#        for k in ehead.keys():
#            print 
#            dhead, enc = decode_header(''.join(ehead[k]).replace('?==?', '?= =?') )[0]
#            if re.match('-no-hn-',k):
#                fpr('Header-name: <None>')
#            else:
#                fpr('Header-Name: %s' % k)
#            fpr('Header: %s' % dhead)
#            ##print dhead
#            fpr('Encoding: %s' % enc)
#        print
#        fpr('- '*(tc/2-4))
#        waitin() 
    # _end_of_decode_multiline_headers    


# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
# https://www.theeggeadventure.com/wikimedia/index.php/IsBase64
def isBase64(s):
    #import re
    return (len(s) % 4 == 0) and re.match('^[A-Za-z0-9+/]+[=]{0,2}$', s)

# --------------------------------------------------------------------------- #
# encode inputs - get raw data string and return base64 encoded string
#
# standard base64 does encode input as one long string 
# without any newline, as we are working with smtp wher 
# the length of line is assumed to be 76 characters long 
# it's better to use base64MIME from email module which 
# do the job by default 
# --------------------------------------------------------------------------- #
def encode_attch(inputs):

    #import email
    try:
     #   enc = base64.b64encode(inputs)
        enc = email.base64MIME.encode(inputs)
        return dict({'b64': enc})
    except:
        print Exception;
        return None

# --------------------------------------------------------------------------- #
# decode inputs - get base64 encoded string and return raw data
# --------------------------------------------------------------------------- #
def decode_attch(inputs):

    #import base64
    try:
        dec = base64.b64decode(inputs)
        #print 'DEC:',dec
        return dict({'raw': dec})
    except:
        print Exception;
        return None






 
