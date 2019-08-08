import os
import socket
import datetime

from core.ui.cfpr import Fpr


DEBUG = False
VERSION = '1.0.0beta'
AUTHOR = 'Bartosz Kozak'
MAIL='<bakozak@cisco.com>'
COPYDATE='2016-2018'

# --------------------------------------------------------------------------- #
# initiate fancy print and update terminal size 
fpr = Fpr()
fpr.tsauto = 1
tc, tr = fpr.get_term_size() 
tc, tr = fpr.ts_auto_refresh()
# for dev time let's create a new print effect
fpr.off = fpr.info


# --------------------------------------------------------------------------- #
MAX_THREADS = 100
MAX_MSG_PER_TH = 500
MAX_RCPT_PER_MSG = 1000
MAX_CMD_PER_TH = 15
TH_DELAY = 1000
TH_TIMEOUT = 5000
# --------------------------------------------------------------------------- #
# hostname

#hostname = socket.gethostname()
hostname = socket.getfqdn()

# date
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d %H:%M")

# --------------------------------------------------------------------------- #
# envelope defaults
def get_login():
    try:
       import pwdi 
       return pwd.getpwuid(os.geteuid()).pw_name
    except ImportError:
       try:
           import getpass
           return getpass.getuser()
       except ImportError:
           return 'postmaster'

# DEFAULT VALUE
rcpt = os.environ.get('RCPTTO')
mfrom = os.environ.get('MFROM') or get_login()+'@'+hostname

#helo   = hostname
#sender = get_login() + '@' + hostname
# --------------------------------------------------------------------------- #
# dictionary of smtp settings & message contents
# --------------------------------------------------------------------------- #
smtp = {
# 'host': 'localhost',
# 'port': 25,
# 'user': '',
# 'pswd': '',
# 'mode': 'NoTLS',
# 'helo': hostname or '',
# 'mail_from': (get_login() + '@' + hostname) or '',
# 'mail_from': '',
# 'rcpt_to'  : rcpt or '',
# 'rcpts'    : [],
# 'rcptsref' : {},  # refused recipients


    # connecion
    'connect'  : {
               'hosts' : {
                       0 : {
                         'host': 'localhost',
                         'port': 25,
                         'smtp_auth_method': None,
                         'smtp_auth_user': '',
                         'smtp_auth_pass': '',
                         'tls_mode': 'NoTLS',
                         'helo': hostname or '',
                         #'iface': '',
                       },
               },
               #TODO: global proxy
               #'proxy' : {
               #        0 : {
               #          'proxy_host': '',
               #          'proxy_port': '',
               #          'proxy_type': '',
               #          'proxy_user': '',
               #          'proxy_pass': '',
               #        },
               #},
    },

    # address list
 
    'addrlist' : {
               'mail_from': mfrom or '',
               'rcpt_to'  : rcpt or '',
               'rcpts'    : [],
               'r_reject' : {},  # refused recipients
               'r_valid'  : {},
               #'senders'    : [],
               #'s_reject' : [],

    },
####
    # feature: smtp replay
    'replay'  : {
              'threads' : {
                    'delay': TH_DELAY,
                    'reals': {},
                      'ok' : [],
                    'fail' : [],
              },
    },
####
    # feature: smtp enumeration
    'dha'  : {
              'cmd': 'RCPT TO',
              'threads' : {
                    'delay': TH_DELAY,
                    'timeout': TH_TIMEOUT,
                    #'not': 1,
                    'reals': {},
                      'ok' : [],
                    'fail' : [],
              },
    },
#
### FIXME: use_mime ... ?
    'use_mime': True,
    # message
    'headers' : {},
    'content' : {
              'text'  : [],
              'html'  : [],
              'mal'   : {},
              'vof'   : {},
              'img'   : {},
              'zip'   : {},
              'att'   : {},
              'string': '',
# 'att'  : {
#          0: {
#               'b64' : [],   # OR 'raw' : [],
#               'h_Content-Type:':            '',
#               'h_Content-Disposition:       '',
#               'h_Content-Disposition:       '',
#               'h_Content-transfer-encoding: '',
#               'h_Content-Description:       '',
#             },
#          },
    },
    # signatures
    'sign': {
          'dkim': {
          'dstat': 0, 
          },
    },
}


# DEBUG EXAMPLE 
#smtp['h_To'] = 'friend@ciscolab.not, John Smith <john.smith@ciscolab.not>,"Smith, Jane" <jane.smith@ciscolab.not>'    
#smtp['h_Cc'] = 'duffy@ciscolab.not, Aleks <aleks@ciscolab.not>,"Jake, Smith" <jake@ciscolab.not>'    
#smtp['h_Bcc'] = 'bunny@ciscolab.not, Henry <henryh@ciscolab.not>,"Joe, Doe" <Joe@ciscolab.not>'    

# --------------------------------------------------------------------------- #
# settings
# --------------------------------------------------------------------------- #

#FIXME: run initial function to create workspace hierarchy

cfgs = {

  'cfg_path': os.environ['HOME']+'/.minja',
  'log_path': os.environ['HOME']+'/.minja/logs',
  'smpl_path': os.environ['HOME']+'/.minja/samples',
  'sess_path': os.environ['HOME']+'/.minja/session',
  'msgs_path': os.environ['HOME']+'/.minja/messages',
  'mparts_path': os.environ['HOME']+'/.minja/messages/mparts',
  'key_path': os.environ['HOME']+'/.minja/keys',
  # enable/disable smtp conversaton logs
  'conv_logs': 1,
  'editor'  : os.environ.get('EDITOR','vim'),
 
}

