"""
Notation (part of Sonic Waves)

started 22.03.18
by Bushuev Ilya

updated 11.07.18:
    unlimited alteration signs

function: 
    note => hz
"""

from re import compile

NOTE_AMOUNT = 12
NOTES = {'C': 0, 'D': 2, 'E': 4, 
         'F': 5, 'G': 7, 'A': 9, 'H': 11}
A4 = {'HZ': 440.00, 'NUM': (12 * 4 + 9)}
NOTE = compile(r'^([CDEFGAH])([#b]*)([0-9])$')

class NotationError(Exception):
    pass

class Note:
    @staticmethod
    def name_to_num(name):
        try:
            found = NOTE.search(name)
            if found:
                note = NOTES[found.group(1)]
                alter = len(found.group(2))
                if alter > 0:
                    if found.group(2)[0] == 'b':
                        alter = -alter
                octave = int(found.group(3))
                res = NOTE_AMOUNT * octave + (note+alter)
            else:
                raise NotationError()
        except NotationError:
            print('Notation: cannot get note number, '+
                  'unknown note "{}"'.format(name))
            res = False
        return res

    @staticmethod
    def num_to_hz(num):
        # look for scientific pitch notation
        return A4['HZ'] * (2 ** ((num - A4['NUM']) / 12)) 

    @staticmethod
    def name_to_hz(name):
        num = Note.name_to_num(name)
        res = Note.num_to_hz(num) if num >= 0 else False
        return res
        
def __test():
    names = ['A4', 'A#4', 'A##4', 'Ab4', 'Abb4']
    for name in names:
        print('Test', name)
        print('name to num', Note.name_to_num(name))
        print('num to hz', Note.num_to_hz(Note.name_to_num(name)))
        print('name to hz', Note.name_to_hz(name))

if __name__ == '__main__':
    __test()
    
    
"""
major = [2,2,1,2,2,2,1]

def steps(ton):
    s = 0
    res = []
    for el in ton:
        s += el
        res.append(s)
    return res
    
smajor = steps(major)
print(major)
print(minor)
"""