from core.data import smtp,VERSION,AUTHOR,MAIL,COPYDATE


m = {
  'head': 'Choose the operation you want to perform:',
  'info': '',
  'opts': [
    #( '1',  'def SMTP Connection Settings'),
    #( '2',  'def SMTP Message and Envelope'),
    ( '1',  'SMTP Connection Settings'),
    ( '2',  'SMTP Message and Envelope'),
#    ('nl',''),
    #( '3',  'send/replay Message'),
    ( '3',  'SMTP Playground'),
#    ('nl',''),
    #('4',  'run analyses'),
    #('5',  'run diagnostics'),
    ('4',  'Analyses'),
    ('5',  'Diagnostics'),
    ('nl',''),
    ('6',  'Load/Save Session'),
    ('98',  'Load/Save Message'),
    ('nl',''),
    ('i','Help, License and About'),
  ],
  'offs': ['97','98'],

}

m1 = {
   'head': 'Define SMTP Connection Settings',
   'info': '',
   'opts': [

#      ('sep', '-- set Target Host   --'), 
#      ('nl',''),
      ('1', 'set SMTP Host'),
      ('2', 'set SMTP Port'),

#      ('nl',''),
#      ('sep', '-- set your identity  --'),
#      ('nl',''),
      ('3', 'set SMTP HELO/EHLO '),

#      ('nl',''),
#      ('sep', '-- Authentication --'), 
      ('nl',''),
      ('4', 'set SMTP AUTH Mechanism'),
      ('5', 'set SMTP Auth User'),
      ('6', 'set SMTP Auth Password '),

#      ('nl',''),
#      ('sep', '-- Encryption --'),
#TODO:
# Encryption Mode: STARTTLS/SMTPoSSL/NoTLS/SSL

      ('nl',''),
      ('7', 'set TLS Mode (STARTTLS)'),

      ('99', 'set SMTP over SSL  [port 465 - enable SSL from the beginning]'),

      ('99', 'set OpenSSL Cipher Suite'),
      ('99', 'set Client Certificate & PrivKey'),
      ('99', 'set CA Certificate(s)'),
 
      ('nl',''),
      ('99', 'set Proxy Server '),
      ('nl',''),
      ('9', 'view Connection settings '),
      ('nl',''),
      ('w', 'run Wizzard'),
      ('?', 'help '),
   ],
   'offs': ['sep','4','99','?'], 
}



m2 = {
   'head': 'Define SMTP Message Data Content and Headers, Helo and Envelope',
   'info': '',
   'opts': [
      ( '1','set HELO'),
      ( '2','set MAIL FROM      [ Envelope Sender ] '),
      ( '3','set RCPT TO        [ Envelope Recipient(s) ]'),
      ( '4','set DATA Headers   [ Subject, From, To, Cc, Bcc, .. ]'),
      ( '5','set DATA Content   [ Message Composer ]'),
 #     ( '6','set DATA Security  [ DKIM, S/MIME, PGP ]'),
      ( '6','set DATA Security  [ Encryption and Signature ]'),
      ('nl',''),
#      ('nl',''),
      ( '7','view Envelope'),
      ( '8','view Message headers'),
      ( '9','view Message body'),
      ('10','view Message structure'),
      ('11','view Message and Envelope'),
      ('nl',''),
      ('12','flush Envelope recipients'),
      ('13','flush Message body '),
      ('14','flush Message headers '),
      ('nl',''),
      ( '?','help '),
  ],
   'offs': ['?',], 
}

m3 = {
   'head': 'SMTP Playground',
   'info': '',
   'opts': [
      ('1','inject Message'),
      ('2','replay Message'),
#      ('nl',''),
      ('3','enumerate Recipients'),
      ('nl',''),
      ('4','view Connection settings'),
      ('5','view Message and Envelope '),
      ('6','view Results and Logs')
  ],
   'offs': ['sep','99'], 
}
### 


