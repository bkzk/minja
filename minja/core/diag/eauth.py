#
# diag.eauth.py
#

from core.data import fpr,tc,tr,DEBUG
from core.func import waitin,dbginfo,dbglog,info,get_yesno_input,get_inputs
from core.ui.banner import banner, bancls

from pprint import pprint
#try:
#    import spf
#except:
#    pass

import re
# pydns: 
#import dns
#import ipaddr
#import ipaddress
import spf

SPF_MODIFIERS=('redirect','explanation')


DDDEBUG=False


"""

     |  query:
     |
     |  i: ip address of SMTP client in dotted notation
     |  s: sender declared in MAIL FROM:<>
     |  l: local part of sender s
     |  d: current domain, initially domain part of sender s
     |  h: EHLO/HELO domain
     |  v: 'in-addr' for IPv4 clients and 'ip6' for IPv6 clients
     |  t: current timestamp
     |  p: SMTP client domain name
     |  o: domain part of sender s
     |  r: receiver
     |  c: pretty ip address (different from i for IPv6)
     |
     |  This is also, by design, the same variables used in SPF macro
     |  expansion.
     |
     |  Also keeps cache: DNS cache.
     |
     |  Methods defined here:
     |
     |  __init__(self, i, s, h, local=None, receiver=None, strict=True, timeout=20, verbose=False, querytime=0)


"""

"""                
Mechanism
    * all * a * mx * ptr * ip4 * ip6 * include * exists * extensions 
Domains may also define modifiers. Each modifier can appear only once.
    * redirect * explanation 
Mechanisms can be prefixed with one of four characters:
    - fail
    ~ softfail
    + pass
    ? neutral 
If a mechanism results in a hit, its prefix value is used. The default prefix value is 'pass".

"""
 
# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def spfmech(spfpl,q,mode,level=0):

    #MODE = 0 : syntax validation mode QUITE 
    #MODE = 1 : syntax validation mode VERBOSE
    #MODE = 2 : spf validation (req spf values) - show flow 

    #mode = 0

    #if mode:
    #    fpr('SPF Policy: "%s"' % spfpl)
    #    print
    

    RE_SPFMODS   = re.compile(br'^(redirect=|explanation=)',re.IGNORECASE)
    RE_SPFMODRED = re.compile(br'^redirect=(.*)',re.IGNORECASE)
    RE_SPFMODEXP = re.compile(br'^explanation=(.*)',re.IGNORECASE)

    


    for m in spfpl.split():
        #FIXME: exclude' v=spf'
         # validate query against each mechanism spearately

         if m != 'v=spf1':

              try:
#                  mech,mtype,arg,cidrlength,result = None,None,None,None,None
                 # do not validate SPF modifiers 
                  # http://www.openspf.org/Mechanisms
                  m_m = re.match(RE_SPFMODS,m)
                  if m_m:
                      fpr(' -> modifier: %s' % m) 
                      m_m2 = re.match(RE_SPFMODRED,m)
                      if m_m2:
                          if mode:
                              red = q.dns_spf(m_m2.group(1))
                              level += 1
                              #fpr.info('    ************************************************************************')
                              #fpr.info(' <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                              print 
                              fpr('%sFallowing DNS/TXT RR of %s' % ('_'*level,m_m2.group(1)))
                              fpr('_'*(tc-4))
                              print
                              fpr.info('%s' % red)
                              fpr('_'*(tc-4))
                              print
                              spfmech(red,q,1,level)
                              print
                              fpr('%sFinishing recursive evaluating of %s' % ('_'*level, m_m2.group(1)))
                              print
                              #fpr.info(' >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                              #fpr.info('    ************************************************************************')
                              #fpr.info('    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                  else:
                      if mode:
                         fpr(' -> mechanism: %s' % m)
                      try:
                         mech,mtype,arg,cidrlength,result = q.validate_mechanism(m)
                      except Exception,e:
                         fpr.err('Err: %s' % e)

                      if mode:
                          #fpr('    %s,%s,%s,%s,%s' %(mech,mtype,arg,cidrlength,result) )
                          fpr.info('    %s -> %s, cidr: %s, prefix value: %s' %(mtype,arg,cidrlength,result) )
                          if mtype == 'include':
                              try: 
                                  inc = q.dns_spf(arg)
                                  if mode:
                                      level += 1
                                   #   fpr.info('    ************************************************************************')
                                   #   fpr.info('    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                                      #fpr.info('    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                                      print
                                      fpr('%sFallowing DNS/TXT RR of %s' % ('_'*level,arg))
                                      fpr('_'*(tc-4))
                                      print
                                      fpr.info('%s' % inc)
                                      fpr('_'*(tc-4))
                                      print
                                      spfmech(inc,q,1,level)
                                      #fpr.info('    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                                      #fpr.info('    ************************************************************************')
                                      print
                                      fpr('%sFinishing recursive evaluating of %s' %('_'*level,arg))
                                      print
                              except spf.PermError, e:
                                  if mode:  
                                      print
                                      fpr.err('SPF policy error: %s' % e)
                                      print
                                          

              except spf.PermError, e:
                  if mode:  
                      print
                      fpr.err('SPF policy error: %s' % e)
                      print
                  return False
    return True

# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def spfdns(domain,q):


    #local_part,domain = spf.split_email(s=dd['id'].get('mfrom'),h='')
    txt = q.dns_spf(domain)
    if txt:
        fpr.green('TXT: %s\n\n' % txt)
    else:
        fpr.err('SPF record not found or more than one record found')


# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def get_rrtxt(mfrom):

        RE_SPF = re.compile(br'^v=spf1$|^v=spf1 ',re.IGNORECASE)
        fpr('MFROM identity: %s' % mfrom) 

        try:
            local_part,domain = spf.split_email(s=mfrom, h='')
            fpr('Domain: %s' % domain)

            print
            _dns = spf.DNSLookup(domain, 'TXT', strict=True, timeout=20)

            if _dns:
                #dbginfo('debug','DNS: %s ' % dns)
                # for k, v in DNSLookup(name, qtype, self.strict, timeout):
                for k, v in _dns:
                    #k = (k[0].lower(), k[1]) 
                    if k[1] == 'TXT':
                       m =  re.match(RE_SPF, v[0])
                       if m:                    
                           fpr( 'DNS RR: %s' % k[1])
                           print
                           #for i in v:
                           #    fpr.green('%s' % i )
                           fpr.green('%s' % "".join(v)  )
                    #print
            else:
                fpr('No TXT RR was found')
                print

        except spf.TempError,e:
            fpr.err('Error: %s' % e)
            print


# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def auth_spfplflow(dd,spfid):

   # info('info','SPF Validation  process tests SPF record if it is syntactically correct \n' \
   #             'according to RFC 7208 compliant library pyspf. To present the whole path \n' \
   #             'this test additionally follow all "include" mechanisms using DNS query to \n' \
   #             'retrieve all external SPF policies.' \
   #             , adj='l')
   # print



    fpr('SPF identity type  : %s' % spfid) 
    fpr('SPF identity value : %s' % dd['id'].get(spfid)) 
    if spfid == 'mfrom':
        local_part,domain = spf.split_email(s=dd['id'].get('mfrom'),h=dd['id'].get('helo'))
    if spfid == 'helo':
        local_part,domain = spf.split_email(s='', h=dd['id'].get('helo'))
    fpr('Domain: %s' % domain)

    print
    try:
        q = spf.query( i=dd.get('ip'),
               s=dd['id'].get('mfrom'),
               h=dd['id'].get('helo'),
               timeout=20, verbose=False, querytime=0
             )
    except Exception,e: 
        fpr.err('Err: %s'%e)
        waitin()
        return

    if not dd['id'].get(spfid):
        print
        fpr.warn('Verification skipped. No identity found')
        waitin()
        return

    if not dd.get('ip'):
        print
        fpr.warn('Verification skipped. Missing client IP address!')
        waitin()
        return

    # if SPF Policy is defined manually skip DNS and use it
    if dd.get('policy'):
        #fpr('SPF record supplied by input is found! ')
        fpr('Policy origin: User input\n\n')
        if get_yesno_input('  Run validation against supplied SPF record [y/N]: > '):
            print
            fpr('Policy origin: INPUT\n\n')
            fpr('_'*(tc-4))
            print
            fpr.green('%s' % dd['policy'])
            fpr('_'*(tc-4))
            print
            fpr('Evaluating policy mechanism ..')
            print
            spfmech(dd['policy'],q,1)
            print
            return
    if True:
        print
        fpr('Policy origin: DNS/TXT RR\n\n')
        try:
            txt = q.dns_spf(domain)
            if txt:
                fpr('_'*(tc-4))
                print
                fpr.green('%s' % txt)
                fpr('_'*(tc-4))
            else:
                fpr.err('SPF record not found or more than one record found')
                waitin()
                return
            print
            fpr('Evaluating policy mechanism ..')
            print
            spfmech(txt,q,1)
