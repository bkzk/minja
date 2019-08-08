from core.data import fpr,tr,tc,DEBUG,VERSION,AUTHOR,MAIL,COPYDATE
def infos(op):


   if op == 'help':
      fpr('Building a help and documentation is always the most time consuming task.' \
          'I have written a tool in such a way it should be a self explanatory in ' \
          'most cases. Although one of the goal of using this tool is to learn how ' \
          'an SMTP protocol and email authentication features works, I would like to ' \
          'include additional help for each of the submenu this tool shares.\n' \
          'Let\'s see how this will work.')
      print
      fpr('Feedback! I really appreciate all feedbacks, so please feel free to mail me!')

   if op == 'license':
       fpr("""
#########################################################################
# Copyright (C)  %9s   Bartosz Kozak                              #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 2 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#########################################################################
       """ % COPYDATE,adj='c')
   if op == 'about':
       fpr.white('minja version: %s written by %s %s' % (VERSION,AUTHOR,MAIL))

