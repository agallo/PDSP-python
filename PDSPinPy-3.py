#!/usr/bin/python

from time import sleep
import wiringpi2 as wiringpi

usleep = lambda x: sleep(x / 1000000.0)

# TODO figure out wiringPi2 shift register use
# TODO command line argument: -i (string to display (need to fiugre out how to accept special chars)
# TODO command line argument: -t (system local time, 12 hour (no AM or PM))
# TODO command line argument: -T (system local time, 24 hour)
# TODO command line argument: -u (UTC, 24 hour)
# TODO command line argument: -s (echo what is being sent to display to standard out)


'''
document pin assignment here
probably want to use PHY pin numbering because the others are confusing
function    dest    via header  GPIO (header pin number)
RESet       PDSP-1  ??          3
A0          PDSP-3  ??          5
A1          PDSP-4  ??          7
A2          PDSP-5  ??          11
A3          PDSP-6  ??          13
CE          PDSP-14 ??          15
WRite       PDSP-13 ??          19
latch       ShfR-12 ??          21
Data-out    ShfR-14 ??          23
Clock       ShfR-11 ??          29
--- Power & Ground
GND         PDSP-16,18, ShfR-8,13 ??
5V          PDSP-2,10,11,15,19 SfhR-10,16 ??
--- Additional wiring (Shift Register to PDSP) included for documentation of schemaitc
ShfR -  PDSP
15      20
1       21
2       25
3       26
4       27
5       28
6       29
7       30
'''

# define pin names (reformat pin assignment documentation (above) to be included here to avoid duplication)
RST = 3
A0 = 5
A1 = 7
A2 = 11
A3 = 13
CE = 15
WR = 19
latch = 21
SER = 23
CLK = 29


def reset():
    # some code to reset
    wiringpi.digitalWrite(RST, 0)
    usleep(1)
    wiringpi.digitalWrite(RST, 1)
    usleep(150)
    wiringpi.digitalWrite(A3, 1)
    return


def setup():
    wiringpi.wiringPiSetupPhys()
    # assign pins
    wiringpi.pinMode(3, 1)
    wiringpi.pinMode(3, 1)
    wiringpi.pinMode(5, 1)
    wiringpi.pinMode(7, 1)
    wiringpi.pinMode(11, 1)
    wiringpi.pinMode(13, 1)
    wiringpi.pinMode(15, 1)
    wiringpi.pinMode(19, 1)
    wiringpi.pinMode(21, 1)
    wiringpi.pinMode(23, 1)
    wiringpi.pinMode(29, 1)
    # reset display


def scrolldisplay(istring):
    for c in istring:
        tmpstr = ''.join(istring)
        print tmpstr[0:8]
        writedisplay(tmpstr)
        istring.append(istring.pop(0))
        sleep(.5)
    return


def writedisplay(whattodisplay):
    print
    for pos in range(0, 8):
        a0 = pos & 1
        a1 = pos & 2
        a2 = pos & 4
        print whattodisplay[pos], 'will be displayed at position ', a0, a1, a2
    return


def pad(needtopad):
    while len(needtopad) <= 6:
        needtopad.append(' ')
        needtopad.insert(0, ' ')
    if len(needtopad) == 7:
        needtopad.append(' ')
    return needtopad

# main (to be replaced with arguments)
inputstring = list('123456789')
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
        sleep(1)


main()