# coding: utf-8
import requests
import telegram_bot_sent
from telegram_bot_sent import get_reputation_server, send_message_parser
import config
import threading
from threading import Thread
from sqlite import SQLighter
import time, datetime, calendar
from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.common.exceptions import NoSuchElementException

names={"s2":"93.84.119.237","s3":"93.84.119.238","s4":"93.84.119.239","s5":"93.84.119.240","s6":"93.84.119.241","s7":"93.84.119.242","s8":"93.84.119.243"}
#names={"s2":"93.84.119.237","s3":"93.84.119.238"}
time_report ="09:30"
def parser(key, value):
    global messages
    db_worker = SQLighter(config.database)
    reputation = db_worker.iformation_reputation_server(key)
    options={}
    headers = {

  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
  }
    driver.get("https://www.talosintelligence.com/reputation_center/lookup?search=%s" %(value))

    time.sleep(5)

    try:
        options["EMAIL_REPUTATION"] = driver.find_element_by_xpath('//*[@id="email-data-wrapper"]/table/tbody/tr[1]/td[2]/span').text
        if (options.get("EMAIL_REPUTATION")!= reputation[0][1]) and ((options["EMAIL_REPUTATION"] and reputation[0][1])!= "None" ):
            messages +="%s.open.by E-mail:%s \u27A1 %s\n" %(key, reputation[0][1],options.get("EMAIL_REPUTATION"))
    except NoSuchElementException:
        options["EMAIL_REPUTATION"] ="None"

    time.sleep(5)

    try:
        options["WEB_REPUTATION"] = driver.find_element_by_xpath('//*[@id="email-data-wrapper"]/table/tbody/tr[2]/td[2]/span').text
        if (options.get("WEB_REPUTATION")!= reputation[0][2]) and ((options["WEB_REPUTATION"] and reputation[0][2])!= "None"):
            messages +="%s.open.by Web:%s \u27A1 %s\n" %(key, reputation[0][2],options.get("WEB_REPUTATION"))
    except NoSuchElementException:
        options["WEB_REPUTATION"] = "None"

    time.sleep(5)

    try:
        options["WEIGHTED_REPUTATION"] = driver.find_element_by_xpath('//*[@id="email-data-wrapper"]/table/tbody/tr[3]/td[2]/span').text
        if (options.get("WEIGHTED_REPUTATION")!=reputation[0][3]) and ((options["WEIGHTED_REPUTATION"] and reputation[0][3])!= "None"):
             messages +="%s.open.by Weighed:%s \u27A1 %s\n" %(key, reputation[0][3],options.get("WEIGHTED_REPUTATION"))
    except NoSuchElementException:
        options["WEIGHTED_REPUTATION"]= "None"

    time.sleep(5)

    try:
        options["VOLUME_CHANGE"] = driver.find_element_by_xpath('//*[@id="email-data-wrapper"]/table/tbody/tr[7]/td[2]').text
        if (options.get("VOLUME_CHANGE")!= reputation[0][4]) and ((options["VOLUME_CHANGE"] and reputation[0][4])!= "None"):
            messages +="%s.open.by Vol:%s \u27A1 %s\n" %(key, reputation[0][4],options.get("VOLUME_CHANGE"))
    except NoSuchElementException:
        options["VOLUME_CHANGE"] = "None"

    time.sleep(5)

    try:
        options["BL"] = driver.find_element_by_xpath('//*[@id="blacklist-data-wrapper"]/table/tbody/tr[6]/td[2]/span').text 
        if (options.get("BL")!= reputation[0][5]) and ((options["BL"] and reputation[0][5])!= "None"):
            messages +="%s.open.by Black list:%s \u27A1 %s\n" %(key, reputation[0][5],options.get("BL"))
    except NoSuchElementException:
        options["BL"]= "None"
    db_worker.update_iformation_reputation(calendar.timegm(time.gmtime()), options.get("EMAIL_REPUTATION"), options.get("WEB_REPUTATION"), options.get("WEIGHTED_REPUTATION"), options.get("VOLUME_CHANGE"), options.get("BL"), key)
    db_worker.close()
    
    #for key, value in options.items():
    #    print(key,":",value)
   

def Thread_parser(time_report):
    thr = Thread(target=start_get_time_information_reputation_server, args=[time_report])
    thr.start()
def start_get_time_information_reputation_server(time_report):
    while True:
       if (datetime.datetime.fromtimestamp(calendar.timegm(time.gmtime())).strftime('%H:%M') == time_report):
           get_reputation_server()
           time.sleep(82800)
       else:
           time.sleep(1)
driver = webdriver.PhantomJS(executable_path=r'/usr/local/bin/phantomjs')
Thread_parser(time_report)
def parser_sanderbase():
    global options
    global messages
    messages=''
    while True:
        for key, value in names.items():
            print('parsing server',key)
            parser(key, value)
        if len(messages)!=0:
            send_message_parser(messages)
            del messages
            messages=''
        time.sleep(5)







    