m4 = {
   'head': 'Message Analyses',
   'info': '',
   'opts': [

      ('1','load Message file [EML]'),
      ('2','view Message file [EML]'),
      ('nl',''),
      ('3','run Message parser'),

      ('nl',''),
      ('4','run SPF/SIDF verification'),
      ('5','run DKIM verification' ),
      ('6','run DMARC verification'),
  ],
   'offs': ['sep','6','7','99'], 
}


m4s2 = {
   'head': 'Message Analyses: Parser',
   'info': '',
   'opts': [
      ('txt','Choose content'),
      ('nl',''),
      ('1','parse content from body composer'),
      ('2','parse content from file '),
  ],
   'offs': ['sep'], 
}
m4s5 = {
   'head': 'Analyses: DKIM Verification',
   'info': 
     'DKIM Verification result is based on the found DKIM-Signature headers\n',
   'opts': [
      ('txt','Choose content'),
      ('nl',''),
      ('1','parse content from body composer'),
      ('2','parse content from file '),
  ],
   'offs': ['sep'], 
}

m4s4_ = {
   'head': 'Analyses: SPF/SIDF Verification',
   'info': 
     'SPF Verification results are based on SPF values parsed from Received-SPF: \n' \
     'or Authentication-Results: headers. Useful when SPF has already been run on\n' \
     'a trusted mail gateway. \n\n' \
     'Additionaly set manually require SPF values to get a verification result and\n' \
     'more specific information about the process.',
   'opts': [

      ('txt','Provide results based on:'),
      ('nl',''),
      ('1','parse SPF headers from body composer'),
      ('2','parse SPF headers from file '),
      ('3','parse SPF headers from input '),
      ('nl',''),
      ('4','set SPF values'),

  ],
   'offs': ['sep','1','2','3'], 
}

m4s4 = {
   'head': 'Analyses: SPF/SIDF Verification',
   'info': 
     'SPF Verification results are based on SPF values parsed from Received-SPF: \n' \
     'or Authentication-Results: header fields. \n\n' \
     'Additionaly define all required SPF values manually to proceed with the \n' \
     'verification process.',
   'opts': [
 
      ('txt','Get SPF values:'),
      ('nl',''),
      ('1','parse SPF headers from body composer'),
      ('2','parse SPF headers from file '),
      ('3','parse SPF headers from input '),
      ('nl',''),
      ('4','set SPF values'),
      ('nl',''),
      ('sep','--  Process SPF  --'),
      ('nl',''),
      ( '5','get SPF Policy             [retrieve policy via DNS TXT RR]'),
      ( '6','set SPF Policy             [define policy]'),
      ('nl',''),
      ( '7','view SPF values'),
      ( '8','view parsed SPF values'),
      ( '9','run SPF Verification       [verify Sender IP against SPF]'),
      ( '10','run SPF Validation         [validate SPF policy]'),
 
  ],
   'offs': ['sep','1','2'], 
}


m4s4s4_ = {
   'head': 'Analyses: SPF/SIDF Verification',
   'info': 
     'Provide manually require SPF values to get a verification result and\n' \
     'more specific information about the process.',
   'opts': [
      ('txt','Set values:'),
      ('nl',''),
      ( '1','set MAIL FROM identity     [Envelope Sender -  5321.MFROM]'),
      ( '2','set HELO/EHLO identity     [FQDN]'),
      ( '3','set PRA identity           [SIDF/fake spf=2.0 ] ** UNSUPPORTED **'),
      ( '4','set Client IP              [Sender IP]'),
      ( '5','set Receiver address       [Recipient email address]'),
      ('nl',''),
      ( '6','get SPF Policy             [retrieve policy via DNS TXT RR]'),
      ( '7','set SPF Policy             [define policy]'),
      ('nl',''),
      ( '8','view SPF values'),
      ( '9','run SPF Verification       [verify Sender IP against SPF]'),
      ('10','run SPF Validation         [validate SPF policy]'),
      ('nl',''),
#      ('99','view Verification results'),
#      ('99','generate SPF Headers'),
      

  ],
   'offs': ['sep','3','99'], 
}



