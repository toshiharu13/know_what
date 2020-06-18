import os
import pythonping
import socket
import datetime

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

def logwritting(data):
    with open(way_to + '\\log.txt', 'a')as logfile:
        logfile.write(data + '\n')

name_programm = 'Дежурн' #поиск программы ведется по этому словосочетанию
user = 'gmc\\' + input('type username ') #имя пользователя с правами админа
pasw = input('type password ') #пароль
#way_to = 'c:\\nowwhat'  #папка где всё хранится
linebreake = '********************'
way_to = os.path.abspath(__file__)
way_to = os.path.dirname(way_to)

#подгатавливаем файл логов к записи событий данной сессии
with open(way_to + '\\log.txt', 'w') as logfile:
    logfile.write(str(datetime.datetime.now()) + '\n')

with open(way_to + "\list.txt") as list_of_arms: #читаем по списку армы
    for ARM in list_of_arms:
        ARM = ARM.strip()
        print(linebreake)
        logwritting(linebreake)

        # если АРМ доступен, узнаём IP адрес
        response = pythonping.ping(ARM, count=1 )
        try:
            if response.success():
                IP_address = socket.gethostbyname(ARM)
                print('IP addres of ARM: ' + IP_address)
                print('Name of ARM ' + ARM)
                logwritting(ARM)
                logwritting(IP_address)

                #узнаём версию СПО
                print('searching soft...')
                tmpprogramm = knowversion(ARM,way_to)
                if tmpprogramm != '':
                    print('now installed ' + tmpprogramm)
                else:
                    print('No DT programm installed')
                logwritting(tmpprogramm)

                #узнаём активного пользователя
                user_DT = knowuser(ARM,way_to)
                print('Now working: ' + user_DT + ' user')
                logwritting(user_DT)

                #узнаём версию OS
                version = know_OS(ARM,way_to)
                print('Версия ОС: ' + version)
                logwritting(version)

            else:
                notavailable = ARM + ' is not available'
                print(notavailable)
                logwritting(notavailable)
        except:
            print('can\'t work with' + ARM)
            break
print(linebreake)
print(linebreake)
while True:
    pass
