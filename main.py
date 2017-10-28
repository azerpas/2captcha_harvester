# coding=utf-8
import random
import sys
import threading
import time
import requests, json, datetime, time, BeautifulSoup, pickle



# How many threads?
Hthreads = 10
sitekeyEnabled = False
repeat = True
repeatTime = '19:23' #end of the loop
# To-Add, how many does it have to run, False True, d is showing hour and minute
# in format '16:18' 
#######
CaptchaList = []
active_threads = 0


sitekey = '6LcMxjMUAAAAALhKgWsmmRM2hAFzGSQqYcpmFqHx'  #### ENTER YOUR SITEKEY HERE

API_KEY = '' ##### ENTER YOUR API KEY HERE

captcha_url = '' ##### ENTER THE URL CAPTCHA


def main():
    global CaptchaList
    global sitekey
    global API_KEY
    global captcha_url
    global headers

    log('Welcome')
    if sitekeyEnabled == True:
        log('Retriving Sitekey')
        sitekey = get_sitekey(captcha_url)

    d = datetime.datetime.now().strftime('%H:%M') 
    # Shitty coding
    if repeat == True: 
        while not str(d) == repeatTime:
            for i in range(0,Hthreads):
                t = threading.Thread(target=get_captcha, args=(API_KEY,sitekey,captcha_url))
                t.daemon = True
                t.start()
                time.sleep(0.1)
            while not active_threads == 0 or active_threads == 1:
                log('Active Threads ---------- ' + str(active_threads))
                time.sleep(5)
                d = datetime.datetime.now().strftime('%H:%M')

    else: 
        for i in range(0,Hthreads):
            t = threading.Thread(target=get_captcha, args=(API_KEY,sitekey,captcha_url))
            t.daemon = True
            t.start()
            time.sleep(0.1)
        while not active_threads == 0 or active_threads == 1:
            log('Active Threads ---------- ' + str(active_threads))
            time.sleep(5)


def log(event):
    print('Captcha by Azerpas :: ' + str(datetime.datetime.now().strftime('%H:%M:%S')) + ' :: ' + str(event))


def get_captcha(API_KEY,sitekey,captcha_url):
    global active_threads

    active_threads += 1

    session = requests.session()
    session.cookies.clear()
    randomID = random.getrandbits(16)
    log('Generating Captcha for task ID: ' + str(randomID))
    captcha_id = session.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, sitekey, captcha_url)).text.split('|')[1]
    recaptcha_answer = session.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        print(recaptcha_answer)
        time.sleep(3)
        recaptcha_answer = session.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    recaptcha_answer = recaptcha_answer.split('|')[1]
    log('Captcha successfully obtained, task ID: ' + str(randomID))
    saveCaptcha(recaptcha_answer,randomID)
    log('Task ID ' + str(randomID) + ' is closing...')
    active_threads -= 1

def saveCaptcha(recaptcha_answer, ID):
    d = datetime.datetime.now().strftime('%H:%M')
    log("Saving Captcha into '" + str(d) + ".txt', valid for 2 minutes")
    try : 
        file = open(str(d)+'.txt','r')
        print('Txt already exists, task ID: ' + str(ID))
        Filelist = pickle.load(file)
        Filelist.append(recaptcha_answer)
        file = open(str(d)+'.txt','w')
        pickle.dump(Filelist,file)
        #file.write(Filelist)
        #file.write(str(recaptcha_answer))
        #file.write('\n')
    except IOError as e:
        print('Creating txt, task ID: ' + str(ID))
        file = open(str(d)+'.txt','w')
        Filelist = []
        Filelist.append(recaptcha_answer)
        #file.write(Filelist)
        pickle.dump(Filelist,file)
        #file.write('\n')
    print('Captcha successfuly saved, task ID: ' + str(ID))
    CaptchaList.append(recaptcha_answer)

if __name__ == "__main__":
    main()
