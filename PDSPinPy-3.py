#!/usr/bin/python

from time import sleep
import wiringpi2 as wiringpi

# this local definition is no longer needed because
# wiringpi has high speed delays
# usleep = lambda x: sleep(x / 1000000.0)

# TODO figure out wiringPi2 shift register use (complete??)
# TODO command line argument: -i (string to display (need to fiugre out how to accept special chars)
# TODO command line argument: -t (system local time, 12 hour (no AM or PM))
# TODO command line argument: -T (system local time, 24 hour)
# TODO command line argument: -u (UTC, 24 hour)
# TODO command line argument: -s (echo what is being sent to display to standard out)


'''
hardware notes
using PDSP-1880 and 74HC595 (check)
see pin assignments for GPIO (header pin number) to variable to chip mapping
header pin column to be filled in after perfboard prototype is laid out
--- Power & Ground
GND         PDSP-16,18, ShfR-8,13 ??
5V          PDSP-2,10,11,15,19 SfhR-10,16 ??
additional (intra board, SR-->PDSP) connections documented here for completeness
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

# define pin names
# VAR = GPIO header     PDSP or Shift Register pin#     via header pin
RST = 3                 # PDSP-1                        ??
A0 = 5                  # PDSP-3                        ??
A1 = 7                  # PDSP-4                        ??
A2 = 11                 # PDSP-5                        ??
A3 = 13                 # PDSP-6                        ??
CE = 15                 # PDSP-14                       ??
WR = 19                 # PDSP-13                       ??
latch = 21              # ShiftRegister-12              ??
SER = 23                # ShiftRegister-14              ??
CLK = 29                # ShiftRegister-11              ??

# some wiringPi vars to make reading the code easier to read
LOW = 0
HIGH = 1
OUTPUT = 1


def resetdisplay():
    # some code to reset
    wiringpi.digitalWrite(RST, LOW)
    wiringpi.delayMicroseconds(1)
    wiringpi.digitalWrite(RST, HIGH)
    wiringpi.delayMicroseconds(150)
    wiringpi.digitalWrite(A3, HIGH)
    return


def setup():
    wiringpi.wiringPiSetupPhys()
    # assign pins
    wiringpi.pinMode(3, OUTPUT)
    wiringpi.pinMode(3, OUTPUT)
    wiringpi.pinMode(5, OUTPUT)
    wiringpi.pinMode(7, OUTPUT)
    wiringpi.pinMode(11, OUTPUT)
    wiringpi.pinMode(13, OUTPUT)
    wiringpi.pinMode(15, OUTPUT)
    wiringpi.pinMode(19, OUTPUT)
    wiringpi.pinMode(21, OUTPUT)
    wiringpi.pinMode(23, OUTPUT)
    wiringpi.pinMode(29, OUTPUT)
    resetdisplay()


def scrolldisplay(istring):
    for c in istring:
        tmpstr = ''.join(istring)
        print tmpstr[0:8]
        writedisplay(tmpstr)
        istring.append(istring.pop(0))
        sleep(.5)
    return


def writedisplay(whattodisplay):
    '''
    ORIGINAL Arduino code -- need to check
    digitalWrite(a0, (1&i)!=0?HIGH:LOW);
    digitalWrite(a1, (2&i)!=0?HIGH:LOW);
    digitalWrite(a2, (4&i)!=0?HIGH:LOW);
    '''



    for pos in range(0, 8):

        if 1 & pos <> 0 then:
            digitalWrite(A0, HIGH)
        else:
            digitalWrite(A0, LOW)
        if 2 & pos <> 0 then:
             digitalWrite(A1, HIGH)
        else:
            digitalWrite(A1, LOW)
        if 4 & pos <> 0 then:
            digitalWrite(A2, HIGH)
        else:
            digitalWrite(A2, LOW)

        #is this code needed or was it an attempt to convert the arduino C code in one line?
        wiringpi.digitalWrite(A0, pos & 1)
        wiringpi.digitalWrite(A1, pos & 2)
        wiringpi.digitalWirte(A2, pos & 4)

        wiringpi.digitalWrite(latch, LOW)
        wiringpi.shiftOut(SER, CLK, 1, whattodisplay[pos])
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