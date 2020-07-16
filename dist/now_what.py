import os
import pythonping
import socket
import datetime
import tkinter

def knowversion(ARM,way_to): #берем версию программы установленной сейчас
    os.system('wmic /NODE:\"' + ARM + '\" /USER:\"' + user + '\" /password: \"' + pasw + '\" product get name| findstr \"' + name_programm + '\">\"' + way_to + '\\temp\\\"' + ARM + '.txt')
    if os.stat(way_to + '\\temp\\' + ARM + '.txt').st_size == 0:
        print('Программы не найдено')
        tmp = ''
        return tmp
    with open(way_to + '\\temp\\' + ARM + '.txt') as t:
        for tmp in t:
            tmp = tmp.encode('cp1251').decode('cp866').strip()
            return tmp

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

def if_ARM_online(arm):
    try:
        response = pythonping.ping(arm, count=1)
        if response.success():
            print(arm + ' доступен')
        else:
            print(arm + ' не доступен')
            return False
    except:
        print(arm + ' не доступен')
        return False

def Start(ivent):
    # передаём занчение логин пароль в переменные
    global user, pasw
    user = 'gmc\\' + enter_login.get()  # имя пользователя с правами админа
    pasw = enter_passw.get()  # пароль

    # читаем по списку армы
    with open(way_to + "\list.txt") as list_of_arms:
        for ARM in list_of_arms:
            ARM = ARM.strip()
            print(linebreake)
            logwritting(linebreake)
            logwritting(ARM)

            # если АРМ доступен, узнаём IP адрес
            if if_ARM_online(ARM) == False:
                print("не доступен")
                logwritting("не доступен")
                continue
            else:
                IP_address = socket.gethostbyname(ARM)
                print('Name of ARM ' + ARM)
                print('IP addres of ARM: ' + IP_address)

                logwritting(IP_address)

                # узнаём версию СПО
                print('searching soft...')
                tmpprogramm = knowversion(ARM, way_to)
                if tmpprogramm != '':
                    print('now installed ' + tmpprogramm)
                else:
                    print('No DT programm installed')
                logwritting(tmpprogramm)

                # узнаём активного пользователя
                user_DT = knowuser(ARM, way_to)
                print('Now working: ' + user_DT + ' user')
                logwritting(user_DT)

                # узнаём версию OS
                version = know_OS(ARM, way_to)
                print('Версия ОС: ' + version)
                logwritting(version)


    print(linebreake)
    print(linebreake)




name_programm = 'Дежурн' #поиск программы ведется по этому словосочетанию

linebreake = '********************'
way_to = os.path.abspath(__file__)
way_to = os.path.dirname(way_to)

# подгатавливаем файл логов к записи событий данной сессии
with open(way_to + '\\log.txt', 'w') as logfile:
    logfile.write(str(datetime.datetime.now()) + '\n')

# читаем файл с армами для отображения в окне
with open(way_to + "\list.txt") as list_of_arms:
    text_of_arms = list_of_arms.readlines()
    text_of_arms = "".join(text_of_arms)


#Основное окно программы
main_window = tkinter.Tk()
main_window.title("Know_what программа анализа сведений об АРМ-е")
main_window.geometry('600x350+500+200')
#вторичное окно для отображения списка АРМ-ов
list_arm_window = tkinter.Tk()
list_arm_window.title("Список АРМ-ов")
list_arm_window.geometry('300x250+1110+200')
#описание элементов окна
lbl_log = tkinter.Label(main_window, text = "файл лога: " + way_to + "\log.txt", font = ("Arial", 8, 'bold'))
lbl_list = tkinter.Label(list_arm_window, text = "список АРМ-ов: " + way_to + "\list.txt", font = ("Arial", 8, 'bold'))
enter_passw = tkinter.Entry(main_window, width = 20, show = "*")
enter_login = tkinter.Entry(main_window, width = 20)
lbl_login = tkinter.Label(main_window, text = "User")
lbl_passw = tkinter.Label(main_window, text = "Password")
btn_start = tkinter.Button(main_window, text = "Start")
lbl_list_arm = tkinter.Label(list_arm_window, text = text_of_arms)
# расстановка элементов в окне
lbl_log.place(x = 5, y = 310)
lbl_list.place(x = 5, y = 5)
enter_login.place(x = 80, y = 60)
enter_passw.place(x = 350, y = 60)
lbl_login.place(x = 45, y = 60)
lbl_passw.place(x = 285, y = 60)
btn_start.place(x =260, y = 120)
lbl_list_arm.place(x = 5, y = 20)

# кнопка старта
btn_start.bind('<Button-1>', Start)



main_window.mainloop()