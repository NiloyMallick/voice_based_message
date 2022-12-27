from django.shortcuts import render, redirect
from django.contrib import auth
from . import forms
from .models import Details
from .models import Compose
import imaplib,email
from gtts import gTTS
import os
from playsound import playsound
from django.http import HttpResponse
import speech_recognition as sr
from django.http import JsonResponse
import re
from .models import *
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from datetime import datetime, timedelta



file = "good"
i="0"
passwrd = ""
addr = ""
item = ""
subject = ""
body = ""

attachment_dir = 'C:/Users/Chacko/Desktop/'

def texttospeech(text, filename):
    filename = filename + '.mp3'
    flag = True
    while flag:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            flag = False
        except:
            print('Trying again')
    playsound(filename)
    os.remove(filename)
    return

def speechtotext(duration):
    global i, addr, passwrd
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        playsound('speak.mp3')
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
    except:
        response = 'N'
    return response

def convert_special_char(text):
    temp=text
    special_chars = ['attherate','dot','underscore','dollar','hash','star','plus','minus','space','dash']
    for character in special_chars:
        while(True):
            pos=temp.find(character)
            if pos == -1:
                break
            else :
                if character == 'attherate':
                    temp=temp.replace('attherate','@')
                elif character == 'dot':
                    temp=temp.replace('dot','.')
                elif character == 'underscore':
                    temp=temp.replace('underscore','_')
                elif character == 'dollar':
                    temp=temp.replace('dollar','$')
                elif character == 'hash':
                    temp=temp.replace('hash','#')
                elif character == 'star':
                    temp=temp.replace('star','*')
                elif character == 'plus':
                    temp=temp.replace('plus','+')
                elif character == 'minus':
                    temp=temp.replace('minus','-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp=temp.replace('dash','-')
    return temp

def login_view(request):
    global i, addr, passwrd 

    if request.method == 'POST':
        text1 = "Welcome to our Voice Based Message Service Connect Blindly. Login with your User Name in order to continue. "
        texttospeech(text1, file + i)
        i = i + str(1)

        flag = True
        while (flag):
            texttospeech("Enter your User Name", file + i)
            i = i + str(1)
            addr = speechtotext(10)
            
            if addr != 'N':
                texttospeech("You meant " + addr + " say yes to confirm or no to enter again", file + i)
                i = i + str(1)
                say = speechtotext(3)
                if say == 'yes' or say == 'Yes':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
        addr = addr.strip()
        addr = addr.replace(' ', '')
        addr = addr.lower()
        addr = convert_special_char(addr)
        print(addr)
        request.email = addr

        flag = True
        while (flag):
            
            texttospeech("Enter your password", file + i)
            i = i + str(1)
            passwrd = speechtotext(10)
            
            if addr != 'N':
                texttospeech("You meant " + passwrd + " say yes to confirm or no to enter again", file + i)
                i = i + str(1)
                say = speechtotext(3)
                if say == 'yes' or say == 'Yes':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
        passwrd = passwrd.strip()
        passwrd = passwrd.replace(' ', '')
        passwrd = passwrd.lower()
        passwrd = convert_special_char(passwrd)
        print(passwrd)   
        try:
            user = auth.authenticate(username=addr, password=passwrd)
            auth.login(request, user)
            texttospeech("Congratulations. You have logged in successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
            return JsonResponse({'result' : 'success'})
        except:
            texttospeech("Invalid Login Details.")
            return JsonResponse({'result': 'failure'})

    detail  = Details()
    detail.email = addr
    detail.password = passwrd
    return render(request, 'homepage/login.html', {'detail' : detail}) 

def options_view(request):
    global i, addr, passwrd
    if request.method == 'POST':
        flag = True
        texttospeech("You are logged into your account. What would you like to do ?", file + i)
        i = i + str(1)
        while(flag):
            texttospeech("To Send an message say Send Message. To open Unread message say Chat. To See All Sent Message say Sent. To open All Message say All. To know the current Time say time. To Logout say Logout. Do you want me to repeat? ", file + i)
            i = i + str(1)
            say = speechtotext(3)
            if say == 'No' or say == 'no':
                flag = False
        texttospeech("Enter your desired action", file + i)
        i = i + str(1)
        act = speechtotext(5)
        act = act.lower()
        if act == 'send message':
            return JsonResponse({'result' : 'compose'})
        elif act == 'chat':
            return JsonResponse({'result' : 'inbox'})
        elif act == 'sent':
            return JsonResponse({'result' : 'sent'})
        elif act == 'all':
            return JsonResponse({'result' : 'all'})
        
        elif act == 'time' or 'Time':
            current = datetime.now()
            formate_time = current.strftime("%H:%M")
            time_text = "Current Time is" + str(formate_time )
            texttospeech(time_text, file + i)
            return JsonResponse({'result' : 'time'})

        elif act == 'log out':
            addr = ""
            passwrd = ""
            texttospeech("You have been logged out of your account and now will be redirected back to the login page.",file + i)
            i = i + str(1)
            return JsonResponse({'result': 'logout'})
        else:
            texttospeech("Invalid action. Please try again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
    elif request.method == 'GET':
        return render(request, 'homepage/options.html')

def compose_view(request):
    global i, addr, passwrd, s, item, subject, body
    if request.method == 'POST':
        text1 = "You have reached the page where you can compose and send an message. "
        texttospeech(text1, file + i)
        i = i + str(1)
        flag = True
        flag1 = True
        fromaddr = addr
        toaddr = list()
        while flag1:
            while flag:
                texttospeech("enter receiver's email address:", file + i)
                i = i + str(1)
                to = ""
                to = speechtotext(15)
                if to != 'N':
                    
                    texttospeech("You meant " + to + " say yes to confirm or no to enter again", file + i)
                    i = i + str(1)
                    say = speechtotext(5)
                    if say == 'yes' or say == 'Yes':
                        toaddr.append(to)
                        flag = False
                else:
                    texttospeech("could not understand what you meant", file + i)
                    i = i + str(1)
            texttospeech("Do you want to enter more recipients ?  Say yes or no.", file + i)
            i = i + str(1)
            say1 = speechtotext(3)
            if say1 == 'No' or say1 == 'no':
                flag1 = False
            flag = True

        newtoaddr = list()
        for item in toaddr:
            item = item.strip()
            item = item.replace(' ', '')
            item = item.lower()
            item = convert_special_char(item)
            newtoaddr.append(item)
            print(item)

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ",".join(newtoaddr)
        flag = True
        while (flag):
            texttospeech("enter subject", file + i)
            i = i + str(1)
            subject = speechtotext(10)
            if subject == 'N':
                texttospeech("could not understand what you meant", file + i)
                i = i + str(1)
            else:
                flag = False
        msg['Subject'] = subject
        flag = True
        while flag:
            texttospeech("enter body of the message", file + i)
            i = i + str(1)
            body = speechtotext(20)
            if body == 'N':
                texttospeech("could not understand what you meant", file + i)
                i = i + str(1)
            else:
                flag = False

        msg.attach(MIMEText(body, 'plain'))
        texttospeech("any attachment? say yes or no", file + i)
        i = i + str(1)
        x = speechtotext(3)
        x = x.lower()
        if x == 'yes':
            texttospeech("Do you want to record an audio and send as an attachment?", file + i)
            i = i + str(1)
            say = speechtotext(2)
            say = say.lower()
            if say == 'yes':
                texttospeech("Enter filename.", file + i)
                i = i + str(1)
                filename = speechtotext(5)
                filename = filename.lower()
                filename = filename + '.mp3'
                filename = filename.replace(' ', '')
                print(filename)
                texttospeech("Enter your audio message.", file + i)
                i = i + str(1)
                audio_msg = speechtotext(10)
                flagconf = True
                while flagconf:
                    try:
                        tts = gTTS(text=audio_msg, lang='en', slow=False)
                        tts.save(filename)
                        flagconf = False
                    except:
                        print('Trying again')
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
            elif say == 'no':
                texttospeech("Enter filename with extension", file + i)
                i = i + str(1)
                filename = speechtotext(5)
                filename = filename.strip()
                filename = filename.replace(' ', '')
                filename = filename.lower()
                filename = convert_special_char(filename)
                
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
        try:
            s.sendmail(fromaddr, newtoaddr, msg.as_string())
            texttospeech("Your email has been sent successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
        except:
            texttospeech("Sorry, your email failed to send. please try again. You will now be redirected to the the compose page again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
        s.quit()
        return JsonResponse({'result' : 'success'})
    
    compose  = Compose()
    compose.recipient = item
    compose.subject = subject
    compose.body = body

    return render(request, 'homepage/compose.html', {'compose' : compose})
  
def get_attachment(msg):
    global i
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if bool(filename):
            filepath = os.path.join(attachment_dir, filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
                texttospeech("Attachment has been downloaded", file + i)
                i = i + str(1)
                path = 'C:/Users/Chacko/Desktop/'
                files = os.listdir(path)
                paths = [os.path.join(path, basename) for basename in files]
                file_name = max(paths, key=os.path.getctime)
            with open(file_name, "rb") as f:
                if file_name.find('.jpg') != -1:
                    texttospeech("attachment is an image", file + i)
                    i = i + str(1)
                if file_name.find('.png') != -1:
                    texttospeech("attachment is an image", file + i)
                    i = i + str(1)
                if file_name.find('.mp3') != -1:
                    texttospeech("Playing the downloaded audio file.", file + i)
                    i = i + str(1)
                    playsound(file_name)

def reply_mail(msg_id, message):
    global i,s
    TO_ADDRESS = message['From']
    FROM_ADDRESS = addr
    msg = email.mime.multipart.MIMEMultipart()
    msg['to'] = TO_ADDRESS
    msg['from'] = FROM_ADDRESS
    msg['subject'] = message['Subject']
    msg.add_header('In-Reply-To', msg_id)
    flag = True
    while(flag):
        texttospeech("Enter body.", file + i)
        i = i + str(1)
        body = speechtotext(20)
        print(body)
        try:
            msg.attach(MIMEText(body, 'plain'))
            s.sendmail(msg['from'], msg['to'], msg.as_string())
            texttospeech("Your reply has been sent successfully.", file + i)
            i = i + str(1)
            flag = False
        except:
            texttospeech("Your reply could not be sent. Do you want to try again? Say yes or no.", file + i)
            i = i + str(1)
            act = speechtotext(3)
            act = act.lower()
            if act != 'yes':
                flag = False

def frwd_mail(item, message):
    global i,s
    flag1 = True
    flag = True
    global i
    newtoaddr = list()
    while flag:
        while flag1:
            while True:
                texttospeech("Enter receiver's email address", file + i)
                i = i + str(1)
                to = speechtotext(15)
                texttospeech("You meant " + to + " say yes to confirm or no to enter again", file + i)
                i = i + str(1)
                yn = speechtotext(3)
                yn = yn.lower()
                if yn == 'yes':
                    to = to.strip()
                    to = to.replace(' ', '')
                    to = to.lower()
                    to = convert_special_char(to)
                    print(to)
                    newtoaddr.append(to)
                    break
            texttospeech("Do you want to add more recepients?", file + i)
            i = i + str(1)
            ans1 = speechtotext(3)
            ans1 = ans1.lower()
            print(ans1)
            if ans1 == "no" :
                flag1 = False

        message['From'] = addr
        message['To'] = ",".join(newtoaddr)
        try:
            s.sendmail(addr, newtoaddr, message.as_string())
            texttospeech("Your mail has been forwarded successfully.", file + i)
            i = i + str(1)
            flag = False
        except:
            texttospeech("Your mail could not be forwarded. Do you want to try again? Say yes or no.", file + i)
            i = i + str(1)
            act = speechtotext(3)
            act = act.lower()
            if act != 'yes':
                flag = False

def read_mails(mail_list):
    global s, i
    mail_list.reverse()
    mail_count = 0
    to_read_list = list()
    for item in mail_list:
        message_from= item.message_from
        create_at = item.created_at
        id =item.id
        texttospeech("Message number" + str(mail_count+1) + " .Message from " + message_from.username , file + i)
        i = i + str(1)
        print('message id= ', id)
        print('From :', message_from)
        print(' :', subject)
        print("\n")
        to_read_list.append(id)
        mail_count = mail_count + 1

    flag = True
    while flag :
        n = 0
        flag1 = True
        while flag1:
            texttospeech("Enter the Message number of mail you want to read.",file + i)
            i = i + str(1)
            n = speechtotext(2)
            print(n)
            texttospeech("You meant " + str(n) + ". Say yes or no.", file + i)
            i = i + str(1)
            say = speechtotext(2)
            say = say.lower()
            if say == 'yes':
                flag1 = False
        n = int(n)
        msgid = to_read_list[n - 1]
        print("message id is =", msgid)
        message = mail_list[n - 1]
        texttospeech("Message from" + str(message_from.username) + "time" + str(message.create_at) + "Message is" + message.messsage ,file + i)
        message.seen= True
        message.save()
        texttospeech("Do you want to read more message?", file + i)
        i = i + str(1)
        ans = speechtotext(2)
        ans = ans.lower()
        if ans == "no":
            flag = False
    return JsonResponse({'result': 'success'})

def search_specific_mail(folder,key,value,foldername):
    global i, conn
    conn.select(folder)
    result, data = conn.search(None,key,'"{}"'.format(value))
    mail_list=data[0].split()
    if len(mail_list) != 0:
        texttospeech("There are " + str(len(mail_list)) + " emails with this email ID.", file + i)
        i = i + str(1)
    if len(mail_list) == 0:
        texttospeech("There are no emails with this email ID.", file + i)
        i = i + str(1)
    else:
        read_mails(mail_list,foldername)

def inbox_view(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        imap_url = 'imap.gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        conn.login(addr, passwrd)
        conn.select('"INBOX"')
        result, data = conn.search(None, '(UNSEEN)')
        unread_list = data[0].split()
        no = len(unread_list)
        result1, data1 = conn.search(None, "ALL")
        mail_list = data1[0].split()
        text = "You have reached your inbox. There are " + str(len(mail_list)) + " total mails in your inbox. You have " + str(no) + " unread emails" + ". To read unread emails say unread. To search a specific email say search. To go back to the menu page say back. To logout say logout."
        texttospeech(text, file + i)
        i = i + str(1)
        flag = True
        while(flag):
            act = speechtotext(5)
            act = act.lower()
            print(act)
            if act == 'unread':
                flag = False
                if no!=0:
                    read_mails(unread_list,'inbox')
                else:
                    texttospeech("You have no unread emails.", file + i)
                    i = i + str(1)
            elif act == 'search':
                flag = False
                emailid = ""
                while True:
                    texttospeech("Enter email ID of the person who's email you want to search.", file + i)
                    i = i + str(1)
                    emailid = speechtotext(15)
                    texttospeech("You meant " + emailid + " say yes to confirm or no to enter again", file + i)
                    i = i + str(1)
                    yn = speechtotext(5)
                    yn = yn.lower()
                    if yn == 'yes':
                        break
                emailid = emailid.strip()
                emailid = emailid.replace(' ', '')
                emailid = emailid.lower()
                emailid = convert_special_char(emailid)
                search_specific_mail('INBOX', 'FROM', emailid,'inbox')

            elif act == 'back':
                texttospeech("You will now be redirected to the menu page.", file + i)
                i = i + str(1)
                conn.logout()
                return JsonResponse({'result': 'success'})

            elif act == 'log out':
                addr = ""
                passwrd = ""
                texttospeech("You have been logged out of your account and now will be redirected back to the login page.", file + i)
                i = i + str(1)
                return JsonResponse({'result': 'logout'})

            else:
                texttospeech("Invalid action. Please try again.", file + i)
                i = i + str(1)

            texttospeech("If you wish to do anything else in the inbox or logout of your mail say yes or else say no.", file + i)
            i = i + str(1)
            ans = speechtotext(3)
            ans = ans.lower()
            if ans == 'yes':
                flag = True
                texttospeech("Enter your desired action. Say unread, search, back or logout. ", file + i)
                i = i + str(1)
        texttospeech("You will now be redirected to the menu page.", file + i)
        i = i + str(1)
        conn.logout()
        return JsonResponse({'result': 'success'})

    elif request.method == 'GET':
        return render(request, 'homepage/inbox.html')

def sent_view(request):
    global i, addr, passwrd, conn
    all_messages = Message.objects.filter(message_from__username=request.user).all()

    if request.method == 'POST':
        read_mails(all_messages)
        return JsonResponse({'result': 'success'})
    elif request.method == 'GET':
        return render(request, 'homepage/sent.html', {"message": all_messages})

def all_message_view(request):
    global i, addr, passwrd, conn
    all_messages = Message.objects.filter(message_to__username=request.user).all()
    print(all_messages.count())
    if request.method == 'POST':
            read_mails(all_messages)
            return JsonResponse({'result': 'success'})
    
    elif request.method == 'GET': 
        return render(request, 'homepage/all_message.html', {"message": all_messages})
        

def group_create_view(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        text = "You have reached your Send message page. Enter group member username to add group"
        texttospeech(text, file + i)
        i = i + str(1)
        flag = True
        flag1 = True
        toaddr = ['bhai']
        while flag1:
            while flag:
                texttospeech("enter receiver's username address:", file + i)
                i = i + str(1)
                to = ""
                to = speechtotext(15)
                if to != 'N':
                    
                    texttospeech("You meant " + to + " say yes to confirm or no to enter again", file + i)
                    i = i + str(1)
                    say = speechtotext(5)
                    if say == 'yes' or say == 'Yes':
                        toaddr.append(to)
                        flag = False
                else:
                    texttospeech("could not understand what you meant", file + i)
                    i = i + str(1)
            texttospeech("Do you want to enter more recipients ?  Say yes or no.", file + i)
            i = i + str(1)
            say1 = speechtotext(3)
            if say1 == 'No' or say1 == 'no':
                flag1 = False
            flag = True

        newtoaddr = list()
        for item in toaddr:
            item = item.strip()
            item = item.replace(' ', '')
            item = item.lower()
            item = convert_special_char(item)
            newtoaddr.append(item)
            print(item)

        flag = True
        while (flag):
            texttospeech("enter subject", file + i)
            i = i + str(1)
            subject = speechtotext(10)
            if subject == 'N':
                texttospeech("could not understand what you meant", file + i)
                i = i + str(1)
            else:
                flag = False
        Subject = subject
        flag = True
        while flag:
            texttospeech("enter body of the message", file + i)
            i = i + str(1)
            body = speechtotext(20)
            if body == 'N':
                texttospeech("could not understand what you meant", file + i)
                i = i + str(1)
            else:
                flag = False
        msg = body
        print(msg)

        try:
 
            users = User.objects.filter(username__in=toaddr)
            message = Message.objects.create(message_from=request.user, messsage=msg, subject=Subject)
            message.message_to.set(users)

        except Exception as e:
            print(e)
        # message = Message.objects.create(from_message= request.user, to_message=User.objects.filter(name__in=toaddr), message=msg)
        return JsonResponse({'result': 'success'})
    elif request.method == 'GET':
        return render(request, 'homepage/compose.html')

def get_message(request):
    global i, addr, passwrd, conn
    all_messages = Message.objects.filter(message_to__username=request.user, seen = False ).all()

    if request.method == 'POST':
        read_mails(all_messages)
        return JsonResponse({'result': 'success'})
 
    elif request.method == 'GET': 
        return render(request, 'homepage/message.html', {"message": all_messages})



def signup_view(request):
    global i, addr, passwrd, repasswrd
    if request.method == 'POST':
        text1 = "Welcome to our Voice Based Message Service Connect Blindly. Are you an existing User? Speek Yes or No"
        texttospeech(text1, file + i)
        i = i + str(1)
        flag = True
        while (flag):
            addr = speechtotext(10)
            print(addr)
            
            if addr == 'No' or 'no':
                flag1 = True
                while (flag1):
                    texttospeech("Enter your User Name", file + i)
                    i = i + str(1)
                    username = speechtotext(10)

                    if username != 'N':
                        texttospeech("You meant " + username + " say yes to confirm or no to enter again", file + i)
                        i = i + str(1)
                        say = speechtotext(3)
                        if say == 'yes' or say == 'Yes':
                            flag1 = False
                    else:
                        texttospeech("could not understand what you meant:", file + i)
                        i = i + str(1)
                username = username.strip()
                username = username.replace(' ', '')
                username = username.lower()
                username = convert_special_char(username)
                
            
            elif addr == 'Yes' or 'yes':
                flag = False
                return JsonResponse({'result' : 'success'})

            else:
                text3 = "Couldnot Understand what you ment try again"
                flag=False
                texttospeech(text2, file + i)
                i = i + str(1)


            try:
                user = User.objects.get(username = username)
                text2 = "You are already an register user please login in order to continue."
                texttospeech(text2, file + i)
                i = i + str(1)
                return JsonResponse({'result' : 'success'})
                print(user)
            except ObjectDoesNotExist:
                while (flag):
                    texttospeech("Enter your password", file + i)
                    
                    i = i + str(1)
                    passwrd = speechtotext(10)
                    
                    if passwrd != 'N':
                        texttospeech("You meant " + passwrd + " say yes to confirm or no to enter again", file + i)
                        i = i + str(1)
                        say = speechtotext(3)
                        if say == 'yes' or say == 'Yes':
                            flag = False
                    else:
                        texttospeech("could not understand what you meant:", file + i)
                        i = i + str(1)
                        
                passwrd = passwrd.strip()
                passwrd = passwrd.replace(' ', '')
                passwrd = passwrd.lower()
                passwrd = convert_special_char(passwrd)
                print(passwrd)

                flag3 = True
                while (flag3):
                    texttospeech("Re-Enter your password", file + i)
                    i = i + str(1)
                    repasswrd = speechtotext(10)
                    
                    if repasswrd != 'N':
                        texttospeech("You meant " + repasswrd + " say yes to confirm or no to enter again", file + i)
                        i = i + str(1)
                        say = speechtotext(3)
                        if say == 'yes' or say == 'Yes' or 'speak yes' or 'Speak Yes':
                            flag3 = False
                        
                    else:
                        texttospeech("could not understand what you meant:", file + i)
                        i = i + str(1)
                    repasswrd = repasswrd.strip()
                    repasswrd = repasswrd.replace(' ', '')
                    repasswrd = repasswrd.lower()
                    repasswrd = convert_special_char(passwrd)
                    print(repasswrd)

                    if passwrd == repasswrd:
                        user = User.objects.create_user(username=username, password = repasswrd)
                        return JsonResponse({'result' : 'success'})

                    else: 
                        texttospeech("Password Didn't match Try Again", file + i)
                        i = i + str(1)
                    # auth.login(request, user)
                        return JsonResponse({'result' : 'signup'})
    
    elif request.method == 'GET': 
        return render(request, 'homepage/signup.html')

        