m4s4s4 = {
   'head': 'Analyses: SPF/SIDF Verification',
   'info': 
     'Provide manually require SPF values to get a verification result and\n' \
     'more specific information about the process.',
   'opts': [
      ('txt','Set values:'),
      ('nl',''),
      ( '1','set MAIL FROM identity     [Envelope Sender -  5321.MFROM]'),
      ( '2','set HELO/EHLO identity     [FQDN]'),
      ( '3','set PRA identity           [SIDF/fake spf=2.0 ] ** UNSUPPORTED **'),
      ( '4','set Client IP              [Sender IP]'),
      ( '5','set Receiver address       [Recipient email address]'),
      ('nl',''),
      

  ],
   'offs': ['sep','3','99'], 
}


m4s4s4s9 ={
   'head': 'Analyses: SPF/SIDF Verification > SPF Sender Verification',
   'info': 
     'SPF Sender Verification tests client IP against SPF identities\n' \
     'according to RFC 7208 compliant library pyspf. \n' ,
   'opts': [

      ('txt','Choose identity:'),
      ('nl',''),
      ('1','MAIL FROM identity'),
      ('2','HELO/EHLO identity'),
      ('3','PRA identity'),
      ('4','ALL')
 
  ],
   'offs': ['sep','3'], 
}



m4s4s4s10 ={
   'head': 'Analyses: SPF/SIDF Verification > SPF Validation',
   'info': 
     'SPF Validation  process tests SPF record if it is syntactically correct \n' \
     'according to RFC 7208 compliant library pyspf. To present the whole path \n' \
     'this test additionally follow all "include" mechanisms using DNS query to \n' \
     'retrieve all external SPF policies.' ,
   'opts': [

      ('txt','Retrieves SPF records for the specified domain:'),
      ('nl',''),
      ('1','MAIL FROM identity'),
      ('2','HELO/EHLO identity'),
      ('3','PRA identity'),
 
  ],
   'offs': ['sep','3'], 
}





m5 = {
   'head': 'Diagnostics',
   'info': '',
   'opts': [
      ('1','run SMTP i-session'),
      ('2','run SSL/TLS check'),
      ('3','run SMTP commands check'),
#      ('3','run SPF/SIDF verification'),
#      ('4','run DKIM verification' ),
#      ('5','run DMARC verification'),
      ('nl',''),
      ('sep',' -- decoders & encoders --'),
      ('nl',''),
      ('6','dec Headers                     7)  enc Headers'),
      ('8','dec Base64                      9)  enc Base64'),
      ('10','dec uuencode                   11)  enc uuencode'),

#Content-Transfer-Encoding := "BASE64" / "QUOTED-PRINTABLE" / 
#                             "8BIT"   / "7BIT" / 
#                             "BINARY" / x-token 

#      ('9','dec '),
#      ('9','dec AUTH PLAIN'),
#      ('9','dec AUTH LOGIN'),
#      ('9','dec AUTH CRAM-MD5'),
      ('12','dec SMTP AUTH                  13)  enc SMTP AUTH'),
      ('nl',''),
      ('nl',''),
      ('99',' -- list generators --'),
      ('nl',''),
      ('14','fixed size list  [sort|random]'),
#      ('15','list before/behind attach '),
      
  


  ],
   'offs': ['sep','1','2','4','5','99','9','12','10','14','15'], 
}

m5s14 = {
   'head': 'Diagnostics: Fixed size list generator',
   'info': '',
   'opts': [
      ('1','set LENGTH'),
      ('2','set CHARS'),
      ('3','set ORDER'),
      ('nl',''),
      ('4','run Generator'),
      ('5','view List'),
      ('6','save List'),
      ('nl',''),

  ],
   'offs': ['sep'], 
}

m5s14s2 = {
   'head': 'Diagnostics: Fixed size list generator > Characters',
   'info': '',
   'opts': [
      ('1','lowercase letters       [a-z]'),
      ('2','uppercase letters       [A-Z]'),
      ('3','digits                  [0-9]'),
      #('4','special characters      [~`!@#$%^&*()_+-={}|[]\:";\'<>?,./]'),
      ('4','special characters      [~`!@#$%^&...]'),
      ('5','whitespace              [ ]'),
      ('6','minus sign              [-]'),
      ('7','underline sign          [_]'),
      ('8','dot sign                [.]'),
      ('nl',''),
      ('9','custom list             []'),

  ],
   'offs': ['sep'], 
}

