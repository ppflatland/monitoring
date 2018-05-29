# -*- coding: utf-8 -*-
import config
from config import token,chat_id_Maxim, chat_id_All 
import requests
from collections  import defaultdict

del_mess_list = defaultdict(list)
check=0
check_mess_id=0
check_str=""

def bot_check_ping (last_check_ping):
    if last_check_ping == 'Network Error':
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u274C %s' %(token,chat_id_Maxim,last_check_ping))
    else:
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u2705 %s' %(token,chat_id_Maxim,last_check_ping))

def bot_err_sent (number,ip,error,st):
    if error != 0:
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u274C %s-%s error: %s time: %s' %(token,chat_id_Maxim, number,ip,error,st))
        print(response.content)
    else:
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u2705 %s-%s error: %s time: %s' %(token,chat_id_Maxim, number,ip,error,st))

def bot_code_sent(number,ip,code,st):
    global del_mess_list
    if code != 200:
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u26A0 Внимание! Обнаружены проблемы с доступом к серверу %s.open.by IP - %s код ответа: %s' %(token,chat_id_Maxim, number, ip, code))
        data = response.json()
        #del_mess_list[data['result']['chat']['id']].append(data['result']['message_id'])
        del_mess_list[number].append(data['result']['message_id'])
        print(del_mess_list[number])
    else:
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u2705 Сервер %s.open.by начал работать в штатном режиме, код ответа %s' %(token,chat_id_All, number, code))
        for i, server in enumerate(del_mess_list[number]):
            response = requests.get('https://api.telegram.org/bot%s/deleteMessage?chat_id=%s&message_id=%s' %(token,chat_id_All, server))
        print(response.content)

def get_all_status(status):
    global check, check_str, check_mess_id
    server_status = ""
    for i, server in enumerate(status): 
        if server[1] != "200":
            server_status += "Сервер %s.open.by - код ответа %s\n"%(server[0], server[1])
            check=1
        elif len(server_status)== 0:
            check=0
    if len(server_status)!= 0 and (check_str.lower() != server_status.lower()):
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u26A0 Внимание!  Обнаружена проблема с доступом к серверу(ам):\n%s' %(token,chat_id_All, server_status))
        data = response.json()
        check_mess_id=data['result']['message_id']
        requests.get('https://api.telegram.org/bot%s/pinChatMessage?chat_id=%s&message_id=%s' %(token,chat_id_All, data['result']['message_id']))
        check_str=server_status
        check=1 
    elif check_mess_id != 0 and check==0:
        requests.get('https://api.telegram.org/bot%s/unpinChatMessage?chat_id=%s&message_id=%s' %(token,chat_id_All, check_mess_id))
        check=0


        
        




