"""
Written by:
    Ilya Bushuev @scorpthe
Date:
    15.03-18.03.2018
Description:
    Version 0.5S [splitting]:
        file   -> string,
        string -> commands.
"""

from winsound import Beep

NOTE_AMOUNT = 12
A4 = (440.00, (12*4 + 9)) # A4 in scientific notation = 440.0 Hz
NOTE_ID = {'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4,
           'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9,
           'A#':10, 'Hb':10, 'H':11}
MS_IN_MIN = 60 * 1000 # SecInMin * MsInSec
BPM = 120 # beats (quarter note) per minute
QTR = 4

class Sounder:
    def defMsWhole(self, bpm):
        return MS_IN_MIN // bpm * QTR
        
    def defStDiv(self, div):
        return div
    
    def __init__(self):
        self.msWhole = self.defMsWhole(BPM)
        self.stDiv = self.defStDiv(QTR)
    
    def _noteNumByName(self, name):
        try:
            octave = int(name[-1])
            note = NOTE_ID[name[:-1]]
            res = NOTE_AMOUNT*octave + note
        except Exception: # KeyError, ValueError, IndexError...
            res = False
        return res

    def _noteHzByNum(self, num):
        return A4[0] * (2 ** ((num - A4[1])/12))

    def noteHzByName(self, name):
        num = self._noteNumByName(name)
        return self._noteHzByNum(num)

    def _playNoteMs(self, name, ms):
        hz = self.noteHzByName(name)
        Beep(round(hz), ms)

    def playNoteDur(self, name, dtr, ntr):
        hz = self.noteHzByName(name)
        div = ntr/dtr
        ms = int(self.msWhole * div)
        Beep(round(hz), ms)

    def playMusic(self, music):
        for note in music:
            print(note)
            self.playNoteDur(note[0], note[1], note[2])

    def _readFile(self, name):
        text = ''
        with open(name,'r') as file:
            text = file.read()
        text = text.replace(' ','')
        text = text.replace('\n',',')
        expr = text.split(',')
        for el in expr:
            if el == '':
                del el
        return expr

    def _defActs(self, expr=[]):
        acts = []
        for el in expr:
            if el == '':
                pass
            elif el.find('bpm=') == 0:
                split = el.split('=')
                acts.append(tuple([split[0], int(split[1])]))
            elif el.find('div=') == 0:
                split = el.split('=')
                acts.append(tuple([split[0], int(split[1])]))
            else:
                el = el.replace('*',' ')
                el = el.replace(':',' ')
                split = el.split(' ')
                for i in range(len(split)):
                    if i > 0:
                        split[i] = int(split[i])
                acts.append(tuple(split))
        return acts

    def _playActs(self, acts=[]):
        for el in acts:
            if el[0] == 'bpm':
                bpm = el[1]
                self.msWhole = self.defMsWhole(bpm)
                print('tempo set to', bpm)
            elif el[0] == 'div':
                div = el[1]
                self.stDiv = self.defStDiv(div)
                print('div set to', div)
            else:
                div = self.stDiv
                dur = 1
                note = el[0]
                if len(el) == 3:
                    div = el[1]
                    dur = el[2]
                elif len(el) == 2:
                    div = el[1]
                self.playNoteDur(note,div,dur)

    def playFile(self, name):
        expr = self._readFile(name)
        acts = self._defActs(expr)
        self._playActs(acts)

snd = Sounder()
snd.playFile('music')