m5s14s3 = {
   'head': 'Diagnostics: Fixed size list generator > Orders',
   'info': '',
   'opts': [
      ('1','set SORT ASC'),
      ('2','set SORT DSC'),
      ('3','set RANDOM'),

  ],
   'offs': ['sep'], 
}




m4s4_sh = {
   'head': '',
   'info': '',
   'opts': [

      ('1','list SPF Headers'),
      ('2','load SPF values'),
  
  ],
   'offs': ['sep'], 
}






mX = {
   'head': '',
   'info': '',
   'opts': [

  ],
   'offs': ['sep'], 
}

# m1 submenus: 
m1s4 = {
   'head': 'SMTP Authentication Mechanism',
   'info': '',
   'opts': [
      ('nl',''),
      ('sep',' -- Plaintext Mechanism --'),
      ('nl',''),
      ('1','PLAIN             [Base64 encoding]'),
      ('2','LOGIN             [Base64 encoding]'),
      ('nl',''),
      ('sep',' -- Non-plaintext mechanism --'),
      ('nl',''),

      ('3','CRAM-MD5          [Chalange-response authentication]'),
      ('4','DIGEST-MD5        [Digest access authentication]'),
      ('5','GSSAPI            [Generic Security Services - API]'),

  ],
   'offs': ['sep','1','2','3','4','5'], 

}


# m2 submenus:

m2s3 = {
   'head': 'Envelope Recipients',
   'info': '',
   'opts': [
#      ('sep',' -- define single line  -- '),
#      ('nl',''),
      ('1','Set single recipient'),
#      ('nl',''),
#      ('sep',' -- define recipients -- '),
      ('nl',''),
      ('2','Build list from Headers [To:, Cc:, Bcc:]'),
      ('3','Load from Text file'),
      ('4','Load from CSV file'),
      ('5','Load from DB'),
      ('6','Input'),
      ('nl',''),
      ('7','view Recipients'),
      ('nl',''),
      ('8','flush Envelope Recipients'),
      ('nl',''),
      ('?','help'),
                             
  ],
   'offs': ['sep','3','4','5','?'], 
}
                    
m2s3s2 = {
   'head': 'Envelope Recipients > Build List from Headers',
   'info': 
"""    If some recipients were defined with Cc, Bcc or To headers 
              you can use  them as envelope recipients.

    Note: By default all recipients from headers stays with the headers. 
          Header recipients are not envelope recipients. 
""",
   'opts': [
      ('txt','Choose header with addresses:'),
      ('nl',''),
      ('1','To:  '),
      ('2','Cc:  '),
      ('3','Bcc: '),
      ('4','All above'),
      ('nl',''),
      ('?','help'),
    
  ],
   'offs': ['sep','?'], 
}


m2s4_ = {
   'head': 'Message Headers',
   'info': 
"""   Choose one of the common header or run wizzard
   Note: A current date value is generated for every run!
   Type dot '.' to clear a value 
""",
   'opts': [

    ('sep', ' -- Originator Fields --'),
    ('nl', ''),
    ( '1', 'From:'),
    ( '2', 'Sender:'),
    ( '3', 'Return-Path:'),
    ( '4', 'Reply-To:'),

    ('nl', ''),
    ('sep',' -- Destination Address Fields --'),
    ('nl', ''),
    ( '5', 'To:'),
    ( '6', 'Cc:'),
    ( '7', 'Bcc:'),

    ('nl', ''),
    ('sep',' -- Information Field --'),
    ('nl', ''),
    ( '8', 'Subject:'),
    ( '9', 'Comment:'),

    ('nl', ''),
    ('sep',' -- The Origination Date Field --'),
    ('nl', ''),
    ('10', 'Date:'),
    ('11', 'X-Custom:'),

    ('nl',''),
    ('12', 'view Message headers '),
    ('w', 'run Wizzard'),
  ],
   'offs': ['sep','1','2','3','4','5','6','7','8','9','10','11','12'], 
}

