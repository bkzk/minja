from core.func import dbginfo

def flushRecipients():

    from core.data import smtp,fpr

    if raw_input('  Flush envelope recipients list [y/N]:> ') in ['y','Y']:
        if type(smtp['addrlist']['rcpts']) is list:
            del smtp['addrlist']['rcpts'][:]
        else:
            fpr.err('Err: rcpts is not a list !')
        smtp['addrlist']['rcpt_to'] = None
        fpr.info('Recipients were flushed !')

def flushMsgContent():

    from core.data import smtp,smpls,fpr

    if raw_input('  Flush message data part [y/N]:> ') in ['y','Y']:
        #print smtp
        for k in smtp['content'].keys():
            if type(smtp['content'][k]) is list:
                del smtp['content'][k][:]
            if type(smtp['content'][k]) is dict:
                smtp['content'][k].clear()
            if type(smtp['content'][k]) is str:
                smtp['content'][k] = ''
        for k in smpls.keys():
            if 'astat' in smpls[k]:
                smpls[k]['astat'] = 0 
        for k in smpls['zip'].keys():
            if type(smpls['zip'][k]) is dict:
                if 'astat' in smpls['zip'][k]:
                    smpls['zip'][k]['astat'] = 0
                #   print smpls['zip'][k]['astat']
        for k in smpls['zip-smpls'].keys():
            if type(smpls['zip-smpls'][k]) is dict:
                if 'astat' in smpls['zip-smpls'][k]:
                    smpls['zip-smpls'][k]['astat'] = 0


        # reset the custom mime settings
        smtp['use_mime'] = True

        #print smtp
        fpr.ok('Message data was flushed !')

def flushMsgHeaders():

    import re
    from core.data import smtp,fpr

    if raw_input('  Flush message headers [y/N]:> ') in ['y','Y']:
        for k in smtp['headers'].keys():
            if re.match('^h\d*_',k):
                h = re.match('^h\d*_(.*)$',k)
                #print (k,h.group(1)) #DEBUG
                del smtp['headers'][k]
        fpr.ok('Message headers were flushed !')

def flushDKIMHeaders():

    import re 
    from core.data import smtp,fpr

    if raw_input('  Flush attached DKIM-Signature headers and Private Key [y/N]:> ') in ['y','Y']:
        for k in smtp['headers'].keys():
            h = re.match('^(h\d*_DKIM-Signature)$',k)
            #if re.match('^h\d*_DKIM',k):
            if h:
                #print k
                #h = re.match('^h\d*_DKIM-Signature$',k)
                #if h:
                #print (k,h.group(1)) #DEBUG
                del smtp['headers'][k]
                fpr(' * %s flushed ' % h.groups())
        for k in range(smtp['sign']['dkim']['dstat']):
            if smtp['sign']['dkim'].get(k):
               smtp['sign']['dkim'].pop(k,None)
               fpr(' * Private Key #%s flushed ' % k)
        # if key in dict
        if smtp['sign']['dkim']['dstat'] in smtp['sign']['dkim']:
          # print 'POP'
           smtp['sign']['dkim'].pop(smtp['sign']['dkim']['dstat'],None)

        #smtp['sign']['dkim'].pop(smtp['sign']['dkim']['dstat'],None)
        smtp['sign']['dkim']['dstat'] = 0

        fpr.ok('DKIM-Signature headers were flushed !')
        fpr.ok('DKIM Private Keys were flushed')






def get_addresses(h,part=1):

    import email.utils

    if part:
        only_addr = []
       
        t = [] 
        if type(h) is str:
            t = email.utils.getaddresses([h])
        elif type(h) is list:
            t = email.utils.getaddresses(h)
            
        for (n,a) in t:
        #    print (n,a)
            if a:
                only_addr.append(a)
        return only_addr
    else:
        return email.utils.getaddresses([h]) 


def get_address_domain(addr):

    #from email.utils import parseaddr
    # return tuple of ('John S.',jsmith@domain.com')

    #from core.func import dbginfo
    #dbginfo('debug',str(addr))
    # get_addresses returns list not string
    addr = get_addresses(addr)
    dbginfo('debug',str(addr))

    if len(addr):
       if '@' in addr[0]:
          m = addr[0].split("@")
          if len(m):
            return m[1]
    return None



