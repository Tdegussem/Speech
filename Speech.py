


##### SETTINGS #####
ser_enable = 0
speed_th = 70 #lower = sensitive


screen_width = 1000

scorespeed = 100
scoresound = 100






import pyaudio
import wave
import struct
import math
import time

import pygame, sys
import serial


if ser_enable:
    ser = serial.Serial('/dev/ttyACM0',9600, timeout =1) 
#ser.open()


global speed_inegrator
speed_inegrator = 5 

global minimum
global maximum

global timepast
timepast = 0

trig = 0
#print ser.portstr  

from pygame.locals import *

pygame.init()
scr = pygame.display.set_mode((screen_width, 500)) #was 640*480
global amplitude
global oldsound
global delta
delta = 0
score = 0
global soundlevel
global last_stop
last_stop = 0
global silence
global speed
sendbyte = 0
send_delay = 0
silence = 0
oldsound = 0
INITIAL_TAP_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
breath = 0
totaltime = 0


OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    

UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME # if we get this many quiet blocks in a row, decrease the threshold

MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME # if the noise was longer than this many blocks, it's not a 'tap'

def get_rms(block):

    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
    # sample is a signed short in +/- 32768. 
    # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

pa = pyaudio.PyAudio()                                 #]
                                                       #|
stream = pa.open(format = FORMAT,                      #|
         channels = CHANNELS,                          #|---- You always use this in pyaudio...
         rate = RATE,                                  #|
         input = True,                                 #|
         frames_per_buffer = INPUT_FRAMES_PER_BLOCK)   #]

                                       #]         

def audio_analyze(loops):
    tap_threshold = INITIAL_TAP_THRESHOLD                  #]
    noisycount = MAX_TAP_BLOCKS+1                          #|---- Variables for noise detector...
    quietcount = 0                                         #|
    errorcount = 0  
    try:                                                    #]
        block = stream.read(INPUT_FRAMES_PER_BLOCK)         #|
    except IOError, e:                                      #|---- just in case there is an error!
        errorcount += 1                                     #|
        print( "(%d) Error recording: %s"%(errorcount,e) )  #|
        noisycount = 1                                      #]

    global amplitude
    amplitude = get_rms(block)
    if amplitude > tap_threshold: # if its to loud...
        quietcount = 0
        noisycount += 1
        if noisycount > OVERSENSITIVE:
            tap_threshold *= 1.1 # turn down the sensitivity

    else: # if its to quiet...

        if 1 <= noisycount <= MAX_TAP_BLOCKS:
            print 'tap!'
        noisycount = 0
        quietcount += 1
        if quietcount > UNDERSENSITIVE:
            tap_threshold *= 0.9 # turn up the sensitivity  

print("* starting")
def noiseoffset():
    print("* Setting noise level")
    global noise
    noise = 0
    for i in range(10):
        audio_analyze(1)
        if amplitude > noise:
            noise = amplitude
        i +=1
    

myfont = pygame.font.SysFont("verdana", 15)
readnow = pygame.font.SysFont("verdana", 25)
scorefont = pygame.font.SysFont("verdana", 30)
readnext = pygame.font.SysFont("verdana", 25)
pygame.display.update()
text=   ["Hallo"    ,"mijn" ,"naam" ,"is"   ,"xxx"  ,"en"   ,"ik"   ,"ga"   ,"nu"   ,"proberen" ,"om"   ,"zo"   ,"goed" ,"mogelijk" ,"aaneengesloten"   ,"te"   ,"blijven"  ,"praten", "...","dit"  ,"doe"  ,"ik"   ,"doorrr"]
frames =[2          ,1      ,1      ,1      ,3      ,1      ,1      ,1      ,1      ,3          ,1      ,1      ,1      ,3          ,5                  ,1      ,2          ,2       , 4    ,   1   ,  1    , 1     , 2     ]
i = 0
word = 0
counter = 0
global speed

