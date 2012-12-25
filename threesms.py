#!/usr/bin/env python2.7

# it ain't pretty, it ain't nice but it was 10 minutes so hey.

# echo "message" | threesms.py number number2

import cookielib
import os
import sys
import tempfile
import urllib
import urllib2

have_bs = None

try:
    import BeautifulSoup
    have_bs = True
except ImportError:
    pass

LOGIN_URL = "https://webtexts.three.ie//webtext/users/login"
MESSAGE_URL = "https://webtexts.three.ie/webtext/messages/send"

class MessageSender(object):
    """Wrap logging into the Three site and sending messages"""

    def __init__(self, username, password, cookie_filename=tempfile.mkstemp()[1]):
        self.username = username
        self.__password = password

        cj = cookielib.MozillaCookieJar(cookie_filename)
        self.cookie_filename = cookie_filename

        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(cj)
            )

        self.__login_data = urllib.urlencode({
            'data[User][telephoneNo]' : username,
            'data[User][pin]' : password,
            })

    def sendMessage(self, recipient, message):
        response = self.opener.open(LOGIN_URL, self.__login_data)
        data = ''.join(response.readlines())

        message_data = urllib.urlencode({
            "data[Message][message]": message,
            "data[Message][recipients_individual]": recipient
            })

        response = self.opener.open(MESSAGE_URL, message_data)
        data = ''.join(response.readlines())
        return data


def parse_config(path=os.path.expanduser("~/.threesms/config")):
    config_f = open(path, "r")
    config_dat = [ i.strip().split() for i in config_f.readlines()]
    config_f.close()

    login = {}
    numbers = {}

    for section, person, number in [ i for i in config_dat if len(i) == 3]:
        if section == "alias":
            numbers[person] = number

    for section, value in  [ i for i in config_dat if len(i) == 2 ]:
        if section == "username":
            login["username"] = value
        elif section == "password":
            login["password"] = value

    return login, numbers

def main(recipients):

    login, numbers = parse_config()

    to_msg = ", ".join([ "%s" % i for i in recipients if i not in numbers ])
    to_indict_msg = ", ".join([ "%s (%s)" % (i, numbers[i]) for i in recipients if i in numbers ])
    header = "[ Message to %s ]" % (",".join([ i for i in [to_msg, to_indict_msg] if i]))

    if sys.__stdin__.isatty():
        print header

    try:
        message = sys.stdin.read()
    except KeyboardInterrupt as e:
        print "[ okay, I'm outta here. ]"
        sys.exit(1)

    if "username" not in login:
        print "No username"
        sys.exit(1)
    elif "password" not in login:
        print "No password"
        sys.exit(1)

    sender = MessageSender(login["username"], login["password"])

    for recipient in recipients:
        if recipient in numbers:

            data = sender.sendMessage(numbers[recipient], message)
        else:
            data = sender.sendMessage(recipient, message)

        #print data

        if have_bs:
            soup = BeautifulSoup.BeautifulSoup(data)

            if soup.find("div", {"class": "success", "id": "flashMessage" }):
                print "Message sent to %s successfully" % recipient
            else:
                sys.stderr.write("Message sending failed!\n")
                sys.exit(1)

    os.unlink(sender.cookie_filename)
    return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("threesms.py [number...]\n")
        sys.exit(1)

    main(sys.argv[1:])
