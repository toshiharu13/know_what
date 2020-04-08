import os
import pythonping
import socket

def knowversion(ARM,way_to): #берем версию программы установленной сейчас
    os.system('wmic /NODE:\"' + ARM + '\" /USER:\"' + user + '\" /password: \"' + pasw + '\" product get name| findstr \"' + name_programm + '\">\"' + way_to + '\\temp\\\"' + ARM + '.txt')
    if os.stat(way_to + '\\temp\\' + ARM + '.txt').st_size == 0:
        print('Программы не найдено')
        tmp = ''
    with open(way_to + '\\temp\\' + ARM + '.txt') as t:
        for tmp in t:
            tmp = tmp.encode('cp1251').decode('cp866').strip()
            return tmp
            #break
    #return tmp

def knowuser(ARM, way_to):
    os.system('wmic.exe /node:\"' + ARM + '\" computersystem get username >' + way_to + '\\temp\\' + ARM + '.txt')
    with open(way_to + '\\temp\\' + ARM + '.txt') as user_tmp:
        linecount = 0
        for tmp in user_tmp:
            tmp = tmp.strip()
            linecount += 1
            if linecount == 3:
                return tmp

def know_OS(ARM,way_to):
    os.system('WMIC /NODE:\"' + ARM + '\" OS get Caption >' + way_to + '\\temp\\' + ARM + '.txt')
    with open(way_to + '\\temp\\' + ARM + '.txt') as version_tmp:
        linecount = 0
        for tmp in version_tmp:
            tmp = tmp.encode('cp1251').decode('cp866').strip()
            linecount += 1
            if linecount == 3:
                return tmp

name_programm = 'Дежурн' #поиск программы ведется по этому словосочетанию
user = 'gmc\\' + input('type username ')
pasw = input('type password ')
way_to = 'c:\\nowwhat'  #папка где всё хранится

with open(way_to + "\list.txt") as list_of_arms:
    for ARM in list_of_arms:
        ARM = ARM.strip()
        print('********************')

        # если АРМ доступен, узнаём IP адрес
        response = pythonping.ping(ARM, count=1 )
        if response.success():
            IP_address = socket.gethostbyname(ARM)
            print('IP addres of ARM: ' + IP_address)
            print('Name of ARM ' + ARM)

            #узнаём версию СПО
            print('searching soft...')
            tmpprogramm = knowversion(ARM,way_to)
            if tmpprogramm != '':
                print('now installed ' + tmpprogramm)
            else:
                print('No DT programm installed')

            #узнаём активного пользователя
            user_DT = knowuser(ARM,way_to)
            print('Now working: ' + user_DT + ' user')

            #узнаём версию OS
            version = know_OS(ARM,way_to)
            print('Версия ОС: ' + version)

        else:
            print(ARM + ' is not available')

while True:
    pass
