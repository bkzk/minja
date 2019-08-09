
<p align="center">
  <img src="https://raw.githubusercontent.com/bkzk/screens/master/minja/logo128.png">
</p>

**minja** - is a tool design to test email security policies, SMTP session, authentication mechanism, run stress tests, enumerate users and message analyze

- menu oriented CLI based tool
- feature-rich
- written in python

<p align="center">
    <img src="https://raw.githubusercontent.com/bkzk/screens/master/minja/minja_main.png">
</p>

minja is here to help you with


- test email security policies and SMTP session
- learn about SMTP protocol and email authentication mechanism like SPF and DKIM
- diagnostic SMTP
- investigate vulnerabilities
- analyze messages

Beneficial for:

- system administrators
- security investigators
- pentesters
- support engineers

## DISCLAIMER

This tool for LEGAL testing purposes only!


## Requirement

minja is written in python 2.7 so you may need to install it.  In such case I would recommend you to get familiar with  https://github.com/pyenv/pyenv.


### Python 2.7 requirement:

```
dkimpy == 0.6.1
pydns
pyspf >= 2.0.12t
pydns
ipaddr
authres
```

To start working with DKIM signing and verification feature please install dkimpy module (version 0.6.1) and pydns which is required for this module. There is an older version of this module called pydkim and is available in version 0.3.1 - do not install this module as they are not compatibile. Please also avoid installing module dnspython which can be in conflict with pydns.

To use the SPF verification and validation feature please install pyspf in the latest 2.0.12t version as it seems this is the only version which is working properly with python 2.7 and required modules ipaddr and pydns. An additional modules authres is partially used to parse Authentication-Results header field.


### Installation


```
git clone https://github.com/bkzk/minja.git

# install all modules with one command

cd minja
pip install -r minja/requirement.txt

# or per module

pip install pydns
pip install dkimpy==0.6.1
pip install ipaddr
pip install 'pyspf>=2.0.12t'
pip install authres

```

### virtualenv

If you don't want to install modules in your system paths you should use a virtualenv to separate your environments. You may want to check it: https://virtualenv.pypa.io/en/stable/


```
pip install virtualenv
```

```
$ mkdir minja.app
$ cd minja.app


$ virtualenv venv --no-site-packages
$ source venv/bin/activate

(venv) $ git clone https://github.com/bkzk/minja.git

(venv) $ pip install -r minja/requirements.txt

(venv) $ pip list

# now you can run unzipped code

(venv) $ ./bin/minja.sh

# or thru zipped binary

(venv) $ ./minja.bin

$ deactivate
```

The zipped code in minja.bin can be easiy copy to your /usr/local/bin directory as long you installed required modules in system paths.
When you use a minja.bin you may want to export PYTHONPATH where the libs are installed. Please see Issue#Missing module section




## Configuration

### Usage

Although I'm trying the usage would be self-explanatory, some features should be properly documented to be fully understandable (e.g. SMTP Replay). This section is going to provide this additional help.

Soon ..

### Environments variable

By default minja is using some of local shell variable to determine the default settings like smtp hostname, helo name, sender and recipient address.
- The localhost and port 25 are used by default for SMTP host.
- The local username and hostname are used to set a default sender address. If username can not be determined the postmaster name is used for local part address.

#### MFROM= and RCPTTO=

Envelope sender and recipients addresses can be also defined with local shell variables. By exporting one or both of below environment variable the default sender and/or recipient addresses can be set. You can set these variable for your current shell session, per instance or globally with your shell rc file (e.g. ~/.bashrc).

```
# export for bash session

$ export MFROM=a@example.com
$ export RCPTTO=b@domain.com

```
```
# export only for single instance, place them before command
$ MFROM=a@example.com RCPTTO=b@domain.com minja
```

#### EDITOR=

Default editor is set to Vim, so if you have a different preferences and there is a big chance you have, than editor defined by an environment EDITOR variable is used. If your system or your local environment does not export this variable please do it yourself to use your prefer editor. For example to use a nano:

```
# per bash session
$ export EDITOR=nano
$ minja
```

```
# per instance
EDITOR=nano minja
```



## Issues

#### Missing module

You have installed module but python returns "ImportError: No module named ...".
Please check the path where the module is installed and export this path to your bash environment.

```
## check the path
$ python -c 'import spf; print spf.__file__'
/usr/local/lib/python2.7/site-packages/spf.pyc

### export the path
$ export PYTHONPATH="$PYTHONPATH:/usr/local/lib/python2.7/site-packages/"
```


## Author

Written by: Bartosz Kozak (C) 2016-2019
