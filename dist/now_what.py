import os
import pythonping
import socket


user = 'gmc\\' + input('введите пользователя ')
pasw = input('введите пароль ')
ARM = input('введите имя компьютера для получения информации ')
print('********************')
# если АРМ доступен, узнаём IP адрес
response = pythonping.ping(ARM, count=1 )
if response.success():
    IP_address = socket.gethostbyname(ARM)
    print('IP адрес АРМ-а: ' + IP_address)
    #узнаём версию СПО
    os.system('wmic /NODE:\"' + ARM + '\" /USER:\"' + user + '\" /password: \"' + pasw + '\" product get name| findstr \"Дежурн\" > temp.txt')
    if os.stat('temp.txt').st_size == 0:
        print('Программы не найдено')
        tmp = ''
    with open('temp.txt') as t:
        for tmp in t:
            tmp = tmp.encode('cp1251').decode('cp866').strip()
            break
    print('СПО: ' + tmp)
    #узнаём активного пользователя
    os.system('wmic.exe /node:\"' + ARM + '\" computersystem get username > temp.txt')
    with open('temp.txt') as user_tmp:
        linecount = 0
        for tmp in user_tmp:
            tmp = tmp.strip()
            linecount += 1
            if linecount == 3:
                user = tmp
                print('Сейчас на АРМ-е работает пользователь: ' + user)
    #узнаём версию OS
    os.system('WMIC /NODE:\"' + ARM + '\" OS get Caption > temp.txt')
    with open('temp.txt') as version_tmp:
        linecount = 0
        for tmp in version_tmp:
            tmp = tmp.encode('cp1251').decode('cp866').strip()
            linecount += 1
            if linecount == 3:
                version = tmp
                print('Версия ОС: ' + version)


else:
    print(ARM + ' is not available')

while True:
    pass


