# --------------------------------------------------------------------------- #
# http://stackoverflow.com/questions/3305287/python-how-do-you-view-output-that-doesnt-fit-the-screen

class Less(object):

    def __init__(self, num_lines):
        self.num_lines = num_lines

    def __ror__(self, text):

        if True:
            if type(text) is not str:
                s = str(text)
                #print type(s)
                #print type(text)
                #print s
                print
                self.syspager(s)
            else:
                self.syspager(text)
 
        else:
            s = str(text).split("\n")
            for i in range(0, len(s), self.num_lines):
                print "\n".join(s[i:i+self.num_lines])
                if raw_input("Press <Enter> for more") == 'q':
                    break


    # some other tricks aka less
    #def fun2(self, text):
    #    import pydoc
    #    pydoc.pager(text)

    #def fun3(self, text):
    #    help(text)

    # call a system less
    def syspager(self,text):

        import subprocess
        import sys

        # -N
        # -R
        # -S
        # -X
        # -K
        # -F
        # -C

        try:
            pager = subprocess.Popen(['less', '-R', '-S', '-X',], 
                                       stdin=subprocess.PIPE, stdout=sys.stdout)
            #pager = subprocess.Popen(['less', '-F', '-R', '-S', '-X', '-K'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            #for num in range(1000):
            #    pager.stdin.write('This is output line %s\n' % num)
            try:
                pager.stdin.write(text)
                pager.communicate()
                pager.stdin.close()
                pager.wait()
            except IOError as e:
                pass
        except KeyboardInterrupt:
        # let less handle this, -K will exit cleanly
            pass


