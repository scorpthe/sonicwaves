"""
File-player (as part of Sonic Waves)

started 22.03.18
by Bushuev Ilya

updated 25.06.18

function: file (splitted) => sound
"""

from sonic import Sonic
from notation import Note
from split import split_file as split

MIN = 60
BPM = 120
QUARTER_NOTE = 4


class Player:
    def set_default_tempo(self, bpm):
        self.whole_note_sec = MIN / bpm * QUARTER_NOTE

    def _set_default_note_value(self, val):
        self.default_note_value = val

    def __init__(self):
        self.set_default_tempo(BPM)
        self._set_default_note_value(QUARTER_NOTE)
        self.phrases = None
        self.sg = Sonic(echo=True)

    def play_note_sec(self, name, sec):
        hz = Note.name_to_hz(name)
        if hz:
            self.sg.sound(hz, sec)

    def play_note(self, name, divisor, dividend=1):
        hz = Note.name_to_hz(name)
        if hz:
            division = dividend / divisor
            sec = float(self.whole_note_sec * division)
            self.sg.sound(hz, sec)

    def play_command_list(self, command_list):
        for el in command_list:
            if el[0] == 'tempo':
                tempo = el[1]
                self.set_default_tempo(tempo)
                print('default tempo set to', tempo)
            elif el[0] == 'value':
                value = el[1]
                self._set_default_note_value(value)
                print('default note value set to', value)
            elif el[0] == 'note':
                sound = el[1]['snd']
                value = el[1]['val'] if el[1]['val'] else self.default_note_value
                duration = el[1]['dur'] if el[1]['dur'] else 1
                self.play_note(sound, value, duration)

    def load(self, file_name):
        self.phrases = split(file_name)

    def play(self, phrase_name='all'):
        if self.phrases:
            if phrase_name == 'all':
                for name, commands in self.phrases.items():
                    # try_echo(name)
                    self.play_command_list(commands)
            else:
                # try_echo(riff_name)
                try:
                    commands = self.phrases[phrase_name]
                    self.play_command_list(commands)
                except KeyError:
                    print('Sounder error! Unknown riff "{}"'.format(phrase_name))

    def play_now(self, file_name, phrase_name='all'):
        self.load(file_name)
        self.play(phrase_name)


def test(file_name, phrase_name='all'):
    player_ = Player()
    player_.play_now(file_name, phrase_name)

if __name__ == '__main__':
    test('music','Brave Knights')
