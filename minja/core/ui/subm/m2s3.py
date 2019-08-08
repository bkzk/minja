import core.ui.menu as menu
import core.msg.viewers as viewers
import core.msg.builder as builder
import core.msg.utils as mutils

from core.data import smtp, fpr, tc, tr, DEBUG
from core.func import get_single_input, get_yesno_input, waitin, dbginfo, info
from core.ui.cmenu import Menu
from core.ui.banner import banner, bancls
  


def m2s3_rcptlist():             
    while True:
        bancls()
        m2s3_menu = Menu(menu.m2s3)
        #menu: return
        if m2s3_menu.op == '':
           break
        #menu: m2s3s1 - Set single recipient
        if m2s3_menu.op == '1':
           bancls()
           a = smtp['addrlist']['rcpt_to'] 
           smtp['addrlist']['rcpt_to'] = get_single_input(
                'Please set single RCPT TO (Envelope Recipient):', smtp['addrlist']['rcpt_to']
           )
           b = smtp['addrlist']['rcpt_to']
           if DEBUG: fpr('old: %s\nnew: %s' % (a,b)) 
           def upsingleRecipient(items, a, b):
               if not b:
                  if a and a in items:
                      #return [b if x == a else x for x in items]
                      # remove a - old 
                      items.remove(a)
                  return items
               if a and a in items: 
                   return [b if x == a else x for x in items]
               else:
                  #print a, 'not in ', items
                  items.insert(0,b)
                  #print items
                  return items
                  
 

           if DEBUG: print  smtp['addrlist']['rcpts'] 
           smtp['addrlist']['rcpts'] = upsingleRecipient( smtp['addrlist']['rcpts'],a,b)
           if DEBUG: print  smtp['addrlist']['rcpts'] 
           waitin()
        #menu: m2s3s2 - Build list from headers [To:, Cc:, Bcc:]
        if m2s3_menu.op == '2':
           while True:
             bancls()
             m2s3s2_menu = Menu(menu.m2s3s2)
             #menu: return
             if m2s3s2_menu.op == '':
                break
             if m2s3s2_menu.op in ['1','2','3','4']:
                bancls()
                # load func from msg.builder
                builder.rcpt_builder(m2s3s2_menu.op)
                waitin()                              

            #waitin()
           
        #menu: m2s3s3
        if m2s3_menu.op == '3':
           pass
        #menu: m2s3s4
        if m2s3_menu.op == '4':
           pass
        #menu: m2s3s5
        if m2s3_menu.op == '5':
           pass
        #menu: m2s3s6 - Get Recipients from STDIN 
        if m2s3_menu.op == '6':
           bancls()
           builder.rcpt_builder_f_inputs()
           waitin()
                         
        #menu: m2s3s7
        if m2s3_menu.op in ['7','v']:
           bancls()
           fpr('Envelope Recipients')
           print
           viewers.viewMsg('envelope')
           if smtp['addrlist']['rcpts']:
              viewers.viewEnvelope()
           waitin()
        #menu: m2s3s8
        if m2s3_menu.op in ['8','f']:
           bancls() 
           mutils.flushRecipients()
           waitin()
        #menu: m2s3sHELP
        if m2s3_menu.op == '?':
           pass
