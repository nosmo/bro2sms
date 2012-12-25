bro_2_sms
===========

Send messages via Three's webtext service. Named (with apologies) after [o2sms](http://o2sms.sourceforge.net/).

Configuration
-----------

bro2sms shamelessly steals everything possible from o2sms, from output style to configuration file.

Configuration is read from ~/.threesms/config. Configuration is simply of the format

<pre>username 0811111111
password 223344
alias dude 00353822222222
</pre>

Requirements
-----------
bro2sms can use BeautifulSoup if you have it installed, but it is not required. The module is used to check whether the message has sent successfully. This is entirely down to laziness.

N(C)! license.
