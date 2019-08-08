# --------------------------------------------------------------------------- #
# Load/Save Sessions
# --------------------------------------------------------------------------- #

import os
import base64
import glob
import json
from datetime import datetime

from core.data import smtp,cfgs,fpr,DEBUG
from core.func import info,dbginfo,dbglog,get_yesno_input,waitin

from pprint import pprint

# --------------------------------------------------------------------------- #
# dump smtp dict to file
# --------------------------------------------------------------------------- #
def dumpSession():
    info('info','Saved session allows to save current connection and message setting to be \n' \
                'useful with further tests, as a proof of successful test or used as template\n\n'\
                'Note: Session file can store sensitive data like SMTP authentication\n' \
                '      credential or private keys and certificate.',adj='l')

    print
    if not get_yesno_input('  Would you like to save your current session: [y/N]> '): 
        return
 
    print
    fpr('Session files are stored under the session subdirectory by default.\n' \
        'Please provide a full path if you would like to store you session somehere else.')

    sessfile ='minja-'+datetime.now().strftime('%Y%m%d%H%M%S')+'.session'

    print 
    sf = raw_input('  [%s]> ' % sessfile) or sessfile
    print    
 
    if sf == sessfile or not os.path.dirname(sf):
       sf =  cfgs['sess_path']+'/'+sf

    if os.path.exists(sf):
        fpr('Session file already exist')

    else:
        if os.access(os.path.dirname(sf), os.W_OK):
            #the file does not exists but write privileges are given
            fpr('Saving under %s\n' % sf)
            #import json

            dd = outSMTPdict(smtp)
            
            try:
               #f = codecs.open(sf, 'w', encoding='utf-8')
               f = open(sf, 'w')

               json.dump(dd, f, indent=3)

               fpr.ok('Session saving')
            except IOError as e:
               fpr.err('Saving file failed: %s' % e)
        else:
            fpr.fail('Missing write permission')    

# --------------------------------------------------------------------------- #
#
# --------------------------------------------------------------------------- #
def loadSession():

    print
    if not get_yesno_input('  Would you like to load saved session: [y/N]> '): 
        return
    print 
    fpr('Session files are stored under the session subdirectory by default.\n' \
        'Please provide a full path if you would like to load a session file from different location.')
    # get the latest file as default:
    print
    latest = max(glob.iglob( os.path.join(cfgs['sess_path'], '*.session')), key=os.path.getctime)
    if latest:
        fpr('Latest saved session is %s' %  os.path.basename(latest))

    print 
    sf = raw_input('  [%s]> ' % os.path.basename(latest)) or latest
    print    
    
    # if filename does not include path than search file in session dir  
    if not os.path.dirname(sf):
        sf =  cfgs['sess_path']+'/'+sf
    if os.path.exists(sf):
#        import json
        try:
            f = open(sf, 'r')
            # json loads 
            tmp = json.load(f)
            #from pprint import pprint
            #pprint(tmp)
            #TODO: test tmpe dict 
            x=0
            for k in tmp.keys():
                if k in ['connection', 'signatures','replay','content','headers']:
                      x+=1
            if x:        
                fpr.ok('Session file seems to be proper')
            else: 
                fpr.fail('Session file is not proper')
                return    
            # overwrite main SMTP dict 
            print '====='
            #smtp = {k:v for k,v in tmp.items()}
            for k,v in inSMTPdict(tmp).items():
                print k,v
                smtp[k] = v
            print '====='
            fpr.ok('Session load successful')
        except IOError as e:
            fpr.err('Loding session failed: %s' % e)
    else:
        fpr.err('Session file does not exist')




# --------------------------------------------------------------------------- #
# Search all raw data in nested dict and encode
#  r2b - raw to base64 - encode raw data to base64 
#  b2r - base to raw - decode base data to raw
# --------------------------------------------------------------------------- #
def findkeys(node, kv, r2b=False, b2r=False):
    if isinstance(node, dict):
        if kv in node:
            #print'-- inodekv1', node[kv]
            if r2b:
                node[kv] = base64.b64encode(node[kv])
            if b2r:
                node[kv] = base64.b64decode(node[kv])
            #print '-- inodekv',node[kv]
            
        for j in node.values():
            #print '------ j',j
            findkeys(j,kv,r2b,b2r)

