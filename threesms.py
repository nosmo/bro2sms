#!/usr/bin/env python2.7

# it ain't pretty, it ain't nice but it was 10 minutes so hey.

# echo "message" | threesms.py number

import cookielib
import urllib
import urllib2
import os.path
import sys

have_bs = None

try:
    import BeautifulSoup
    have_bs = True
except ImportError:
    pass

#passfile in format number:password
password_f = open(os.path.expanduser("~/.threepass"))
uid, password = password_f.read().strip().split(":")
password_f.close()

login_url = "https://webtexts.three.ie//webtext/users/login"
message_url = "https://webtexts.three.ie/webtext/messages/send"

cookie_filename = "/tmp/.threesms"

def main():

    cj = cookielib.MozillaCookieJar(cookie_filename)

    opener = urllib2.build_opener(
        urllib2.HTTPRedirectHandler(),
        urllib2.HTTPHandler(debuglevel=0),
        urllib2.HTTPSHandler(debuglevel=0),
        urllib2.HTTPCookieProcessor(cj)
        )

    login_data = urllib.urlencode({
        'data[User][telephoneNo]' : uid,
        'data[User][pin]' : password,
        })
    response = opener.open(login_url, login_data)
    data = ''.join(response.readlines())

    print data

    message_data = urllib.urlencode({
        "data[Message][message]": sys.stdin.read(),
        "data[Message][recipients_individual]": sys.argv[1]
        })

    response = opener.open(message_url, message_data)
    data = ''.join(response.readlines())

    if have_bs:
        soup = BeautifulSoup.BeautifulSoup(data)

        if soup.find("div", {"class": "success", "id": "flashMessage" }):
            print "Message sent successfully"
        else:
            sys.stderr.write("Message sending failed!\n")
            sys.exit(1)

    return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("threesms.py <number>\n")
        sys.exit(1)

    main()
