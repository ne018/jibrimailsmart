#author drey
#05282020 0752

import sys
import os
import shutil
import time
import json
import urllib.parse
import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

print("work in progress...")

dirPath = "/tmp/recordings"
batt_field = "/var/www/recordings"
serviceurl = "meet.domain.com"
boshroomchkr = "http://%s:5280/room?room=%s&domain=%s&subdomain="

sender_email = 'youremail'
sender_passwd = 'yourpass'
roomname = None
dirPrefix = None
videoname = None

def file_get_contents(filename):
    if os.path.exists(filename):
        fp = open(filename, "r")
        content = fp.read()
        fp.close()
        return content

def send_mail(receiver_email, sender_email, sender_pass, urllink, roomname):

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
    #message["Bcc"] = receiver_email # for mass mails

    text = """\
        Hi there,
        You may download your recorded video from room %s on the link below:
        %s
        - Service System
        """

    html = """\
        <html>
        <body>
        <p>Hi there,<br>
        You may download your recorded video from room %s on the link below: <br>
        %s
        <br>- Service System <br>
        </p>
        </body>
        </html>
        """

    text = text % (roomname, urllink)
    html = html % (roomname, urllink)

    #file_path = os.path.join(dirpath, filename)
    #attachment = open(file_path, "rb")
    #p = MIMEBase('application', 'octet-stream')
    #p.set_payload((attachment).read())
    #encoders.encode_base64(p)
    #p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    #message.attach(p)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    password = sender_pass

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


if os.listdir(dirPath) != []:
    os.chdir(dirPath)
    enemies = sorted(os.listdir('.'), key=os.path.getmtime)

    if enemies is not None:
        victim = None

        for enemy in enemies:
            if victim is not None:
                break

            os.chdir(dirPath+"/"+enemy)
            scanmeta = os.listdir('.')

            for fmeta in scanmeta:
                if fmeta == "metadata.json":
                    print("has a meta")
                    victim = enemy
                    break

        if victim is not None:
            print(victim)
            target = victim
            print("here's the target: ", target)
            loc_target = (dirPath+"/"+target)
            print("target location: ", loc_target)

#           prod
            fieldWar = shutil.move(loc_target, batt_field)
            print("field war: ",fieldWar)

#           for testing
#           fieldWar = "/var/www/html/recordings/uguxtmtcqlmlkwna"

            dirPrefix = str.split(fieldWar, '/var/www/html/recordings/')[1]

            if os.listdir(fieldWar) != []:
                print("Meron")
                os.chdir(fieldWar)
                anatomy = os.listdir('.')

                mod_emails = []

                for getneed in anatomy:
                    if getneed == "metadata.json":

                        metadatafile = file_get_contents(getneed)
                        getattr = json.loads(metadatafile)
                        urlpath = urllib.parse.urlparse(getattr["meeting_url"]).path
                        roomname = str.split(urlpath, '/')[1]
                        print('roomname: '+roomname)
                        skillatk = boshroomchkr % (serviceurl, roomname, serviceurl)
                        req = requests.get(skillatk)
                        if req.status_code == 200:
                            boshresp = req.text
                            print(boshresp)
                            getlist = json.loads(boshresp)

                            for item in getlist:
                                itemstr = str(item)
                                print(item)

                                # for organize condition
                                if itemstr.find("'role': 'moderator'") == -1:
                                    print("participants")
                                else:
                                    print("moderators")
                                    getresp = json.loads(itemstr.replace("'",'"'))
                                    #print("your_email: ",getresp['email'])
                                    if getresp['email'] != '':
                                        mod_emails.append(getresp['email'])
                                        print("moderator added..")
                                    else:
                                        print('moderator no existing email')

                                #for sureball
                                #getresp = json.loads(itemstr.replace("'",'"'))
                                #print("your_email: ",getresp['email'])
                                #if getresp['email'] != "":
                                #mod_emails.append(getresp['email'])
                        else:
                            print('roomname not found')

                    else:
                        videoname = getneed


                print(videoname)
                print(mod_emails)
                if mod_emails != []:
                    urllink = 'https://'+serviceurl+'/recordings/'+dirPrefix+'/'+videoname
                    for mod in mod_emails:
                        print("moderator: ",mod)

                        send_mail(mod, sender_email, sender_passwd, urllink, roomname)
                        print("mail sent to ",mod)

else:
    print('no files found in recording file path')
