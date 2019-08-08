# --------------------------------------------------------------------------- #
# 2.6 - Data Security - DKIM
# --------------------------------------------------------------------------- #

import re
import base64
from core.func import dbginfo,info
from core.data import smtp,fpr,tc,tr
from core.ui.banner import bancls

__all__=[
'dkim_signature',
'att_dkim_signature',
'dkim_pktest',
'dkim_canontest',
'dkim_canon'
]

# --------------------------------------------------------------------------- #
# generate DKIM-Signature
# --------------------------------------------------------------------------- #
def dkim_signature(body,d={}):

    try:
        import dkim
        dsig = dkim.sign(body,
                         d.get('selector',''),
                         d.get('domain',''), 
                         d.get('privkey',''),
                         d.get('identity',None),
                         dkim_canontest(d.get('canonicalize','relaxed/simple')),
                         #d.get('canonicalize','relaxed/simple'),
                         include_headers=d.get('include_headers',['from', 'to','subject']),
                         length=d.get('length',False),
                         #debuglog=None,
                        )
        #dbginfo('debug', dsig)
        #smtp['h_DKIM-Signature'] = dsig[len("DKIM-Signature: "):]
        return dsig[len("DKIM-Signature: "):]
    except ImportError:
        print
        dbginfo('warrning','Warrning: Missing module: dkimpy. Use: pip install dkimpy') 
        print
    except Exception,e:
        print
        fpr.err('Err: ' + str(e))
        print
# --------------------------------------------------------------------------- #
# attach DKIM-Signature header 
# --------------------------------------------------------------------------- #
def att_dkim_signature(dsig):

    if smtp['sign']['dkim']['dstat'] != 0:
       fpr('It seems you have already attached %s DKIM Signature' % smtp['sign']['dkim']['dstat'])
       if not raw_input('  Do you want to append another one [y/N]:') in ['y','Y']:
          return
        
    smtp['headers']['h'+str(smtp['sign']['dkim']['dstat'])+'_DKIM-Signature'] = dsig
    smtp['sign']['dkim']['dstat'] += 1 

    fpr.ok('DKIM Signature attached (x%d)' % smtp['sign']['dkim']['dstat']  )


# --------------------------------------------------------------------------- #
# perform basic test of private key format
# --------------------------------------------------------------------------- #
def dkim_pktest(privkey):

    if not (privkey or type(privkey) is str):
       return False
    m = re.search("--\n(.*?)\n--", privkey, re.DOTALL) 
    if m is None:
         return False 

    try: 
        bancls() 
        pkdata = base64.b64decode(m.group(1))
        fpr('Private key')
        info('info',m.group(1),adj='l')
        return True
    except TypeError, e: 
        fpr (str(e))
        return False 

# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def dkim_canontest(canon):
   
    if canon:
        m = re.match('^(simple|relaxed)/(simple|relaxed)$', canon.strip(' \t\n\r').lower())
        if m:
            try:
               from dkim import Simple,Relaxed
               cl = Relaxed
               cr = Simple

               if m.group(1) == 'simple':
                   cl = Simple
               else:
                   cl = Relaxed
               if m.group(2) == 'simple':
                   cr = Simple
               else:
                   cr = Relaxed
               return (cl,cr)

            except ImportError:
               print
               dbginfo('warrning','Warrning: Missing module: dkimpy. Use: pip install dkimpy') 
               print
        else:
            #fpr.err('NO MATCH %s' %canon)
            return None

    return False

# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def dkim_canon(canon,message):
   
    if True:
        m = re.match('^(simple|relaxed)/(simple|relaxed)$', canon.strip(' \t\n\r').lower())
        if m:
            try:
               import dkim

               (headers, body) = dkim.rfc822_parse(message)

               ch = dkim.canonicalization.Simple
               cb = dkim.canonicalization.Simple

               #print headers
               #print body 
               #dbginfo('info',str(headers))

               if m.group(1) == 'simple':
                   ch = dkim.canonicalization.Simple.canonicalize_headers(headers)
               else:
                   ch = dkim.canonicalization.Relaxed.canonicalize_headers(headers)
               #print ch


               if m.group(2) == 'simple':
                   cb = dkim.canonicalization.Simple.canonicalize_body(body)
               else:
                   cb = dkim.canonicalization.Relaxed.canonicalize_body(body)

               #print cb

               return (ch,cb)

            except ImportError:
               print
               dbginfo('warrning','Warrning: Missing module: dkimpy. Use: pip install dkimpy') 
               print
        else:
            #fpr.err('NO MATCH %s' %canon)
            return None

    return False

# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def dkim_vrfy(message):



    PYDNS_AVAILABLE=False
    DNSPYTHON_AVAILABLE=False

    # check dns libraries
    try:
        import dns
        DNSPYTHON_AVAILABLE=True
    except ImportError:
        pass
  
    try:
        import DNS
        PYDNS_AVAILABLE=True
    except ImportError:
       pass
  
    try:
       from dkim import DKIM,verify,DKIMException
  
       if not (PYDNS_AVAILABLE or DNSPYTHON_AVAILABLE):
            raise Exception("no supported dns library available")
    except:
       pass

    try:
       import dkim
       if True:
           d = dkim.DKIM(message)
           #print 'dir:',dir(d)
           #print 'sel:',d.selector
           #print 'dom:',d.domain
           #print 'h:',d.headers
           #print 'sh:',d.signed_headers
           #print 'sa:',d.signature_algorithm
           #print 'sf:',d.signature_fields
           #print 'ks:',d.keysize

           r = d.verify()

           fpr('Signature details')
           fpr('_'*(tc-4))
           print
           fpr(' selector (s): %s' % d.selector)
           fpr(' domain   (d): %s' % d.domain)
           fpr(' headers     : %s' % d.headers)
           fpr(' signed heads: %s' % d.signed_headers)
           fpr(' key algo (a): %s' % d.signature_algorithm)
           fpr(' key size    : %s' % d.keysize)
           print
           fpr(' DKIM-Signature: %s' % d.signature_fields)
           fpr('_'*(tc-4))
           print


       else:
           r = dkim.verify(message)
       if r:
           fpr.ok("DKIM signature verification successful")
       else:
           fpr.fail("DKIM signature verification failed")

    except DKIMException,e:

       fpr("Verification result:")
       print
       fpr('%s' % e)
       print
       fpr.fail("DKIM signature verification failed")


    except Exception as e:
       fpr.err('Err: %s' % e)