m2s4 = {
   'head': 'Message Headers',
   'info': 
"""   Set one of the common message header or use wizzard
   Note: A current date value is generated for every run!
   Type dot '.' to clear a value 
""",
   'opts': [

    ('sep',' -- Originator Fields --        -- Destination Address Fields --'),
    ('nl', ''),
    ( '1', 'From:                           5)  To:  '),
    ( '2', 'Sender:                         6)  Cc:  '),
    ( '3', 'Return-Path:                    7)  Bcc: '),
    ( '4', 'Reply-To:'),

#    ('nl', ''),
#    ('sep',' -- Destination Address Fields --'),
#    ('nl', ''),
#    ( '5', 'To:'),
#    ( '6', 'Cc:'),
#    ( '7', 'Bcc:'),

    ('nl', ''),
    ('sep',' -- Information Field --       -- The Origination Date Field --'),
    ('nl', ''),
    ( '8', 'Subject:                       10)  Date:  '),
    ( '9', 'Comment:                       11)  X-Custom: '),

#    ('nl', ''),
#    ('sep',' -- The Origination Date Field --'),
#    ('nl', ''),
#    ('10', 'Date:'),

    ('nl',''),
    ('12', 'view Message headers '),
    ('w', 'run Wizzard'),
  ],
   'offs': ['sep'], 
}




m2s5 = {
  'head': 'Message Body Composer',
  'info': 
""" Feel free to use one of predefined sample to test your mail flow policies 
        or compose your own text message or include your own files
""",
  'opts': [
    ('sep', ' -- define new body or content parts --'),
    ('nl', ''),
    ( '1', 'build custom Body Contents '),
    ( '2', 'load  custom Attachment '),
    ('nl', ''),
    ('sep', ' -- attach predefined samples --'),
    ('nl', ''),
    ( '3', 'attach SPAM         [ GTUBE sample ]'),
    ( '4', 'attach VIRUS        [ EICAR sample ]'),
    ( '5', 'attach MALWARE      [ MALWARE sample ]'),
    ( '6', 'attach DLP          [ DLP-PCI sample ]'),
    ( '7', 'attach VOF          [ VOF sample ]'), # Virus Outbreak Filters
    ( '8', 'attach IMG          [ Image Analysis sample ]'),
    ( '9', 'attach TEXT         [ Generic Plain/Text sample ] '),
    ('10', 'attach HTML         [ Generic Plain/HTML sample ] '),
    ('nl', '' ),
    ('11', 'attach ZIP parts    [ ZIP attachment ] '),
    ('nl', '' ),
    ('12', 'view Message body'),
    ('13', 'edit Message body' )

   ],
   'offs': ['sep'],
}


m2s5s1 ={
   'head': 'Build custom Body Contents' ,
   'info': '',
   'opts': [

      ('sep','-- define holistic body content --'),
      ('nl',''),
      ('1','compose custom Body Content      [ input ]'),
      ('2','compose custom Body Content      [ editor ]'),
      ('3','load raw content                 [ eml file ]'),
      ('nl',''),
      ('sep','-- attach custom MIME part --'),
      ('nl',''),
      ('4','attach custom text content       [ plain/text ]'),
      ('nl',''),
  ],
   'offs': ['sep'],
}

m2s5s2 = {
   'head': 'Define new attachment(s)' ,
   'info': '',
   'opts': [
      ('1','load file '),
      ('2','paste encoded file (base64)'),
  ],
   'offs': ['sep'], 
}


