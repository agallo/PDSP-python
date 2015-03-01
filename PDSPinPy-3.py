__author__ = 'agallo'
# third try at PDSP display in Python
# remark to change

from time import sleep
import wiringpi2 as wiringpi

'''
document pin assignment here
probably want to use PHY pin numbering because the others are confusing
'''


def setup():
    wiringpi.wiringPiSetupPhys()
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

# main
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
