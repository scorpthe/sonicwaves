"""
Player (part of Sonic Waves)

started 22.03.18
by Bushuev Ilya

updated 17.07.18

function: splitted file => notes
"""

from sonic import Sonic
from notation import Note
from split import split

MIN = 60
BPM = 120
QRT = 4
VOL = 100
WAV = 'e'

class Player:
    def set_tempo(self, bpm):
        self.whole_ms = MIN / bpm * QRT
    
    def set_duration(self, duration):
        self.duration = duration
    
    def set_volume(self, volume):
        self.volume = volume/1000
    
    def set_waves(self, waves):
        self.waves = waves
    
    def __init__(self,echo=True,now=False):
        self.echo = echo
        self.now = now
        self.sonic = Sonic(echo=self.echo)
        self.set_tempo(BPM)
        self.set_duration(QRT)
        self.set_volume(VOL)
        self.set_waves(WAV)
        self.rep = []

    def notes(self, names, duration, length, volume, waves):
        if self.echo: print('Player: info -','note:',names,
                            'dur:',duration,'len:',length,
                            'vol:',volume,'wav:',waves)
        hz = [Note.name_to_hz(name) for name in names]
        if hz:
            division = 1 * length / duration
            sec = float(self.whole_ms * division)
            self.sonic.waves(hz, sec, volume, waves, self.now)

    def durlen(self, string):
        try:
            duration = self.duration
            length = 1
            if string != '':
                if string[0] == '/':
                    duration *= int(string[1:])
                elif string[0] == '*':
                    length *= int(string[1:])
                elif string[0] == ':':
                    duration = int(string[1:])
                else:
                    raise PlayError(string)
            res = (duration, length)
        except PlayError as pe:
            print('Player: error in expression <{0}>'.format(pe.args[0]))
            res = 0
        return res

    def read(self, com):
        i = 0
        while i < len(com):
            if com[i][0] == 'tempo':
                tempo = com[i][1]
                self.set_tempo(tempo)
                if self.echo: print('Player: tempo:', tempo)
            elif com[i][0] == 'value':
                duration = com[i][1]
                self.set_duration(duration)
                if self.echo: print('Player: value:', duration)
            elif com[i][0] == 'volume':
                volume = com[i][1]
                self.set_volume(volume)
                if self.echo: print('Player: volume:', volume)
            elif com[i][0] == 'waves':
                waves = com[i][1]
                self.set_waves(waves)
                if self.echo: print('Player: waves:', waves)
            elif com[i][0] == 'for':
                self.rep.append([1,i])
                if self.echo: print('Player: start loop')
            elif com[i][0] == 'rep':
                if self.rep[-1][0] == com[i][1]:
                    if self.echo: 
                        print('Player: looped {0} times'.format(self.rep[-1][0]))
                    if self.echo: 
                        print('Player: end loop')
                    self.rep.pop()
                else:
                    i = self.rep[-1][1]
                    if self.echo: 
                        print('Player: looped {0} times'.format(self.rep[-1][0]))
                    self.rep[-1][0]+=1
            elif com[i][0] == 'note':
                sound = [com[i][1]]
                duration, length = self.durlen(com[i][2])
                volume, waves = self.volume, self.waves
                self.notes(sound, duration, length, volume, waves)
            elif com[i][0] == 'chord':
                sounds = list(com[i][1])
                duration, length = self.durlen(com[i][2])
                volume, waves = self.volume, self.waves
                self.notes(sounds, duration, length, volume, waves)
            elif com[i][0] == 'pause':
                sound = ['C0']
                duration, length = self.durlen(com[i][1])
                volume, waves = 0, self.waves
                self.notes(sound, duration, length, volume, waves)
            i+=1
        self.sonic.play()

    def load(self, file_name):
        text = ''
        with open(file_name, 'r') as f:
            text = f.read()
        self.commands = split(text,echo=self.echo)

    def go(self, mark=['all']):
        if self.commands:
            if mark == ['all']:
                self.read(self.commands)
            else:
                com = self.commands
                marks = []
                for i in range(len(com)):
                    if com[i][0] == 'mark':
                        marks.append([com[i][1],i])
                take = []
                for i in range(len(marks)):
                    if marks[i][0] in mark:
                        start = marks[i][1]
                        end = marks[i+1][1] if i!=len(marks)-1 else len(com)
                        take+=com[start:end]
                self.read(take)

def _test(name, mark='all'):
    player = Player(echo=True)
    player.load(name)
    player.go(mark)

if __name__ == '__main__':
    _test('music',['August'])