# --------------------------------------------------------------------------- #
# dictionary of samples
# --------------------------------------------------------------------------- #

smpls = {
   'spam'    : {
      'type' : 'text',
      'sval' : '',
     'astat' : 0,
          '1': {
               'sval' : '_',
                'val' : 'X_J_S_*_C_4_J_D_B_Q_A_D_N_1_._N_S_B_N_3_*_2_I_D_N_E_N_*_G_T_U_B_E_-_S_T_A_N_D_A_R_D_-_A_N_T_I_-_U_B_E_-_T_E_S_T_-_E_M_A_I_L_*_C_._3_4_X',
              'descr' : 'Generic Test of Unsolicited Bulk Email - GTUBE sample',
             },
          '2': {
               'sval' : '_',
                'val' : 'X_J_S_*_C_4_J_D_B_Q_A_D_N_1_._N_S_B_N_3_*_2_I_D_N_E_N_*_G_T_P_H_I_S_H_-_S_T_A_N_D_A_R_D_-_A_N_T_I_-_P_H_I_S_H_-_T_E_S_T_-_E_M_A_I_L_*_C_._3_4_X',
              'descr' : 'Generic Test of Phishing - GTPHISH sample',
             }
   },
   'virus'   : {
      'type' : 'text',
     'astat' : 0,
          '1': {
               'sval' : '_',
                 'val': 'X_5_O_!_P_%_@_A_P_[_4_\_P_Z_X_5_4_(_P_^_)_7_C_C_)_7_}_$_E_I_C_A_R_-_S_T_A_N_D_A_R_D_-_A_N_T_I_V_I_R_U_S_-_T_E_S_T_-_F_I_L_E_!_$_H_+_H_*_',
              'descr' : 'European Institute for Computer Antivirus Research - EICAR Sample',
             },
   },
   'mal' : {
      'type' : 'text',
     'astat' : 0,
          '1': {
               'type' : 'text',
               'sval' : '_',
               'val'  : 'h_t_t_p_:_/_/_m_a_l_w_a_r_e_._t_e_s_t_i_n_g_._g_o_o_g_l_e_._t_e_s_t_/_t_e_s_t_i_n_g_/_m_a_l_w_a_r_e_/',
              'descr' : 'Malicious Google URL',
             },
          '2': {
               'type' : 'text',
               'sval' : '_',
               'val'  : 'h_t_t_p_:_/_/_m_a_l_w_a_r_e_._w_i_c_a_r_._o_r_g',
              'descr' : 'Malicious WICAR URL: https://github.com/wicar/wicar.github.io',
             },

   },
   'dlp' : {
      'type' : 'text',
     'astat' : 0,
          '1': {
               'sval' : '',
               'val'  : 'Some Visa 4999999999999996',
              'descr' : 'Data Lose Prevention - Payment Card Industry (PCI) Violation Test',
             }
   },
   'vof'     : {
      'type' : 'b64',
  'mimetype' : 'application/octet-stream',
     'astat' : 0,
         '1' : {
                'val' : 'ESA VOF TEST is based on the name of this file not its content',
           'filename' : 'photo.voftest',
              'descr' : 'ESA VOF Sample',
             },
         '2' : {
               'type' : 'text',
               'sval' : '_',
                'val' : 'X_J_S_*_C_4_J_D_B_Q_A_D_N_1_._N_S_B_N_3_*_2_I_D_N_E_N_*_G_T_P_H_I_S_H_-_S_T_A_N_D_A_R_D_-_A_N_T_I_-_P_H_I_S_H_-_T_E_S_T_-_E_M_A_I_L_*_C_._3_4_X',
              'descr' : 'GTPHISH sample',
             } 
   },
   'img'     : {
      'type' : 'file',
  'mimetype' : 'image/jpeg',
     'astat' : 0,
          '1': {
                'val' : '',
           'filename' : cfgs['smpl_path']+'/bsdtest2.jpg',
              'descr' : 'Image Analysis Sample', 
                'url' : 'http://cisco.poligon.it/minja/samples/bsdtest2.jpg',
                'md5' : '9e59a88cbed02698008043d5f90cea06',
             },
   },
   'txt'     : {
      'type' : 'text',
     'astat' : 0,
          '1': {
                'sval' : '',
                'val'  : 'This is a generic test message generated with minja tool on %s' % hostname,
                'descr' : 'PLAIN Text Sample',
             },
   },
   'html'     : {
       'type' : 'html',
      'astat' : 0,
           '1': {
                 'sval' : '',
                 'val'  : """
<html>
   <head></head>
   <body>
     <p>This is a generic test HTML message generated with minja tool on 
        <b> """ + hostname + """ </b>
     </p>
   </body>
</html>
   """,
                'descr' : 'PLAIN HTML Sample',
             },
   },
   'userin'   : {
       'file' : '',
        'val' : '',
      'descr' : 'User INPUT',
      'astat' : 0,

   },
   'zip'     : {
      'type' : 'file',
   'content' : '',
  'filename' : 'minj.zip',
     'descr' : 'ZIP Sample',
     'astat' : 0,
   },
   'zip-smpls' : {
      'type' : 'file',
   'content' : '',
  'filename' : 'minj.zip',
     'descr' : '',
     'astat' : 0,
      'spam' : { 
                'astat': 0,
             },
   },
}