#            res,code,expl = q.check()
#            valid = True
        except spf.TempError,e:
            fpr.err('Error: %s' % e)


 


# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def auth_spf(dd,spfid='all'):


    #TODO: validate value ip, helo (fqdn), mfrom (isemail)


    fpr('SPF Values')
    fpr('_'*(tc-4)+'\n\n')
    fpr('  id MAIL FROM  : %s' % dd['id'].get('mfrom'))
    fpr('  id HELO/EHLO  : %s' % dd['id'].get('helo'))
    fpr.info('  id PRA        : %s' % dd['id'].get('pra'))
    fpr('  Client IP     : %s' % dd.get('ip'))
    fpr('_'*(tc-4)+'\n\n')


    try:
        #if spfid == 'mfrom':
        qs = spf.query( i=dd.get('ip'),
               s=dd['id'].get('mfrom'),
               #s='',
               h=dd['id'].get('helo'),
               timeout=20, verbose=False, querytime=0
             )
        #if spfid == 'helo':
        qh = spf.query( i=dd.get('ip'),
            #   s=dd['id'].get('mfrom'),
               s='',
               h=dd['id'].get('helo'),
               timeout=20, verbose=False, querytime=0
             )

    except Exception,e: 
        fpr.err('Err: %s'%e)
        waitin()
        return

    SPF_IDS=[]
    if spfid == 'mfrom':
        if dd['id'].get('mfrom'):
            SPF_IDS.append(qs)
    if spfid == 'helo':
        if dd['id'].get('helo'):
            SPF_IDS.append(qh)
    if spfid == 'all':
        if dd['id'].get('mfrom'):
            SPF_IDS.append(qs)
        if dd['id'].get('helo'):
            SPF_IDS.append(qh)
        
    if not SPF_IDS:
        fpr.warn('Please set some of SPF values first !')



    res,code,expl = None,None,None

    for q in SPF_IDS:
   
        if q==qs:
            fpr.green('Processing MFROM identity')
            fpr('_'*(tc-4))
            local_part,domain = spf.split_email(s=dd['id'].get('mfrom'),h='')
        if q==qh:
            fpr.green('Processing HELO identity')
            fpr('_'*(tc-4))
            local_part,domain = spf.split_email(s='',h=dd['id'].get('helo'))
        print
        valid = False
        # if SPF Policy is defined manually skip DNS and use it
        if dd.get('policy'):
            fpr('Policy origin: INPUT\n\n')
    
            fpr.green('%s' % dd['policy'])
            print
    #        spfmech(dd['policy'],q,1)
    #        print
            # if spf syntax bad 
            if spfmech(dd['policy'],q,0):
                res,code,expl = q.check(spf=dd['policy'])
                valid = True
            else:
                fpr.err("SPF mechanism validation has failed")
                #fpr('%s,%s,%s,%s,%s' % (mech,m,arg,cidrlength,result))
         
    
        else:
            fpr('Policy origin: DNS/TXT RR\n\n')
            try:

                txt = q.dns_spf(domain)
                if txt:
                    fpr('_'*(tc-4))
                    print
                    fpr.green('%s\n' % txt)
                    fpr('_'*(tc-4))
                else:
                    fpr('_'*(tc-4))
                    print
                    fpr.err('SPF record not found or more than one record found')
                    fpr('_'*(tc-4))
                if dd.get('ip'):   
                    res,code,expl = q.check()
                    valid = True
                else:
                    print
                    fpr.warn('Verification skipped. Missing client IP address!')
            except spf.TempError,e:
                fpr.err('Error: %s' % e) 
        print
        if not valid:
            fpr.fail('SPF policy validation')
            return
    
        fpr.ok('SPF policy validation')
        print 
    
        fpr('SPF Verification result')
        fpr('_'*(tc-4)+'\n\n')
        fpr.info('%s,%s,%s' % (res,code,expl) )
    
        print
        fpr('SPF status  : %s' % res)
        fpr.info('SPF code    : %s ' % code)
        fpr('SPF info    : %s' % expl)
        fpr('_'*(tc-4)+'\n\n')
    
        """
         |  get_header(self, res, receiver=None, header_type='spf', aid=None, **kv)
         |      Generate Received-SPF or Authentication Results header based on the
         |       last lookup.
         |
         |      >>> q = query(s='strong-bad@email.example.com', h='mx.example.org',
         |      ...           i='192.0.2.3')
         |      >>> q.r='abuse@kitterman.com'
         |      >>> q.check(spf='v=spf1 ?all')
         |      ('neutral', 250, 'access neither permitted nor denied')
         |      >>> q.get_header('neutral')
        """
    
    #    if False:
        if res:
    
            if dd.get('receiver'):
                q.r=dd.get('receiver')
    
            
            fpr('_'*(tc-4)+'\n\n')
            # return header value
            header = q.get_header(res, header_type='spf',  aid=dd.get('authserv-id','UNKNOWN'))
            fpr('Received-SPF: %s' % header)
    
    
            # the ID of the authentication server, a token known as an authserv-id
            fpr('_'*(tc-4)+'\n\n')
            try:
                import authres
                # return header-name: header-value
                header = q.get_header(res, header_type='authres', aid=dd.get('authserv-id','UNKNOWN'))
                fpr('%s' % header)
            except ImportError:
                dbginfo('warrning','Warrning: Missing module: authres. Use: pip install authres')
    
            fpr('_'*(tc-4))
    
            #print q.check_lookups()
    
    
    """
        res,code,expl = spf.check(i=ip,s=mfrom,h=helo)
        fpr('%s,%s,%s' % (res,code,expl) )
    
    ## 
    
        res,expl = spf.check2(i=ip, s='liukebing@bcc.com', h='bmsi.com')
    
        fpr('%s,%s' % (res,expl) )
    """






# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def parse_spfHeaders2(h):

    from email.message import Message
    import re

    if not h:
       return False

    #print type(h)
    #print h

    #h1 = h.replace('\n','')
    #print h1

    # re.DOTALL '.'match everything inludinf newline
    # re.IGNORECASE is used at the splitHeaders() function first
    AUTHRE=re.compile('^(Authentication-Results):(.*)',re.DOTALL)
    RECSPF=re.compile('^(Received-SPF):(.*)', re.DOTALL)

    m1 = re.match(AUTHRE,h)
    m2 = re.match(RECSPF,h)

    if DDDEBUG:  fpr.purple(h)

    dd = { 'hn': '', 'hv': '' }


    #""" Authentication-Results """ 
    if m1: 
        dd['hn'] = m1.group(1)
        dd['hv'] = m1.group(2)
        
        fpr.info('_'*(tc-4))
        print
        fpr('Header-name  : %s' % m1.group(1))
        fpr('Header-value : %s' % m1.group(2))
        fpr.info('_'*(tc-4))
        print

        try:
            import authres

            # FIXME: fast workaround for authres module
            # 
            # remove "d=" tag from dmarc auth method as authres 
            # does recognize only below ptype
            # ->  elif ptype.lower() not in ['smtp', 'header', 'body', 'policy']
            # and it raise a Syntax error for d=
            h=h.replace('\n','')
            h=h.replace('\r','')
            h=h.replace('\t',' ')
            DTAG=re.compile('.*dmarc=.* \(.*\)* d=([a-z0-9\.\-]+)',re.IGNORECASE)
            md = re.match(DTAG,h)
            if md:
                fpr.warn('Stripping "d=" tag from dmarc method: d=%s' % md.group(1))
                #fpr.green( '%s ---- %s' % (md.group(1), md.group()))
                h = re.sub('d=%s'% md.group(1),'', h)
                if DDDEBUG: print h

            #else:
            #    print 'no d-tag'

            arh = authres.AuthenticationResultsHeader.parse(h)

            #if DDDEBUG:
            #  from pprint import pprint
            #  pprint(str(arh))

        except Exception,e:
            fpr.err('Exception: %s' % e)
             
        p = {}

        if str(arh.authserv_id):
            p['authserv_id'] = str(arh.authserv_id)

        print len(arh.results)
        for i in arh.results:

            if DDDEBUG:
                pprint(i)
                fpr('method: %s' %  str(i.method) )

            
            if str(i.method) == 'spf':
                p.setdefault('spf',{})
                p['spf'].setdefault('mailfrom',{})
                p['spf'].setdefault('helo',{})
                p['spf'].setdefault('pra',{})
                
                if DDDEBUG:
                    fpr('result        : %s' %  str(i.result) )
                    if hasattr(i,'smtp_mailfrom'): fpr('smtp.mailfrom : %s' %  str(i.smtp_mailfrom) )
                    if hasattr(i,'smtp_helo'): fpr('smtp.helo     : %s' %  str(i.smtp_helo) )
                    if hasattr(i,'smtp_pra'): fpr('smtp.pra      : %s' %  str(i.smtp_pra) )

                for j in i.properties:
                    if j.name == 'mailfrom':                     
                        p['spf']['mailfrom']['result'] = str(i.result)
                        p['spf']['mailfrom']['type'] = str(j.type)
                        p['spf']['mailfrom']['name'] = str(j.name)
                        p['spf']['mailfrom']['value'] = str(j.value)
                    if j.name == 'helo':                     
                        p['spf']['helo']['result'] = str(i.result)
                        p['spf']['helo']['type'] = str(j.type)
                        p['spf']['helo']['name'] = str(j.name)
                        p['spf']['helo']['value'] = str(j.value)
                    if j.name == 'pra':                     
                        p['spf']['pra']['result'] = str(i.result)
                        p['spf']['pra']['type'] = str(j.type)
                        p['spf']['pra']['name'] = str(j.name)
                        p['spf']['pra']['value'] = str(j.value)
                    if DDDEBUG:
                       fpr.green('  type: %s' %  str(j.type) )
                       fpr('  name: %s' %  str(j.name) )
                       fpr('  value: %s' %  str(j.value) )

            if str(i.method) == 'dkim':
                p.setdefault('dkim',{})
                p['dkim']['result'] = str(i.result)
                if DDDEBUG:
                    fpr('result        : %s' %  str(i.result) )
                    fpr('header_i      : %s' %  str(i.header_i) )
                for j in i.properties:
                    # dkim header identity
                    p['dkim']['header_i']=str(j.value)                   
                    if DDDEBUG:
                        fpr.green('  type: %s' %  str(j.type) )
                        fpr('  name: %s' %  str(j.name) )
                        fpr('  value: %s' %  str(j.value) )
                
            if str(i.method) == 'dmarc':
                p.setdefault('dmarc',{})
                p['dmarc']['result'] = str(i.result)
                if DDDEBUG:
                    fpr('result        : %s' %  str(i.result) )


        p['h_value'] = dd['hv']
        return p


    #""" Received-SPF """ 
    if m2: 
        dd['hn'] = m2.group(1)
        dd['hv'] = m2.group(2)
        
        fpr.info('_'*(tc-4))
        print

        fpr('Header-name  : %s' % m2.group(1))
        fpr('Header-value : %s' % m2.group(2))

        fpr.info('_'*(tc-4))
        print

    try:
        msg = Message()
        msg.add_header(dd['hn'], dd['hv'])
        p = {}
        MRES = re.compile('(.*)\s+\((.*)\)(\s+(.*))*',re.DOTALL)

        """ Received-SPF header value """
        def v_check(k,p,v):
            if k == 'client-ip':  p['client-ip'] = v
            elif k == 'client_ip':  p['client-ip'] = v
            elif k == 'envelope-from': p['envelope-from'] = v
            elif k == 'helo': p.setdefault('helo',v)
            elif k == 'receiver': p['receiver'] = v
            elif k == 'problem': p['problem'] = v
            elif k == 'mechanism': p['mechanism'] = v
            elif k == 'identity': p['identity'] = v
            elif k.startswith('x-'): 
               if 'x' in p:
                    p['x'][k] = v
               else:
                    p.setdefault('x',{k:v})


        if not dd['hn'] == 'Received-SPF':
            return

        for k,v in msg.get_params(header=dd['hn']):
            if DDDEBUG:  fpr.warn('k=%s,v=%s'% (k,v))
          
            mr = re.match(MRES,k)
            if mr: 
                if mr.group(1).lower() in spf.RESULTS.keys():
                    #fpr.green('%s' % mr.group(1))
                    p['result'] = mr.group(1)
                if mr.group(2):
                    #fpr.blue('%s' % mr.group(2))
                    p['explanation'] = mr.group(2)
                if mr.group(3):
                    #fpr.err('%s' % mr.group(4))
                    v_check(mr.group(4),p,v)     
            else:
                v_check(k,p,v)

        p['h_value'] = dd['hv']
        return p

    except Exception,e: 
        fpr.err('Error: %s' % e)


# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def parse_spfHeaders(h):

    if h:
        print h
        try:
            q = spf.query('0.0.0.0','','')
            q.mechanism = 'unknown'

            p = q.parse_header(h)
            ph = q.get_header(q.result,**p)
          
            print 
            print p['identity']
            fpr.blue( str(p) )
            fpr.warn( str(ph) )


        except Exception,e:
            fpr.err("Error: %s" % e)


# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def splitHeaders(inputs,crlf=False):

    #TODO: split headers and parse one header per 

    import email

    bancls()    
    print 
    fpr.warn('_'*(tc-4))
    print
    print inputs
    print 
    fpr.warn('_'*(tc-4))
    print
    print '\r\n'.join(inputs) 
    print 
    fpr.warn('_'*(tc-4))
    print
    waitin()
    bancls()


    if crlf:
        # remove empty elements from list
        # no newlines are allowed between headers
        inputs = [x for x in inputs if x != '']

    msg = email.message_from_string('\r\n'.join(inputs))


    AUTHRE=re.compile('Authentication-Results',re.IGNORECASE)
    RECSPF=re.compile('Received-SPF', re.IGNORECASE)

    hh = {
      'Received-SPF': list(),
      'Authentication-Results': list(),
    }

    parser = email.parser.HeaderParser()
    headers = parser.parsestr(msg.as_string())

    for hn,hv in headers.items():
        if DDDEBUG: fpr.green('Found: %s\n%s' % (hn,hv))
        m1 = re.match(AUTHRE,hn)
        m2 = re.match(RECSPF,hn)
        if m1:
            if DDDEBUG: print hn,hv
            hh['Authentication-Results'].append(hv)

        if m2:
            if DDDEBUG: print hn,hv
            
            hh['Received-SPF'].append(hv)

 
