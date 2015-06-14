from threading import Thread, Event
from subprocess import call
import datetime
import mpd
import time
import sys
import RPi.GPIO as GPIO
import spotify

def onoff(command):
    date = datetime.datetime.now()
    command = command.lower()
    if command == "on":
        GPIO.output(7, True) #Accendi
        print("[" + date.strftime("%d %b %Y - %X") + "] ~ Stereo turned up")
    elif command == "off":
        GPIO.output(7, False) #Spegni
        print("[" + date.strftime("%d %b %Y - %X") + "] ~ Stereo shut down")
    else:
        print("Command is not calid")

def do_something(command, uri=""):
    global disabled
    if command == "0":
        return -1
    if command == "toggleMPD":
        status = client.status()
        if status['state'] in ('stop', 'pause'):
            client.play()
        else:
            client.pause()
    elif command == "nextMPD":
        client.next()
    elif command == "previousMPD":
        client.previous()
    elif command == "disable":
        if disabled:
            disabled = 0
            GPIO.output(26, False)
            print("Check routine enabled")
        else:
            disabled = 1
            GPIO.output(26, True)
            print("Check routine disabled")
            if previous_status == 0:
                onoff("on")
                open("minutes.txt", 'w+').write("0\n")

stdout_ = sys.stdout
sys.stdout = open("auto_off.log", 'a', buffering=0)

print("=================== RESTART ===================")
MPD_HOST = "localhost"
MPD_PORT = "6600"
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, True)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, False)
print("GPIO set up")
timer_minutes = 150 # 10 minutes (seconds/2)
open("minutes.txt", 'w+').write("0\n")
disabled = 0

spotify_client = spotify.SpopClient("localhost", 6602)
print("Linked to Spotify")
client = mpd.MPDClient()
connected = False
previous_status = 1
def connectMPD():
    global connected
    while connected == False:
        connected = True
        try:
            client.connect(MPD_HOST, MPD_PORT)
        except SocketError as e:
            connected = False
        if connected == False:
            print("Couldn't connect! Retrying...")
            time.sleep(5)
    print("Connected to MPD")

def check():
    global previous_status, connected
    date = datetime.datetime.now()
    minutes = int(open("minutes.txt").readlines()[0].strip())
    try:
        status = client.status()
    except ConnectionError as e:
        connected = False
	print("MPD connection lost! Reconnecting...")
    spotify_status = spotify_client.status()
    if status['state'] in ('stop', 'pause') and spotify_status[u'status'] in ('stopped', 'paused'):
        if minutes < timer_minutes:
            open("minutes.txt", 'w+').write(str(minutes+1))
        else:
            if previous_status == 1:
                onoff("off")
                previous_status = 0                
    else:
        if previous_status == 0:
            onoff("on")
            previous_status = 1
            if spotify_status[u'status'] == 'playing':
                spotify_client.toggle()
                time.sleep(2)
                spotify_client.uplay(str(spotify_status[u'uri']))
            else:
                client.pause()
                time.sleep(2)
                client.playid(client.currentsong()['id'])
            open("minutes.txt", 'w+').write("0\n")

def file_check():
    file_ = open("action", 'r').readlines()[0].strip()
    file_l = file_.split('$')
    do_something(file_l[0], file_l[1])
    open("action", 'w+').write("0$0")
    

class checkThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
    
    def run(self):
        while not self.stopped.wait(2.0):
            file_check()
	    if not disabled and connected:
                check()
            if not connected:
                connectMPD()

connectMPD()
stopEvent = Event()
thread = checkThread(stopEvent)
thread.start()
print("Thread started")