m2s5s11 = {
   'head': 'Message Body Composer',
   'info': '',
   'opts': [
      ('txt','Choose one of predefined sample to Zip and attach: '),
      ('nl',''),
      ('sep',' -- zip predefined samples --'),
      ('nl',''),
      ( '1','zip SPAM  Sample  [ GTUBE Sample ]'),
      ( '2','zip VIRUS Sample  [ EICAR Sample ]'),
      ( '3','zip MALWARE Sample'),
      ( '4','zip DLP  Sample   [ DLP-PCI Sample ]'),
      ( '5','zip VOF  Sample   [ ESA photo.voftest ]'),
      ( '6','zip IMG  Sample   [ ImA ]'),
      ( '7','zip TXT  Sample   [ Basic TEXT Sample ]'),
      ( '8','zip HTML Sample   [ Basic HTML Sample ]'),
      ('nl',''),
      ('sep','  -- zip new data --'),
      ('nl',''),
      ( '9','zip input TEXT'),
      ('10','zip loaded ATT (raw-only)'),
      ('11','zip new ATT (load and zip it)'),
      ('nl',''),
      ('?','help'),
 
  ],
   'offs': ['sep','3','10','?'], 
}

m2s6 = {
   'head': 'Message Body Security',
   'info': '',
   'opts': [
      ('txt','Choose one of the method:'),
      ('nl',''),
#      ('sep',' -- --'),
      ('1',' DKIM Signature'),
      ('2',' S/MIME'),
      ('3',' PGP/GPG'),

  ],
   'offs': ['sep','2','3'], 
}


m2s6s1 = {
   'head': 'Message Body Security: DKIM Signing',
   'info': 'DomainKey Identified Mail',
   'opts': [
      ('txt','Choose one::'),
      ('nl',''),
#      ('sep',' -- --'),
      ('1','set DKIM Private Key    [PKCS#1 priv key in base64 encoded form]'),
      ('2','set DKIM-Signature      '),
      ('nl',''),
      ('3','view DKIM Signatures'),
      ('4','flush DKIM Signatures & Private Keys'),

  ],
   'offs': ['sep'], 
}


m2s6s1s1 = {
   'head': 'DKIM private key',
   'info': 'Load DKIM private key in PKCS#1 base64 encoded form',
   'opts': [
      ('1','load from input'),
      ('2','load from file'),
      ('nl',''),
      ('3','view Private Key(s)'),

  ],
   'offs': ['sep'], 
}


m2s6s1s2 = {
   'head': 'DKIM-Signature',
   'info': 'RFC 4871',
   'opts': [
      ('txt','Choose tag:'),
      ('nl',''),
      ('1','version           v=  [1]'),
      ('2','algorithm         a=  [rsa-sha256]'),
      ('3','canonicalization  c=  [relaxed/simple]'),
      ('4','selector          s=  []'),
      ('5','domain            d=  []'),
      ('6','headers           h=  [from : to : subject]'),
#      ('6','timestamp         t='),
      ('7','identity          i=  []'),
      ('8','length            l=  None'),
      ('nl',''),
      ('sep','-- --'),
      ('nl',''),

      ( '9','view Canonicalized Message'),
      ('10','view Tags & Signature'),
      ('11','flush Tags & Signature'),
      ('12','generate Signature'),
      ('13','attach Signature'),
      ('nl',''),
      ('w','run Wizzard'),
  ],
   'offs': ['sep','1','2','w'], 
}





m2s6s1s2s1 = {
   'head': 'DKIM-Signature > Headers sign',
   'info': 'List of header names need to be lowercased and separated by colon',
   'opts': [
      ('txt','Choose headers group:'),
      ('nl',''),
      ('1','set default headers    [from : to : subject]'),
      ('2','set new headers '),
#      ('nl',''),
  ],
   'offs': ['sep'], 
}




mX = {
   'head': '',
   'info': '',
   'opts': [

  ],
   'offs': ['sep'], 
}

# m3:

m3s2 = {
   'head': 'SMTP Replay',
   'info': 
"""                          Multithread Mailer
                                 or
                --- (SPAM load, DHA and DoS tester) --- """,
   'opts': [
      ('1','set THREADS             [ number of separate connections ]'),
      ('2','set RATES & LIMITS      [ number of msg or rcpt / thread ]'),
      ('3','set INTERFACE(S)        (feature*)'),
      ('4','set RELAYS              (define additional host ? )'),
      ('5','set PROXY               (define SOCKS/HTTP proxy servers)'),
      ('nl',''),
#      ('x', 'set DHA MODE      [log return code RCPT TO]'),
      ('nl',''),
      ('6','view Connection settings'),
      ('7','flush sets'),
      ('nl',''),
      ('8','run Threads       (Lets magic begin %*!@#$)'),
      ('nl',''),
 #     ('9','view logs'),
      ('nl',''),
      ('?','help'),

  ],

  'offs': ['3','4','5','?','x'], 
}

