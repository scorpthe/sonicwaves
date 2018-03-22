from winsound import Beep

class Sounder:
    """ BASICS """
    NoteAmount = 12
    A4 = (440.00, (12*4 + 9))
    # A4(hz, number) in scientific notation
    # C0 = 16.352 Hz
    NoteID = {'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4,
              'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9,
              'A#':10, 'Hb':10, 'H':11}
    MsInSec = 1000
    SecInMin = 60
    MsInMin = SecInMin * MsInSec
    StdTempo = 120 #beat (quarter note) per minute

    bpm = StdTempo
    quarter = MsInMin // bpm
    whole = quarter * 4
    div = 8
    
    #tact = [('C4', 1/2), ('D4', 1/2)]
    #sum = 0
    #for el in tact: sum += el[1]
    #sum == 1

    #in file:
    #s = 'bpm = 120'
    #int(s.split('=')[1])
    
    #Notes12 = ('C','CD','D','DE','E','F','FG','G','GA','A','AH','H')
    
    #Major = (2,2,1,2,2,2,1)
    #Minor = (2,1,2,2,1,2,2)

    def _setTempo(self, tempo):
        self.tempo = tempo
        self.quarter = self.MsInMin // self.tempo
        self.whole = self.quarter * 4

    def _setDiv(self, div):
        self.div = div

    def _noteNumByName(self, name='C0'):
        try:
            octave = int(name[-1])
            note = self.NoteID[name[:-1]]
            res = self.NoteAmount*octave + note
        except Exception: #KeyError, ValueError, IndexError...
            res = False
        return res

    def _noteHzByNum(self, num=0):
        return self.A4[0] * (2 ** ((num - self.A4[1])/12))

    def noteHzByName(self, name='A4'):
        num = self._noteNumByName(name)
        return self._noteHzByNum(num)

    def playNoteMs(self, name='C4', ms=1000):
        hz = self.noteHzByName(name)
        Beep(round(hz), ms)

    def playNoteDur(self, name='C4', dur=1):
        hz = self.noteHzByName(name)
        ms = int(self.whole * dur)
        Beep(round(hz), ms)

    def playMusic(self, music=[]):
        for note in music:
            print(note)
            self.playNoteDur(note[0], note[1])

    def playFile(self, name):
        lines = []
        with open(name,'r') as file:
            lines = file
            #for line in file:
            #    lines.append(line)
        print(lines)
        phrases = []
        for i in range(len(lines)):
            lines[i] = lines[i].replace(' ','')
            lines[i] = lines[i].replace('\n','')
            #lines[i].split(',')
            for el in phrases:
                if el.find('bpm=') == 0:
                    self._setTempo(int(el.split('=')[1]))
                    print('tempo set to', self.tempo)
                elif el.find('div=') == 0:
                    self._setDiv(int(el.split('=')[1]))
                    print('div set to', self.div)
        print(phrases)

"""    
    def getNoteByName(self, note):
        failed = False
        try:
            note = self.Notes12.index(note)
        except ValueError:
            failed = True
        note = note if not failed else -1
        return note

    def getToneByName(self, tone):
        if tone == 'major':
            tone = self.Major
        elif tone == 'minor':
            tone = self.Minor
        else:
            tone = -1
        return tone

    def getDiBeNote(self, curNote, prevNote):
        if len(curNote) != len(prevNote):
            
            curNote = curNote[0]+'#'
        return curNote

    def getDiBeGamma(self, oldGamma):
        gamma = []
        for i in range(len(oldGamma)):
            gamma.append(self.getDiBeNote(oldGamma[i], oldGamma[i-1]))
        return gamma
    
    def getGamma(self, note='C', tone='major'):
        gamma = []
        failed = 0
        # Get note
        note = self.getNoteByName(note)
        if note == -1:
            failed += 1
        # Get tone
        tone = self.getToneByName(tone)
        if tone == -1:
            failed += 1
        # If not failed
        if not failed:
            ln = len(self.Notes12)
            cur = note
            for i in tone:
                gamma.append(self.Notes12[cur%ln])
                cur += i
            #gamma = self.getDiBeGamma(gamma)
        res = gamma if not failed else not failed
        return res
"""







snd = Sounder()
"""
cmaj = snd.getGamma('CD','minor')
print(cmaj)
print(snd.noteHzByName('D4'), round(snd.noteHzByName('D4')))
snd._setTempo(60)
music = [('E4',1/8*3), ('E4',1/16), ('F#4',1/16),
         ('G4',1/8), ('F#4',1/16), ('E4',1/16),
         ('D4',1/8), ('E4',1/16), ('F#4',1/16),
         ('E4',1/8*3), ('D4',1/16), ('E4',1/16),
         ('D4',1/8*3), ('H3',1/16), ('D4',1/16)]
snd.playMusic(music)
"""
snd.playFile('music')
