from winsound import Beep as beep

class Sounder:

    C0 = 16.352 #Hz
    A4 = 440.00 #Hz
    Notes12 = ('C','CD','D','DE','E','F','FG','G','GA','A','AH','H')
    Major = (2,2,1,2,2,2,1)
    Minor = (2,1,2,2,1,2,2)

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

#snd = Sounder()
#cmaj = snd.getGamma('D','major')
#print(cmaj)

    {'C':261.63, 'CD':277.18, 'D':293.66, 'DE':311.13, 'E':329.63,
     'F':349.23, 'FG':369.99, 'G':392.00, 'GA':415.30, 'A':440.00,
     'AH':466.16, 'H':493.88}