spdelay = 0
speed =0
noiseoffset()
noise = 0.10
while True:
    timepast += 1
    totaltime +=1
    if timepast > screen_width:
        timepast = 0
    audio_analyze(1)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                global speed
                speed += 1
            
            if event.key == pygame.K_c:
                   noiseoffset()

            if event.key == pygame.K_RIGHT:
                i += 1
            if event.key == pygame.K_q:
                pygame.quit ()
            if event.key == pygame.K_s:
                trig = 1
    #background = pygame.Surface(scr.get_size())
    background = pygame.Surface((1000,350))
    background = background.convert()
    global delta
    background.fill(0)
    scr.blit(background, (0, 0))
    global amplitude
    global oldamplitude
    global soundlevel
    soundlevel = (amplitude-noise) * 255
    if soundlevel > 255:
        soundlevel = 255
        clip = 1
    if soundlevel < 0:
        soundlevel = 0
    delta = int (oldsound - soundlevel)*2
    if delta < 0:
        delta = 0
    if delta > 255:
        delta = 255
    oldsound = soundlevel

    if delta > 40:
       global last_stop
       spdelay = int (pygame.time.get_ticks() - last_stop)
       last_stop = pygame.time.get_ticks()

    
    spdelay +=100
    if spdelay > 1000:
        spdelay = 1000
    global silence
    if soundlevel < 25:
        silence += 1
    else:
        silence = 0
    if silence > 100:
        silence = 100
    print int(soundlevel),"silence= ", silence, "delta= ", delta, "speed =", speed
    y = 0
    end = soundlevel
    while y < end:
        pygame.draw.lines(scr, (soundlevel,255-soundlevel,0), True, [(100+y,100),(100+y,150)], 3)
        y +=1

    y = 0
    speednew = (spdelay)/5
    global speed_inegrator
    speed = (speed *(speed_inegrator-1) + speednew)/speed_inegrator


    if speed > scorespeed and soundlevel > scoresound:
        score += 0.1

    end = speed
    while y < end:
        pygame.draw.lines(scr, (255-y,y,0), True, [(400,250-y),(450,250-y)], 3)
        y +=1

    y = 0
    end = silence *2.5
    while y < end:
        pygame.draw.lines(scr, (y,255-y,0), True, [(100+y,200),(100+y,250)], 3)
        y +=1
    pygame.draw.rect(scr, (255,255,255), (100,100,255,50), 2)
    pygame.draw.rect(scr, (255,255,255), (100,200,255,50), 2)
    pygame.draw.rect(scr, (255,255,255), (400,50,50,200), 2)
    pygame.draw.lines(scr, (soundlevel,255-soundlevel,0), True, [(10+timepast,450),(10+timepast,450-soundlevel/2.5)], 1)
    pygame.draw.lines(scr, (0,0,0), True, [(12+timepast,450),(12+timepast,350)], 3)
    label = myfont.render("Audio level", 1, (255,255,0))
    label2 = myfont.render("Silence", 1, (255,255,0))
    label_score = scorefont.render(str(score),1,(255,255,255))
    label_timepast = scorefont.render(str(totaltime),1,(255,255,255))
    warn = myfont.render("Trager!", 1, (255,255,0))
    read = readnow.render(text[word], 1, (255,255,255))
    if word < len(text)-1:
        nextr = readnext.render(text[word+1], 1, (155,155,150))    
    
    scr.blit(label, (1, 125))
    scr.blit(label2, (1, 225))
    scr.blit(label_score, (500, 125))
    scr.blit(label_timepast, (500, 175))
    pygame.draw.circle(scr, (50,50,50), (200+counter*2,310), 20, 0)
    pygame.draw.circle(scr, (255-speed,speed,0), (800,175), int(breath), 0)
    pygame.draw.circle(scr, (50,50,50), (800,175), 152, 2)

    scr.blit(read, (200, 300))
    if speed < 125:
        scr.blit(warn, (800, 175))
    scr.blit(nextr, (400, 300))
    pygame.display.update()
    counter +=1
    if counter ==(20*frames[word]):
        counter = 0
        if word < len(text)-1:
            word += 1
    global breath
    if breath < 150:
        breath += 1
    sendbyte = 0
    if send_delay <10:
        send_delay += 1
    if send_delay == 10:
        if speed < speed_th or trig == 1:
            send_delay = 0
            breath = breath * 0.7
            trig = 0
            if ser_enable :
                sendstr = chr(sendbyte)
                ser.write(sendstr)
                print sendstr
            send_delay = send_delay+1
        
       






