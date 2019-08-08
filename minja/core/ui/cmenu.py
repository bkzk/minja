import os 
import re
import sys

from core.data import smtp,fpr,tc,tr,DEBUG
from core.func import utf8Term

class Menu:

    # return to menu utf8 sign 
    esign = b"\xE2\x8F\x8E" 

    prompt = '  []> '
    op = ''

    def __init__(self, menu):
        # set 
        self.menu = menu

        fpr( menu.get('head','Test Menu Options:') )

        if menu.get('info'):
            fpr.warn('_' * (tc-4) )
            print
            fpr( menu.get('info')  )
            fpr.warn('_' * (tc-4) )
        print

        #print menu

        opts = menu.get('opts',[])
        offs = menu.get('offs',[])

        #print offs

        for (i,o) in opts:
            #print (i,o)
            if i in offs:
                fpr.DFLT = fpr.GRAY
             
            if i == 'nl':
                print
            elif i == 'sep':
                fpr ('  %s' % o)
            elif i == 'txt':
                fpr ('  %s' % o)
            else:
                if not DEBUG and i in offs:
                   pass
                elif len(i) > 1:
                    fpr ('  %s)  %s' % (i,o))
                else:
                    fpr ('   %s)  %s' % (i,o))
            # reset tmp colour set
            fpr.DFLT = None

        print 
        if utf8Term():
           fpr("   %s   return or q to quit" % self.esign )  
        else:
           fpr("  Press Enter to return or q to quit" )  
        print
        #################################################################      
        self.op =  raw_input(self.prompt)
        if self.op in offs:
            if not DEBUG:
                self.op = ''
        if self.op in ['q','x', 'Q', 'X']:                                          
            print; fpr ('See You Later Alligator')                      
            sys.exit(0)
        if self.op == '':
            fpr ('Return to Main Menu')
            #sys.exit(0)
            #break
            return                                                                    
        else:                                                                  
            print  
        #################################################################      

        return



