#!/usr/bin/python

from time import sleep
import wiringpi2 as wiringpi

# this local definition is no longer needed because
# wiringpi has high speed delays
# usleep = lambda x: sleep(x / 1000000.0)

# TODO command line argument: -i (string to display (need to fiugre out how to accept special chars)
# TODO command line argument: -t (system local time, 12 hour (no AM or PM))
# TODO command line argument: -T (system local time, 24 hour)
# TODO command line argument: -u (UTC, 24 hour)
# TODO command line argument: -s (echo what is being sent to display to standard out)
# TODO gracefully handle SIG-INT (ctrl-c) and clear display upon exit


'''
hardware notes
using PDSP-1880 and 74LS595N
header pin numbers refer to customer PCB header row
if using a breadboard, ignore header pins and connect GPIO pins as indicated
see pin names section for GPIO (header pin number) to variable to chip mapping
--- Power & Ground
Signal      destination                     header
GND         PDSP-16,18, ShfR-8,13           16
5V          PDSP-2,10,11,15,19 SfhR-10,16   15

additional (intra board, SR-->PDSP) connections documented here for completeness
ShfR    PDSP    Signal
15      20      D0
1       21      D1
2       25      D2
3       26      D3
4       27      D4
5       28      D5
6       29      D6
7       30      D7
'''

# define pin names
# VAR = GPIO header     PDSP or Shift Register pin#     via header pin
RST = 3                 # PDSP-1                        1
A0 = 5                  # PDSP-3                        3
A1 = 7                  # PDSP-4                        4
A2 = 11                 # PDSP-5                        5
A3 = 13                 # PDSP-6                        6
CE = 15                 # PDSP-14                       7
WR = 19                 # PDSP-13                       8
latch = 21              # ShiftRegister-12              10
SER = 23                # ShiftRegister-14              11
CLK = 18                # ShiftRegister-11              12

# some wiringPi vars to make reading the code easier to read
LOW = 0
HIGH = 1
OUTPUT = 1


def resetdisplay():
    wiringpi.digitalWrite(RST, LOW)
    wiringpi.delayMicroseconds(1)
    wiringpi.digitalWrite(RST, HIGH)
    wiringpi.delayMicroseconds(150)
    wiringpi.digitalWrite(A3, HIGH)
    return


def setup():
    wiringpi.wiringPiSetupPhys()
    # assign pins
    wiringpi.pinMode(RST, OUTPUT)
    wiringpi.pinMode(A0, OUTPUT)
    wiringpi.pinMode(A1, OUTPUT)
    wiringpi.pinMode(A2, OUTPUT)
    wiringpi.pinMode(A3, OUTPUT)
    wiringpi.pinMode(CE, OUTPUT)
    wiringpi.pinMode(WR, OUTPUT)
    wiringpi.pinMode(latch, OUTPUT)
    wiringpi.pinMode(SER, OUTPUT)
    wiringpi.pinMode(CLK, OUTPUT)
    resetdisplay()


def scrolldisplay(istring):
    for c in istring:
        tmpstr = ''.join(istring)
        print tmpstr[0:8]
        writedisplay(tmpstr)
        istring.append(istring.pop(0))
        sleep(.3)
    return


def writedisplay(whattodisplay):
    for pos in range(0, 8):
        if 1 & pos <> 0:
            wiringpi.digitalWrite(A0, HIGH)
        else:
            wiringpi.digitalWrite(A0, LOW)
        if 2 & pos <> 0:
             wiringpi.digitalWrite(A1, HIGH)
        else:
            wiringpi.digitalWrite(A1, LOW)
        if 4 & pos <> 0:
            wiringpi.digitalWrite(A2, HIGH)
        else:
            wiringpi.digitalWrite(A2, LOW)

        wiringpi.digitalWrite(latch, LOW)
        wiringpi.shiftOut(SER, CLK, 1, ord(whattodisplay[pos]))
        wiringpi.digitalWrite(latch, HIGH)
        wiringpi.delay(1)
        wiringpi.digitalWrite(CE, LOW)
        wiringpi.delay(1)
        wiringpi.digitalWrite(WR, LOW)
        wiringpi.delay(1)
        wiringpi.digitalWrite(WR, HIGH)
        wiringpi.delay(1)
        wiringpi.digitalWrite(CE, HIGH)
        wiringpi.delay(1)
    return


def pad(needtopad):
    while len(needtopad) <= 6:
        needtopad.append(' ')
        needtopad.insert(0, ' ')
    if len(needtopad) == 7:
        needtopad.append(' ')
    return needtopad

# main (to be replaced with arguments)
inputstring = list('23:52:00')
# 24 hour time for input
# inputstring = time.strftime('%H:%M:%S')
# 24 hour time for input
# inputstring = time.strftime('%I:%M:%S')


def main():
    setup()
    while True:
        if len(inputstring) == 8:
            writedisplay(inputstring)
        elif len(inputstring) > 8:
            scrolldisplay(inputstring)
        else:
            pad(inputstring)
        #sleep(1)


main()