m3s2s2 = {
   'head': 'SMTP Replay: Rates and Limits ',
   'info': '',
   'opts': [

      ('txt','Set rates and limits:'),
      ('nl',''),
      ('sep',' -- def Limits -- '),
      ('nl',''),
      ('1','set RPM   [ number of Recipients Per Message ]'),
      ('2','set MPT   [ number of Messages Per Connection ]'),
      ('nl',''),
      ('sep',' -- def Rates/Intervals -- '),
      ('nl',''),
      ('3','set RATE  [ number of Recipients Per Hour / Minute / Second ]'),
      ('4','set DELAY [ delay between threads (connections) ]'),
                                 
  ],
   'offs': ['sep','3'], 
}


m3s3 = {
   'head': 'SMTP Enumeration',
   'info': '                         SMTP Enumeration / DHA  ',
   'opts': [

#      ('sep','-- def Userlist --'),
      ('nl',''),
      ('1','set USERSLIST           [ envelope Recipients]'),
#      ('nl',''),
      ('2','set METHOD              [ VRFY, EXPN, RCPT TO ]'),
#      ('nl',''),
      ('3','set THREADS'),
      ('4','set CPT                 [ number of CMD per Thread (connection) ]'),
      ('5','set TIMEOUT             [ query timeout ]'), # timewait ile czekac na odpowiedz
      ('6','set DELAY               [ delay between threads (connections) ]'),
      ('nl',''),
      ('7','view Connection settings'),
      ('8','flush settings'),

      ('nl',''),
      ('9','run Enumeration'),
      ('nl',''),
#      ('99','run SMTP Enumerate'),

  ],
   'offs': ['sep','99'], 
}
#???????????

m3s3s1 = {
   'head': 'SMTP Enumeration: Userlist',
   'info': '',
   'opts': [
      ('sep','--  --'),
      ('nl',''),

      ('1','set DOMAIN'),
      ('2','load  Userlist'),
      ('3','build Userlist'),
#      ('sep','--  --'),

  ],
   'offs': ['sep','1','2','3'], 
}


m3s3s1s2 = {
   'head': 'SMTP Enumeration: Userlist > Load Userlist',
   'info': '',
   'opts': [
      ('1','load data from file'),
      ('2','load data from input'),
  ],
   'offs': [''], 
}


m3s3s1s3 = {
   'head': 'SMTP Enumeration: Userlist > Build Userlist',
   'info': 'Generate a list of local parts names using custom criteria',
   'opts': [
      ('1','set LENGTH'), #up to X or a range between X-Y
      ('2','set CHARACTERS TYPE'), # only lower/only upper letters and/or numbers , special characters like [-+.=]
      ('nl',''),
      ('sep','--  --'),
      ('nl',''),
      ('3','view LIST'),
      ('4','save LIST'),
  ],
   'offs': ['sep','1','2','3','4'], 
}



m3s3s2 = {
   'head': 'SMTP Enumeration: SMTP Method Command',
   'info': '',
   'opts': [
      ('txt','Current method: %s' % smtp['dha'].get('cmd')),
      ('nl',''),
      ('txt','Choose one of SMTP Commands'),
      ('nl',''),
      ('1','EXPN'),
      ('2','VRFY'),
      ('3','RCPT TO'),
  ],
   'offs': [''], 
}








m3s6 = {
   'head': 'View logs',
   'info': '',
   'opts': [
 #     ('nl',''),
      ('1','Addresses Refused'),
      ('2','Addresses Accepted'),
      ('nl',''),

  ],
   'offs': ['sep'], 
}

