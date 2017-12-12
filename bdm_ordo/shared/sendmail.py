
import smtplib
import sys
import urllib2
import time

def send_mail(subject, body):
    sender = 'XXX@XXX.brussels'
    receivers = ['XXX@XXX.brussels']
    msg = "\r\n".join([
        "From: " + sender,
        "To: " + ",".join(receivers),
        "Subject: " + subject,
        "",
        body
        ])
    try:
        server = smtplib.SMTP('relay.XXX')
        server.ehlo()
        server.sendmail(sender, receivers, msg)
        print "Successfully sent mail"
    except Exception:
        print "Error : Unable to send email", sys.exc_info[0]

def send_mail_ext(subject, body, recipients):
    sender = 'brugis@sprb.brussels'
    receivers = recipients
    msg = "\r\n".join([
        "From: " + sender,
        "To: " + ",".join(receivers),
        "Subject: " + subject,
        "",
        body
        ])
    try:
        server = smtplib.SMTP('relay.XXX')
        server.ehlo()
        server.sendmail(sender, receivers, msg)
        print "Successfully sent mail"
    except Exception as e:
        print "Error : Unable to send email", e.strerror


if __name__ == "__main__":
    for cpt in range(60):
        body = urllib2.urlopen("http://www.iheartquotes.com/api/v1/random").read()
        send_mail("Your random Quote by a (not so?) funny? consultant", body)
        time.sleep(1)

    
        
             
