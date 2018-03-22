class Sounder:
    
    Notes12 = ('C','CD','D','DE','E','F','FG','G','GA','A','AH','H')
    Major = (2,2,1,2,2,2,1)
    Minor = (2,1,2,2,1,2,2)

    def getGamma(self, note='C', tone='major'):
        gamma = []
        failed = 0
        # Get note
        try:
            note = self.Notes12.index(note)
        except ValueError:
            failed += 1
        # Get tone
        if tone == 'major':
            tone = self.Major
        elif tone == 'minor':
            tone = self.Minor
        else:
            failed += 1
        # If not failed
        if not failed:
            ln = len(self.Notes12)
            gamma.append(self.Notes12[note])
            cur = note
            for i in tone:
                cur += i
                gamma.append(self.Notes12[cur%ln])
        res = gamma if not failed else not failed
        return res

snd = Sounder()
cmaj = snd.getGamma('Do','major')
print(cmaj)