# --------------------------------------------------------------------------- #
# replace string key to int key if key is a digit
# - JSON does not support key of int type
# --------------------------------------------------------------------------- #
# -- MOVED to 
#def keystrJSONint(d):
#
#    for k,v in d.items():
#        print "==",k,type(k)
#        if type(k) in [str,unicode] and k.isdigit():
#            print "==string==",k
#            d[int(k)] = d.pop(k)
#        if isinstance(v,dict):
#            print "==v-dict==",v
#            keystrJSONint(v)

# --------------------------------------------------------------------------- #
# convert unicode to string
# - JSON loads all string as unicode type
# FIXME: keep it like that for now
# --------------------------------------------------------------------------- #
def unJSONstr(d):

    for k,v in d.items():
        print '==kv==',k
        if type(k) is unicode:
            if k.isdigit():
                d[int(k)] = d.pop(k)
            else:
                d[str(k)] = d.pop(k)
        if type(v) is unicode:
            #print '==v=u=',d[k],type(d[k])
            d[k] = str(v)
            #print '==v=u=',d[k],type(d[k])
        if isinstance(v,list):
            #print '==v=lu=',d[k],type(d[k])
            for i,e in enumerate(v):
                if type(e) is unicode:
                    v[i] = str(e) 
        if isinstance(v,dict):
            #print'--'
            #print '== v = d =', v
            unJSONstr(v)
            #print'--'
         

    #pprint(d)
    #fpr.err('-'*40)

# --------------------------------------------------------------------------- #
# sanitaze loaded JSON data before saving them into smtp dict
# --------------------------------------------------------------------------- #
def inSMTPdict(din):

    # crate a copy 
    dd = dict()

    #FIXME: what about att stats from smpls dict  - astats -- ???

    # smtp connection settings: 
    dd.setdefault('connect',dict()).setdefault('hosts',dict()).setdefault(0,dict())
    dd['connect']['hosts'][0] = din['connection']
    # userlist settiings (senders and recipients) 
    dd['addrlist'] = din['addrlists']
    # signatures (dkim/s/mime/pgp)
    dd['sign'] = din['signature']
    # feature: smtp replay
    dd['replay'] = din['replay']
    # feature: enumeration 
    #dd..
    # global setting use_mime .. ?
    dd['use_mime'] = din['custom_mime']
    # headers:
    dd['headers'] = din['headers']

    # copy of messae content as it need to be modified before dumping
    dd['content'] = din['content'].copy()
    #dbglog(str(dd))

    # find all 'raw' keys and convert value using base64 decoder to raw value
    findkeys(dd,'raw',b2r=True)
    #dbglog(str(dd))

    # conver JSON loaded dict: 
    # - convert all unicode key and val for dict and lists in dict 
    # - conver all digit keys to int
    unJSONstr(dd)
    #keystrJSONint(dd)

    dbglog(dd)

    return dd

# --------------------------------------------------------------------------- #
# sanitize smtp dict before dumping it with JSON 
# --------------------------------------------------------------------------- #
def outSMTPdict(d):

    # crate a copy 

    dd = dict()


#FIXME:
# smpls - astats -- ?


    # smtp connection settings: 
    dd['connection'] = d['connect']['hosts'][0]

    # userlist settiings (senders and recipients) 
    dd['addrlists'] = d['addrlist']
 
    # signatures (dkim/s/mime/pgp)
    dd['signature'] = d['sign']
    
    # feature: smtp replay
    dd['replay'] = d['replay']
   
    # feature: enumeration 
    #dd..

    # global setting use_mime .. ?
    dd['custom_mime'] = d['use_mime']

    # headers:
    dd['headers'] = d['headers']


    # copy of messae content as it need to be modified before dumping
    dd['content'] = d['content'].copy()
    dbglog(str(dd))

    # find all 'raw' keys and convert value using  base64 encoders
    findkeys(dd,'raw',r2b=True)
    
#    import base64

#    for i in dd['content']:
#        for j in dd['content'][i]:
#            for k in dd['content'][i][j]:
#                if k == 'raw':
#                     print 'Found RAW'
#                     dd['content'][i][j][k] =  base64.b64encode( dd['content'][i][j][k] )

#    dd['content']['att'][1]['raw'] = base64.b64encode(dd['content']['att'][1]['raw'])

    dbglog(str(dd))

    return dd