#    print "---------------------------------"
#    from pprint import pprint
#    pprint(hh)
#    print "---------------------------------"
#    print
      
    #build a list
#    print len(hh['Received-SPF'])
#    print len(hh['Authentication-Results'])


    pp = {
      'Received-SPF': dict(),
      'Authentication-Results': dict(),
    }
    for hn in ['Received-SPF','Authentication-Results']:
        x = 0
        for h in hh[hn]:
            p = parse_spfHeaders2('%s: ' % hn + h)
            if DDDEBUG: pprint(p)
            pp.setdefault(hn,x)
            x += 1
            pp[hn].setdefault(x,p)



    print "---------------------------------"
    pprint(pp)
    print "---------------------------------"
    return pp
        

# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #

def get_spfHeaders():


    fpr('Please provide your input')
    fpr('Use Ctrl-D with new line to continue.')
    print 
    fpr.info('_'*(tc-4))
    print
    inputs = get_inputs(nl=True)
    fpr.info('_'*(tc-4))
    
    if inputs:
        #dbglog(inputs)
        #inputs = [x.lstrip() for x in inputs]
        return splitHeaders(inputs,crlf=True)
#        parse_spfHeaders2(''.join(inputs).rstrip())
        

# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #

def list_spfHeaders(sh):


    if len(sh['Received-SPF'].keys()):
        fpr('Received-SPF Headers:')
           
        for h in sh['Received-SPF'].values():
             #print h
             fpr('_'*(tc-4))
             print

             #fpr('Header # %s' % )
             fpr('Result:            : %s' % h.get('result'))
             fpr('Explanation        : %s' % h.get('explenation'))
             fpr(' receiver          : %s' % h.get('receiver'))
             fpr(' client IP         : %s' % h.get('client-ip'))
             fpr(' identity          : %s' % h.get('identity'))
             fpr(' envelope-from     : %s' % h.get('envelope-from'))
             fpr(' helo              : %s' % h.get('helo'))
             print
             if 'x' in h:
                 for x in h.get('x'):
                     fpr(' %s : %s' % (x,h['x'][x]))
             print
             fpr('%s' % h.get('h_value'))
             print
             fpr('_'*(tc-4))
             print
    
    if len(sh['Authentication-Results'].keys()):
        fpr('Authentication-Results Headers:')
        for h in sh['Authentication-Results'].values():
             fpr('_'*(tc-4))
             print
             fpr('SPF values')
           
             for s in h['spf'].values():
                 #print s
                 fpr(' Result     : %s ' % s.get('result') )
                 fpr(' Identity   : %s ' % s.get('name') )
                 fpr(' Value      : %s ' % s.get('value') )
                 print
             fpr('%s' % h.get('h_value'))
             print
           
             fpr('_'*(tc-4))
             print
                         
        
        
    
    
 
# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #

def setSPFvalues(deauth,sh,x):
# deauth - dictionary with current SPF values
# sh - dictionary with parsed headers
# xhv - header number

    def cldeauth(death=deauth):
        del deauth['spf']
        deauth.setdefault('spf',dict( {'id': {'mfrom': '', 'helo': '', 'pra': '' }, 'ip': None} ) )

    from pprint import pprint
    from core.func import get_single_input
    n = 0
    for i in sh:
        #fpr("%s" % i)
        for j in sh[i]:
            n += 1
            if n == x: 
#               pprint(sh[i][j])
                if i == 'Received-SPF':
                    if sh[i][j].get('identity') == 'mailfrom':
                        cldeauth()
                        deauth['spf']['id']['mfrom'] = sh[i][j].get('envelope-from')
                        deauth['spf']['ip'] = sh[i][j].get('client-ip')
                    # x-sender - container of helo value (Cisco ESA)
                    if sh[i][j].get('identity') == 'helo':
                        cldeauth()
                        if sh[i][j].get('x'):
                            deauth['spf']['id']['helo'] = sh[i][j]['x'].get('x-sender')
                        deauth['spf']['ip'] = sh[i][j].get('client-ip')

                if i == 'Authentication-Results':
                    if sh[i][j].get('spf'):
                        if sh[i][j]['spf'].get('helo') and sh[i][j]['spf'].get('mailfrom'):
                            fpr('The Authentication-Results store more than one SPF identity')
                            fpr('Choose identity:')
                            print
                            fpr(' 1) mailfrom') 
                            fpr(' 2) helo') 
                            fpr.info(' 3) pra') 
                            x = get_single_input( '', '')

                            if x == '1':
                                 cldeauth()
                                 deauth['spf']['id']['mfrom'] = sh[i][j]['spf']['mailfrom'].get('value')
                            if x == '2':
                                 cldeauth()
                                 deauth['spf']['id']['helo'] = sh[i][j]['spf']['helo'].get('value')
         

    #from core.msg.viewers import viewers
    bancls()
    import core.msg.viewers as viewers
    viewers.viewSPFvalues(deauth['spf'])
    fpr.ok('SPF values has been set')

    if DDDEBUG: pprint(deauth)
 