m5s8 = {
   'head': 'Diagnostics: Base64 decoder',
   'info': 'Load or paste a Base64 encoded content. Decoded results will be a raw data  for non text encoded content and can be saved as a seperate file or viewed.',
   'opts': [
      ('nl',''),
      (' 1','load Base64 content from file'),
      (' 2','load Base64 content from input'),
      ('nl',''),
      (' 3','view decoded content '),
      (' 4','save decoded content '),
      ('nl',''),

  ],
   'offs': ['sep'], 
}

m5s9 = {
   'head': 'Diagnostics: Base64 encoder',
   'info': 'Load or paste content. Encoded base64 content can be saved as a seperate file or viewed.',
   'opts': [
      ('nl',''),
      (' 1','load content from file'),
      (' 2','load content from input'),
      ('nl',''),
      (' 3','view Base64 encoded content '),
      (' 4','save Base64 encoded content '),
      ('nl',''),

  ],
   'offs': ['sep'], 
}



m6 = {
   'head': 'Session management',
   'info': '',
   'opts': [
#      ('nl',''),
      ('1','Save session'),
      ('2','Load session'),
      ('nl',''),
      ('3','Save current session settings as default'),

  ],
   'offs': ['sep','3'], 
}


mX = {
   'head': '',
   'info': '',
   'opts': [

  ],
   'offs': ['sep'], 
}


mHelp = {
   'head': 'Help, License and About',
   'info': '\
DISCLAIMER: This software is for LEGAL testing purposes only.\n\n\
Copyright (C) %s %s %s\n' % (COPYDATE,AUTHOR,MAIL),

   'opts': [
      ('1','Help'),
      ('2','License'),
      ('3','About'),
#      ('nl',''),

  ],
   'offs': ['sep'], 
}






# --------------------------------------------------------------------------- #
# samples menus

sm_spam = {
  'head': 'SPAM Samples:',
  'info': 'Sample will be attached after you hit a number',
  'opts': [ 
     ('1','Spam GTUBE text sample    [ MIME text/plain ]'),  
     ('2','Phish GTPHISH text sample [ MIME text/plain ]'),  
  ],
}
 
sm_virus = {
  'head': 'Virus Samples:',
  'info': 'Sample will be attached after you hit a number',
  'opts': [ 
     ('1','Virus EICAR text sample   [ MIME text/plain ]'),  
  ],
}

sm_mal = {
  'head': 'Malware Samples:',
  'info': 'Sample will be attached after you hit a number',
  'opts': [ 
     ('1','Malicious Test Google URL [ MIME text/plain ]'),  
     ('2','Malicious Test WICAR URL  [ MIME text/plain ]'),  
  ],
}


sm_dlp = {
  'head': 'Data Loss Prevention Samples:',
  'info': 'Sample will be attached after you hit a number',
  'opts': [ 
     ('1','DLP PCI text sample       [ MIME text/plain ]'),  
  ],
}
 
sm_txt = {
  'head': 'Plain Text Samples:',
  'info': 'Sample will be attached after you hit a number',
  'opts': [ 
     ('1','Simple plain/text sample  [ MIME text/plain ]'),  
  ],
}
  
sm_html = {
  'head': 'Plain HTML Samples:',
  'info': 'Sample will be attached after you hit a number',
  'opts': [ 
     ('1','Basic HTML sample         [ MIME text/html ]'),  
     ('2','Basic HTML sample with URLS'),
  ],
  'offs': ['2']
}

  
sm_img = {
  'head': 'Image Analyses Samples:',
  'info': 'Sample will be attached after you hit a number',
  'opts': [ 
     ('1','Basic ImA sample          [ MIME image/jpeg ]'),  
  ],
  'offs': ['']
}

 
sm_vof = {
  'head': 'Cisco IronPort Virus Outbreak Filters Samples:',
  'info': 'Sample will be attached after you hit a number',
  'opts': [ 
     ('1','Basic VOF sample          [ MIME application/octet-stream ]'),
     ('2','Phish GTPHISH text sample [ MIME text/plain ]'),  
  ],
  'offs': ['']
}

