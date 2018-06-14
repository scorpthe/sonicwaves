"""
Notation (as part of Sonic Waves)

started 22.03.18
by Bushuev Ilya

updated 25.06.18

function: note => hz
"""

NOTE_AMOUNT = 12
A4 = {'HZ': 440.00, 'NUM': (12 * 4 + 9)}
NOTE_ID = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4,
           'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9,
           'A#': 10, 'Hb': 10, 'B':10, 'H': 11}


class Note:
    @staticmethod
    def name_to_num(name):
        try:
            octave = int(name[-1])
            note = NOTE_ID[name[:-1]]
            res = NOTE_AMOUNT * octave + note
        except (KeyError, ValueError, IndexError):
            print('Notation: cannot get note number, '+
                  'unknown note "{}"'.format(name))
            res = False
        return res

    @staticmethod
    def num_to_hz(num):
        return A4['HZ'] * (2 ** ((num - A4['NUM']) / 12))

    @staticmethod
    def name_to_hz(name):
        num = Note.name_to_num(name)
        res = Note.num_to_hz(num) if num >= 0 else False
        return res
        
def _test():
    name = 'C8'
    print('Test {} note'.format(name))
    print('name to num', Note.name_to_num(name))
    print('name to hz', Note.name_to_hz(name))

if __name__ == '__main__':
    _test()